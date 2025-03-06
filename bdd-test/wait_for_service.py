#!/usr/bin/env python3

import sys
import time
import socket
import requests
from urllib.parse import urlparse
from colorama import Fore, Style, init

# Initialize colorama for cross-platform support
init(autoreset=True)


def print_message(message, color, emoji=""):
    """Helper function to print colored messages with an optional emoji."""
    print(f"{color}{emoji} {message}{Style.RESET_ALL}")


def wait_for_http(url, timeout):
    """Wait for an HTTP service to be available."""
    print_message(f"Waiting for HTTP endpoint: {url} with a timeout of {timeout} seconds...", Fore.CYAN, "🌍")
    start_time = time.time()

    while True:
        try:
            response = requests.head(url, timeout=5)
            if response.status_code < 500:  # Accept 2xx, 3xx, and even 4xx (but not 5xx)
                print_message(f"HTTP endpoint {url} is available.", Fore.GREEN, "✅")
                return True
        except requests.RequestException:
            pass

        if time.time() - start_time >= timeout:
            print_message(f"Timeout reached for HTTP endpoint: {url}", Fore.RED, "🚨")
            sys.exit(1)

        time.sleep(1)


def wait_for_tcp(host, port, timeout):
    """Wait for a TCP service to be available."""
    print_message(f"Waiting for TCP connection: {host}:{port} with a timeout of {timeout} seconds...", Fore.CYAN, "🌍")
    start_time = time.time()

    while True:
        try:
            with socket.create_connection((host, int(port)), timeout=5):
                print_message(f"TCP connection to {host}:{port} is available.", Fore.GREEN, "✅")
                return True
        except (socket.timeout, ConnectionRefusedError):
            pass

        if time.time() - start_time >= timeout:
            print_message(f"Timeout reached for TCP connection: {host}:{port}", Fore.RED, "🚨")
            sys.exit(1)

        time.sleep(1)


def wait_for_service(service_url, timeout):
    """Determine whether to wait for HTTP or TCP based on the URL scheme."""
    parsed_url = urlparse(service_url)
    if parsed_url.scheme in ("http", "https"):
        wait_for_http(service_url, timeout)
    elif parsed_url.scheme == "tcp":
        host, port = parsed_url.netloc.split(":")
        wait_for_tcp(host, port, timeout)
    else:
        print_message(f"⚠️ Invalid service URL format: {service_url}", Fore.YELLOW, "⚠️")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_message("Usage: wait_for_service.py <service_url> <timeout_seconds>", Fore.GREEN, "ℹ️")
        sys.exit(1)

    service_url = sys.argv[1]
    timeout = int(sys.argv[2])

    wait_for_service(service_url, timeout)
