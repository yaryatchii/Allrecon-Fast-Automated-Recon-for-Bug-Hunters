import os
import subprocess
import requests
from bs4 import BeautifulSoup
import re

# Fonction pour afficher la bannière
def print_banner():
    banner = '''
    
 █████╗ ██╗     ██╗         ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██║     ██║         ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
███████║██║     ██║         ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██║██║     ██║         ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗███████╗    ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝╚══════╝    ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                                                                  
    '''
    print(banner)

# Fonction pour énumérer les sous-domaines
def enumerate_subdomains(domain):
    print(f"Enumerating subdomains for {domain}...")
    command = f"subfinder -d {domain} -silent"  # Meilleure commande pour trouver des sous-domaines
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    subdomains = result.stdout.splitlines()
    print(f"Found {len(subdomains)} subdomains.")
    return subdomains

# Fonction pour crawler les URLs sur un sous-domaine
def crawl_subdomain(subdomain):
    print(f"Crawling URLs for {subdomain}...")
    try:
        response = requests.get(f"http://{subdomain}")
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = [link.get('href') for link in soup.find_all('a', href=True)]
        print(f"Found {len(urls)} URLs on {subdomain}.")
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Failed to crawl {subdomain}: {e}")
        return []

# Fonction pour filtrer les URLs potentiellement vulnérables
def filter_vulnerable_urls(urls):
    print("Filtering potentially vulnerable URLs...")
    vulnerable_urls = [url for url in urls if re.search(r'\?.+=', url)]
    return vulnerable_urls

# Fonction principale
def main():
    # Affichage de la bannière
    print_banner()

    domain = input("Enter the domain to enumerate subdomains: ")
    
    # Étape 1: Énumération des sous-domaines
    subdomains = enumerate_subdomains(domain)
    
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
    with open('vuln.txt', 'w') as f:
        f.write("\n".join(vulnerable_urls))
    
    print(f"Saved {len(all_urls)} URLs to output.txt")
    print(f"Saved {len(vulnerable_urls)} potentially vulnerable URLs to vuln.txt")

if __name__ == "__main__":
    main()
