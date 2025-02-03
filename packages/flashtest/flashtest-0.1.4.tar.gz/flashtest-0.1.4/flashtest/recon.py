import subprocess
import requests
import socket
import whois

def get_dns_info(domain):
    """
    Perform a basic DNS lookup on the domain.
    """
    print(f"Gathering DNS information for {domain}...")

    try:
        # Use 'dig' to get DNS information (assumes it's installed)
        result = subprocess.run(['dig', domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"DNS Information for {domain}:\n{result.stdout.decode()}")
        else:
            print(f"Error running dig command: {result.stderr.decode()}")
    except FileNotFoundError:
        print("The 'dig' command is not found. Please install it to use this feature.")

def get_whois_info(domain):
    """
    Perform a WHOIS lookup on the domain to get ownership information.
    """
    print(f"Gathering WHOIS information for {domain}...")

    try:
        # Perform WHOIS lookup
        whois_info = whois.whois(domain)
        print(f"WHOIS Information for {domain}:\n{whois_info}")
    except Exception as e:
        print(f"Error retrieving WHOIS information: {e}")

def get_ip_info(ip):
    """
    Perform a reverse DNS lookup and geolocation info based on IP.
    """
    print(f"Gathering IP information for {ip}...")

    try:
        # Reverse DNS lookup
        reverse_dns = socket.gethostbyaddr(ip)
        print(f"Reverse DNS for {ip}: {reverse_dns}")
    except socket.herror:
        print(f"No reverse DNS entry for IP: {ip}")

    # Geolocation lookup (using a free API)
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        ip_data = response.json()
        print(f"Geolocation Info for {ip}: {ip_data}")
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving geolocation data: {e}")
