#!/usr/bin/env python3

import subprocess
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

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
...  █████╗ ██╗     ██╗         ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
... ██╔══██╗██║     ██║         ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
... ███████║██║     ██║         ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
... ██╔══██║██║     ██║         ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
... ██║  ██║███████╗███████╗    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
... ╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
... @https://github.com/yaryatchii                                          
    {Colors.RESET}
    '''
    print(banner)

# Fonction pour énumérer les sous-domaines
def enumerate_subdomains(domain):
    print(f"{Colors.BLUE}Enumerating subdomains for {domain}...{Colors.RESET}")
    command = f"subfinder -d {domain} -silent"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{Colors.RED}Error: Unable to enumerate subdomains for {domain}.{Colors.RESET}")
        return []
    subdomains = result.stdout.splitlines()
    print(f"{Colors.GREEN}Found {len(subdomains)} subdomains.{Colors.RESET}")
    return subdomains

# Vérification si l'URL est dans le domaine scope (ndd et sous-domaines)
def is_in_scope(url, base_domain):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain.endswith(f".{base_domain}") or domain == base_domain

# Fonction pour récupérer toutes les URLs via la commande 'gau'
def get_all_urls_with_gau(domain):
    print(f"{Colors.BLUE}Retrieving URLs for {domain} using gau...{Colors.RESET}")
    command = f"gau {domain}"  # Commande gau pour obtenir toutes les URLs
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{Colors.RED}Error: Unable to retrieve URLs using gau for {domain}.{Colors.RESET}")
        return []
    urls = result.stdout.splitlines()
    print(f"{Colors.GREEN}Found {len(urls)} URLs using gau for {domain}.{Colors.RESET}")
    return urls

# Fonction pour filtrer les URLs potentiellement vulnérables et exclure celles hors scope
def filter_vulnerable_urls(urls, base_domain):
    print(f"{Colors.BLUE}Filtering potentially vulnerable URLs...{Colors.RESET}")
    vulnerable_urls = [url for url in urls if re.search(r'\?.+=', url) and is_in_scope(url, base_domain)]
    print(f"{Colors.GREEN}Found {len(vulnerable_urls)} potentially vulnerable URLs.{Colors.RESET}")
    return vulnerable_urls

# Fonction pour traiter et sauvegarder les URLs sans la suite des paramètres après '='
def clean_urls(vulnerable_urls):
    print(f"{Colors.BLUE}Cleaning URLs by removing parameters after '='...{Colors.RESET}")
    cleaned_urls = []
    for url in vulnerable_urls:
        if '=' in url:
            cleaned_urls.append(url.split('=')[0] + '=')
        else:
            cleaned_urls.append(url)
    return cleaned_urls

# Fonction principale
def main():
    print_banner()

    domain = input(f"{Colors.YELLOW}Enter the domain to enumerate subdomains: {Colors.RESET}")
    
    use_cookie = input(f"{Colors.YELLOW}Do you want to provide a custom cookie for authentication? (y/n): {Colors.RESET}").lower()
    cookies = None
    if use_cookie == 'y':
        cookies = input(f"{Colors.YELLOW}Enter your cookie: {Colors.RESET}")

    use_user_agent = input(f"{Colors.YELLOW}Do you want to provide a custom user agent? (y/n): {Colors.RESET}").lower()
    user_agent = None
    if use_user_agent == 'y':
        username = input(f"{Colors.YELLOW}Enter your custom user agent: {Colors.RESET}")
        user_agent = f"user-agent:{username}"

    # Énumérer les sous-domaines
    subdomains = enumerate_subdomains(domain)
    if not subdomains:
        print(f"{Colors.RED}No subdomains found. Exiting...{Colors.RESET}")
        return

    # Récupérer les URLs pour le domaine principal
    print(f"{Colors.YELLOW}Processing domain: {domain}{Colors.RESET}")
    domain_urls = get_all_urls_with_gau(domain)
    vulnerable_domain_urls = filter_vulnerable_urls(domain_urls, domain)

    all_urls = domain_urls  # Inclure les URLs du domaine principal
    vulnerable_urls = vulnerable_domain_urls  # Inclure les URLs vulnérables du domaine principal

    # Récupérer les URLs pour chaque sous-domaine
    for subdomain in subdomains:
        urls = get_all_urls_with_gau(subdomain)  # Appel à 'gau' pour obtenir toutes les URLs
        all_urls.extend(urls)
        vulnerable_subdomain_urls = filter_vulnerable_urls(urls, domain)  # Filtrer pour les sous-domaines
        vulnerable_urls.extend(vulnerable_subdomain_urls)  # Ajouter les URLs vulnérables des sous-domaines

    cleaned_urls = clean_urls(vulnerable_urls)

    with open('output.txt', 'w') as f:
        f.write("\n".join(all_urls))
    print(f"{Colors.GREEN}Saved {len(all_urls)} URLs to output.txt{Colors.RESET}")

    with open('vuln.txt', 'w') as f:
        f.write("\n".join(cleaned_urls))
    print(f"{Colors.GREEN}Saved {len(cleaned_urls)} cleaned vulnerable URLs to vuln.txt{Colors.RESET}")

if __name__ == "__main__":
    main()
