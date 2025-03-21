Vous commencez votre premier job de bioinformaticien.ne. La personne précédente vous a laissé un code quasi sans commentaire et sans test, et votre chef est biologiste et n'y comprend rien. Il sait seulement que ce code était très pratique pour rechercher des k-mer dans des jeux de données. 
Vous allez améliorer la situation pour que l'équipe puisse se servir du code de manière pérenne.

1. Décrivez à quoi sert `class SimpleBloomFilter`. Ecrivez les doctests pour cette classe.

cf class SimpleBloomFilter.

Cette classe permettra de stocker efficacement les éléments ajoutés dans l'arbre finale qui correspondent à ses feuilles .
Chaque élément est un filtre de Bloom. Afin de construire l'arbre, les noeuds parents seront créés en fusionnant les 
filtres de Bloom des noeuds fils.

2. Décrivez à quoi sert `class StructureNode`. 

cf class StructureNode.

Cette classe permet de modéliser les noeuds d'un arbre de données en conservant les étiquettes des jeux de données et les possibles noeuds gauches et droits pour les noeuds parents et en les initialisant avec un filtre de Bloom défini ou automatiquement créé. 

3. Décrivez à quoi sert `class Structure`. Ecrivez les doctests pour cette classe.

cf class Structure.

Cette classe a pour objectif de construire un arbre de données. 
Pour chaque jeu de données, un filtre de Bloom est produit : ils constitueront les noeuds feuilles.
Afin de créer les noeuds-parents, on fusionne les filtres Bloom des noeuds-fils. Le nouveau filtre de Bloom contiendra les valeurs
de présences et d'absence des 2 filtres-fils. 
On réalise cette opération jusqu'au noeud-racine.
A partir de ce dernier, on pourra déterminer rapidement l'absence ou la présence d'un élement dans l'arbre en le hashant et en 
vérifiant si les positions données par le hash sont toutes présentes dans le filtre de Bloom du noeud-racine et s'il est noté présent, on remontera les filtres de Bloom pour retrouver le jeu de données dans lequel il est présent (méthode 'query' et '__query_recursive')


4. Cette structure mélange donc deux structures de données que nous avons vues. Quelles sont elles ?

4. D'après vous, que peut-on dire sur la complexité de la requête de cette structure ? 

5. Quelles sont les différences avec la table basée sur une MPHF que nous avons vu ? 

6. Bonus : Pouvez-vous retracer de quel papier de bioinformatique vient cette idée ?
PAPIER DE 2018 