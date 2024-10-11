import os
import subprocess
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# Couleurs pour le terminal
class Colors:
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'

# Fonction pour afficher la bannière
def print_banner():
    banner = f'''
{Colors.BLUE}

 █████╗ ██╗     ██╗         ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██║     ██║         ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
███████║██║     ██║         ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██║██║     ██║         ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗███████╗    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝            

    {Colors.RESET}
    '''
    print(banner)

# Fonction pour énumérer les sous-domaines
def enumerate_subdomains(domain):
    print(f"{Colors.BLUE}Enumerating subdomains for {domain}...{Colors.RESET}")
    command = f"subfinder -d {domain} -silent"  # Meilleure commande pour trouver des sous-domaines
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{Colors.RED}Error: Unable to enumerate subdomains for {domain}.{Colors.RESET}")
        return []
    subdomains = result.stdout.splitlines()
    print(f"{Colors.GREEN}Found {len(subdomains)} subdomains.{Colors.RESET}")
    return subdomains

# Fonction pour crawler les URLs sur un sous-domaine
def crawl_subdomain(subdomain):
    print(f"{Colors.BLUE}Crawling URLs for {subdomain}...{Colors.RESET}")
    try:
        response = requests.get(f"http://{subdomain}")
        soup = BeautifulSoup(response.text, 'html.parser')
        # Utilisation de urljoin pour s'assurer que les URLs sont complètes
        urls = [urljoin(f"http://{subdomain}", link.get('href')) for link in soup.find_all('a', href=True)]
        print(f"{Colors.GREEN}Found {len(urls)} URLs on {subdomain}.{Colors.RESET}")
        return urls
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}Failed to crawl {subdomain}: {e}{Colors.RESET}")
        return []

# Fonction pour filtrer les URLs potentiellement vulnérables
def filter_vulnerable_urls(urls):
    print(f"{Colors.BLUE}Filtering potentially vulnerable URLs...{Colors.RESET}")
    vulnerable_urls = [url for url in urls if re.search(r'\?.+=', url)]
    print(f"{Colors.GREEN}Found {len(vulnerable_urls)} potentially vulnerable URLs.{Colors.RESET}")
    return vulnerable_urls

# Fonction principale
def main():
    # Affichage de la bannière
    print_banner()

    domain = input(f"{Colors.YELLOW}Enter the domain to enumerate subdomains: {Colors.RESET}")
    
    # Étape 1: Énumération des sous-domaines
    subdomains = enumerate_subdomains(domain)
    if not subdomains:
        print(f"{Colors.RED}No subdomains found. Exiting...{Colors.RESET}")
        return

    all_urls = []
    vulnerable_urls = []
    
    # Étape 2: Crawler des sous-domaines et collecte des URLs
    for subdomain in subdomains:
        urls = crawl_subdomain(subdomain)
        all_urls.extend(urls)
        
        # Étape 3: Filtrage des URLs vulnérables
        vulnerable_urls.extend(filter_vulnerable_urls(urls))
    
    # Étape 4: Sauvegarde des résultats
    with open('output.txt', 'w') as f:
        f.write("\n".join(all_urls))
    print(f"{Colors.GREEN}Saved {len(all_urls)} URLs to output.txt{Colors.RESET}")

    with open('vuln.txt', 'w') as f:
        f.write("\n".join(vulnerable_urls))
    print(f"{Colors.GREEN}Saved {len(vulnerable_urls)} potentially vulnerable URLs to vuln.txt{Colors.RESET}")

if __name__ == "__main__":
    main()
