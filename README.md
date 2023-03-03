# Visualisation de données géolocalisées

L'objectif de ce problème est de visualiser diverses collections de données
géolocalisées sur une carte, à l'aide de `fltk`. On s'appuiera pour cela sur des données publiquement
disponibles, par exemple sur le site du gouvernement dédié à l'« open data », [data.gouv.fr](http://data.gouv.fr).

## Exemple

Voici une capture d'écran montrant un prototype de programme de ce genre :

![Licenciés de basket-ball en 2011 en Seine-et-Marne](capture.png)

Il s'agit d'une carte de la Seine-et-Marne, où chaque disque représente le nombre de licenciés d'une fédération sportive (ici la fédération française de basket-ball en 2011). 

L'aire de chaque disque est proportionnelle au nombre de licenciés. Le nom d'une commune et le nombre de licenciés qui y habitent sont affichés quand le pointeur de la souris survole le disque correspondant.

Le programme n'utilise aucun fichier image, le contour du département est dessiné grâce à la fonction `polygone` de `fltk`.

## Tâches obligatoires

Il est demandé de réaliser *a minima* un programme permettant d'afficher le type de carte illustré ci-dessus.

Les données utilisées pour composer cet exemple sont les suivantes :

- [Carte des licenciés sportifs en Seine-et-Marne](https://www.data.gouv.fr/fr/datasets/carte-des-licencies-sportifs-en-seine-et-marne-idf/), au format [CSV](https://www.data.gouv.fr/fr/datasets/r/e83e26cf-e533-44aa-8605-733b42302826)
- [Contours des départements français issus d'OpenStreetMap](https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/), au format [shapefile](https://www.data.gouv.fr/fr/datasets/r/eb36371a-761d-44a8-93ec-3d728bec17ce)

Il est recommandé de bien explorer ces données afin de comprendre ce qu'elles contiennent. Vous aurez pour cela besoin de vous documenter sur les formats [shapefile](https://en.wikipedia.org/wiki/Shapefile) et [CSV](https://fr.wikipedia.org/wiki/Comma-separated_values), et d'explorer le contenu des fichiers grâce au module [`pyshp`](https://pypi.org/project/pyshp/) ou à un logiciel de tableur comme [LibreOffice](https://fr.libreoffice.org/).

### Comment tracer le contour du département ?

La manipulation du format shapefile a été faite à l'aide du module tiers [`pyshp`](https://pypi.org/project/pyshp/) dont la documentation contient des exemples simples d'utilisation.

Pour accéder à la liste des points constituant le contour du département de Seine-et-Marne, on a par exemple exécuté les commandes suivantes, après avoir installé `pyshp` et téléchargé et décompressé le document indiqué ci-dessus.

```
>>> import shapefile
>>> sf = shapefile.Reader("departements-20180101")
>>> sf.records()
[...,
Record #47: ['77', 'Seine-et-Marne', 'FR102', 'fr:Seine-et-Marne', 5927.0],
...]
>>> seine_et_marne = sf.shape(47)
>>> seine_et_marne.bbox
[2.3923284961351237, 48.12014561527111, 
3.559220826259302, 49.11789167125887]
>>> seine_et_marne.points
[(2.3923284961351237, 48.335929161584076), (2.393003669902668, 48.336290983108846), (2.3940130169559044, 48.3356802622364), ...]
```

L'attribut `seine_et_marne.bbox` indique les quatre coordonnées extrêmes présentes dans le tracé du contour du département : longitude minimale, latitude minimale, longitude maximale et latitude maximale exprimées en degré dans le système [WGS 84](https://fr.wikipedia.org/wiki/WGS_84).

La liste des points `seine_et_marne.points` est donnée sous la forme d'une liste de couples de coordonnées (longitude, latitude) également exprimées en degré.

### Comment construire les disques bleus ?

Chaque disque bleu représente le nombre de licenciés de la fédération française de basket dans une commune donnée. Cette information a été récupérée dans le fichier CSV indiqué ci-dessus.

La manipulation du format CSV a été faite à la main, notamment à l'aide de la méthode `split` de Python. 

On s'est en particulier intéressé aux colonnes suivantes du tableau :
- `'commune'` : nom de chaque ville, pour l'affichage des étiquettes textuelles ;
- `'federation'` : nom de la fédération sportive concernée, pour la sélection des lignes concernant la fédération de basket-ball ;
- `'licences_en_2011'` : nombre de licenciés par commune en 2011, pour le calcul du rayon de chaque disque bleu ;
- `'wgs84'`: latitude et longitude de la commune, en degrés, dans le système [WGS 84](https://fr.wikipedia.org/wiki/WGS_84) déjà mentionné, pour le placement de chaque disque bleu.

Pour le calcul du rayon de chaque disque, il a été choisi de dessiner des disques d'*aire* proportionnelle au nombre représenté.

## Suggestions d'améliorations

Voici une liste (comme d'habitude non exhaustive) d'améliorations possibles :

### Programme paramétrable

Le programme dispose de plusieurs paramètres en ligne de commande qui permettent de modifier son fonctionnement. 

Par exemple, il pourrait être possible de sélectionner :
- des données différentes dans la même base (par exemple : autres sports), 
- des bases de données différentes (par exemple : restaurants, stations de train ou de métro, etc.),
- un département, région ou commune différente,
- des paramètres d'affichage (échelle des disques, couleurs, taille du texte, etc.).

### Sélection et agrégation de données

Le programme permet de filtrer les données présentées, ou de rassembler plusieurs données entre elles. 

Par exemple, on pourrait souhaiter afficher le nombre total de licenciés par commune, tous sports confondus, si celui-ci dépasse 2% de la population de la commune.

### Visualisation avancée

Le programme permet d'afficher plusieurs données par commune (par exemple plusieurs sports), par exemple à l'aide d'un « diagramme camembert » coloré ou d'un autre mode de visualisation.

### Ajout de repères géographiques

Le programme dessine les contours des communes, ou les principales routes, les voies de chemin de fer, etc. De nombreuses données sont mises à la disposition du public par l'organisation OpenStreetMap, y compris sur le site [data.gouv.fr](data.gouv.fr).

### Interactivité

Il est possible d'obtenir des informations supplémentaires en survolant ou en cliquant sur les éléments graphiques de la fenêtre.

Il est également envisageable de déplacer la carte grâce à des touches du clavier, de zoomer ou dézoomer, etc.

### Explorations diverses

Il est également possible d'explorer :
- d'autres formats de données géographiques (par exemple [GeoJSON](https://geojson.org/)) ou de tableurs (`odt`, `docx`) ;
- d'autres méthodes d'accès aux données (par exemple dynamiquement à l'aide d'API et de bibliothèques dédiées) ;
- d'autres échelles géographiques (quartier, commune, région, pays, continent, monde) ;
- d'autres types de données (végétation, climat, pollution, démographie, santé, culture, trafic, célébrités, réseaux sociaux ou media...) ;
- une évolution de données au cours du temps si l'on dispose de plusieurs jeux de données sur une certaine période.