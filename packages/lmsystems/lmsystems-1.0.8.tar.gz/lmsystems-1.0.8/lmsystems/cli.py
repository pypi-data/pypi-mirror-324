import click
import os
import zipfile
import base64
import json
import logging
import tempfile
import shutil
from .custom_node import upload_custom_node
from .config import Config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_and_transform_config(config: dict) -> dict:
    """Transform user-friendly config into internal format."""
    # Required field validation
    if "nodes" not in config:
        raise click.ClickException("lmsystems.json must contain 'nodes' section")

    if len(config["nodes"]) != 1:
        raise click.ClickException("Currently only one node per config is supported")

    # Get node configuration
    node_name, node_config = next(iter(config["nodes"].items()))

    # Handle both string and dict formats for backward compatibility
    if isinstance(node_config, str):
        handler_path = node_config
        handler_function = "lambda_handler"  # default
    elif isinstance(node_config, dict):
        handler_path = node_config.get("file")
        handler_function = node_config.get("function", "lambda_handler")

        if not handler_path:
            raise click.ClickException("Node configuration must include 'file' field")
    else:
        raise click.ClickException("Invalid node configuration format")

    # Validate node name
    if not node_name.replace("-", "").replace("_", "").isalnum():
        raise click.ClickException("Node name must contain only letters, numbers, hyphens, and underscores")

    if len(node_name) > 64:
        raise click.ClickException("Node name must be less than 64 characters")

    # Validate handler path
    if not handler_path.endswith('.py'):
        raise click.ClickException("Handler file must be a Python file (.py)")

    if not os.path.exists(handler_path):
        raise click.ClickException(f"Handler file not found: {handler_path}")

    # Validate handler function exists in the file
    try:
        with open(handler_path, 'r') as f:
            file_content = f.read()
            if f"def {handler_function}" not in file_content:
                raise click.ClickException(
                    f"Function '{handler_function}' not found in {handler_path}"
                )
    except Exception as e:
        raise click.ClickException(f"Error validating handler function: {str(e)}")

    # Transform to internal config format
    internal_config = {
        "name": node_name,
        "handler_file": handler_path,
        "handler_function": handler_function,
        "description": config.get("description", f"Custom node: {node_name}"),
        "version": config.get("version", "0.1.0"),
        "runtime": f"python{config.get('python_version', '3.11')}",
        "memory_size": config.get("memory_size", 256),
        "timeout": config.get("timeout", 30),
        "include_files": [],
        "env_vars": {},
        "directions": None,  # Initialize directions field
        "api_key": config.get("api_key")  # Add API key from config
    }

    # Handle directions file
    if "directions" in config:
        directions_path = config["directions"]
        if not os.path.exists(directions_path):
            raise click.ClickException(f"Directions file not found: {directions_path}")

        if not directions_path.endswith('.md'):
            raise click.ClickException("Directions file must be a Markdown (.md) file")

        try:
            with open(directions_path, 'r', encoding='utf-8') as f:
                directions_content = f.read()
                if not directions_content.strip():
                    raise click.ClickException("Directions file is empty")
                internal_config["directions"] = directions_content
                logger.info(f"Loaded directions from {directions_path}")
        except Exception as e:
            raise click.ClickException(f"Error reading directions file: {str(e)}")

    # Validate optional fields
    if "memory_size" in config:
        memory = config["memory_size"]
        if not isinstance(memory, int) or memory < 128 or memory > 10240:
            raise click.ClickException("memory_size must be between 128 and 10240 MB")
        internal_config["memory_size"] = memory

    if "timeout" in config:
        timeout = config["timeout"]
        if not isinstance(timeout, int) or timeout < 1 or timeout > 900:
            raise click.ClickException("timeout must be between 1 and 900 seconds")
        internal_config["timeout"] = timeout

    if "python_version" in config:
        version = str(config["python_version"])
        supported_versions = ["3.7", "3.8", "3.9", "3.10", "3.11"]
        if version not in supported_versions:
            raise click.ClickException(f"python_version must be one of: {', '.join(supported_versions)}")
        internal_config["runtime"] = f"python{version}"

    # Handle dependencies
    if "dependencies" in config:
        deps = config["dependencies"]
        if not isinstance(deps, list):
            raise click.ClickException("dependencies must be a list")

        if "." in deps:
            internal_config["include_all_py"] = True
            logger.info("Will include all Python files in the project directory")

        for dep in deps:
            if dep != ".":
                if not os.path.exists(dep):
                    raise click.ClickException(f"Dependency not found: {dep}")
                internal_config["include_files"].append(dep)
                logger.debug(f"Added dependency: {dep}")

    # Handle environment variables
    env_vars = config.get("env_vars", {})

    # If env file is specified, read those variables
    if "env" in config:
        env_path = config["env"]
        if not os.path.exists(env_path):
            raise click.ClickException(f"Environment file not found: {env_path}")

        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' not in line:
                            raise click.ClickException(f"Invalid environment variable format in {env_path}")
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
        except Exception as e:
            raise click.ClickException(f"Error reading environment file: {str(e)}")

    # Process environment variable templates
    processed_env_vars = {}
    for key, value in env_vars.items():
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            # Get value from local environment
            env_var_name = value[2:-1]
            env_value = os.environ.get(env_var_name)
            if env_value is None:
                raise click.ClickException(f"Environment variable {env_var_name} not found")
            processed_env_vars[key] = env_value
        else:
            processed_env_vars[key] = value

    internal_config["env_vars"] = processed_env_vars
    logger.info(f"Processed {len(processed_env_vars)} environment variables")

    return internal_config

def install_dependencies(requirements_path: str, target_dir: str):
    """Install dependencies from requirements.txt into target directory."""
    import subprocess
    import sys
    import venv
    from pathlib import Path

    logger.info(f"Installing dependencies from {requirements_path} to {target_dir}")

    # Create a temporary virtual environment
    with tempfile.TemporaryDirectory() as temp_env_dir:
        logger.debug(f"Creating temporary venv in {temp_env_dir}")
        venv.create(temp_env_dir, with_pip=True)

        # Get path to pip in the new venv
        if sys.platform == "win32":
            pip_path = Path(temp_env_dir) / "Scripts" / "pip"
        else:
            pip_path = Path(temp_env_dir) / "bin" / "pip"

        try:
            # First, install packages to get their dependencies
            subprocess.check_call([
                str(pip_path),
                "install",
                "-r", requirements_path,
                "--target", target_dir,
                "--platform", "manylinux2014_x86_64",
                "--implementation", "cp",
                "--python-version", "311",  # Python 3.11
                "--only-binary=:all:",
                "--upgrade"
            ])

            # Install certifi for SSL certificates
            subprocess.check_call([
                str(pip_path),
                "install",
                "certifi",
                "--target", target_dir,
                "--platform", "manylinux2014_x86_64",
                "--implementation", "cp",
                "--python-version", "311",
                "--only-binary=:all:",
                "--upgrade"
            ])

            logger.info("Successfully installed dependencies")

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e.output if hasattr(e, 'output') else str(e)}")
            raise click.ClickException(f"Failed to install dependencies: {str(e)}")

def create_deployment_zip(config_path: str) -> tuple[str, dict]:
    """Create a ZIP file from the directory containing lambda_config.json."""
    logger.info(f"Reading config from: {config_path}")

    # Read and transform config
    with open(config_path, 'r') as f:
        user_config = json.load(f)

    config = validate_and_transform_config(user_config)
    logger.debug(f"Transformed config: {json.dumps(config, indent=2)}")

    # Get the directory containing lambda_config.json
    base_dir = os.path.dirname(os.path.abspath(config_path))
    zip_path = os.path.join(base_dir, "deployment.zip")

    logger.info(f"Creating ZIP file at: {zip_path}")
    logger.info(f"Base directory: {base_dir}")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a directory for the Lambda package
        package_dir = os.path.join(temp_dir, "package")
        os.makedirs(package_dir)

        # Install dependencies to the package directory
        requirements_path = os.path.join(base_dir, "requirements.txt")
        if os.path.exists(requirements_path):
            try:
                install_dependencies(requirements_path, package_dir)
            except Exception as e:
                logger.error(f"Failed to install dependencies: {str(e)}")
                raise click.ClickException("Failed to create deployment package")

        # Create ZIP file
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add lambda config
            zipf.writestr('lambda_config.json', json.dumps(config))

            # Add the handler file maintaining src directory structure
            handler_path = os.path.join(base_dir, config["handler_file"])
            if not os.path.exists(handler_path):
                raise click.ClickException(f"Handler file not found: {handler_path}")
            zipf.write(handler_path, config["handler_file"])
            logger.debug(f"Added handler: {config['handler_file']}")

            # Add all installed dependencies from package directory
            for root, _, files in os.walk(package_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    # Get relative path from package directory
                    arc_path = os.path.relpath(full_path, package_dir)
                    zipf.write(full_path, arc_path)
                    logger.debug(f"Added dependency: {arc_path}")

            # Add other project files
            if config.get("include_files"):
                for include_file in config["include_files"]:
                    if include_file != "requirements.txt":
                        file_path = os.path.join(base_dir, include_file)
                        if os.path.exists(file_path):
                            zipf.write(file_path, include_file)
                            logger.debug(f"Added included file: {include_file}")

    # Verify ZIP contents
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        logger.info("ZIP contents:")
        for filename in zipf.namelist():
            logger.info(f"  - {filename}")

    return zip_path, config

@click.group()
def cli():
    """
    LMSystems CLI - Deploy and manage AI nodes and graphs.

    Basic Commands:
      lmsystems node up              Deploy a node
      lmsystems node up -v           Deploy with verbose logging
      lmsystems node up -c config    Deploy with custom config
      lmsystems node --help          Show detailed node options

    Quick Start:
      1. Create lmsystems.json:
         {
             "nodes": {
                 "my-node": {
                     "file": "handler.py",
                     "function": "lambda_handler"
                 }
             },
             "description": "My node",
             "python_version": "3.11"
         }

      2. Set your API key:
         export LMSYSTEMS_API_KEY=your-key

      3. Deploy your node:
         lmsystems node up

    Options:
      --help          Show this message
      -v, --verbose   Enable detailed logging
      --version       Show version

    Need help? Visit https://lmsystems.ai/contact
    """
    pass

@cli.group()
def node():
    """
    Manage custom AI nodes on the LMSystems platform.

    Commands:
      up    Deploy a node to LMSystems

    Options:
      -c, --config    Config file path (default: lmsystems.json)
      -t, --api_key   Your API key (or set LMSYSTEMS_API_KEY env)
      -u, --url       Custom backend URL
      -v, --verbose   Enable detailed logging

    Config Options (lmsystems.json):
      nodes*          Your node name and handler file
      description     Node description
      python_version  Python runtime (default: 3.11)
      dependencies    Files to include (use ["."] for all)
      env            Path to .env file
      memory_size    Lambda memory in MB (128-10240)
      timeout        Lambda timeout in seconds (1-900)
      directions     Path to README.md file

      * Required fields

    Examples:
      lmsystems node up
      lmsystems node up -v
      lmsystems node up -c custom.json
      lmsystems node up -t your-api-key
    """
    pass

@node.command()
@click.option('--config', '-c',
              default='lmsystems.json',
              help='Path to your lmsystems.json configuration file')
@click.option('--api_key', '-t',
              envvar='LMSYSTEMS_API_KEY',
              help='Your LMSystems API key (or set LMSYSTEMS_API_KEY env var)')
@click.option('--url', '-u',
              default=Config.DEFAULT_BASE_URL,
              help='Custom backend URL (optional)')
@click.option('--verbose', '-v',
              is_flag=True,
              help='Enable detailed logging output')
def up(config, api_key, url, verbose):
    """
    Deploy a custom node to the LMSystems platform.

    This command packages and deploys your node code as a serverless function.
    It will:
    1. Read your lmsystems.json configuration
    2. Package your node code and dependencies
    3. Deploy to LMSystems as a serverless function
    4. Return node ID and API key for integration

    OPTIONS:
      -c, --config    Config file path (default: lmsystems.json)
      -t, --api_key   Your API key (or set LMSYSTEMS_API_KEY env var)
      -u, --url       Custom backend URL
      -v, --verbose   Enable detailed logging

    EXAMPLES:
      $ lmsystems node up
      $ lmsystems node up --config custom-config.json
      $ lmsystems node up --verbose
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    logger.info(f"Backend URL: {url}")
    logger.info(f"API Key: {api_key[:8]}..." if api_key else "No API Key provided")

    if not os.path.exists(config):
        raise click.ClickException(f"Config file not found: {config}")

    # Read config file
    with open(config, 'r') as f:
        user_config = json.load(f)

    # Use API key from config file if not provided via CLI or env var
    if not api_key and "api_key" in user_config:
        api_key = user_config["api_key"]
        logger.info("Using API key from lmsystems.json")

    if not api_key:
        raise click.ClickException("API key required. Set via:\n" +
                                 "1. LMSYSTEMS_API_KEY environment variable\n" +
                                 "2. --api_key command line option\n" +
                                 "3. api_key field in lmsystems.json")

    # Initialize zip_path
    zip_path = None

    try:
        # Create deployment package
        click.echo("Creating deployment package...")
        zip_path, config_data = create_deployment_zip(config)

        # Read and encode the zip
        with open(zip_path, "rb") as f:
            zip_data = f.read()
        encoded_zip = base64.b64encode(zip_data).decode("utf-8")
        logger.debug(f"ZIP file size: {len(zip_data)} bytes")

        # Prepare metadata
        metadata = {
            "name": config_data.get("name", "CustomNode"),
            "version": config_data.get("version", "0.1.0"),
            "description": config_data.get("description", ""),
            "directions": config_data.get("directions")
        }
        logger.debug(f"Metadata: {json.dumps(metadata, indent=2)}")

        # Upload the node
        click.echo("Uploading node...")
        try:
            response = upload_custom_node(
                node_code=encoded_zip,
                metadata=metadata,
                client_token=api_key,
                backend_url=url
            )
        except Exception as upload_error:
            logger.error(f"Upload failed with error: {str(upload_error)}")
            if hasattr(upload_error, 'response'):
                logger.error(f"Response status code: {upload_error.response.status_code}")
                logger.error(f"Response headers: {upload_error.response.headers}")
                logger.error(f"Response body: {upload_error.response.text}")
            raise

        # Cleanup
        if zip_path and os.path.exists(zip_path):
            os.remove(zip_path)

        click.echo("\nNode deployed successfully! 🚀")
        click.echo(f"Node ID: {response['node_id']}")
        click.echo(f"Endpoint URL: {response['endpoint_url']}")
        click.echo(f"API Key: {response['api_key']}")

    except Exception as e:
        # Safe cleanup
        if zip_path and os.path.exists(zip_path):
            os.remove(zip_path)
        raise click.ClickException(str(e))