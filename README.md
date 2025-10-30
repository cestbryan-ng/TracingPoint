# Tracing Point


#### SetUp

Pour éxecuter le script, suivez les commmandes suivantes :
```bash
git clone https://github.com/cestbryan-ng/TracingPoint.git
cd TracingPoint
pip install -r requirements.txt

# Pour éxecuter le script
python tracingpoint.py
```


#### Description

**Tracing Point** est une application desktop interactive permettant de tracer des fonctions mathématiques avec une interface graphique moderne et intuitive. Développée en Python avec CustomTkinter et Matplotlib, cette application offre aux passionnés de mathématiques un outil puissant pour visualiser rapidement n'importe quelle fonction mathématique.


## Fonctionnalités principales

L'application permet de saisir des fonctions mathématiques en notation naturelle (par exemple "2x+4" au lieu de "2*x+4") et génère automatiquement des graphiques professionnels. Elle gère intelligemment les discontinuités, les asymptotes et les valeurs non définies, produisant des tracés nets et précis même pour des fonctions complexes comme tan(x).

Une fonctionnalité clé est la possibilité de tracer plusieurs fonctions successivement sans fermer les graphiques précédents, permettant ainsi des comparaisons visuelles directes. Un bouton "Quitter" permet de fermer toutes les fenêtres de graphiques en un seul clic, offrant une gestion propre et efficace des ressources.


## Architecture du projet


### `tracingpoit.py` - Application principale

Ce fichier contient la classe `MonApp` qui hérite de `CTk.CTk` (CustomTkinter). J'ai choisi CustomTkinter plutôt que Tkinter standard pour son apparence moderne et son thème sombre natif, offrant une expérience utilisateur plus agréable.

La méthode `config_interface()` initialise la fenêtre avec une taille de 800x650 pixels, redimensionnable pour s'adapter à différents écrans. Le thème sombre et la palette de couleurs bleues ont été choisis pour réduire la fatigue oculaire lors d'une utilisation prolongée.

La méthode `config_polices()` définit une hiérarchie typographique cohérente avec différentes polices pour les titres (Helvetica 36pt bold), les sous-titres, les boutons et les champs de saisie (Consolas pour un aspect monospace adapté aux formules mathématiques).

La méthode `create_interface()` construit méthodiquement l'interface en plusieurs sections.


### Gestion intelligente de la syntaxe

La méthode `preparation_fonction()` est au cœur de l'expérience utilisateur. Elle utilise des expressions régulières pour transformer la notation naturelle en syntaxe Python valide :
- `2x` devient `2*x`
- `x2` devient `x*2`
- `2(x+1)` devient `2*(x+1)`
- `(x+1)3` devient `(x+1)*3`

Cette fonctionnalité évite aux utilisateurs de se soucier de la syntaxe exacte, rendant l'application accessible même aux débutants.


### Gestion d'entrée robuste

L'application implémente une validation stricte des entrées pour garantir la sécurité et la fiabilité. Seule la variable `x` est reconnue comme variable valide - toute autre variable générera une erreur. Cette restriction délibérée évite les confusions et les erreurs d'évaluation, en fournissant un retour clair à l'utilisateur en cas de tentative d'utilisation d'autres variables comme `y`, `t` ou `n`. L'évaluation des fonctions utilise `eval()` avec un contexte contrôlé qui limite l'accès aux fonctions mathématiques de NumPy uniquement, empêchant l'exécution de code arbitraire ou malveillant.


### Algorithme de tracé avancé

La méthode `calcul_image()` évalue la fonction en un point donné en utilisant `eval()` avec un contexte sécurisé. Si le résultat est infini (`isinf()`) ou indéfini (`isnan()`), la fonction retourne `nan` pour permettre à Matplotlib de gérer l'interruption du tracé. Cette approche évite les erreurs lors du tracé de fonctions comme `1/x` ou `tan(x)` qui ont des asymptotes.

La méthode `creation_segments()` est l'algorithme le plus sophistiqué du projet. Il parcourt tous les points et construit des segments séparés en détectant trois types de discontinuités : les valeurs `nan`, les pentes supérieures à 10,000, et les sauts de valeur supérieurs à 0.5. Quand une discontinuité est détectée, le segment en cours est sauvegardé (s'il contient au moins 2 points) et un nouveau segment commence. Cette logique évite les lignes verticales indésirables qui relieraient artificiellement les branches séparées d'une fonction discontinue. Le seuil de 10,000 pour la pente a été déterminé expérimentalement pour bien détecter les asymptotes sans créer de fausses discontinuités sur des fonctions raides mais continues.

La méthode `tracer()` est la méthode principale qui orchestre tout le processus de tracé. Elle évalue la fonction sur 110,000 points (choix délibéré pour obtenir des courbes lisses) et détecte automatiquement les sauts brutaux qui indiqueraient une discontinuité ou une asymptote. Chaque appel à `tracer()` ouvre une nouvelle fenêtre Matplotlib indépendante, permettant d'avoir plusieurs graphiques simultanément à l'écran pour comparer différentes fonctions.

Les valeurs infinies et NaN sont remplacées par `nan` de NumPy, permettant à Matplotlib de gérer naturellement les interruptions dans le tracé.


### Interface utilisateur

L'interface se compose de plusieurs sections :
- Un titre élégant avec dégradé de couleur
- Un champ de saisie avec placeholder explicite montrant des exemples
- Des sliders pour ajuster les plages X (de -500 à 500)
- Des boutons stylisés avec effets de survol

J'ai délibérément limité les paramètres ajustables pour éviter de surcharger l'interface, en me concentrant sur l'essentiel : la fonction et sa plage de tracé.

La méthode `fermer()` assure une fermeture propre de l'application en appelant `plt.close('all')` pour fermer toutes les fenêtres de graphiques ouvertes, puis libère les ressources avec `quit()` et `destroy()`. Cette approche garantit qu'aucune fenêtre orpheline ne reste ouverte après la fermeture de l'application principale.


## Choix de conception

**Pourquoi 110,000 points ?** Après expérimentation, ce nombre offre le meilleur compromis entre fluidité des courbes et performance. Moins de points donnaient des courbes anguleuses, davantage ralentissait l'affichage sans amélioration visible.

**Pourquoi CustomTkinter ?** Tkinter standard a une apparence désuète. CustomTkinter offre des widgets modernes, un thème sombre natif et une meilleure intégration avec les systèmes d'exploitation récents.

**Pourquoi pas de sauvegarde d'images ?** J'ai préféré me concentrer sur la fonctionnalité principale de tracé. Matplotlib permet déjà de sauvegarder via son interface graphique, évitant la duplication de fonctionnalités.

**Tracés multiples simultanés** - La décision de permettre l'ouverture de plusieurs fenêtres de graphiques simultanément plutôt qu'une seule fenêtre réutilisable offre plus de flexibilité. Les utilisateurs peuvent comparer visuellement différentes fonctions côte à côte, repositionner les fenêtres, et garder un historique visuel de leur exploration. Le bouton "Quitter" centralise la fermeture de toutes ces fenêtres, évitant la tâche fastidieuse de les fermer une par une.

**Variable unique 'x'** - Restreindre l'application à une seule variable `x` simplifie l'interface et l'utilisation. Cette contrainte correspond à l'usage standard en mathématiques où les fonctions d'une variable utilisent traditionnellement `x`. Supporter plusieurs variables aurait nécessité une interface plus complexe avec des contrôles supplémentaires, diluant la simplicité qui fait la force de l'application.


## Conclusion

Tracing Point démontre qu'une application mathématique peut être à la fois puissante et accessible. L'accent mis sur l'expérience utilisateur, avec la notation naturelle et la gestion automatique des discontinuités, en fait un outil pratique pour l'apprentissage et l'enseignement des mathématiques. La possibilité de tracer et comparer plusieurs fonctions simultanément, combinée à une gestion d'entrée robuste, fait de Tracing Point un outil à la fois simple pour les débutants et suffisamment puissant pour l'exploration mathématique avancée.
