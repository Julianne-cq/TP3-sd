import hashlib

class SimpleBloomFilter:
	'''
	Cette classe a pour but de modéliser un filtre de Bloom qui répond à la requête d'existence en hashant un élément donné, 
	en remplaçant par 1 les positions renvoyées par la fonction de hashage dans le table de bits. 
	On peut également vérifier si l'élément est présent lorsque l'ensemble des positions renvoyées par la table de hashage 
	de cet élément correspondent à des "1" dans le tableau de bits.
	'''
	def __init__(self, size: int =100, num_hashes: int =1)-> None:
		'''
		Initialise l'objet SimpleBloomFilter.

		Paramètres:
		:param size: définit la taille du tableau de bits ; défaut = 100
		:param num_hashes: nombre de hash à réaliser ; défaut = 1

		Exemples:
		>>> obj = SimpleBloomFilter()
		>>> len(obj.bit_array)
		100
		>>> obj.num_hashes
		1
		>>> obj = SimpleBloomFilter(size=10)
		>>> len(obj.bit_array)
		10
		>>> obj.bit_array
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		'''
		#Initialise la taille du tableau de bits
		self.size = size
		#Initialise le nombre de hash à réaliser
		self.num_hashes = num_hashes

		#Initialise un tableau de bits de la taille définie
		self.bit_array = [0] * size

	def _hashes(self, item: str)-> list[int]:
		'''
		Définie une fonction de hashage a utiliser sur l'item passé en paramètre et retourne la/les position(s) dans le tableau
		de bits après l'avoir hashé.

		Paramètres:
		:param item: l'élément sur lequel la fonction de hashage doit être appliquée

		Exemples:
		>>> obj = SimpleBloomFilter()
		>>> item = 'Bonjour'
		>>> obj._hashes(item)
		[45]
		>>> bf = SimpleBloomFilter(size = 20, num_hashes=3)
		>>> hashes = bf._hashes("item")
		>>> print(hashes)
		[2, 10, 1]
		>>> all (0 <= h <= 20 for h in hashes)
		True
		'''
		hash_values = []
		#Parcourt le nombre de hashs à générer 
		for i in range(self.num_hashes):
			#Définie la fonction de hashage et hash l'élément passé en paramètre
			hash_func = hashlib.sha256((str(i) + item).encode()).hexdigest()
			hash_values.append(int(hash_func, 16) % self.size)
		return hash_values

	def add(self, item)-> None:
		'''
		Ajoute l'élement item dans le tableau de bits en hashant celui-ci et en remplaçant les 0 en 1 aux positions renvoyés
		par la fonction de hashage.

		Paramètres:
		:param item: l'élément sur lequel la fonction de hashage doit être appliquée

		Exemples:
		>>> obj = SimpleBloomFilter()
		>>> item = 'Bonjour'
		>>> obj.add(item)
		>>> obj.bit_array.count(1)
		1
		>>> item = ''
		>>> obj.add(item)
		>>> obj.bit_array.count(0)
		98
		>>> obj = SimpleBloomFilter(num_hashes=3)
		>>> obj.add(item)
		>>> obj.bit_array.count(1)
		3
		'''
		#Parcourt les positions dans le tableau de bits renvoyés par la méthode _hashes sur l'objet item
		for pos in self._hashes(item):
			#Modifie le bit en 1 à la position donnée
			self.bit_array[pos] = 1

	def contains(self, item)-> bool:
		'''
		Vérifie si l'élément passé en paramètre est présent dans le tableau de bits

		Paramètres:
		:param item: l'élément sur lequel la fonction de hashage doit être appliquée

		Exemples:
		>>> obj = SimpleBloomFilter()
		>>> item = 'Bonjour'
		>>> obj.contains(item)
		False
		>>> obj.add(item)
		>>> obj.contains(item)
		True
		>>> obj = SimpleBloomFilter(size = 1)
		>>> obj.add(item)
		>>> obj.contains(item)
		True
		>>> obj.bit_array
		[1]
		>>> obj.contains ("a")  # Cas d'un faux-positif
		True
		'''
		return all(self.bit_array[pos] for pos in self._hashes(item))

	def merge(self, other):
		'''
		Fusionne les tableaux de bits de 2 filtres de Bloom.

		Paramètres:
		:param other: un objet SimpleBloomFilter 

		Exemples:
		>>> obj = SimpleBloomFilter(size=10)
		>>> obj.add('T')
		>>> obj.bit_array
		[0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
		>>> obj.contains('AT')
		False
		>>> other = SimpleBloomFilter(size=10)
		>>> other.add('AT')
		>>> other.bit_array
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
		>>> merged = obj.merge(other)
		>>> merged.bit_array
		[0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
		>>> merged.contains('AT')
		True
		'''
		#Vérifie que les 2 filtres de Bloom à fusionner ont la même taille
		assert self.size == other.size, "Bloom filters must be of the same size!"
		#On crée un objet SimpleBloomFilter 
		merged_filter = SimpleBloomFilter(self.size, self.num_hashes)
		#Fusionne les tableaux de bits des 2 filtres de Bloom pour combiner les valeurs de présence de leurs éléments.
		#Si un élément est présent dans au moins l'un des filtres, sa présence est conservée dans le filtre fusionné
		#Un bit sera à 1 dans le tableau final si il vaut 1 à cette position dans l'un des deux filtres.
		merged_filter.bit_array = [a | b for a, b in zip(self.bit_array, other.bit_array)]
		return merged_filter

class StructureNode:
	'''
	Cette classe a pour but de modéliser les noeuds d'un arbre de données dont les valeurs sont stockées dans un filtre de Bloom.
	Elle modélise également les noeuds parents en conservant les données des noeuds gauches et droits (fils) si le filtre de Bloom 
	du noeud actuel est obtenu via une fusion des deux précédents.
	'''
	def __init__(self, bloom_filter=None)-> None:
		'''
		Initialise un objet StructureNode à partir d'un filtre de Bloom.

		Paramètres:
		:param bloom_filter: un objet SimpleBloomFilter ; si aucun n'est fourni, un nouveau est créé.
		'''
		#Initialise un filtre de bloom. Si aucun n'est fourni, un nouveau est créé
		self.bloom = bloom_filter if bloom_filter else SimpleBloomFilter()
		
		#Initialise les liens vers les noeuds enfants à None.
		#Pour les noeuds feuilles, resteront à None
		self.left = None
		self.right = None

		#Initialise la liste des noms de jeux de données aux nœuds feuilles
		self.datasets = [] 

class Structure:
	'''
	Cette classe a pour but de modéliser et de construire un arbre de données à partir d'une liste d'étiquettes de jeu de données, leurs 
	valeurs associées dans un dictionnaire et des paramètres nécessaires à la création d'un filtre de Bloom.
	Après la construction de celui-ci, la méthode query permet de déterminer si un élément y est présent en utilisant la méthode _query_recursive
	qui remonte l'arbre. 
	'''
	def __init__(self, datasets: list, kmers_dict: dict[:str], bloom_size=10000, num_hashes=3)-> None:
		'''
		Initialise un objet Structure à partir d'une liste d'étiquettes de datasets, d'un dictionnaire de kmers associés aux étiquettes,
		d'une taille de filtre de Bloom et le nombre de hash à réaliser sur les éléments des noeuds.

		Paramètres:
		:param datasets: une liste d'étiquettes de jeu de données
		:param kmers_dict: un dictionnaire de kmers associés à chaque étiquette de dataset
		:param bloom_size: définit la taille du tableau de bits ; défaut = 10000
		:param num_hashes: nombre de hash à réaliser ; défaut = 3

		Exemples:
		>>> datasets = ["d1", "d2", "d3", "d4", "d5"]
		>>> kmers_dict = {"d1":['A'], "d2":['T'], "d3":['C'], "d4":['G'], "d5":['N']}
		>>> s = Structure(datasets, kmers_dict)
		'''
        #Dictionnaire qui associe les noms des datasets à leurs noeuds (filtre de Bloom) correspondants dans l'arbre.
		self.leaves = {}

		#Construit l'arbre en utilisant la méthode _build_tree et stocke la racine de l'arbre 
		self.root = self._build_tree(datasets, kmers_dict, bloom_size, num_hashes)

	def _build_tree(self, datasets: list, kmers_dict: dict[:str], bloom_size: int, num_hashes: int)-> None:
		'''
		Construit l'arbre grâce aux filtres de Bloom calculés pour chaque datasets et leurs valeurs.

		Paramètres:
		:param datasets: l'étiquette des noeuds-feuilles de l'arbre
		:param kmers_dict: les kmers associés aux étiquettes des noeuds-feuilles de l'arbre 
		:param bloom_size: la taille des filtres de Bloom a créer
		:param num_hashes: le nombre de hash à réaliser dans le filtre de Bloom

		Exemples:
		>>> datasets = ["d1", "d2", "d3", "d4", "d5"]
		>>> kmers_dict = {"d1":['A'], "d2":['T'], "d3":['C'], "d4":['G'], "d5":['N']}
		>>> s = Structure(datasets, kmers_dict)
		>>> len(s.leaves)
		5
		>>> 'd1' in s.leaves
		True
		>>> '8' in s.leaves
		False
		'''
		#Initialise une liste qui contiendra les noeuds 
		nodes = []

		# Step 1
		#Parcours les datasets
		for dataset in datasets:
			#Initialise le filtre de Bloom
			bf = SimpleBloomFilter(bloom_size, num_hashes)
			#Parcours les kmers présents dans le dataset actuel
			for kmer in kmers_dict[dataset]:
				#Les ajoutent aux filtres de Bloom
				bf.add(kmer)
			#Création du noeud de l'arbre à partir du filtre de Bloom
			node = StructureNode(bf)
			#défini le nom du noeud
			node.datasets = [dataset]
			#Définie les feuilles du dataset comme étant le noeud 
			self.leaves[dataset] = node
			#Ajoute le noeud dans la liste des noeuds de l'arbre
			nodes.append(node)

		# Step 2
		#Tant qu'il y a au moins 2 noeuds dans la liste
		while len(nodes) > 1:
			#Initialise une liste qui contiendra les nouveaux noeuds 
			new_nodes = []
			#On parcourt la liste de nodes de 2 en 2
			for i in range(0, len(nodes), 2):
				#Tant qu'il y a des noeuds après 
				if i + 1 < len(nodes): 
					#On fusionne le noeud actuelle avec le suivant 
					merged_bf = nodes[i].bloom.merge(nodes[i + 1].bloom)
					#On crée le noeud précédent la feuille
					parent = StructureNode(merged_bf)
					#On défini les deux noeuds fils de part et d'autres du parent
					parent.left = nodes[i]
					parent.right = nodes[i + 1]
					#On ajoute les noms des 2 datasets aux noeuds parents
					parent.datasets = nodes[i].datasets + nodes[i + 1].datasets
				else:
					#Sinon il ne reste qu'un noeud 
					parent = nodes[i] 
				#On ajoute le noeud parent à la liste de noeuds
				new_nodes.append(parent)
			#On met à jour la liste de noeuds
			nodes = new_nodes

		#Renvoie la première feuille de l'arbre ?
		return nodes[0] if nodes else None  

	def query(self, kmer: str)-> list:
		'''
		Recherche si le kmer est présent dans l'arbre et renvoie dans quel noeud il est présent

		Paramètres:
		:param kmer: le kmer a recherché dans l'arbre

		Exemples:
		>>> datasets = ["d1", "d2", "d3", "d4", "d5"]
		>>> kmers_dict = {"d1":['A'], "d2":['T'], "d3":['C', 'N'], "d4":['G', 'N'], "d5":['N']}
		>>> s = Structure(datasets, kmers_dict)
		>>> s.query ('AT')
		[]
		>>> s.query('A')
		['d1']
		>>> s.query('N')
		['d3', 'd4', 'd5']
		'''
		#Initialise une liste vide de résultats
		results = []

		#Recherche tous les noeuds où le kmer est présent 
		self._query_recursive(self.root, kmer, results)
		return results

	def _query_recursive(self, node: StructureNode, kmer: str, results: list):
		'''
		Remonte l'arbre pour trouver dans quel dataset le kmer est présent

		Paramètres:
		:param node: le noeud concerné par la recherche
		:param kmer: le kmer a recherché dans l'arbre
		:param results: une liste vide où stocker la présence du kmer

		Exemples:
		>>> datasets = ["d1", "d2", "d3", "d4", "d5"]
		>>> kmers_dict = {"d1":['A'], "d2":['T'], "d3":['C', 'N'], "d4":['G', 'N'], "d5":['N']}
		>>> s = Structure(datasets, kmers_dict)
		>>> res = []
		>>> s._query_recursive(s.root, 'T', res)
		>>> res
		['d2']
		'''
		#Si aucun noeud n'est présent ne renvoie rien
		if node is None:
			return
		#Si le kmer est présent dans le noeud actuel
		if node.bloom.contains(kmer): 
			#Vérifie s'il est présent dans les noeuds fils
			if node.left is None and node.right is None: 
				#Si absent, ajoute l'étiquette du noeud actuel dans la liste des résultats
				results.extend(node.datasets)
			else:
				#De manière récursive, met à jour la recherche pour les noeuds gauches et droits afin de déterminer le dernier noeud
				#qui présente le kmer 
				self._query_recursive(node.left, kmer, results)
				self._query_recursive(node.right, kmer, results)


datasets = ["Dataset1", "Dataset2", "Dataset3", "Dataset4"]
kmers_dict = {
	"Dataset1": ["ACGT", "TGCA", "GCTA"],
	"Dataset2": ["CGTA", "GCTA", "TACC"],
	"Dataset3": ["AAGT", "TCCA", "CGGT"],
	"Dataset4": ["TGGC", "GGCA", "CCAA"]
}
#test

structure = Structure(datasets, kmers_dict, bloom_size=100, num_hashes=1)
query_kmers = ["GCTA", "TCCA", "ACGT", "GGGG"]
for kmer in query_kmers:
	result = structure.query(kmer)
	print(f"K-mer '{kmer}' found in datasets: {result}")

if __name__ == "__main__":
    import doctest
    doctest.testmod()