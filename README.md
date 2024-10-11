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
