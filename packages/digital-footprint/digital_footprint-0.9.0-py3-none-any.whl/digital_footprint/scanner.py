import re
import os
import requests
from bs4 import BeautifulSoup
import whois
import dns.resolver
import hashlib
import urllib.parse
import argparse
import json
from datetime import datetime
from waybackpy import WaybackMachineCDXServerAPI
import socket
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class AdvancedFootprintScanner:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://duckduckgo.com/",
            "DNT": "1"
        }
        self.social_networks = {
            "Twitter": "https://twitter.com/{}",
            "LinkedIn": "https://www.linkedin.com/in/{}",
            "Facebook": "https://www.facebook.com/{}",
            "Instagram": "https://www.instagram.com/{}",
            "GitHub": "https://github.com/{}",
            "Spotify": "https://open.spotify.com/user/{}",
            "Discord": "https://discord.com/users/{}"
        }
        self.dork_operators = {
            'filetype': ['pdf', 'doc', 'docx', 'xls', 'xlsx'],
            'site': ['pastebin.com', 'github.com', 'stackoverflow.com'],
            'intitle': ['password', 'credentials', 'confidential'],
            'inurl': ['admin', 'login', 'secret']
        }
    
    # --- Métodos de impresión ---
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

    # --- Validación y extracción de datos ---
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def extract_username(self, target):
        if "@" in target:
            return target.split('@')[0]
        return target

    def extract_domain(self, email):
        if "@" in email:
            return email.split('@')[-1]
        return None

    # --- Generación de Dorks ---
    def advanced_dork_generator(self, email):
        base_dorks = [
            f'intext:"{email}"',
            f'filetype:log "user {email}"',
            f'site:pastebin.com "{email}"',
            f'inurl:"{self.extract_username(email)}"'
        ]
        for operator, values in self.dork_operators.items():
            for value in values:
                base_dorks.append(f'{operator}:{value} "{email}"')
        return base_dorks

    def advanced_dork_generator_generic(self, input_str):
        dorks = [
            f'intext:"{input_str}"',
            f'inurl:"{input_str}"'
        ]
        for operator, values in self.dork_operators.items():
            for value in values:
                dorks.append(f'{operator}:{value} "{input_str}"')
        return dorks

    # --- Wayback Machine ---
    def get_archived_snapshot(self, url):
        try:
            cdx_api = WaybackMachineCDXServerAPI(url, self.user_agent)
            snapshots = list(cdx_api.snapshots())
            if snapshots:
                return snapshots[0].archive_url
            else:
                return "No archive found"
        except Exception as e:
            return f"Archive Error: {str(e)}"

    # --- Data breach alternativa ---
    def check_data_breach_alternative(self, target):
        query = f'"{target}" ("breach" OR "leak" OR "compromised")'
        results = self.search_duckduckgo(query)
        if results:
            return f"Possible breach mentions found ({len(results)} results)"
        else:
            return "No data breach mentions found"
    
    # --- WHOIS y DNS ---
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
            repos = response.json()
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

    # --- DuckDuckGo Search Mejorado ---
    def search_duckduckgo(self, query):
        try:
            url = "https://html.duckduckgo.com/html/"
            data = {'q': query, 'kl': 'us-en'}
            response = requests.post(url, headers=self.headers, data=data, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            results = []
            for result in soup.find_all('div', class_='result'):
                title_elem = result.find('a', class_='result__a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                link = title_elem.get('href')
                if link and '//duckduckgo.com/l/' in link:
                    link = self._resolve_redirect(link)
                
                snippet_elem = result.find('a', class_='result__snippet')
                snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                
                results.append({
                    'title': title,
                    'link': link,
                    'snippet': snippet
                })
            
            return results[:5]
        except Exception as e:
            return []

    def _resolve_redirect(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10, allow_redirects=True)
            return response.url
        except Exception:
            return url

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

    # --- Funciones adicionales OSINT ---
    def search_public_documents(self, term):
        queries = [
            f'filetype:pdf "{term}"',
            f'filetype:doc "{term}"',
            f'filetype:docx "{term}"',
            f'intitle:"confidential" "{term}"'
        ]
        results = []
        for query in queries:
            r = self.search_duckduckgo(query)
            results.append({"query": query, "results": r})
        return results

    def search_phone_numbers(self, term):
        query = f'"{term}" ("phone:" OR "tel:" OR "contact:" OR "cell:")'
        return self.search_duckduckgo(query)

    def search_password_leaks(self, term):
        query = f'"{term}" ("password leak" OR "data breach" OR "compromised")'
        return self.search_duckduckgo(query)

    def search_ips_domains(self, term):
        query = f'"{term}" ("IP address" OR "IPv4" OR "domain" OR "server")'
        return self.search_duckduckgo(query)

    def search_photos_posts(self, term):
        query = f'"{term}" ("photo" OR "image" OR "post" OR "tweet" OR "instagram")'
        return self.search_duckduckgo(query)

    def search_username_mentions(self, username):
        query = f'"{username}" (site:twitter.com OR site:reddit.com OR site:facebook.com)'
        return self.search_duckduckgo(query)

    def search_deleted_content(self, username):
        results = []
        for site, base_url in self.social_networks.items():
            url = base_url.format(username)
            query = f'site:{urllib.parse.urlparse(url).netloc} "{username}" "deleted"'
            search_results = self.search_duckduckgo(query)
            for item in search_results:
                link = item.get("link", "")
                if link:
                    archive = self.get_archived_snapshot(link)
                    item["archived"] = archive
                    results.append(item)
        return results

    # --- Check Social Media ---
    def check_social_profile(self, url):
        try:
            r = requests.head(url, headers=self.headers, timeout=10, allow_redirects=True)
            return url if r.status_code in [200, 301, 302] else "Not found"
        except Exception:
            return "Not found"

    def check_all_socials(self, username):
        socials = {}
        for site, url_template in self.social_networks.items():
            url = url_template.format(username)
            result = self.check_social_profile(url)
            socials[site] = result
        return socials

    # --- Full Scan Orchestration ---
    def full_scan(self, target):
        is_email = "@" in target
        if is_email and not self.validate_email(target):
            self._print_result("Invalid Email", "Please enter a valid email address", 'critical')
            return

        banner = rf"""
{Fore.RED}
  ______           _       _         _____                _             
 |  ____|         | |     | |       / ____|              | |            
 | |__   _ __   __| | __ _| | ___  | (___   ___ _ __   __| | ___  _ __  
 |  __| | '_ \ / _ |/ _ | |/ _ \  \___ \ / _ \ '_ \ / _ |/ _ \| '_ \ 
 | |____| | | | (_| | (_| | |  __/  ____) |  __/ | | | (_| | (_) | | | |
 |______|_| |_|\__,_|\__,_|_|\___| |_____/ \___|_| |_|\__,_|\___/|_| |_|
{Fore.BLUE}
                              Footprint Searcher
                               by Ivan
{Style.RESET_ALL}
        """
        print(banner)
        self._print_result("Target", target, 'info')
        
        username = self.extract_username(target)
        domain = self.extract_domain(target) if is_email else None
        search_term = target if is_email else username

        # Domain Intelligence
        if domain:
            self._print_section_header("Domain Intelligence")
            self._print_result("Domain", domain)
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
        if is_email:
            self._print_section_header("Email Intelligence")
            self._print_result("Gravatar Check", self.check_gravatar(target))
            breach_alt = self.check_data_breach_alternative(target)
            self._print_result("Data Breaches", breach_alt)
        
        # Web Presence Analysis
        self._print_section_header("Web Presence Analysis")
        if domain:
            archive_domain = self.get_archived_snapshot(domain)
            self._print_result("Wayback Archive (Domain)", archive_domain)
        
        socials = self.check_all_socials(username)
        for site, link in socials.items():
            if link != "Not found":
                archive = self.get_archived_snapshot(link)
                self._print_result(f"{site} Profile", f"{link} | Archived: {archive}")
            else:
                self._print_result(f"{site} Profile", "Not found")
        
        github_repos = self.github_search(username)
        if isinstance(github_repos, list) and github_repos:
            self._print_result("GitHub Repositories", "\n".join(github_repos[:3]))
        else:
            self._print_result("GitHub Repositories", "No repositories found", 'warning')
        
        # Advanced Dorking
        self._print_section_header("Advanced Dorking Results")
        dorks = self.advanced_dork_generator(target) if is_email else self.advanced_dork_generator_generic(username)
        for dork in dorks[:5]:
            results = self.search_duckduckgo(dork)
            self._print_result(f"Dork: {dork}", f"{len(results)} results found")
            for idx, result in enumerate(results[:3], 1):
                self._print_result(f"Result {idx}", result.get('title', 'No title'), 'success')
                self._print_result("URL", result.get('link', 'No URL'))
        
        # Additional OSINT Queries
        self._print_section_header("Additional OSINT Queries")
        
        # Public Documents
        self._print_result("Public Documents", "", 'info')
        pub_docs = self.search_public_documents(search_term)
        for doc_group in pub_docs:
            self._print_result(f"Query: {doc_group['query']}", "")
            for idx, doc in enumerate(doc_group['results'][:3], 1):
                self._print_result(f"Doc {idx}", doc.get('title', 'No title'), 'success')
                self._print_result("URL", doc.get('link', 'No URL'))
        
        # Other Queries
        queries = [
            ("Phone Numbers", self.search_phone_numbers(search_term)),
            ("Password Leaks", self.search_password_leaks(search_term)),
            ("IP/Domain Info", self.search_ips_domains(search_term)),
            ("Photos/Posts", self.search_photos_posts(search_term)),
            ("Username Mentions", self.search_username_mentions(username)),
            ("Deleted Content", self.search_deleted_content(username))
        ]
        
        for title, results in queries:
            self._print_result(title, "")
            for idx, result in enumerate(results[:3], 1):
                self._print_result(f"Result {idx}", result.get('title', 'No title'), 'success')
                self._print_result("URL", result.get('link', 'No URL'))
        
        self._print_result("Scan Completed", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'success')

def main():
    parser = argparse.ArgumentParser(description="Advanced Digital Footprint Scanner (Free Tools Only)")
    parser.add_argument("target", help="Target email address or username for scanning")
    args = parser.parse_args()

    scanner = AdvancedFootprintScanner()
    scanner.full_scan(args.target)

if __name__ == "__main__":
    main()