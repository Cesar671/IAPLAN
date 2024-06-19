import random
from pyeasyga import pyeasyga

class GASearch:
  def __init__(self, tree, optimize_money = False) -> None:
    self.tree = tree # list of set of action nodes
    self.optimize_money = optimize_money
    self.ga = pyeasyga.GeneticAlgorithm(tree, population_size = 200, generations = 100, maximise_fitness = False, elitism=False)
  
  def start_search(self):
    self.ga.create_individual = self.__create_individual
    self.ga.fitness_function = self.__fitness
    self.ga.mutate_function = self.__mutate
    self.ga.crossover_function = self.__crossover
    self.ga.run()
    return self.ga.best_individual()


  def __create_individual(self, data):
    individual = []
    for action_nodes_set in data:
      aux_element = random.choice(tuple(action_nodes_set))
      individual.append(aux_element)
    return individual

  def __fitness(self, individual, data):
    cost = 0
    first = True
    for action_node in individual:
      if self.optimize_money:
        cost += action_node.action.get_cost()
      else:
        cost += action_node.action.get_duration()
      if first:
        first = False
        children_set = action_node.children
      else:
        if not action_node in children_set:
          cost += 1000
    return cost
  
  def __crossover(self, parent1, parent2):
    mask = [random.randint(0,1) for _ in range(len(parent1))]
    child1 = []
    child2 = []
    i = 0
    for val in mask:
      if val == 0:
        child1.append(parent1[i])
        child2.append(parent2[i])
      else:
        child1.append(parent2[i])
        child2.append(parent1[i])
      i += 1
    return child1, child2

  def __mutate(self, individual):
    mutate_index1 = random.randrange(len(individual))
    action_set = self.tree[mutate_index1]
    aux_element = random.choice(tuple(action_set))
    individual[mutate_index1] = aux_element

