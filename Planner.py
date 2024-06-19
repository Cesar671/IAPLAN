from State import State
from GeneticALgorithm import GASearch
from AbstractAction import AbstractAction
import Predicate


class Planner:

    # optimize_money: true entonces prioriza gastar menos
    # Si el optimize_money está en false prioriza el tiempo
    # Si esta en True entonces prioriza el dinero
    def __init__(self, initState, goal, actions, rules, optimize_money=False) -> None:
        self.initState = initState
        self.goal = goal
        self.actions = actions
        self.optimize_money = optimize_money
        self.rules = rules
        self.total_time = 0
        self.total_cost = 0
        self.action_sequence = []

    """
    Inicia el plan con un estado inicial
  """

    def start_plann(self):
        graphplan, last_state = self.create_plan()
        if last_state.contains_goal(self.goal):
            ############################################
            ####      creando el arbol
            ##########################################
            tree = self.create_tree(graphplan)
            self.clean_tree(tree)
            self.update_values_with_dijstrak(tree)
            self.print_tree_result(tree)
        else:
            print("No existe un plan que permita llegar al objetivo")

    def create_plan(self):
        graphplan = []  # lista de State
        current_state = State()

        for predicate in self.initState:
            current_state.add_predicate(predicate)
        for predicate in self.rules:
            current_state.add_predicate(predicate)
        ####      creacion del graphplan
        # i = 0 #! borrar
        finished = False
        prev_state = None
        while not finished:
            for action in self.actions:
                available_actions = action.possible_actions(current_state)
                for available_action in available_actions:
                    current_state.add_action(available_action)
            graphplan.append(current_state)
            # print ("Estado " + str(i)) #! borrar
            # current_state.print_state() #! borrar
            # i += 1 #! borrar
            # input() #! borrar
            prev_state = current_state
            current_state = current_state.generate_next_state()
            finished = prev_state == current_state
        return graphplan, prev_state

    #### Limpieza del arbol?
    def clean_tree(self, tree):
        first = True
        must_have_actions = None
        for action_set in reversed(tree):
            if first:
                first = False
                must_have_actions = action_set
            else:
                to_remove = []
                for action_node in action_set:
                    new_children_set = set()
                    for children in action_node.children:
                        if children in must_have_actions:
                            new_children_set.add(children)
                    if new_children_set:  # not empty
                        action_node.children = new_children_set
                    else:
                        to_remove.append(action_node)
                for action_node in to_remove:
                    action_set.remove(action_node)
                must_have_actions = action_set

    #  seleccionando el mejor secuencia de acciones con la idea de dijstrak
    #####

    def get_heuristic(self, tree):
        if self.optimize_money:

        else:

    #####

    def update_values_with_dijstrak(self, tree):
        first = True
        child_visited = {}
        current_nodes = {}
        for action_set in tree:
            for action_node in action_set:

                action_cost = action_node.action.get_cost()
                action_time = action_node.action.get_duration()
                if first:
                    action_node.best_weight = action_cost
                    action_node.best_time = action_time
                else:
                    if action_node in current_nodes:
                        action_node.best_parent = current_nodes[action_node][0]
                        action_node.best_weight = current_nodes[action_node][1] + action_cost
                        action_node.best_time = current_nodes[action_node][2] + action_time
                    else:
                        print("error?")
                total_cost = action_node.best_weight
                total_time = action_node.best_time
                for action_child in action_node.children:
                    if action_child in child_visited:
                        old_cost = child_visited[action_child][1]
                        old_time = child_visited[action_child][2]
                        if self.optimize_money:
                            if total_cost < old_cost:
                                child_visited[action_child] = (action_node, total_cost, total_time)
                            elif total_cost == old_cost:
                                if total_time < old_time:
                                    child_visited[action_child] = (action_node, total_cost, total_time)
                        else:
                            if total_time < old_time:
                                child_visited[action_child] = (action_node, total_cost, total_time)
                            elif total_time == old_time:
                                if total_cost < old_cost:
                                    child_visited[action_child] = (action_node, total_cost, total_time)
                    else:
                        child_visited[action_child] = (action_node, total_cost, total_time)
            first = False
            current_nodes = child_visited
            child_visited = {}

    def get_costs(self):
        return self.total_cost, self.total_time

    def print_tree_result(self, tree):
        best_action = self.get_best_cost_from_tree(tree)
        self.action_sequence = []
        while not best_action is None:
            if not best_action.action.persistent:
              self.total_cost += best_action.action.get_cost()
              self.total_time += best_action.action.get_duration()
              self.action_sequence.append(best_action.action)
              print(f"{self.total_cost}$ {self.total_time}min {best_action.action.get_interpretation()}")
            best_action = best_action.best_parent

    def get_best_cost_from_tree(self, tree):
        best_action = None
        for action_node in tree[-1]:
            if best_action is None:
                best_action = action_node
            else:
                prev_cost = best_action.best_weight
                prev_time = best_action.best_time
                current_cost = action_node.best_weight
                current_time = action_node.best_time
                if self.optimize_money:
                    if current_cost < prev_cost:
                        best_action = action_node
                    elif current_cost == prev_cost:
                        if current_time < prev_time:
                            best_action = action_node
                else:
                    if current_time < prev_time:
                        best_action = action_node
                    elif current_time == prev_time:
                        if current_cost < prev_cost:
                            best_action = action_node
        return best_action

    # desde aca no hemos tocado nada
    def get_last_state_predicates(self):
        state = set()
        for predicate in self.initState:
            state.add(predicate)
        for action in self.action_sequence:
            to_add = action.get_add()
            for predicate_add in to_add:
                state.add(predicate_add)
            to_delete = action.get_delete()
            for predicate_delete in to_delete:
                if predicate_delete in state:
                    state.remove(predicate_delete)
        return state

    ############################################################################
    ########       Metodos para la Creacion del arbol de acciones posibles
    ############################################################################

    def create_tree(self, graphplan):
        current_state = set()
        for predicate in self.goal:
            current_state.add(predicate)
        current_nodes = {ActionNode(None, current_state)}
        tree = []
        first = True
        for complete_state in reversed(graphplan):
            next_nodes = set()
            nodes_for_tree = []
            for node in current_nodes:
                generated_state = set()
                for state in node.generated_state:
                    generated_state.add(state)
                if complete_state.contains_goal(generated_state):
                    prev_actions = self.__retrieve_actions(generated_state, complete_state)
                    for prev_action in prev_actions:
                        new_node = self.__generate_new_node(generated_state, prev_action)
                        if not new_node.failed:
                            node.add_child(new_node)
                            next_nodes.add(new_node)
                    nodes_for_tree.append(node)
                else:
                    node.failed = True
            if first:
                first = False
            else:
                if nodes_for_tree:
                    tree.append(nodes_for_tree)
            current_nodes = next_nodes
        return tree

    def __retrieve_actions(self, generated_state, complete_state):
        available_actions = set()
        for predicate in generated_state:
            for action in complete_state.get_prev_actions_from(predicate):
                available_actions.add(action)
        return available_actions

    def __generate_new_node(self, generated_state, prev_action):
        predicates_to_delete = prev_action.get_delete()
        failed = False
        for predicate in predicates_to_delete:
            if predicate in generated_state:
                failed = True
                break
        if failed:
            return ActionNode(prev_action, generated_state, failed)
        else:
            copied_state = set()
            for predicate in generated_state:
                copied_state.add(predicate)
            if not prev_action.persistent:
                predicates_to_add = prev_action.get_add()
                for predicate in predicates_to_add:
                    if predicate in copied_state:
                        copied_state.remove(predicate)
            predicate_preconds = prev_action.get_preconds()
            for predicate in predicate_preconds:
                if not predicate in self.rules:
                    copied_state.add(predicate)
            return ActionNode(prev_action, copied_state)


#######################################################################
#########       Clase Auxiliar
#######################################################################

class ActionNode:
    def __init__(self, action, generated_state, failed=False) -> None:
        self.best_parent = None
        self.best_weight = None
        self.action = action
        self.generated_state = generated_state
        self.children = set()
        self.failed = failed

    def add_child(self, node):
        self.children.add(node)

    def __eq__(self, value) -> bool:
        return self.action == value.action and self.generated_state == value.generated_state

    def __hash__(self) -> int:
        aux = str(self.action) + str(self.generated_state)
        return hash(aux)
