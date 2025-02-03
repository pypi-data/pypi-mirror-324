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
from waybackpy import WaybackMachineSaveAPI
import socket
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class AdvancedFootprintScanner:
    def __init__(self):
        self.user_agent = "FootprintSearcher/2.0 (Professional OSINT Tool; +https://github.com/ivanMartin)"
        self.headers = {"User-Agent": self.user_agent}
        # Redes sociales sobre las cuales se realizará Wayback Machine
        self.social_networks = {
            "Twitter": "https://twitter.com/{}",
            "LinkedIn": "https://www.linkedin.com/in/{}",
            "Facebook": "https://www.facebook.com/{}",
            "Instagram": "https://www.instagram.com/{}",
            "GitHub": "https://github.com/{}"
        }
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

    # --- Validations y Extracción ---
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

    # --- Advanced Dork Generation (sólo para email) ---
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

    # --- Wayback Machine Archive sobre una URL dada ---
    def wayback_machine_check(self, url):
        try:
            save_api = WaybackMachineSaveAPI(url, self.user_agent)
            archive_url = save_api.save()
            return archive_url
        except Exception as e:
            return f"Wayback Machine Error: {str(e)}"

    # --- Data Breach Alternative (búsqueda en DuckDuckGo) ---
    def check_data_breach_alternative(self, email):
        query = f'"{email}" ("breach" OR "leak" OR "compromised")'
        results = self.search_duckduckgo(query)
        if results:
            return f"Possible breaches found: {len(results)} results (e.g. {results[0].get('title', 'No title')})"
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

    # --- DuckDuckGo Search (intentando mayor robustez) ---
    def search_duckduckgo(self, query):
        try:
            url = "https://html.duckduckgo.com/html/"
            params = {'q': query}
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            # En muchos casos los enlaces están en <a class="result__a">
            for a in soup.find_all("a", class_="result__a"):
                title = a.get_text(strip=True)
                link = a.get('href')
                # Buscar un snippet cercano: a veces se encuentra en el siguiente sibling
                snippet_tag = a.find_next_sibling("a", class_="result__snippet")
                snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
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

    # --- Additional OSINT Functions ---
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

    def search_social_profiles(self, username):
        profiles = {}
        for site, base_url in self.social_networks.items():
            url = base_url.format(username)
            query = f'site:{urllib.parse.urlparse(url).netloc} "{username}"'
            results = self.search_duckduckgo(query)
            if results and len(results) > 0:
                profiles[site] = results[0].get("link", "Not found")
            else:
                profiles[site] = "Not found"
        return profiles

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
            # Buscamos indicios de contenido borrado con el operador "deleted"
            query = f'site:{urllib.parse.urlparse(url).netloc} "{username}" "deleted"'
            search_results = self.search_duckduckgo(query)
            for item in search_results:
                link = item.get("link", "")
                if link:
                    archived = self.wayback_machine_check(link)
                    if archived and not archived.startswith("Wayback Machine Error"):
                        item["archived"] = archived
                    results.append(item)
        return results

    # --- Full Scan Orchestration ---
    def full_scan(self, target):
        # Determinar si la entrada es email o username
        is_email = "@" in target
        if is_email and not self.validate_email(target):
            self._print_result("Invalid Email", "Please enter a valid email address", 'critical')
            return

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
        if is_email:
            self._print_result("Target Email", target, 'info')
        else:
            self._print_result("Target Username", target, 'info')
        
        username = self.extract_username(target)
        domain = self.extract_domain(target) if is_email else None

        # Si tenemos dominio (para email), hacer análisis de dominio
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
        
        # Si es email, se hace análisis adicional de email
        if is_email:
            self._print_section_header("Email Intelligence")
            self._print_result("Gravatar Check", self.check_gravatar(target))
            breach_alt = self.check_data_breach_alternative(target)
            self._print_result("Data Breaches", breach_alt)
        
        # Web Presence y Archival para dominios y redes sociales
        self._print_section_header("Web Presence Analysis")
        if domain:
            self._print_result("Wayback Archive (Domain)", self.wayback_machine_check(domain))
        # Para el username, iteramos las redes sociales:
        for site, base_url in self.social_networks.items():
            profile_url = base_url.format(username)
            archived = self.wayback_machine_check(profile_url)
            self._print_result(f"{site} Profile", f"{profile_url} | Archived: {archived}")
        github_repos = self.github_search(username)
        if isinstance(github_repos, list) and github_repos:
            self._print_result("GitHub Repositories", "\n".join(github_repos[:3]))
        else:
            self._print_result("GitHub Repositories", github_repos, 'warning')
        
        # Advanced Dorking (sólo si es email)
        if is_email:
            self._print_section_header("Advanced Dorking Results")
            dorks = self.advanced_dork_generator(target)
            for dork in dorks[:5]:
                results = self.search_duckduckgo(dork)
                self._print_result(f"Dork: {dork}", f"{len(results)} results found")
                for result in results[:2]:
                    self._print_result("Title", result.get('title', ''), 'success')
                    self._print_result("URL", result.get('link', ''))
        
        # Additional OSINT Queries (ordenados)
        self._print_section_header("Additional OSINT Queries")
        if is_email:
            pub_docs = self.search_public_documents(target)
            print(f"{Fore.MAGENTA}-- Public Documents --{Style.RESET_ALL}")
            for item in pub_docs:
                self._print_result("Query", item["query"])
                self._print_result("Results Count", f"{len(item['results'])}")
            phone_results = self.search_phone_numbers(target)
            self._print_result("Phone Numbers", f"{len(phone_results)} results found")
            leak_results = self.search_password_leaks(target)
            self._print_result("Password Leaks", f"{len(leak_results)} results found")
        print(f"{Fore.MAGENTA}-- Social Profiles --{Style.RESET_ALL}")
        social_profiles = self.search_social_profiles(username)
        for site, link in social_profiles.items():
            self._print_result(f"{site} Profile", link)
        print(f"{Fore.MAGENTA}-- Web Queries --{Style.RESET_ALL}")
        ip_domain_results = self.search_ips_domains(target)
        self._print_result("IP/Domain Query", f"{len(ip_domain_results)} results found")
        photos_posts = self.search_photos_posts(target)
        self._print_result("Photos/Posts Query", f"{len(photos_posts)} results found")
        username_mentions = self.search_username_mentions(username)
        self._print_result("Username Mentions", f"{len(username_mentions)} results found")
        deleted_content = self.search_deleted_content(username)
        self._print_result("Deleted Content", f"{len(deleted_content)} results found")
        
        self._print_result("Scan Completed", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'success')

def main():
    parser = argparse.ArgumentParser(description="Advanced Digital Footprint Scanner (Free Tools Only)")
    parser.add_argument("target", help="Target email address or username for scanning")
    args = parser.parse_args()

    scanner = AdvancedFootprintScanner()
    scanner.full_scan(args.target)

if __name__ == "__main__":
    main()
