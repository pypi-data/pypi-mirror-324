# Flashtest

Flashtest is a powerful CLI-based penetration testing tool designed to assist in reconnaissance, vulnerability scanning, and AI-driven exploit simulations. It integrates with various security tools to provide comprehensive security testing for web applications, servers, and networks.

## Features

- **Reconnaissance**: Perform DNS lookups, WHOIS searches, and gather IP information.
- **Vulnerability Scanning**: Run SQL injection tests, Nmap port scanning, and Nikto scans.
- **AI-Assisted Exploitation**: Use AI to simulate exploit scenarios for testing vulnerabilities.
  
## Installation

### 1. Clone the repository or download the source code:
```bash
git clone https://github.com/yourusername/flashtest.git
cd flashtest
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Install `flashtest` globally:
```bash
python setup.py install
```

### 4. Verify the installation:
```bash
flashtest --help
```

## Usage

Flashtest provides several commands for performing penetration testing operations.

### Reconnaissance Commands

#### DNS Information:
Get DNS information for a domain.
```bash
flashtest --dns example.com
```

#### WHOIS Information:
Retrieve WHOIS data for a domain.
```bash
flashtest --whois example.com
```

#### IP Information (Reverse DNS + Geolocation):
Get IP info, including reverse DNS and geolocation data.
```bash
flashtest --ipinfo 192.168.1.1
```

### Scanning Commands

#### SQL Injection Test:
Test for SQL Injection vulnerabilities on a web page (e.g., login form).
```bash
flashtest --sql http://example.com/login
```

#### Nmap Port Scan:
Scan a target for open ports using Nmap.
```bash
flashtest --nmap 192.168.1.1
```

#### Nikto Scan:
Run a basic security scan using Nikto.
```bash
flashtest --nikto http://example.com
```

### AI-Driven Exploitation

#### Simulate AI-Driven Exploitation:
Use AI to simulate a penetration test on a web target and find potential vulnerabilities.
```bash
flashtest --ai-exploit http://example.com
```

### Combined Vulnerability Identification

#### Identify SQL and Nikto Vulnerabilities:
Automatically identify SQL injection vulnerabilities and run Nikto for additional checks.
```bash
flashtest --identify http://example.com
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the open-source communities for tools like `requests`, `whois`, `nmap`, `nikto`, and others that helped make this tool possible.


### Key Points:

1. **Installation**:
   - Instructions to clone the repository, install dependencies, and set up `flashtest`.
2. **Usage**:
   - Detailed descriptions of the available commands (Recon, Scanning, AI Exploitation).
3. **License**:
   - MIT License, with a link to the license file.
4. **Acknowledgments**:
   - Thanks to libraries that helped build `flashtest`.