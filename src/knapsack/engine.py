import random


class KnapsackIndividual:

    # Structure: [Volume, Weight, Value]
    BASE_VALUES = [
        [6, 2, 5], [2, 9, 7], [1, 9, 8], [8, 7, 9], [2, 2, 2],
        [3, 2, 6], [5, 3, 2], [9, 4, 1], [8, 4, 8], [8, 7, 1],
        [6, 7, 8], [2, 3, 10], [7, 7, 9], [9, 7, 6], [7, 3, 2],
        [10, 4, 8], [2, 10, 6], [9, 2, 5], [1, 5, 2], [9, 8, 7],
        [3, 10, 8], [9, 2, 7], [9, 8, 9], [2, 6, 5], [4, 7, 6]
    ]
    PRODUCT_NAMES = "ABCDEFGHIJKLMNOPQRSTUVWXY"

    def __init__(self, genes=None):
        self.genes = genes if genes is not None else [1 if random.random() >= 0.5 else 0 for _ in range(25)]
        self.weight = 0
        self.volume = 0
        self.value = 0
        self.fitness = 0
        self.calculate_properties()

    def calculate_properties(self):
        self.volume = 0
        self.weight = 0
        self.value = 0
        for i in range(len(self.genes)):
            if self.genes[i] == 1:
                self.volume += self.BASE_VALUES[i][0]
                self.weight += self.BASE_VALUES[i][1]
                self.value += self.BASE_VALUES[i][2]
        self.fitness = self.calculate_fitness(self)

    @staticmethod
    def calculate_fitness(individual):
        fit_value = 0
        # Weight Penalty
        if individual.weight < 125:
            fit_value += (125 / (individual.weight + 1))
        else:
            fit_value += (individual.weight - 125)

        # Volume Penalty
        if individual.volume < 125:
            fit_value += (125 / (individual.volume + 1))
        else:
            fit_value += (individual.volume - 125)

        # Value maximization factor (Max Value = 147)
        fit_value += (individual.weight / 125) + (individual.volume / 125) + (147 / (individual.value + 1) * 2)
        return fit_value

    def mutate_gene(self, i):
        self.genes[i] = 1 if self.genes[i] == 0 else 0

    def __lt__(self, other):
        return self.fitness < other.fitness


class KnapsackPopulation:

    def __init__(self, size, selection_percentage, mutation_percentage, mutation_bits):
        self.size = size
        self.selection_percentage = selection_percentage
        self.mutation_percentage = mutation_percentage
        self.mutation_bits = mutation_bits
        self.individuals = [KnapsackIndividual() for _ in range(size)]

    def select_best(self):
        self.individuals.sort()
        qty_to_keep = (len(self.individuals) * self.selection_percentage // 100)

        if len(self.individuals) > 1:
            self.individuals = self.individuals[:qty_to_keep]

            if len(self.individuals) % 2 != 0:
                self.individuals.pop()

    def breed_new_generation(self):
        new_offspring = []
        random.shuffle(self.individuals)
        if len(self.individuals) > 1:
            for i in range(0, len(self.individuals), 2):
                if i + 1 < len(self.individuals):
                    new_offspring.extend(self.generate_children(self.individuals[i], self.individuals[i + 1]))

        self.individuals.extend(new_offspring)
        if self.mutation_bits > 0 and self.mutation_percentage > 0:
            self.apply_mutation()

    def generate_children(self, mother, father):
        cut1 = random.randint(1, 23)
        cut2 = random.randint(1, 23)
        if cut1 > cut2: cut1, cut2 = cut2, cut1

        genes_f1 = [0] * 25
        genes_f2 = [0] * 25

        for i in range(25):
            if cut1 < i < cut2:
                genes_f1[i] = father.genes[i]
                genes_f2[i] = mother.genes[i]
            else:
                genes_f1[i] = mother.genes[i]
                genes_f2[i] = father.genes[i]

        return [KnapsackIndividual(genes_f1), KnapsackIndividual(genes_f2)]

    def apply_mutation(self):
        qty_to_mutate = int(len(self.individuals) * (self.mutation_percentage / 100))
        for _ in range(qty_to_mutate):
            idx = random.randint(0, len(self.individuals) - 1)
            for _ in range(self.mutation_bits):
                gene_idx = random.randint(0, 24)
                self.individuals[idx].mutate_gene(gene_idx)
            self.individuals[idx].calculate_properties()

    def get_best(self):
        return min(self.individuals, key=lambda x: x.fitness)