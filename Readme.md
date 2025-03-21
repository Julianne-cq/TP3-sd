Vous commencez votre premier job de bioinformaticien.ne. La personne précédente vous a laissé un code quasi sans commentaire et sans test, et votre chef est biologiste et n'y comprend rien. Il sait seulement que ce code était très pratique pour rechercher des k-mer dans des jeux de données. 
Vous allez améliorer la situation pour que l'équipe puisse se servir du code de manière pérenne.

1. Décrivez à quoi sert `class SimpleBloomFilter`. Ecrivez les doctests pour cette classe.

cf class SimpleBloomFilter.

Cette classe permet de modéliser des filtres de Bloom. 
Les positions renvoyés par la/les fonction(s) de hashage (méthode '_hashes') d'un élément donnée modifieront les bits du filtre
en ses positions de 0 à 1 à l'ajout de cet élément (méthode 'add'). 
On peut vérifier la présence d'un élément dans le filtre de Bloom (méthode 'contains') mais il peut y avoir des faux positifs.

Elle permettra par la suite de stocker efficacement les jeux de données dans l'arbre de données.

2. Décrivez à quoi sert `class StructureNode`. 

cf class StructureNode.

Cette classe permet de modéliser les noeuds d'un arbre de données.
Chaque noeud est initialisé avec un filtre de Bloom défini ou automatiquement créé et en conservant les étiquettes des jeux de données. 
Pour les noeuds-parents, les 2 noeuds-fils gauches et droits seront stockés : il s'agit d'une fusion de jeu de données fils

3. Décrivez à quoi sert `class Structure`. Ecrivez les doctests pour cette classe.

cf class Structure.

Cette classe a pour objectif de construire un arbre de données (méthode '_build_tree'). 
Pour chaque jeu de données, un filtre de Bloom est produit : ils constitueront les noeuds-feuilles.
Afin de créer les noeuds-parents, on fusionne les filtres de Bloom des noeuds-fils. Le nouveau filtre de Bloom contiendra les valeurs de présences et d'absence des 2 filtres-fils (méthode 'merge' de la classe SimpleBloomFilter). 
On réalise cette opération jusqu'au noeud-racine.
A partir de ce dernier, on pourra déterminer rapidement l'absence ou la présence d'un élement dans l'arbre en le hashant et en 
vérifiant si les positions données par le hash sont toutes présentes dans le filtre de Bloom du noeud-racine et s'il est noté présent, on remontera les filtres de Bloom pour retrouver le jeu de données dans lequel il est présent (méthode 'query' et '__query_recursive' s'appuyant sur la méthode 'contains' de SimpleBloomFilter).

4. Cette structure mélange donc deux structures de données que nous avons vues. Quelles sont elles ?

Cette structure mélange deux structures de données : les filtres de Bloom correspondant à des tables de hashage particulières et les arbres 
de données pour organiser les filtres.

4. D'après vous, que peut-on dire sur la complexité de la requête de cette structure ? 

La recherche dans un arbre binaire a une complexité de O(n) au pire des cas, lorsque l'ensemble de l'arbre doit être remonté. 
Mais ici, on doit également prendre en compte le nombre de hash réalisé de complexité O(k)
La complextié de requête dans cette structure est donc (au pire des cas) : O(n*k).

5. Quelles sont les différences avec la table basée sur une MPHF que nous avons vu ? 

Avec une table basée sur une MPHF, les risques de collision sont nuls contrairement à un filtre de Bloom qui permet les faux positifs en cas de surcharge du filtre par exemple. Cependant, l'utilisation de filtre de Bloom permet de réduire l'espace mémoire nécessaire. 
La complexité de requête dans une MPHF est de O(1) contrairement à une requête dans un filtre (O(k) et donc O(n*k) dans un arbre de données utilsant 
des filtres de Bloom).
En conclusion, l'utilisation de filtre de Bloom plutôt que d'une table basée sur une MPHF permet de réduire l'espace mémoire alloué mais l'utilisation d'une MPHF permet d'éviter les faux positifs (de par son caractère déterministe) et une requête en temps constant.

6. Bonus : Pouvez-vous retracer de quel papier de bioinformatique vient cette idée ?
Bifrost: Highly Parallel Construction and Indexing of Colored and Compacted de Bruijn Graphs" (2018).