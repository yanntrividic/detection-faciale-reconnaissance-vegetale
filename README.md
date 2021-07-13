# Reconnaissance plantale
Ce logiciel a été développé avec Python 3.9, OpenCV et les projets Pl@ntNet et facial_recognition. Après avoir détecté les visages présents dans le champ de votre webcam, il les associe à des espèces de plantes en donnant leurs images à un réseau neuronal profond d'identification de plantes.

<img src="https://raw.githubusercontent.com/yanntrividic/detection-faciale-reconnaissance-vegetale/main/a_plant_and_i.png" alt="exemple1" width="600"/>
<img src="https://raw.githubusercontent.com/yanntrividic/detection-faciale-reconnaissance-vegetale/main/two_ids.png" alt="exemple2" width="600"/>


**Version :** 1.0  
**Auteur :** Yann Trividic  
**Context :** Ce projet a été mené dans le cadre du laboratoire 5 nommé *Reconnaissance faciale : des visages, des mondes*, organisé à l'école d'été *Prendre Racine* qui eut lieu du 5 au 11 juillet 2021 à Poitiers.  
**Licence :** Licence GPL-3.0

## Contenu
Le dépôt contient trois dossiers : `src` pour le code source, `data` pour quelques images de test, et `models` pour les modèles de reconnaissance d'objets.

## Modèles utilisés
Pour la classification d'objets (c'est-à-dire pour la détection des plantes) nous utilisons un modèle de Tensorflow. Celui-ci permet d'isoler une plante du reste de l'image.

Pour la détection de visages, nous utilisons le modèle développé dans le cadre du projet opensource mené par Adam Geitgey : `face_recognition`. Celui-ci est entraîné sur la base de données Labeled Faces in the Wild, une base de données contenant une diversité de visages suffisante pour pouvoir détecter l'extrême majorité des visages. **Au départ, ce projet implémentait le modèle de détections de visages du projet OpenCV. Celui-ci n'offrait pas de performances acceptables sur les visages des personnes non blanches.** Pour plus d'informations sur la question et le travail que nous avons effectué en réaction à ce problème : [lien](https://chloedesmoineaux.surf/desvisagesdesmondes)

Pour l'identification des plantes, nous utilisons l'API du projet Pl@ntNet.

## Installation
Pour ce projet, vous aurez besoin de Python 3.9, d'une webcam ainsi que d'avoir installé les dépendances spécifiées dans le fichiers `requirements.txt`. Pour les installer, la commande est la suivante :
`python3.9 -m pip install -r requirements.txt`

Pour ensuite lancer le programme après installation des prérequis, veuillez entrer la commande suivante depuis le répertoire `src` :
`python3.9 main.py`
