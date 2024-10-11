#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import subprocess


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

# Fonction pour récupérer un jeton CSRF (si nécessaire)
def get_csrf_token(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    token_tag = soup.find('input', {'name': 'csrf_token'})
    return token_tag.get('value') if token_tag else None

# Fonction pour suivre les redirections manuellement
def follow_redirects(url, headers, max_redirects=5):
    for _ in range(max_redirects):
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code in (301, 302):
            url = response.headers['Location']
            print(f"{Colors.YELLOW}Redirected to {url}{Colors.RESET}")
        else:
            return response
    print(f"{Colors.RED}Too many redirects{Colors.RESET}")
    return None

# Fonction pour crawler les URLs sur un sous-domaine avec cookies et redirections
def crawl_subdomain(subdomain, cookies=None, user_agent=None):
    print(f"{Colors.BLUE}Crawling URLs for {subdomain}...{Colors.RESET}")
    
    # Configuration des headers
    headers = {
        'User-Agent': user_agent if user_agent else 'Mozilla/5.0 (compatible;)',
        'Cookie': cookies if cookies else '',
    }

    # Faire une requête HTTP
    response = requests.get(f"http://{subdomain}", headers=headers, allow_redirects=False)
    
    # Suivi des redirections manuelles
    if response.status_code in (301, 302):
        redirect_url = response.headers['Location']
        print(f"{Colors.YELLOW}Redirected to {redirect_url}{Colors.RESET}")
        response = follow_redirects(redirect_url, headers)

    # Récupérer le jeton CSRF si nécessaire
    csrf_token = get_csrf_token(response.text) if response else None
    if csrf_token:
        headers['X-CSRF-Token'] = csrf_token

    # Parser le contenu HTML pour extraire les URLs
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [urljoin(f"http://{subdomain}", link.get('href')) for link in soup.find_all('a', href=True)]
    
    print(f"{Colors.GREEN}Found {len(urls)} URLs on {subdomain}.{Colors.RESET}")
    return urls

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

    # Saisie du domaine cible
    domain = input(f"{Colors.YELLOW}Enter the domain to enumerate subdomains: {Colors.RESET}")
    
    # Option pour ajouter un cookie personnalisé
    use_cookie = input(f"{Colors.YELLOW}Do you want to provide a custom cookie for authentication? (y/n): {Colors.RESET}").lower()
    cookies = None
    if use_cookie == 'y':
        cookies = input(f"{Colors.YELLOW}Enter your cookie: {Colors.RESET}")

    # Option pour ajouter un user-agent personnalisé (pour Intigriti par exemple)
    use_user_agent = input(f"{Colors.YELLOW}Do you want to provide a custom user agent (for compliance)? (y/n): {Colors.RESET}").lower()
    user_agent = None
    if use_user_agent == 'y':
        username = input(f"{Colors.YELLOW}Enter your custom user-agent: {Colors.RESET}")
        user_agent = f"user-agent:{username}"

    # Étape 1: Énumération des sous-domaines
    subdomains = enumerate_subdomains(domain)
    if not subdomains:
        print(f"{Colors.RED}No subdomains found. Exiting...{Colors.RESET}")
        return

    all_urls = []
    vulnerable_urls = []
    
    # Étape 2: Crawler des sous-domaines et collecte des URLs
    for subdomain in subdomains:
        urls = crawl_subdomain(subdomain, cookies=cookies, user_agent=user_agent)
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
