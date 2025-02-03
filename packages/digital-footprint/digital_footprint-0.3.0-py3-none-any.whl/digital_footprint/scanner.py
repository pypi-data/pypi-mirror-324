import re
import requests
from bs4 import BeautifulSoup
import whois
import dns.resolver
import hashlib
import urllib.parse
import argparse
import json
from datetime import datetime
from waybackpy import WaybackMachineSaveAPI
import socket
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class AdvancedFootprintScanner:
    def __init__(self):
        self.user_agent = "FootprintSearcher/2.0 (Professional OSINT Tool; +https://github.com/ivanMartin)"
        self.headers = {"User-Agent": self.user_agent}
        self.dork_operators = {
            'filetype': ['pdf', 'doc', 'docx', 'xls', 'xlsx'],
            'site': ['pastebin.com', 'github.com', 'stackoverflow.com'],
            'intitle': ['password', 'credentials', 'confidential'],
            'inurl': ['admin', 'login', 'secret']
        }
    
    # --- Helper Print Methods ---
    def _print_section_header(self, title):
        print(f"\n{Fore.CYAN}=== {title.upper()} ==={Style.RESET_ALL}")
    
    def _print_result(self, title, result, level='info'):
        colors = {
            'info': Fore.WHITE,
            'warning': Fore.YELLOW,
            'critical': Fore.RED,
            'success': Fore.GREEN
        }
        print(f"{colors.get(level, Fore.WHITE)}[•] {title}:{Style.RESET_ALL} {result}")

    # --- Basic Validations and Extraction ---
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def extract_username(self, email):
        return email.split('@')[0]

    def extract_domain(self, email):
        return email.split('@')[-1]

    # --- Advanced Dork Generation ---
    def advanced_dork_generator(self, email):
        base_dorks = [
            f'intext:"{email}"',
            f'filetype:log "user {email}"',
            f'site:pastebin.com "{email}"',
            f'inurl:"{self.extract_username(email)}"'
        ]
        # Append additional dorks from the operator table.
        for operator, values in self.dork_operators.items():
            for value in values:
                base_dorks.append(f'{operator}:{value} "{email}"')
        return base_dorks

    # --- Wayback Machine Archive ---
    def wayback_machine_check(self, domain_or_url):
        try:
            save_api = WaybackMachineSaveAPI(domain_or_url, self.user_agent)
            archive_url = save_api.save()
            return archive_url
        except Exception as e:
            return f"Wayback Machine Error: {str(e)}"

    # --- Breach Data (Note: HIBP API may require an API key) ---
    def check_breach_data(self, email):
        try:
            # Using the public endpoint without authentication (this might not work reliably)
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                breaches = json.loads(response.text)
                return [breach['Name'] for breach in breaches]
            return "No known breaches found"
        except Exception as e:
            return f"Breach check error: {str(e)}"

    # --- WHOIS and DNS ---
    def advanced_whois(self, domain):
        try:
            details = whois.whois(domain)
            return {
                'registrar': details.registrar,
                'creation_date': details.creation_date,
                'expiration_date': details.expiration_date,
                'name_servers': details.name_servers
            }
        except Exception as e:
            return f"Advanced WHOIS Error: {str(e)}"

    def dns_enumeration(self, domain):
        records = {}
        record_types = ['A', 'AAAA', 'MX', 'NS', 'SOA', 'TXT']
        for rt in record_types:
            try:
                answers = dns.resolver.resolve(domain, rt)
                records[rt] = [r.to_text() for r in answers]
            except Exception:
                continue
        return records

    # --- GitHub Search ---
    def github_search(self, username):
        try:
            response = requests.get(
                f"https://api.github.com/users/{username}/repos",
                headers=self.headers,
                timeout=10
            )
            repos = json.loads(response.text)
            return [repo['html_url'] for repo in repos][:5]
        except Exception as e:
            return f"GitHub API Error: {str(e)}"

    # --- Port Scanning ---
    def port_scan(self, domain):
        common_ports = [21, 22, 25, 53, 80, 443, 3306, 3389]
        open_ports = []
        try:
            ip_address = socket.gethostbyname(domain)
        except Exception as e:
            return f"IP resolution error: {str(e)}"
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip_address, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
        return open_ports

    # --- DuckDuckGo Search (Advanced Dorking) ---
    def search_duckduckgo(self, query):
        try:
            response = requests.get(
                "https://html.duckduckgo.com/html/",
                params={'q': query},
                headers=self.headers,
                timeout=10
            )
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            for result in soup.find_all('div', {'class': 'result'}):
                title = result.find('h2')
                title_text = title.get_text(strip=True) if title else ''
                link_tag = result.find('a', {'class': 'result__url'})
                link = link_tag.get('href') if link_tag else ''
                snippet_tag = result.find('a', {'class': 'result__snippet'})
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else ''
                results.append({
                    'title': title_text,
                    'link': link,
                    'snippet': snippet
                })
            return results[:5]
        except Exception as e:
            return []

    # --- Gravatar Check ---
    def check_gravatar(self, email):
        email_clean = email.strip().lower()
        hash_email = hashlib.md5(email_clean.encode('utf-8')).hexdigest()
        url = f"https://www.gravatar.com/avatar/{hash_email}?d=404"
        try:
            response = requests.get(url, headers=self.headers, timeout=5)
            return "Profile exists" if response.status_code == 200 else "No Gravatar found"
        except Exception as e:
            return f"Connection Error: {str(e)}"

    # --- Additional OSINT Functions from Previous Code ---
    def search_public_documents(self, email):
        queries = [
            f'filetype:pdf "{email}"',
            f'filetype:doc "{email}"',
            f'filetype:docx "{email}"',
            f'intitle:"confidential" "{email}"'
        ]
        results = []
        for query in queries:
            r = self.search_duckduckgo(query)
            results.append({"query": query, "results": r})
        return results

    def search_phone_numbers(self, email):
        query = f'"{email}" ("phone:" OR "tel:" OR "contact:" OR "cell:")'
        return self.search_duckduckgo(query)

    def search_password_leaks(self, email):
        query = f'"{email}" ("password leak" OR "data breach" OR "compromised")'
        return self.search_duckduckgo(query)

    def search_social_profiles(self, email):
        username = self.extract_username(email)
        social_sites = {
            "Twitter": f'site:twitter.com "{username}"',
            "GitHub": f'site:github.com "{username}"',
            "LinkedIn": f'site:linkedin.com/in "{username}"',
            "Facebook": f'site:facebook.com "{username}"',
            "Instagram": f'site:instagram.com "{username}"'
        }
        profiles = {}
        for site, query in social_sites.items():
            results = self.search_duckduckgo(query)
            if results and isinstance(results, list):
                profiles[site] = results[0].get("link", "Not found")
            else:
                profiles[site] = "Not found"
        return profiles

    def search_ips_domains(self, email):
        query = f'"{email}" ("IP address" OR "IPv4" OR "domain" OR "server")'
        return self.search_duckduckgo(query)

    def search_photos_posts(self, email):
        query = f'"{email}" ("photo" OR "image" OR "post" OR "tweet" OR "instagram")'
        return self.search_duckduckgo(query)

    def search_username_mentions(self, email):
        username = self.extract_username(email)
        query = f'"{username}" (site:twitter.com OR site:reddit.com OR site:facebook.com)'
        return self.search_duckduckgo(query)

    def search_deleted_content(self, email):
        username = self.extract_username(email)
        query = f'"{username}" ("deleted tweet" OR "removed comment" OR "erased post")'
        results = self.search_duckduckgo(query)
        # Attempt to enrich results with an archived snapshot URL
        for item in results:
            link = item.get("link", "")
            archived = self.wayback_machine_check(link) if link else None
            if archived and not archived.startswith("Wayback"):
                item["archived"] = archived
        return results

    # --- Full Scan Orchestration ---
    def full_scan(self, email):
        if not self.validate_email(email):
            self._print_result("Invalid Email", "Please enter a valid email address", 'critical')
            return

        # Banner
        banner = rf"""
{Fore.RED}
  ______           _       _         _____                _             
 |  ____|         | |     | |       / ____|              | |            
 | |__   _ __   __| | __ _| | ___  | (___   ___ _ __   __| | ___  _ __  
 |  __| | '_ \ / _` |/ _` | |/ _ \  \___ \ / _ \ '_ \ / _` |/ _ \| '_ \ 
 | |____| | | | (_| | (_| | |  __/  ____) |  __/ | | | (_| | (_) | | | |
 |______|_| |_|\__,_|\__,_|_|\___| |_____/ \___|_| |_|\__,_|\___/|_| |_|
{Fore.BLUE}
                              Footprint Searcher
                               by Ivan
{Style.RESET_ALL}
        """
        print(banner)
        self._print_result("Target Email", email, 'info')
        domain = self.extract_domain(email)
        username = self.extract_username(email)

        # Domain Intelligence
        self._print_section_header("Domain Intelligence")
        self._print_result("Target Domain", domain)
        whois_data = self.advanced_whois(domain)
        if isinstance(whois_data, dict):
            self._print_result("Registrar", whois_data.get('registrar', 'N/A'))
            self._print_result("Creation Date", whois_data.get('creation_date', 'N/A'))
        else:
            self._print_result("WHOIS", whois_data, 'warning')
        dns_data = self.dns_enumeration(domain)
        self._print_result("DNS Records", json.dumps(dns_data, indent=2))
        open_ports = self.port_scan(domain)
        if isinstance(open_ports, list):
            self._print_result("Open Ports", f"{', '.join(map(str, open_ports))}" if open_ports else "None")
        else:
            self._print_result("Port Scan", open_ports, 'warning')
        
        # Email Intelligence
        self._print_section_header("Email Intelligence")
        self._print_result("Gravatar Check", self.check_gravatar(email))
        breaches = self.check_breach_data(email)
        if isinstance(breaches, list):
            self._print_result("Data Breaches", f"Found in {len(breaches)} breaches: {', '.join(breaches)}", 'critical')
        else:
            self._print_result("Data Breaches", breaches)

        # Web Presence and Archival
        self._print_section_header("Web Presence Analysis")
        self._print_result("Wayback Archive (Domain)", self.wayback_machine_check(domain))
        github_repos = self.github_search(username)
        if isinstance(github_repos, list) and github_repos:
            self._print_result("GitHub Repositories", "\n".join(github_repos[:3]))
        else:
            self._print_result("GitHub Repositories", github_repos, 'warning')

        # Advanced Dorking
        self._print_section_header("Advanced Dorking Results")
        dorks = self.advanced_dork_generator(email)
        for dork in dorks[:5]:  # demo limit: 5 dorks
            results = self.search_duckduckgo(dork)
            self._print_result(f"Dork: {dork}", f"{len(results)} results found")
            for result in results[:2]:  # show top 2 results per dork
                self._print_result("Title", result.get('title', ''), 'success')
                self._print_result("URL", result.get('link', ''))
        
        # Additional OSINT Queries
        self._print_section_header("Additional OSINT Queries")
        pub_docs = self.search_public_documents(email)
        for item in pub_docs:
            self._print_result("Public Document Query", item["query"])
            self._print_result("Results Count", f"{len(item['results'])}")
        phone_results = self.search_phone_numbers(email)
        self._print_result("Phone Numbers Query", f"{len(phone_results)} results found")
        leak_results = self.search_password_leaks(email)
        self._print_result("Password Leak Query", f"{len(leak_results)} results found")
        social_profiles = self.search_social_profiles(email)
        for site, link in social_profiles.items():
            self._print_result(f"{site} Profile", link)
        ip_domain_results = self.search_ips_domains(email)
        self._print_result("IP/Domain Query", f"{len(ip_domain_results)} results found")
        photos_posts = self.search_photos_posts(email)
        self._print_result("Photos/Posts Query", f"{len(photos_posts)} results found")
        username_mentions = self.search_username_mentions(email)
        self._print_result("Username Mentions Query", f"{len(username_mentions)} results found")
        deleted_content = self.search_deleted_content(email)
        self._print_result("Deleted Content Query", f"{len(deleted_content)} results found")

        self._print_result("Scan Completed", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'success')

def main():
    parser = argparse.ArgumentParser(description="Advanced Digital Footprint Scanner")
    parser.add_argument("email", help="Target email address for scanning")
    args = parser.parse_args()

    scanner = AdvancedFootprintScanner()
    scanner.full_scan(args.email)

if __name__ == "__main__":
    main()
