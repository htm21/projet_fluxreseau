# *Stratégie de Flux Réseau, un projet de 2ème année de Licence Informatique*
**NOM DES ÉTUDIANTS** : \
Ahmad HATOUM (22202060) - Francesco DI GENNARO (22205989)  



**URL DE DÉPÔT DU PROJET** : [https://github.com/htm21/projet_fluxreseau/]

## Mécanisme d'installation
Avant le lancement du programme, veuillez **installer les modules nécessaires à son fonctionnement**  
L'installation des différents modules sont faits par l'utilisation de  [pip](https://pip.pypa.io/en/stable/)  dans le terminal :
```bash
pip install module
```
Les modules nécessaires sont les suivants : **tkinter**, **ctypes**, **platform**, **pyglet**, **customtkinter**, **matplotlib**, **json**, **pillow**, **os**, **platform**, 


# Les Objectifs du projet

L'objectif de ce projet repose sur l'analyse de *"Stratégie de gestion des flux"*, ces flux arrive dans un système composé de différentes entités tel que des Sources qui contiennent et crée des Paquets. Ces paquets seront extraits par des Buffer (file d'attente) avant d'être envoyé dans le réseau de communications. On utilise alors la programmation oritentée objet.

# Les Différentes Étapes de notre projet

- Création des class permettant la modélisation des éléments clés de notre "système".
- Création de la logique d'intéraction entre ces derniers, avec notamment le passage des Paquets de la Source au Réseau de communication.
- Réalisation de l'interface graphique, en intégrant le code
- Compréhension et intégration de la logique d'arrivée des paquets avec le processus de Poisson
- Ajout des différentes stratégies de gestion du Buffer
- Comparaison des stratégies


# Comment distinguer la structure du projet ?

**Dossier "Modules"**  
Ce dossier contient tout les sous fichiers permettant le fonctionnement du code, les différentes fichiers sont importés dans d'autres pour permettre l'utilisation de leurs code.  

**Fichier main.py**  
Ce fichier permet l'éxécution du code, il rassemble le tout, et son exécution dirige sur l'interface graphique de l'application.  

**Autres**  
Les Dossiers "Icons" et "Fonts" utilisé pour l'embellissement de l'interface graphique
