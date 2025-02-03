import argparse
from flashtest.scanner import sql_injection_test, scan_nmap, scan_nikto, identify_vulnerabilities
from flashtest.recon import get_dns_info, get_whois_info, get_ip_info
from flashtest.ai_exploit import ai_exploit

def main():
    parser = argparse.ArgumentParser(description="Flashtest CLI Tool for Penetration Testing")

    # Reconnaissance Commands
    parser.add_argument('--dns', metavar='DOMAIN', type=str, help='Get DNS information for a domain.')
    parser.add_argument('--whois', metavar='DOMAIN', type=str, help='Get WHOIS information for a domain.')
    parser.add_argument('--ipinfo', metavar='IP', type=str, help='Get IP information (Reverse DNS and geolocation).')

    # Exploitation Commands
    parser.add_argument('--ai-exploit', metavar='TARGET', type=str, help='Run AI-driven exploit tests on a target.')

    # Scanning Commands
    parser.add_argument('--sql', metavar='URL', type=str, help='Test a URL for SQL Injection vulnerabilities.')
    parser.add_argument('--nmap', metavar='IP', type=str, help='Perform an Nmap scan on an IP address.')
    parser.add_argument('--nikto', metavar='URL', type=str, help='Run a Nikto scan on a URL.')
    parser.add_argument('--identify', metavar='URL', type=str, help='Identify vulnerabilities on a URL (SQL Injection & Nikto).')

    # Parse arguments
    args = parser.parse_args()

    # Reconnaissance Commands
    if args.dns:
        get_dns_info(args.dns)
    elif args.whois:
        get_whois_info(args.whois)
    elif args.ipinfo:
        get_ip_info(args.ipinfo)

    # Exploitation Commands
    elif args.ai_exploit:
        ai_exploit(args.ai_exploit)

    # SQL Injection Test
    elif args.sql:
        sql_injection_test(args.sql)

    # Nmap Scan
    elif args.nmap:
        scan_nmap(args.nmap)

    # Nikto Scan
    elif args.nikto:
        scan_nikto(args.nikto)

    # Identify vulnerabilities
    elif args.identify:
        identify_vulnerabilities(args.identify)

    else:
        print("No valid command provided. Use --help for usage instructions.")

if __name__ == "__main__":
    main()
