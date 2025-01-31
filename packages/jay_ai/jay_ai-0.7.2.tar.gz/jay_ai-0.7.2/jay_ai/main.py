import sys
import os
import subprocess
import signal
import click
import httpx
import requests
import uvicorn
from dotenv import load_dotenv
import time
import socket
import webbrowser
import threading
import shutil
import importlib.resources
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from jay_ai.loader import load_parsed_agent
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from pyngrok import ngrok
from jay_ai.utils import fetch_site_url, fetch_headers
from jay_ai.cli.init import init_cli_command

# ------------------------------------------------------------------------------
# Load Environment Variables
# ------------------------------------------------------------------------------
load_dotenv()

platform_url = fetch_site_url()
api_protection_bypass_secret = os.getenv("VERCEL_AUTOMATION_BYPASS_SECRET")
developer_id = os.getenv("JAY_DEVELOPER_ID")
api_key = os.getenv("JAY_API_KEY")

headers = fetch_headers(api_key)


def ensure_valid_agent_path(agent_path: str):
    if agent_path.endswith("main.py"):
        return
    else:
        raise Exception("Agent must be stored in a file named main.py")


def get_playground_path():
    """Determine the path to the playground directory."""
    dev_path = os.path.abspath("./services/playground/out")
    if os.path.exists(dev_path):
        return dev_path

    prod_path = os.path.join(os.path.dirname(__file__), "static/playground")
    if os.path.exists(prod_path):
        return prod_path

    click.secho(
        "Error: Playground directory not found in development or production locations.",
        fg="red",
        bold=True,
    )
    sys.exit(1)


async def call_get_token(request: Request) -> JSONResponse:
    request_body = await request.json()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{platform_url}/api/startSession",
                headers=headers,
                json=request_body,
            )

            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error response {exc.response.status_code}: {exc.response.text}",
            ) from exc

    return JSONResponse(status_code=response.status_code, content=response.json())


@click.group()
def cli():
    pass


@cli.command()
def init():
    """
    Initialize a new project.
    """

    init_cli_command()


@cli.command()
@click.option(
    "--agent",
    "agent_path",
    type=str,
    required=True,
    help="Path to the file containing your Agent.",
)
@click.option("--host", type=str, default="localhost", help="Host to run the agent on.")
@click.option("--port", type=int, default=8000, help="Port to run the agent on.")
@click.option(
    "--connect", "-c", is_flag=True, help="Automatically open the playground."
)
def run(agent_path, host, port, connect):
    """
    Run the playground with a local agent.
    """
    agent_path_abs = os.path.abspath(agent_path)
    if not os.path.isfile(agent_path_abs):
        click.secho(
            f"The functions path {agent_path_abs} is not a file.", fg="red", bold=True
        )
        sys.exit(1)

    if not api_key:
        raise Exception(
            "Did not detect a 'JAY_API_KEY'. Please define it in your .env file."
        )

    if not developer_id:
        raise Exception(
            "Did not detect a 'JAY_DEVELOPER_ID'. Please define it in your .env file."
        )

    os.environ["JAY_INTERNAL__AGENT_API_KEY"] = api_key

    ensure_valid_agent_path(agent_path_abs)

    print(f"Loading agent from: {agent_path_abs}")
    agent = load_parsed_agent(agent_path_abs)
    app = agent.create_api(
        report_status=False,
        skip_security_check=True,
        deployment_id="not-required-during-dev",
    )

    # Determine and serve the playground files
    playground_path = get_playground_path()
    app.mount(
        "/playground",
        StaticFiles(directory=playground_path, html=True),
        name="playground",
    )

    @app.post("/jay/getToken")
    async def get_token(request: Request):
        return await call_get_token(request)

    # Allows the playground to fetch the JAY_AGENT_ID specified by the user in their .env file
    @app.get("/jay/fetch_agent_id")
    def fetch_agent_id():
        return JSONResponse(
            content={
                "AGENT_ID": agent.id,
                "ENVIRONMENT": "development",
                "DEVELOPER_ID": developer_id,
            }
        )

    # Setup ngrok tunnel
    http_tunnel = ngrok.connect(addr=str(port))
    url = http_tunnel.public_url
    update_development_url = f"{platform_url}/api/updateDevelopmentUrl"
    payload = {
        "agent_id": agent.id,
        "developer_id": developer_id,
        "url": url,
    }
    response = requests.post(update_development_url, json=payload, headers=headers)
    if response.status_code != 200:
        print(response.text)
        response.raise_for_status()

    def cleanup(_a, _b):
        click.secho("Shutting down processes...", fg="yellow", bold=True)
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    click.secho(
        f"Starting Agent API server at http://{host}:{port}", fg="green", bold=True
    )
    playground_url = f"http://{host}:{port}/playground"
    click.secho(f"Playground is available at {playground_url}", fg="cyan")
    if connect:
        webbrowser.open(url=playground_url, new=2)

    try:
        uvicorn.run(app, host=host, port=port, log_level="debug")
    except KeyboardInterrupt:
        cleanup()


@cli.command()
@click.option(
    "--agent",
    "agent_path",
    type=str,
    default=None,
    help="Path to the file containing your agent.",
)
@click.option(
    "--agent-id",
    type=str,
    default=None,
    help="Use an Agent ID to connect to a deployed agent.",
)
@click.option(
    "--host", type=str, default="localhost", help="Host to run the playground on."
)
@click.option("--port", type=int, default=8000, help="Port to run the playground on.")
def connect(agent_path, agent_id, host, port):
    """
    Connect to a deployed agent.
    """

    # Ensure the user did not supply both or neither
    if (agent_path and agent_id) or (not agent_path and not agent_id):
        click.secho(
            "Error: Please provide EITHER --agent OR --agent-id (but not both).",
            fg="red",
            bold=True,
        )
        sys.exit(1)

    app = FastAPI()

    # Determine and serve the playground files
    playground_path = get_playground_path()
    app.mount(
        "/playground",
        StaticFiles(directory=playground_path, html=True),
        name="playground",
    )

    # If an agent path was supplied, load it and override the agent_id
    if agent_path:
        agent = load_parsed_agent(agent_path)
        agent_id = agent.id

    @app.post("/jay/getToken")
    async def get_token(request: Request):
        return await call_get_token(request)

    # Allows the playground to fetch the JAY_AGENT_ID specified by the user
    @app.get("/jay/fetch_agent_id")
    def fetch_agent_id():
        return JSONResponse(
            content={
                "AGENT_ID": agent.id,
                "ENVIRONMENT": "production",
            }
        )

    def cleanup(_a, _b):
        click.secho("Shutting down processes...", fg="yellow", bold=True)
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    def start_uvicorn():
        uvicorn.run(app, host=host, port=port, log_level="debug")

    try:
        server_thread = threading.Thread(target=start_uvicorn, daemon=True)
        server_thread.start()

        url = f"http://{host}:{port}/playground"
        click.secho(f"Playground is available at {url}", fg="cyan")
        time.sleep(1)
        webbrowser.open(url=url, new=2)

        server_thread.join()
    except KeyboardInterrupt:
        cleanup()


@cli.command()
@click.option(
    "--agent",
    "agent_path",
    type=str,
    required=True,
    help="Path to the file containing your Agent.",
)
@click.option(
    "--requirement",
    "-r",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="Path to requirements.txt containing agent dependencies.",
)
def deploy(agent_path, requirement):
    """
    Build and deploy the agent.
    """

    click.secho("Deploying agent to Jay platform...", fg="cyan", bold=True)
    agent_path_abs = os.path.abspath(agent_path)
    if not os.path.isfile(agent_path_abs):
        click.secho(
            f"The functions path {agent_path_abs} is not a file.", fg="red", bold=True
        )
        sys.exit(1)

    ensure_valid_agent_path(agent_path_abs)

    # API endpoints
    create_deployment_endpoint = f"{platform_url}/api/deploy/create"
    trigger_build_endpoint = f"{platform_url}/api/deploy/build"
    status_url = f"{platform_url}/api/serviceStatus/fetch"
    cancel_deployment_endpoint = f"{platform_url}/api/deploy/cancel"

    agent_dir = os.path.dirname(agent_path)
    local_package_path = os.getenv("JAY_INTERNAL__LOCAL_PACKAGE_PATH", None)
    tmp_jay_dir = ".tmp_jay"
    target = "prod"

    # [1/7] Acquire deployment resources
    click.secho("[1/7] Acquiring deployment resources...", fg="cyan", bold=True)
    agent = load_parsed_agent(agent_path_abs)

    try:
        create_deployment_payload = {"agent_id": agent.id}
        create_deployment_payload_resp = requests.post(
            create_deployment_endpoint, headers=headers, json=create_deployment_payload
        )
        if create_deployment_payload_resp.status_code != 200:
            click.secho(
                f"Failed to get presigned URL: "
                f"{create_deployment_payload_resp.status_code} - {create_deployment_payload_resp.text}",
                fg="red",
                bold=True,
            )
            sys.exit(1)
        deployment_data = create_deployment_payload_resp.json()
        upload_url = deployment_data["presignedUrl"]
        deployment_id = deployment_data["deploymentId"]
        click.secho(f"  ✓ Deployment ID: {deployment_id}", fg="green")
    except requests.exceptions.RequestException as e:
        click.secho(f"Error triggering Build: {e}", fg="red", bold=True)
        sys.exit(1)

    def call_cancel_deployment():
        try:
            cancel_deployment_payload = {"deployment_id": deployment_id}
            cancel_deployment_resp = requests.post(
                cancel_deployment_endpoint,
                headers=headers,
                json=cancel_deployment_payload,
            )
            if cancel_deployment_resp.status_code == 200:
                click.secho("Deployment canceled!", fg="yellow")
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            click.secho(f"Error canceling deployment: {e}", fg="red", bold=True)
            sys.exit(1)

    def signal_handler(signum, frame):
        click.secho(
            f"Canceling deployment: {deployment_id} and exiting gracefully...",
            fg="yellow",
        )
        call_cancel_deployment()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if local_package_path:
        click.secho(
            "Using local jay source to build (dev mode)...",
            fg="cyan",
            bold=True,
        )
        target = "dev"

        if os.path.exists(tmp_jay_dir):
            shutil.rmtree(tmp_jay_dir)

        os.makedirs(f"{tmp_jay_dir}/jay", exist_ok=True)

        jay_src = Path(local_package_path).resolve()
        if not jay_src.is_dir():
            click.secho(
                f"The local_package_path {jay_src} is not a valid directory.",
                fg="red",
                bold=True,
            )
            sys.exit(1)

        shutil.copytree(str(jay_src), f"{tmp_jay_dir}/jay_ai", dirs_exist_ok=True)

        pyproject_src = jay_src.parent / "pyproject.toml"
        if not pyproject_src.is_file():
            click.secho(
                f"Could not find pyproject.toml at {pyproject_src}", fg="red", bold=True
            )
            sys.exit(1)
        shutil.copy(str(pyproject_src), f"{tmp_jay_dir}/pyproject.toml")
    else:
        click.secho("Using standard jay source (prod mode)...", fg="cyan", bold=True)

    click.secho("[2/7] Building Docker image (agent-api)...", fg="cyan", bold=True)
    click.secho(f"  - Source directory: {agent_dir}", fg="white")

    with importlib.resources.path("jay_ai", "Dockerfile") as dockerfile_path:
        build_cmd = [
            "docker",
            "build",
            "--build-arg",
            f"AGENT_SRC_PATH={agent_dir}",
            "--build-arg",
            f"DEPLOYMENT_ID={deployment_id}",
            "--build-arg",
            f"REQUIREMENT={requirement}",
            "--target",
            target,
            "-t",
            "agent-api",
            "-f",
            str(dockerfile_path),
            "--platform",
            "linux/amd64",
            ".",
        ]
        if local_package_path:
            build_cmd.insert(6, "--build-arg")
            build_cmd.insert(7, f"LOCAL_PACKAGE_PATH={tmp_jay_dir}")

        try:
            subprocess.run(build_cmd, check=True)
            click.secho("  ✓ Docker image built successfully.", fg="green", bold=True)
        except subprocess.CalledProcessError as e:
            click.secho(
                f"Docker build failed with unknown error: {e}", fg="red", bold=True
            )
            call_cancel_deployment()
            sys.exit(1)
        finally:
            # Cleanup the .tmp_jay dir if we created it
            if local_package_path and os.path.exists(tmp_jay_dir):
                shutil.rmtree(tmp_jay_dir, ignore_errors=True)

    click.secho("[3/7] Verifying Docker container health...", fg="cyan", bold=True)
    container_name = f"agent-api-test-{deployment_id}"
    host_port = get_free_port()
    run_cmd = [
        "docker",
        "run",
        "-d",
        "--name",
        container_name,
        "-p",
        f"{host_port}:10000",
        "--platform",
        "linux/amd64",
        "agent-api",
    ]

    try:
        subprocess.run(run_cmd, check=True)
        click.secho(
            f"  - Container '{container_name}' started on port {host_port}.", fg="white"
        )

        # Health check
        wait_for_container_health(host_port, timeout=30)
        click.secho(
            "  ✓ Container is healthy (200 from /health).", fg="green", bold=True
        )

    except subprocess.CalledProcessError as e:
        click.secho(
            f"Error running Docker container health check: {e}", fg="red", bold=True
        )
        print_container_logs(container_name)
        call_cancel_deployment()
        sys.exit(1)
    except TimeoutError as e:
        click.secho(f"Health check failed: {e}", fg="red", bold=True)
        print_container_logs(container_name)
        call_cancel_deployment()
        sys.exit(1)
    except Exception as e:
        click.secho(
            f"Unknown error running Docker container health check: {e}",
            fg="red",
            bold=True,
        )
        print_container_logs(container_name)
        call_cancel_deployment()
        sys.exit(1)
    finally:
        cleanup_container(container_name)

    click.secho("[4/7] Saving Docker image...", fg="cyan", bold=True)
    temp_image_path = "/tmp/agent-api.tar"
    try:
        click.secho(f"  - Saving to {temp_image_path}", fg="white")
        subprocess.run(
            ["docker", "save", "-o", temp_image_path, "agent-api"], check=True
        )
        click.secho("  ✓ Docker image saved.", fg="green", bold=True)
    except Exception as e:
        click.secho(f"Error saving Docker image: {e}", fg="red", bold=True)
        call_cancel_deployment()
        sys.exit(1)

    click.secho("[5/7] 🚀 Uploading image to cloud...", fg="cyan", bold=True)
    try:
        with open(temp_image_path, "rb") as f:
            put_headers = {"Content-Type": "application/x-tar"}
            upload_resp = requests.put(upload_url, data=f, headers=put_headers)
        if upload_resp.status_code not in [200, 204]:
            click.secho(
                f"Failed to upload image: {upload_resp.status_code} - {upload_resp.text}",
                fg="red",
                bold=True,
            )
            call_cancel_deployment()
            sys.exit(1)

        click.secho("  ✓ Image uploaded successfully.", fg="green", bold=True)

    except Exception as e:
        click.secho(f"Error uploading Docker image: {e}", fg="red", bold=True)
        call_cancel_deployment()
        sys.exit(1)
    finally:
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
            click.secho(f"  - Removed temporary file {temp_image_path}.", fg="white")

    try:
        trigger_payload = {"deployment_id": deployment_id}
        trigger_resp = requests.post(
            trigger_build_endpoint, json=trigger_payload, headers=headers
        )
        if trigger_resp.status_code != 200:
            click.secho(
                f"Failed to trigger remote build: {trigger_resp.status_code} - {trigger_resp.text}",
                fg="red",
                bold=True,
            )
            call_cancel_deployment()
            sys.exit(1)
    except Exception as e:
        click.secho(f"Error triggering remote build: {e}", fg="red", bold=True)
        call_cancel_deployment()
        sys.exit(1)

    click.secho("[6/7] Polling deployment status...", fg="cyan", bold=True)
    payload = {"deployment_id": deployment_id}
    spinner = ["-", "\\", "|", "/"]
    idx = 0

    while True:
        try:
            response = requests.post(status_url, json=payload, headers=headers)
        except requests.exceptions.RequestException as e:
            click.secho(
                f"Error polling deployment status, please report this to the developer: {e}",
                fg="red",
                bold=True,
            )
            sys.exit(1)

        if response.status_code == 200:
            status_data = response.json()
            status = status_data.get("deploymentStatus", "")
            if status == "active":
                click.secho(
                    "\n  ✓ Deployment completed successfully!", fg="green", bold=True
                )
                break
            elif status == "failed":
                click.secho("  ✗ Deployment failed.", fg="red", bold=True)
                sys.exit(1)

            # Show a spinning indicator
            click.echo(f"\r  Deploying... {spinner[idx % len(spinner)]}", nl=False)
            idx += 1

        elif response.status_code == 404:
            click.secho(
                "  ✗ Deployment not found. Check the deployment ID.",
                fg="red",
                bold=True,
            )
            sys.exit(1)
        elif response.status_code == 400:
            click.secho(
                f"  ✗ Invalid request checking deployment status: "
                f"{response.status_code}, response: {response.json()}",
                fg="red",
                bold=True,
            )
            sys.exit(1)
        else:
            click.secho(
                f"  ✗ Error fetching status: {response.status_code} - {response.text}",
                fg="red",
                bold=True,
            )
            sys.exit(1)

        time.sleep(2)

    click.secho("Agent deployment process completed. ✨", fg="cyan", bold=True)
    click.secho(
        f"\nConnect in the playground:\n  jay connect --agent {agent_path}",
        fg="cyan",
        bold=True,
    )


def get_free_port():
    """Find a free port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def wait_for_container_health(port, timeout=30, interval=2):
    """Poll the /health endpoint until it's responsive or timeout is reached."""
    health_url = f"http://localhost:{port}/health"
    click.secho(
        f"  - Starting health check at {health_url} (timeout={timeout}s)...", fg="white"
    )

    start_time = time.time()
    while True:
        try:
            response = requests.get(health_url)
            if response.status_code == 200:
                return
        except requests.exceptions.ConnectionError:
            pass  # Container not ready yet

        if time.time() - start_time > timeout:
            raise TimeoutError(
                f"Health check at {health_url} timed out after {timeout}s."
            )
        time.sleep(interval)


def cleanup_container(container_name):
    """Stop and remove a Docker container."""
    try:
        subprocess.run(
            ["docker", "stop", container_name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        click.secho(f"  - Stopped container '{container_name}'.", fg="white")
        try:
            subprocess.run(
                ["docker", "rm", container_name],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            click.secho(f"  - Removed container '{container_name}'.", fg="white")
        except subprocess.CalledProcessError:
            click.secho(
                f"Container '{container_name}' could not be removed or does not exist.",
                fg="red",
                bold=True,
            )
    except subprocess.CalledProcessError:
        click.secho(f"Container '{container_name}' was not running.", fg="yellow")


def print_container_logs(container_name: str):
    """
    Retrieve and print the container logs in red for debugging.
    """
    click.secho(f"Retrieving logs for container '{container_name}'...", fg="yellow")
    try:
        result = subprocess.run(
            ["docker", "logs", container_name],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout:
            click.secho("--- Container Logs (STDOUT) ---", fg="red", bold=True)
            click.secho(result.stdout, fg="red")
        if result.stderr:
            click.secho("--- Container Logs (STDERR) ---", fg="red", bold=True)
            click.secho(result.stderr, fg="red")
    except Exception as ex:
        click.secho(
            f"Failed to retrieve logs for container '{container_name}': {ex}",
            fg="red",
            bold=True,
        )


if __name__ == "__main__":
    cli()
