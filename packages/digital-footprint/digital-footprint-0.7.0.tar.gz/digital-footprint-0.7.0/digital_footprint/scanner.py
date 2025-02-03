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
        self.user_agent = "FootprintSearcher/2.0 (Professional OSINT Tool; +https://github.com/ivanMartin)"
        self.headers = {"User-Agent": self.user_agent}
        # Redes sociales base para búsquedas (se usan para comprobar si la cuenta existe y para obtener la URL archivada)
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

    # --- Validaciones y extracción de datos ---
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

    # --- Generación de Dorks (para emails) ---
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

    # --- Consultar archivo archivado usando CDX (Wayback Machine) ---
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

    # --- GitHub Search (usando la API pública) ---
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

    # --- DuckDuckGo Search (con selectores actualizados) ---
    def search_duckduckgo(self, query):
        try:
            url = "https://html.duckduckgo.com/html/"
            params = {'q': query}
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            # Se buscan enlaces con la clase "result__a"
            for a in soup.find_all("a", class_="result__a"):
                title = a.get_text(strip=True)
                link = a.get('href')
                # Se intenta encontrar un snippet en un contenedor cercano
                snippet = ""
                parent = a.find_parent("div", class_="result")
                if parent:
                    snippet_tag = parent.find("a", class_="result__snippet")
                    if snippet_tag:
                        snippet = snippet_tag.get_text(strip=True)
                results.append({
                    'title': title,
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

    # --- Funciones adicionales OSINT usando DuckDuckGo ---
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

    def search_ips_domains(self, target):
        query = f'"{target}" ("IP address" OR "IPv4" OR "domain" OR "server")'
        return self.search_duckduckgo(query)

    def search_photos_posts(self, target):
        query = f'"{target}" ("photo" OR "image" OR "post" OR "tweet" OR "instagram")'
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

    # --- Funciones para chequear cuentas en redes sociales usando GET ---
    def twitter_check(self, target):
        url = f"https://twitter.com/{target}"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return url if r.status_code == 200 else "Not found"
        except Exception as e:
            return f"Twitter Error: {str(e)}"

    def linkedin_check(self, target):
        url = f"https://www.linkedin.com/in/{target}"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return url if r.status_code == 200 else "Not found"
        except Exception as e:
            return f"LinkedIn Error: {str(e)}"

    def facebook_check(self, target):
        url = f"https://www.facebook.com/{target}"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return url if r.status_code == 200 else "Not found"
        except Exception as e:
            return f"Facebook Error: {str(e)}"

    def instagram_check(self, target):
        url = f"https://www.instagram.com/{target}"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return url if r.status_code == 200 else "Not found"
        except Exception as e:
            return f"Instagram Error: {str(e)}"

    def spotify_check(self, target):
        url = f"https://open.spotify.com/user/{target}"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return url if r.status_code == 200 else "Not found"
        except Exception as e:
            return f"Spotify Error: {str(e)}"

    def discord_check(self, target):
        url = f"https://discord.com/users/{target}"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return url if r.status_code == 200 else "Not found"
        except Exception as e:
            return f"Discord Error: {str(e)}"

    def github_account_check(self, target):
        url = f"https://github.com/{target}"
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
            return url if r.status_code == 200 else "Not found"
        except Exception as e:
            return f"Github Error: {str(e)}"

    def check_all_socials(self, username):
        socials = {
            "Twitter": self.twitter_check(username),
            "LinkedIn": self.linkedin_check(username),
            "Facebook": self.facebook_check(username),
            "Instagram": self.instagram_check(username),
            "GitHub": self.github_account_check(username),
            "Spotify": self.spotify_check(username),
            "Discord": self.discord_check(username)
        }
        return socials

    # --- Full Scan Orchestration ---
    def full_scan(self, target):
        # Determinar si es email o username
        is_email = "@" in target
        if is_email and not self.validate_email(target):
            self._print_result("Invalid Email", "Please enter a valid email address", 'critical')
            return

        banner = rf"""
{Fore.RED}
  ▄████ ██░ ██ ▒█████   ██████▄▄▄█████▓██▓███  ██▀███  ██▓███▄    █▄▄▄█████▓
 ██▒ ▀█▓██░ ██▒██▒  ██▒██    ▒▓  ██▒ ▓▓██░  ██▓██ ▒ ██▓██▒██ ▀█   █▓  ██▒ ▓▒
▒██░▄▄▄▒██▀▀██▒██░  ██░ ▓██▄  ▒ ▓██░ ▒▓██░ ██▓▓██ ░▄█ ▒██▓██  ▀█ ██▒ ▓██░ ▒░
░▓█  ██░▓█ ░██▒██   ██░ ▒   ██░ ▓██▓ ░▒██▄█▓▒ ▒██▀▀█▄ ░██▓██▒  ▐▌██░ ▓██▓ ░ 
░▒▓███▀░▓█▒░██░ ████▓▒▒██████▒▒ ▒██▒ ░▒██▒ ░  ░██▓ ▒██░██▒██░   ▓██░ ▒██▒ ░ 
 ░▒   ▒ ▒ ░░▒░░ ▒░▒░▒░▒ ▒▓▒ ▒ ░ ▒ ░░  ▒▓▒░ ░  ░ ▒▓ ░▒▓░▓ ░ ▒░   ▒ ▒  ▒ ░░   
  ░   ░ ▒ ░▒░ ░ ░ ▒ ▒░░ ░▒  ░ ░   ░   ░▒ ░      ░▒ ░ ▒░▒ ░ ░░   ░ ▒░   ░    
░ ░   ░ ░  ░░ ░ ░ ░ ▒ ░  ░  ░   ░     ░░        ░░   ░ ▒ ░  ░   ░ ░  ░      
      ░ ░  ░  ░   ░ ░       ░                    ░     ░          ░         
                                                                            
{Fore.BLUE}
                              Footprint Searcher
                               by Ivan
{Style.RESET_ALL}
        """
        print(banner)
        if is_email:
            self._print_result("Target Email", target, 'info')
        else:
            self._print_result("Target Username", target, 'info')
        
        username = self.extract_username(target)
        domain = self.extract_domain(target) if is_email else None

        # Si es email, realizar análisis de dominio
        if domain:
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
        
        # Si es email, análisis adicional
        if is_email:
            self._print_section_header("Email Intelligence")
            self._print_result("Gravatar Check", self.check_gravatar(target))
            breach_alt = self.check_data_breach_alternative(target)
            self._print_result("Data Breaches", breach_alt)
        
        # Web Presence: Para dominios y redes sociales
        self._print_section_header("Web Presence Analysis")
        if domain:
            self._print_result("Wayback Archive (Domain)", self.get_archived_snapshot(domain))
        socials = self.check_all_socials(username)
        for site, link in socials.items():
            archive = self.get_archived_snapshot(link) if link != "Not found" and link.startswith("http") else "No archive"
            self._print_result(f"{site} Profile", f"{link} | Archived: {archive}")
        github_repos = self.github_search(username)
        if isinstance(github_repos, list) and github_repos:
            self._print_result("GitHub Repositories", "\n".join(github_repos[:3]))
        else:
            self._print_result("GitHub Repositories", github_repos, 'warning')
        
        # Advanced Dorking (solo para email)
        if is_email:
            self._print_section_header("Advanced Dorking Results")
            dorks = self.advanced_dork_generator(target)
            for dork in dorks[:5]:
                results = self.search_duckduckgo(dork)
                self._print_result(f"Dork: {dork}", f"{len(results)} results found")
                for result in results[:2]:
                    self._print_result("Title", result.get('title', ''), 'success')
                    self._print_result("URL", result.get('link', ''))
        
        # Additional OSINT Queries (ordenadas)
        self._print_section_header("Additional OSINT Queries")
        if is_email:
            self._print_result("-- Public Documents --", "")
            pub_docs = self.search_public_documents(target)
            for item in pub_docs:
                self._print_result("Query", item["query"])
                self._print_result("Results Count", f"{len(item['results'])}")
            self._print_result("Phone Numbers", f"{len(self.search_phone_numbers(target))} results found")
            self._print_result("Password Leaks", f"{len(self.search_password_leaks(target))} results found")
        self._print_result("-- Web Queries --", "")
        self._print_result("IP/Domain Query", f"{len(self.search_ips_domains(target))} results found")
        self._print_result("Photos/Posts Query", f"{len(self.search_photos_posts(target))} results found")
        self._print_result("Username Mentions", f"{len(self.search_username_mentions(username))} results found")
        self._print_result("Deleted Content", f"{len(self.search_deleted_content(username))} results found")
        
        self._print_result("Scan Completed", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'success')

def main():
    parser = argparse.ArgumentParser(description="Advanced Digital Footprint Scanner (Free Tools Only)")
    parser.add_argument("target", help="Target email address or username for scanning")
    args = parser.parse_args()

    scanner = AdvancedFootprintScanner()
    scanner.full_scan(args.target)

if __name__ == "__main__":
    main()
