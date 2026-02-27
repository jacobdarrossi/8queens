import random

class Individual:
    def __init__(self, genes=None):
        # In Java: genes[] = {0,1,2,3,4,5,6,7}
        # Represents [Row 0 Column, Row 1 Column, ..., Row 7 Column]
        self.genes = genes if genes is not None else [0, 1, 2, 3, 4, 5, 6, 7]
        if genes is None:
            self.shuffle_genes()
        
        self.fitness = self.calculate_fitness(self.genes)

    def shuffle_genes(self):
        """Equivalent to your 'embaralhar' method."""
        random.shuffle(self.genes)

    @staticmethod
    def calculate_fitness(genes):
        """
        Equivalent to 'calculaFitness'. 
        Counts diagonal collisions. Lower is better (0 = Solution).
        """
        collision_count = 0
        n = len(genes)
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                
                # The 'abs' logic replaces your 4 'while' loops from Java
                # If distance between rows == distance between columns, it's a diagonal collision
                if abs(i - j) == abs(genes[i] - genes[j]):
                    collision_count += 1
                    
        return collision_count

    def __lt__(self, other):
        """Used for sorting (Collections.sort in Java)."""
        return self.fitness < other.fitness

class Population:
    def __init__(self, size, selection_percentage):
        self.size = size
        self.selection_percentage = selection_percentage
        self.individuals = []
        self.generate_initial_population()

    def generate_initial_population(self):
        """Equivalent to 'geraPopulacao'."""
        for _ in range(self.size):
            self.individuals.append(Individual())

    def select_best(self):
        """Equivalent to 'selecionaMelhores'."""
        self.individuals.sort() # Sorts by fitness (ascending)
        
        # Calculate how many to keep based on percentage
        keep_count = int(len(self.individuals) * (self.selection_percentage / 100))
        
        # Ensure we have at least 2 for breeding and it's an even number
        if keep_count < 2: keep_count = 2
        if keep_count % 2 != 0: keep_count += 1
        
        self.individuals = self.individuals[:keep_count]

    def breed_new_generation(self):
        """Equivalent to 'novaGeracao'."""
        new_offspring = []
        random.shuffle(self.individuals)
        
        # Breeding in pairs
        for i in range(0, len(self.individuals), 2):
            if i + 1 < len(self.individuals):
                parent_a = self.individuals[i]
                parent_b = self.individuals[i+1]
                new_offspring.extend(self.crossover(parent_a, parent_b))
        
        self.individuals.extend(new_offspring)

    def crossover(self, mother, father):
        """
        Equivalent to 'gerarFilhos'.
        Implements your custom logic to avoid duplicate columns.
        """
        cut = random.randint(1, 6)
        
        def create_child(p1, p2):
            # Take a slice from parent 1
            child_genes = p1.genes[:cut]
            # Fill the rest with parent 2 genes if they aren't already present
            for gene in p2.genes:
                if gene not in child_genes:
                    child_genes.append(gene)
            return Individual(genes=child_genes)

        child1 = create_child(mother, father)
        child2 = create_child(father, mother)
        
        return [child1, child2]

    def get_best(self):
        """Returns the individual with the lowest fitness."""
        return min(self.individuals, key=lambda x: x.fitness)