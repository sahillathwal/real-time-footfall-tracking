import argparse
import subprocess
import os

docker_image = "sahillathwal/rtft:latest"

def run_container():
    """Run the pre-built container."""
    subprocess.run("docker-compose up -d", shell=True)

def stop_container():
    """Stop and remove running containers."""
    subprocess.run("docker-compose down", shell=True)

def build_image(force=False, clean=False):
    """Build the Docker image locally."""
    cmd = "docker build -t sahillathwal/rtft:latest ."
    if force:
        cmd = "docker build --no-cache -t sahillathwal/rtft:latest ."
    if clean:
        subprocess.run("docker system prune -a -f", shell=True)
    subprocess.run(cmd, shell=True)

def pull_image():
    """Pull the latest container image from Docker Hub."""
    subprocess.run(f"docker pull {docker_image}", shell=True)

def check_existing_image():
    """Check if the Docker image exists locally."""
    images = subprocess.check_output(["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"]).decode("utf-8").splitlines()
    if docker_image in images:
        print(f"Image {docker_image} exists locally.")
        return True
    else:
        print(f"Image {docker_image} not found locally.")
        return False

def show_logs():
    """Show logs from the running container."""
    subprocess.run("docker-compose logs -f", shell=True)

def exec_command(command):
    """Execute a command inside the running container."""
    subprocess.run(f"docker exec -it rtft_app_1 {command}", shell=True)

def init_app():
    """Initialize the application by pulling Docker images."""
    pull_image()

def dev_mode(root=False, commit=False, vscode=False, terminator=False):
    """Enter development mode inside the container."""
    cmd = "docker exec -it rtft_app_1 /bin/bash"
    if root:
        cmd = "docker exec -it -u 0 rtft_app_1 /bin/bash"
    if commit:
        subprocess.run(f"docker commit rtft_app_1 {docker_image}", shell=True)
    if vscode:
        subprocess.run("code .", shell=True)
    if terminator:
        subprocess.run("terminator", shell=True)
    subprocess.run(cmd, shell=True)

def get_parser():
    parser = argparse.ArgumentParser(description="CLI for Real-Time Footfall Tracking System")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    subparsers.add_parser("run", help="Start the container")
    subparsers.add_parser("stop", help="Stop the container")
    subparsers.add_parser("pull", help="Pull the latest Docker image")
    subparsers.add_parser("logs", help="Show container logs")
    subparsers.add_parser("check", help="Check if the Docker image exists locally")
    subparsers.add_parser("init", help="Initialize the application")
    
    build_parser = subparsers.add_parser("build", help="Build the Docker image locally")
    build_parser.add_argument("--force", "-f", action="store_true", help="Force rebuild without cache")
    build_parser.add_argument("--clean", "-c", action="store_true", help="Clean intermediate build files")
    
    dev_parser = subparsers.add_parser("dev", help="Enter development mode inside the container")
    dev_parser.add_argument("--root", "-r", action="store_true", help="Run as root user")
    dev_parser.add_argument("--commit", "-c", action="store_true", help="Commit changes to the image")
    dev_parser.add_argument("--vscode", "-v", action="store_true", help="Attach container in VS Code")
    dev_parser.add_argument("--terminator", "-t", action="store_true", help="Open terminal in Terminator")
    
    exec_parser = subparsers.add_parser("exec", help="Execute a command inside the running container")
    exec_parser.add_argument("command", type=str, help="Command to run inside the container")
    
    return parser

def parse_args():
    parser = get_parser()
    args = parser.parse_args()
    
    if args.command == "run":
        run_container()
    elif args.command == "stop":
        stop_container()
    elif args.command == "pull":
        pull_image()
    elif args.command == "logs":
        show_logs()
    elif args.command == "check":
        check_existing_image()
    elif args.command == "build":
        build_image(force=args.force, clean=args.clean)
    elif args.command == "init":
        init_app()
    elif args.command == "dev":
        dev_mode(root=args.root, commit=args.commit, vscode=args.vscode, terminator=args.terminator)
    elif args.command == "exec":
        exec_command(args.command)
    else:
        parser.print_help()

if __name__ == "__main__":
    parse_args()
