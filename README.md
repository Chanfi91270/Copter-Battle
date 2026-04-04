# 🚁 Copter Battle

Copter Battle est un jeu vidéo 2D développé en Python avec Pygame.  
Deux joueurs contrôlent chacun un hélicoptère et doivent survivre le plus longtemps possible en évitant les obstacles et en attaquant leur adversaire.
Ce projet s’inscrit dans un objectif d’apprentissage de la programmation de jeux en temps réel.

---

## 🎯 Objectifs

Ce projet a pour objectif de développer un jeu 2D en utilisant la bibliothèque Pygame, en mettant en pratique :

- la gestion d’événements clavier
- la programmation orientée objet
- la gestion des collisions
- la conception d’une boucle de jeu

---

## 🎮 Fonctionnalités

- 👥 Mode 2 joueurs (local)
- 🚁 Contrôle de deux hélicoptères
- 💣 Système de bonus :
  - Bombes
  - Rafales de tir
  - Bouclier temporaire
- 🪨 Obstacles aléatoires (rochers, avions…)
- ❤️ Système de vies
- ⏱ Chronomètre de survie
- 💥 Animation d’explosion et écran de fin

---

## 🕹️ Contrôles

### Joueur 1 :
- Z : Monter
- S : Descendre
- Q : Gauche
- D : Droite
- A : Utiliser bonus

### Joueur 2 :
- ↑ : Monter
- ↓ : Descendre
- ← : Gauche
- → : Droite
- SHIFT droit : Utiliser bonus

---

## ⚙️ Installation

Pour exécuter le projet Copter Battle, certaines installations préalables sont nécessaires.
Tout d’abord, le projet est développé en Python. Il est recommandé d’utiliser une version de Python inférieure ou égale à 3.12, car certaines versions plus récentes ne sont pas entièrement compatibles avec la bibliothèque Pygame utilisée dans ce projet. Vous pouvez télécharger Python depuis le site officiel : https://www.python.org. Lors de l’installation, il est conseillé de cocher l’option “Add Python to PATH” afin de pouvoir exécuter Python depuis un terminal.
Ensuite, le projet repose sur la bibliothèque Pygame, qui permet de gérer l’affichage graphique, les événements clavier ainsi que les interactions du jeu. Une fois Python installé, Pygame peut être installé via la commande suivante :

```bash
pip install pygame
```

Aucune autre dépendance externe n’est nécessaire, les autres modules utilisés (comme random ou socket) étant déjà inclus dans la bibliothèque standard de Python.
Après l’installation des dépendances, il suffit de récupérer le projet (par clonage Git ou téléchargement manuel), puis de se placer dans le dossier racine. Il est important de conserver l’organisation des fichiers, notamment le dossier images/, qui contient les ressources graphiques indispensables au bon fonctionnement du jeu.
Enfin, le jeu peut être lancé avec la commande suivante :	
python script.py

Si toutes les étapes ont été correctement suivies, le jeu se lancera en mode plein écran et sera prêt à être utilisé.


### 1. Cloner le projet

```bash
git clone <url-du-repo>
cd copter-battle
```

---

## ⚙️ Fonctionnement

Le jeu repose sur une boucle principale exécutée en continu grâce à Pygame.  
À chaque itération, plusieurs éléments sont mis à jour :

- les déplacements des hélicoptères en fonction des entrées clavier
- la génération aléatoire des obstacles et des bonus
- la détection des collisions entre les hélicoptères, les obstacles et les projectiles
- l’affichage des éléments graphiques à l’écran

Les obstacles et les bonus apparaissent à intervalles réguliers et se déplacent de droite à gauche.  
Les joueurs doivent adapter leurs mouvements pour éviter les collisions tout en utilisant les bonus pour attaquer leur adversaire.

---

## 📁 Structure du projet

Le projet est organisé en plusieurs fichiers afin de séparer les différentes responsabilités :

- `script.py` : contient la boucle principale du jeu et la gestion globale
- `helico.py` : définit la classe Helicopter (déplacement, vies, bonus, collisions)
- `obstacle.py` : gère la création et le comportement des obstacles
- `bonus.py` : gère les différents bonus du jeu (bombe, rafale, bouclier)
- `joueur.py` : gère la connexion réseau entre deux joueurs (socket)
- `images/` : contient toutes les ressources graphiques utilisées dans le jeu

---

## 🏁 Objectif du jeu (je lai déjà mis au début)

Le but du jeu est de survivre le plus longtemps possible tout en éliminant son adversaire.

Chaque joueur dispose d’un nombre limité de vies. Lorsqu’un joueur entre en collision avec un obstacle ou subit une attaque, il perd une vie.  
La partie se termine lorsqu’un joueur n’a plus de vies. L’autre joueur est alors déclaré vainqueur.

---

## 🚧 Améliorations possibles

Plusieurs améliorations peuvent être envisagées pour enrichir le projet :

- ajout d’un mode multijoueur en ligne complet
- ajout de nouveaux bonus et malus
- intégration de sons et musiques
- amélioration de l’interface utilisateur (menus, animations)
- ajout d’une intelligence artificielle pour jouer en solo (peut être a enlever)
- optimisation des performances du jeu

---


## 👨‍💻 Auteur

Projet réalisé par dans le cadre d’un projet universitaire en informatique par :
-	OUILLEDIRNE Yacine
-	HADJ-CHERIF Yanis
-	MOHAMED Chanfi
-	RIGAULT Kylian 

---

## Commande journal

Commande a mettre dans le terminal sur vs code : git log --pretty=format:'"%an" : "%ad", "%D", "%s",' --date=short > journal.txt
