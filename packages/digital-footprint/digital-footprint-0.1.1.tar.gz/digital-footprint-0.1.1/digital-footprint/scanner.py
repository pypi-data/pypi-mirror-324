import re
import requests
from bs4 import BeautifulSoup
import whois
import dns.resolver
import hashlib
import urllib.parse

class DigitalFootprintScanner:
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (compatible; DigitalFootprintScanner/1.0; +https://example.com)"
    
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def extract_domain(self, email):
        return email.split('@')[-1]

    def whois_lookup(self, domain):
        try:
            info = whois.whois(domain)
            return info
        except Exception as e:
            return f"Error en WHOIS: {str(e)}"

    def get_mx_records(self, domain):
        try:
            answers = dns.resolver.resolve(domain, 'MX')
            records = [r.exchange.to_text() for r in answers]
            return records
        except Exception as e:
            return f"Error en registros MX: {str(e)}"

    def search_duckduckgo(self, query):
        query_encoded = urllib.parse.quote(query)
        url = "https://html.duckduckgo.com/html/?q=" + query_encoded
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            return f"Error en búsqueda web: {str(e)}"
        
        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        for result in soup.find_all("div", class_="result"):
            title_tag = result.find("a", class_="result__a")
            snippet_tag = result.find("div", class_="result__snippet")
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = title_tag.get('href') if title_tag else ""
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            results.append({"title": title, "link": link, "snippet": snippet})
        return results

    def check_gravatar(self, email):
        # Calcular el hash MD5 del correo (minúsculas y sin espacios)
        email_clean = email.strip().lower()
        hash_email = hashlib.md5(email_clean.encode('utf-8')).hexdigest()
        url = f"https://www.gravatar.com/avatar/{hash_email}?d=404"
        headers = {"User-Agent": self.user_agent}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return url
            else:
                return "No se encontró imagen en Gravatar."
        except Exception as e:
            return f"Error al consultar Gravatar: {str(e)}"

    def search_pastebin(self, email):
        # Se utiliza DuckDuckGo para buscar en pastebin entradas que contengan el correo.
        query = f"site:pastebin.com {email}"
        results = self.search_duckduckgo(query)
        return results

    def search_social_profiles(self, email):
        # Se extrae el username (parte antes de la @) y se intenta comprobar la existencia
        # de perfiles en algunas plataformas populares.
        username = email.split('@')[0]
        profiles = {}
        social_sites = {
            "Twitter": f"https://twitter.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}",
            "Facebook": f"https://www.facebook.com/{username}",
        }
        headers = {"User-Agent": self.user_agent}
        for site, url in social_sites.items():
            try:
                r = requests.get(url, headers=headers, timeout=10)
                # Consideramos que si se obtiene un código 200 se ha encontrado un perfil
                if r.status_code == 200:
                    profiles[site] = url
                else:
                    profiles[site] = "No encontrado"
            except Exception as e:
                profiles[site] = f"Error: {str(e)}"
        return profiles

    def scan_email(self, email):
        if not self.validate_email(email):
            print("El correo electrónico no tiene un formato válido.")
            return
        
        banner = r"""
  ____  _       _       _   _  _     _       _     _   
 |  _ \| |     | |     | \ | |/ \   | |     | |   | |  
 | |_) | | ___ | |__   |  \| / _ \  | |     | |   | |  
 |  __/| |/ _ \| '_ \  | . ` / ___ \ | |     | |   | |  
 | |   | | (_) | |_) | | |\ /_/   \_\| |____ | |___| |____
 |_|   |_|\___/|_.__/  |_| \_\     (_)______|_____|______|
        """
        print(banner)
        print("\nInformación de la huella digital para el correo: {}\n".format(email))
        
        # Información del dominio
        domain = self.extract_domain(email)
        print("== Información del Dominio ==")
        print("Dominio: {}\n".format(domain))
        whois_info = self.whois_lookup(domain)
        print("WHOIS:")
        print(whois_info)
        print("\nRegistros MX:")
        mx_records = self.get_mx_records(domain)
        print(mx_records)
        
        # Búsqueda web general
        print("\n== Búsqueda Web ==")
        web_results = self.search_duckduckgo(email)
        if isinstance(web_results, str):
            print(web_results)
        elif len(web_results) == 0:
            print("No se encontraron resultados en la búsqueda web.")
        else:
            for idx, item in enumerate(web_results, start=1):
                print("Resultado {}:".format(idx))
                print("Título     : {}".format(item["title"]))
                print("Enlace     : {}".format(item["link"]))
                print("Descripción: {}".format(item["snippet"]))
                print("-" * 50)
        
        # Consulta a Gravatar
        print("\n== Gravatar ==")
        gravatar_result = self.check_gravatar(email)
        print(gravatar_result)
        
        # Búsqueda en Pastebin
        print("\n== Búsqueda en Pastebin ==")
        pastebin_results = self.search_pastebin(email)
        if isinstance(pastebin_results, str):
            print(pastebin_results)
        elif len(pastebin_results) == 0:
            print("No se encontraron resultados en Pastebin.")
        else:
            for idx, item in enumerate(pastebin_results, start=1):
                print("Resultado {}:".format(idx))
                print("Título     : {}".format(item["title"]))
                print("Enlace     : {}".format(item["link"]))
                print("Descripción: {}".format(item["snippet"]))
                print("-" * 50)
        
        # Búsqueda de perfiles sociales
        print("\n== Perfiles Sociales (búsqueda tentativa) ==")
        social_profiles = self.search_social_profiles(email)
        for site, result in social_profiles.items():
            print(f"{site}: {result}")
        
        print("\nEscaneo completado.")

def main():
    """
    Función principal para ejecutar el scanner desde la línea de comandos.
    Uso: digital_footprint <correo>
    """
    import argparse
    parser = argparse.ArgumentParser(description="Digital Footprint Scanner")
    parser.add_argument("email", help="Correo electrónico a escanear")
    args = parser.parse_args()
    
    scanner = DigitalFootprintScanner()
    scanner.scan_email(args.email)

if __name__ == "__main__":
    main()
