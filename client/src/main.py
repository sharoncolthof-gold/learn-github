"""Simple HTTP Client for app_client component."""

import os
import sys
import time
import requests


def get_base_url() -> str:
    """Resolve base URL from environment or fallback to localhost."""
    server_url = os.environ.get("SERVER_URL", "app_server")
    return f"http://{server_url}:8080"


def check_health(base_url: str, timeout: float = 3.0) -> dict:
    """Query /health endpoint on the server."""
    url = f"{base_url}/health"
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return response.json()


def say_hello(base_url: str, name: str = "Developer", timeout: float = 3.0) -> dict:
    """Query /hello endpoint on the server."""
    url = f"{base_url}/hello"
    response = requests.get(url, params={"name": name}, timeout=timeout)
    response.raise_for_status()
    return response.json()


def send_echo(base_url: str, data: dict, timeout: float = 3.0) -> dict:
    """Query POST /echo endpoint on the server."""
    url = f"{base_url}/echo"
    response = requests.post(url, json=data, timeout=timeout)
    response.raise_for_status()
    return response.json()


def run_client(base_url: str = None, retries: int = 5, retry_delay: float = 1.0) -> bool:
    """Run full client verification suite against the server."""
    target_url = (base_url or get_base_url()).rstrip("/")
    print(f"[app_client] Connecting to app_server at {target_url}...")

    # Wait for server readiness if starting up
    health_data = None
    for attempt in range(1, retries + 1):
        try:
            health_data = check_health(target_url)
            break
        except Exception as exc:
            if attempt < retries:
                print(f"[app_client] Server not ready yet (attempt {attempt}/{retries}): {exc}. Retrying...")
                time.sleep(retry_delay)
            else:
                print(f"[app_client] Could not reach server at {target_url}: {exc}")
                return False

    print(f"[app_client] Health check SUCCESS: {health_data}")

    hello_data = say_hello(target_url, name="DockerUser")
    print(f"[app_client] Hello check SUCCESS: {hello_data}")

    echo_data = send_echo(target_url, {"project": "create_pro", "status": "testing"})
    print(f"[app_client] Echo check SUCCESS: {echo_data}")

    print("[app_client] All tests passed successfully!")
    return True


if __name__ == "__main__":
    success = run_client()
    sys.exit(0 if success else 1)
