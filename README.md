# Allrecon

Allrecon est un outil automatisé de reconnaissance pour les pentests dans le cadre de bug bounty. Ce script permet d'énumérer les sous-domaines d'un domaine, de crawler les URLs présentes sur ces sous-domaines et de filtrer celles qui sont potentiellement vulnérables à des injections comme le XSS, SQLi, LFI, etc.

## Fonctionnalités

- Énumération des sous-domaines avec `subfinder`
- Crawling des URLs pour chaque sous-domaine
- Filtrage des URLs potentiellement vulnérables à l'injection
- Sauvegarde des URLs trouvées dans deux fichiers :
  - `output.txt` : Toutes les URLs trouvées
  - `vuln.txt` : URLs potentiellement vulnérables aux injections (paramètres URL terminant par `=`)

## Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- Python 3.x
- [subfinder](https://github.com/projectdiscovery/subfinder)
- Les modules Python requis, listés dans le fichier `requirements.txt`

### Installation de Subfinder

```bash
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
Installation des dépendances Python
bash
Copier le code
pip install -r requirements.txt
Utilisation
Clonez ce dépôt :
bash
Copier le code
git clone https://github.com/votre-utilisateur/allrecon.git
cd allrecon
Installez les dépendances comme mentionné ci-dessus.

Lancez le script avec la commande suivante :

bash
Copier le code
python allrecon.py
Vous verrez la bannière d'introduction Allrecon s'afficher.

Saisissez le domaine pour lequel vous souhaitez effectuer l'énumération des sous-domaines :

bash
Copier le code
Enter the domain to enumerate subdomains: example.com
Le script exécutera les étapes suivantes :
Énumération des sous-domaines.
Crawling des sous-domaines pour récupérer les URLs.
Filtrage des URLs vulnérables (URLs contenant des paramètres).
Sauvegarde des résultats dans deux fichiers :
output.txt : Contient toutes les URLs.
vuln.txt : Contient uniquement les URLs potentiellement vulnérables.
Exemple
Si vous saisissez example.com comme domaine, voici un exemple de sortie :

bash
Copier le code
Enumerating subdomains for example.com...
Found 5 subdomains.
Crawling URLs for www.example.com...
Found 10 URLs on www.example.com.
Filtering potentially vulnerable URLs...
Saved 10 URLs to output.txt
Saved 3 potentially vulnerable URLs to vuln.txt
Contribution
Les contributions sont les bienvenues ! Si vous avez des suggestions ou des améliorations à apporter, n'hésitez pas à ouvrir une issue ou à créer une pull request.
