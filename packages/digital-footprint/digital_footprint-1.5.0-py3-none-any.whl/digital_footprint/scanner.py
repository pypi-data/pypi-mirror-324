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
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

colorama.init(autoreset=True)

class AdvancedFootprintScanner:
    def __init__(self):
        self.user_agent = "FootprintSearcher/2.0 (Professional OSINT Tool; +https://github.com/ivanMartin)"
        self.headers = {"User-Agent": self.user_agent}
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
        # Para email, se usan consultas específicas
        base_dorks = [
            f'"{email}"',  # Búsqueda básica
            f'"user {email}" ext:log',  # Archivos .log con el email
            f'site:pastebin.com "{email}"',  # Buscar en Pastebin
            f'site:* "{self.extract_username(email)}"'  # Simular inurl:
        ]
        for operator, values in self.dork_operators.items():
            if operator == 'filetype':
                for value in values:
                    base_dorks.append(f'"{email}" ext:{value}')  # Usamos ext: para archivos
            elif operator == 'site':
                for value in values:
                    base_dorks.append(f'site:{value} "{email}"')  # site: funciona igual
            elif operator == 'intitle':
                for value in values:
                    base_dorks.append(f'intitle:"{value}" "{email}"')  # Frase exacta en el título
            elif operator == 'inurl':
                for value in values:
                    base_dorks.append(f'site:* "{value}" "{email}"')  # Simulamos inurl: con site:
        return base_dorks

    def advanced_dork_generator_generic(self, input_str):
        # Para username (o para cuando se desea usar el valor directamente)
        dorks = [
            f'"{input_str}"',  # Búsqueda básica
            f'site:* "{input_str}"'  # Simular inurl:
        ]
        for operator, values in self.dork_operators.items():
            if operator == 'filetype':
                for value in values:
                    dorks.append(f'"{input_str}" ext:{value}')  # Usamos ext: para archivos
            elif operator == 'site':
                for value in values:
                    dorks.append(f'site:{value} "{input_str}"')  # site: funciona igual
            elif operator == 'intitle':
                for value in values:
                    dorks.append(f'intitle:"{value}" "{input_str}"')  # Frase exacta en el título
            elif operator == 'inurl':
                for value in values:
                    dorks.append(f'site:* "{value}" "{input_str}"')  # Simulamos inurl: con site:
        return dorks

    # --- Wayback Machine mediante API CDX (consultar snapshot archivado) ---
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

    # --- Data breach alternativa (usando búsqueda en DuckDuckGo) ---
    def check_data_breach_alternative(self, target):
        query = f'"{target}" ("breach" OR "leak" OR "compromised")'
        results = self.search_google_selenium(query)
        if results and len(results) > 0:
            return f"Possible breach mentions: {len(results)} results (e.g. {results[0].get('title', 'No title')})"
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

    # --- GitHub Search (API pública) ---
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

    def search_google_selenium(self, query):
        options = Options()
        options.add_argument("--headless")  # Ejecutar en modo headless
        options.add_argument(f"user-agent={random.choice(self.user_agents)}")
        driver = webdriver.Chrome(options=options)
        driver.get(f"https://www.google.com/search?q={query}")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = []
        for g in soup.find_all("div", class_="tF2Cxc"):
            title = g.find("h3").text
            link = g.find("a")["href"]
            snippet = g.find("span", class_="aCOpRe").text
            results.append({"title": title, "link": link, "snippet": snippet})
        driver.quit()
        return results[:5]

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
    def search_public_documents(self, term):
        queries = [
            f'"{term}" ext:pdf',  # Buscar archivos PDF
            f'"{term}" ext:doc',  # Buscar archivos DOC
            f'"{term}" ext:docx',  # Buscar archivos DOCX
            f'intitle:"confidential" "{term}"'  # Buscar "confidential" en el título
        ]
        results = []
        
        for query in queries:
            found_results = self.search_google_selenium(query)
            results.append({"query": query, "results": found_results})
        
        return results

    def search_phone_numbers(self, term):
        query = f'"{term}" ("phone" OR "tel" OR "contact" OR "cell")'
        return self.search_google_selenium(query)

    def search_password_leaks(self, term):
        query = f'"{term}" ("password leak" OR "data breach" OR "compromised")'
        return self.search_google_selenium(query)

    def search_ips_domains(self, term):
        query = f'"{term}" ("IP address" OR "IPv4" OR "domain" OR "server")'
        return self.search_google_selenium(query)

    def search_photos_posts(self, term):
        query = f'"{term}" ("photo" OR "image" OR "post" OR "tweet" OR "instagram")'
        return self.search_google_selenium(query)

    def search_username_mentions(self, username):
        query = f'"{username}" (site:twitter.com OR site:reddit.com OR site:facebook.com)'
        return self.search_google_selenium(query)

    def search_deleted_content(self, username):
        results = []
        for site, base_url in self.social_networks.items():
            url = base_url.format(username)
            query = f'site:{urllib.parse.urlparse(url).netloc} "{username}" "deleted"'
            search_results = self.search_google_selenium(query)
            for item in search_results:
                link = item.get("link", "")
                if link:
                    archive = self.get_archived_snapshot(link)
                    item["archived"] = archive
                    results.append(item)
        return results

    # --- Funciones para chequear cuentas en redes sociales directamente ---
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
        search_term = target if is_email else username

        # Análisis de dominio (solo si es email)
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
        
        # Análisis de email (solo si es email)
        if is_email:
            self._print_section_header("Email Intelligence")
            self._print_result("Gravatar Check", self.check_gravatar(target))
            breach_alt = self.check_data_breach_alternative(target)
            self._print_result("Data Breaches", breach_alt)
        
        # Web Presence y Archival: para dominio y redes sociales
        self._print_section_header("Web Presence Analysis")
        if domain:
            archive_domain = self.get_archived_snapshot(domain)
            self._print_result("Wayback Archive (Domain)", archive_domain)
        socials = self.check_all_socials(username)
        for site, link in socials.items():
            if link != "Not found" and link.startswith("http"):
                archive = self.get_archived_snapshot(link)
            else:
                archive = "No archive"
            self._print_result(f"{site} Profile", f"{link} | Archived: {archive}")
        github_repos = self.github_search(username)
        if isinstance(github_repos, list) and github_repos:
            self._print_result("GitHub Repositories", "\n".join(github_repos[:3]))
        else:
            self._print_result("GitHub Repositories", github_repos, 'warning')
        
        # Advanced Dorking Results (usando email o username según corresponda)
        self._print_section_header("Advanced Dorking Results")
        if is_email:
            dorks = self.advanced_dork_generator(target)
        else:
            dorks = self.advanced_dork_generator_generic(username)
        for dork in dorks[:5]:
            results = self.search_google_selenium(dork)
            self._print_result(f"Dork: {dork}", f"{len(results)} results found")
            for result in results[:2]:
                self._print_result("Title", result.get('title', ''), 'success')
                self._print_result("URL", result.get('link', ''))
        
        # Additional OSINT Queries (ordenadas en subgrupos)
        self._print_section_header("Additional OSINT Queries")
        # Public Documents
        print(f"{Fore.MAGENTA}-- Public Documents --{Style.RESET_ALL}")
        pub_docs = self.search_public_documents(search_term)
        for item in pub_docs:
            print(f"[•] Query: {item['query']}")
            if item['results']:
                for res in item['results']:
                    print(f"    - {res['title']}: {res['link']}")
            else:
                print("    No results found.")
        # Phone Numbers & Password Leaks 
        self._print_result("Phone Numbers", f"{len(self.search_phone_numbers(target))} results found")
        self._print_result("Password Leaks", f"{len(self.search_password_leaks(target))} results found")
        # Web Queries
        print(f"{Fore.MAGENTA}-- Web Queries --{Style.RESET_ALL}")
        self._print_result("IP/Domain Query", f"{len(self.search_ips_domains(search_term))} results found")
        self._print_result("Photos/Posts Query", f"{len(self.search_photos_posts(search_term))} results found")
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
