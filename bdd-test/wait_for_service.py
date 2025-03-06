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


def wait_for(check_function, service_info, timeout, service_type):
    """
    Generic wait function for HTTP and TCP.

    check_function: Function to check service availability
    service_info: URL or (host, port) tuple
    timeout: Max wait time
    service_type: "HTTP" or "TCP"
    """
    print_message(f"Waiting for {service_type} service: {service_info} with a timeout of {timeout} seconds...",
                  Fore.CYAN, "⏳")
    start_time = time.time()

    while time.time() - start_time < timeout:
        if check_function(service_info):
            print_message(f"{service_type} service {service_info} is available.", Fore.GREEN, "✅")
            return True
        time.sleep(1)

    print_message(f"Timeout reached for {service_type} service: {service_info}", Fore.RED, "🚨")
    sys.exit(1)


def check_http(url):
    """Check if an HTTP service is available."""
    try:
        response = requests.head(url, timeout=5)
        return response.status_code < 500  # Accept 2xx, 3xx, and even 4xx (but not 5xx)
    except requests.RequestException:
        return False


def check_tcp(host_port):
    """Check if a TCP connection can be established."""
    host, port = host_port
    try:
        with socket.create_connection((host, int(port)), timeout=5):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False


def wait_for_service(service_url, timeout):
    """Determine whether to wait for an HTTP or TCP service."""
    parsed_url = urlparse(service_url)
    if parsed_url.scheme in ("http", "https"):
        wait_for(check_http, service_url, timeout, "HTTP")
    elif parsed_url.scheme == "tcp":
        host, port = parsed_url.netloc.split(":")
        wait_for(check_tcp, (host, port), timeout, "TCP")
    else:
        print_message(f"Invalid service URL format: {service_url}", Fore.RED, "⚠️")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_message("Usage: wait_for_service.py <service_url> <timeout_seconds>", Fore.YELLOW, "ℹ️")
        sys.exit(1)

    service_url = sys.argv[1]
    timeout = int(sys.argv[2])

    wait_for_service(service_url, timeout)
