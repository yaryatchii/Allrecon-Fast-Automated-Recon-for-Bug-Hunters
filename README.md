<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Allrecon - README</title>
</head>
<body>

<h1>Allrecon</h1>

<p>Allrecon est un outil automatisé de reconnaissance pour les pentests dans le cadre de bug bounty. Ce script permet d'énumérer les sous-domaines d'un domaine, de crawler les URLs présentes sur ces sous-domaines et de filtrer celles qui sont potentiellement vulnérables à des injections comme le XSS, SQLi, LFI, etc.</p>

<h2>Fonctionnalités</h2>
<ul>
    <li>Énumération des sous-domaines avec <code>subfinder</code></li>
    <li>Crawling des URLs pour chaque sous-domaine</li>
    <li>Filtrage des URLs potentiellement vulnérables à l'injection</li>
    <li>Sauvegarde des URLs trouvées dans deux fichiers :
        <ul>
            <li><code>output.txt</code> : Toutes les URLs trouvées</li>
            <li><code>vuln.txt</code> : URLs potentiellement vulnérables aux injections (paramètres URL terminant par <code>=</code>)</li>
        </ul>
    </li>
</ul>

<h2>Prérequis</h2>

<p>Avant de commencer, assurez-vous d'avoir installé les éléments suivants :</p>
<ul>
    <li>Python 3.x</li>
    <li><a href="https://github.com/projectdiscovery/subfinder">subfinder</a></li>
    <li>Les modules Python requis, listés dans le fichier <code>requirements.txt</code></li>
</ul>

<h3>Installation de Subfinder</h3>

<pre><code>go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest</code></pre>

<h3>Installation des dépendances Python</h3>

<pre><code>pip install -r requirements.txt</code></pre>

<h2>Utilisation</h2>

<ol>
    <li>Clonez ce dépôt :
        <pre><code>git clone https://github.com/votre-utilisateur/allrecon.git
cd allrecon</code></pre>
    </li>

    Installez les dépendances comme mentionné ci-dessus.

    Lancez le script avec la commande suivante :
        python allrecon.py
    

    Vous verrez la bannière d'introduction Allrecon s'afficher.

    Saisissez le domaine pour lequel vous souhaitez effectuer l'énumération des sous-domaines :
        Enter the domain to enumerate subdomains: example.com
    

    Le script exécutera les étapes suivantes :
        
            Énumération des sous-domaines.
            Crawling des sous-domaines pour récupérer les URLs.
            Filtrage des URLs vulnérables (URLs contenant des paramètres).
            Sauvegarde des résultats dans deux fichiers :
                
                   output.txt : Contient toutes les URLs.
                   vuln.txt : Contient uniquement les URLs potentiellement vulnérables.
               
            
        
    
</ol>

<h2>Exemple</h2>

<p>Si vous saisissez <code>example.com</code> comme domaine, voici un exemple de sortie :</p>

<pre><code>Enumerating subdomains for example.com...
Found 5 subdomains.
Crawling URLs for www.example.com...
Found 10 URLs on www.example.com.
Filtering potentially vulnerable URLs...
Saved 10 URLs to output.txt
Saved 3 potentially vulnerable URLs to vuln.txt</code></pre>

<h2>Contribution</h2>

<p>Les contributions sont les bienvenues ! Si vous avez des suggestions ou des améliorations à apporter, n'hésitez pas à ouvrir une issue ou à créer une pull request.</p>

<h2>Licence</h2>

<p>Ce projet est sous licence MIT. Consultez le fichier <code>LICENSE</code> pour plus d'informations.</p>

</body>
</html>
