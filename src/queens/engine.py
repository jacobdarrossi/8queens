import random


class Individual:
    def __init__(self, genes=None):
        # Representa [Linha 0 Coluna, Linha 1 Coluna, ..., Linha 7 Coluna]
        self.genes = genes if genes is not None else [0, 1, 2, 3, 4, 5, 6, 7]
        if genes is None:
            self.shuffle_genes()

        self.fitness = self.calculate_fitness(self.genes)

    def shuffle_genes(self):
        random.shuffle(self.genes)

    @staticmethod
    def calculate_fitness(genes):
        """Calcula colisões nas diagonais. 0 é a solução perfeita."""
        collision_count = 0
        n = len(genes)
        for i in range(n):
            for j in range(n):
                if i == j: continue
                if abs(i - j) == abs(genes[i] - genes[j]):
                    collision_count += 1
        return collision_count

    def mutate(self):
        """Troca a posição de dois genes para manter a restrição de colunas únicas."""
        idx1, idx2 = random.sample(range(len(self.genes)), 2)
        self.genes[idx1], self.genes[idx2] = self.genes[idx2], self.genes[idx1]
        self.fitness = self.calculate_fitness(self.genes)

    def __lt__(self, other):
        return self.fitness < other.fitness


class Population:
    def __init__(self, size, selection_percentage):
        self.size = size
        self.selection_percentage = selection_percentage
        self.individuals = []
        self.generate_initial_population()

    def generate_initial_population(self):
        for _ in range(self.size):
            self.individuals.append(Individual())

    def select_best(self):
        self.individuals.sort()
        keep_count = int(len(self.individuals) * (self.selection_percentage / 100))
        if keep_count < 2: keep_count = 2
        if keep_count % 2 != 0: keep_count += 1
        self.individuals = self.individuals[:keep_count]

    def breed_new_generation(self, mutation_rate):
        """Cria nova geração aplicando crossover e a taxa de mutação do slider."""
        new_offspring = []

        # Enquanto não recompletarmos a população original
        while len(self.individuals) + len(new_offspring) < self.size:
            parent_a, parent_b = random.sample(self.individuals, 2)
            children = self.crossover(parent_a, parent_b)

            for child in children:
                # Aplica mutação baseada na probabilidade (0.0 a 1.0)
                if random.random() < (mutation_rate / 100):
                    child.mutate()
                new_offspring.append(child)

        self.individuals.extend(new_offspring)
        # Garante que a população não cresça infinitamente
        self.individuals = self.individuals[:self.size]

    def crossover(self, mother, father):
        cut = random.randint(1, 6)

        def create_child(p1, p2):
            child_genes = p1.genes[:cut]
            for gene in p2.genes:
                if gene not in child_genes:
                    child_genes.append(gene)
            return Individual(genes=child_genes)

        return [create_child(mother, father), create_child(father, mother)]

    def get_best(self):
        return min(self.individuals, key=lambda x: x.fitness)