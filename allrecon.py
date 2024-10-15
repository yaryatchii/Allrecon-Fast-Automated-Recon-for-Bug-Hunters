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

# Fonction pour récupérer toutes les URLs via 'waybackurls'
def get_all_urls_with_waybackurls(domain):
    print(f"{Colors.BLUE}Retrieving historical URLs for {domain} using waybackurls...{Colors.RESET}")
    command = f"waybackurls {domain}"  # Commande waybackurls pour obtenir toutes les URLs
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"{Colors.RED}Error: Unable to retrieve URLs using waybackurls for {domain}.{Colors.RESET}")
        return []
    urls = result.stdout.splitlines()
    print(f"{Colors.GREEN}Found {len(urls)} historical URLs using waybackurls for {domain}.{Colors.RESET}")
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
    
    # Choix du mode d'exécution avec 1 ou 2
    mode = input(f"{Colors.YELLOW}Choose an option:\n1. Scan only the main domain\n2. Scan the main domain and subdomains\nEnter 1 or 2: {Colors.RESET}").strip()

    use_cookie = input(f"{Colors.YELLOW}Do you want to provide a custom cookie for authentication? (y/n): {Colors.RESET}").lower()
    cookies = None
    if use_cookie == 'y':
        cookies = input(f"{Colors.YELLOW}Enter your cookie: {Colors.RESET}")

    use_user_agent = input(f"{Colors.YELLOW}Do you want to provide a custom user agent? (y/n): {Colors.RESET}").lower()
    user_agent = None
    if use_user_agent == 'y':
        username = input(f"{Colors.YELLOW}Enter your custom user agent: {Colors.RESET}")
        user_agent = f"user-agent:{username}"

    all_urls = []
    vulnerable_urls = []

    # Mode de scan unique du domaine principal (option 1)
    if mode == '1':
        print(f"{Colors.YELLOW}Processing only the main domain: {domain}{Colors.RESET}")
        domain_urls_gau = get_all_urls_with_gau(domain)
        domain_urls_wayback = get_all_urls_with_waybackurls(domain)
        domain_urls = domain_urls_gau + domain_urls_wayback  # Combine URLs from gau and waybackurls
        
        vulnerable_domain_urls = filter_vulnerable_urls(domain_urls, domain)
        all_urls = domain_urls
        vulnerable_urls = vulnerable_domain_urls

    # Mode complet avec sous-domaines (option 2)
    elif mode == '2':
        # Récupérer les URLs pour le domaine principal
        print(f"{Colors.YELLOW}Processing domain: {domain}{Colors.RESET}")
        
        # Utiliser gau et waybackurls pour le domaine principal
        domain_urls_gau = get_all_urls_with_gau(domain)
        domain_urls_wayback = get_all_urls_with_waybackurls(domain)
        domain_urls = domain_urls_gau + domain_urls_wayback  # Combine URLs from gau and waybackurls
        
        vulnerable_domain_urls = filter_vulnerable_urls(domain_urls, domain)

        all_urls = domain_urls  # Inclure les URLs du domaine principal
        vulnerable_urls = vulnerable_domain_urls  # Inclure les URLs vulnérables du domaine principal

        # Énumérer les sous-domaines
        subdomains = enumerate_subdomains(domain)
        if not subdomains:
            print(f"{Colors.RED}No subdomains found. Exiting...{Colors.RESET}")
            return

        # Récupérer les URLs pour chaque sous-domaine
        for subdomain in subdomains:
            print(f"{Colors.YELLOW}Processing subdomain: {subdomain}{Colors.RESET}")
            
            # Utiliser gau et waybackurls pour chaque sous-domaine
            subdomain_urls_gau = get_all_urls_with_gau(subdomain)
            subdomain_urls_wayback = get_all_urls_with_waybackurls(subdomain)
            subdomain_urls = subdomain_urls_gau + subdomain_urls_wayback  # Combine URLs from gau and waybackurls
            
            all_urls.extend(subdomain_urls)
            vulnerable_subdomain_urls = filter_vulnerable_urls(subdomain_urls, domain)  # Filtrer pour les sous-domaines
            vulnerable_urls.extend(vulnerable_subdomain_urls)  # Ajouter les URLs vulnérables des sous-domaines

    else:
        print(f"{Colors.RED}Invalid option. Please choose '1' or '2'.{Colors.RESET}")
        return

    # Nettoyage des URLs
    cleaned_urls = clean_urls(vulnerable_urls)

    # Sauvegarde des résultats complets
    with open('output.txt', 'w') as f:
        f.write("\n".join(all_urls))
    print(f"{Colors.GREEN}Saved {len(all_urls)} URLs to output.txt{Colors.RESET}")

    # Sauvegarde des URLs vulnérables nettoyées
    with open('vuln.txt', 'w') as f:
        f.write("\n".join(cleaned_urls))
    print(f"{Colors.GREEN}Saved {len(cleaned_urls)} cleaned vulnerable URLs to vuln.txt{Colors.RESET}")

if __name__ == "__main__":
    main()
