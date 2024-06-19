from AbstractAction import AbstractAction
import Predicate

class State:

  def __init__(self):
    self.predicates = {} # {Predicate: (Predicate)}
    self.available_actions = {} # {Action: {mutex}}

  #añade un predicado al estado actual
  def add_predicate(self, predicate):
    name = predicate[0]
    persistent_action = AbstractAction.create_presistent_action(predicate)
    if name in self.predicates:
      if not predicate in self.predicates[name]:
        self.predicates[name][predicate] = {
          "mutex": set(),
          "prev_actions": [],
          "available_actions": [persistent_action]
        }
        self.available_actions[persistent_action] = set()
    else:
      self.predicates[name] = {
        predicate: {
          "mutex": set(),
          "prev_actions": [],
          "available_actions": [persistent_action]
        }
      }
      self.available_actions[persistent_action] = set()

  #verifica si dos predicados son mutex
  def are_mutex(self, predicate1, predicate2):
    name = predicate1[0]
    mutex = self.predicates[name][predicate1]["mutex"]
    return predicate2 in mutex

  #añade una accion al estado actual
  def add_action(self, action):
    if not action in self.available_actions.keys():
      preconds = action.get_preconds()
      for precond in preconds:
        self.__add_available_action_to_predicate(precond, action)
      mutex = set()
      self.__check_mutex(action, mutex)
      self.available_actions[action] = mutex

  #verifica si una accion nueva podria hacer mutex con otras acciones
  #existentes en el estado
  def __check_mutex(self, action, mutex):
    self.__inconsistent_effects(action, mutex)
    self.__interference(action, mutex)
    self.__competing_needs(action, mutex)

  """
    Verifica que los efectos de la nueva accion no tenga conflicto con
    las acciones existentes del estado
  """
  def __inconsistent_effects(self, new_action, mutex_set):
    for saved_action in self.available_actions.keys():
      are_mutex = self.__have_a_common(saved_action.get_add(), new_action.get_delete())
      if not are_mutex:
        are_mutex = self.__have_a_common(saved_action.get_delete(), new_action.get_add())
      if are_mutex:
        self.available_actions[saved_action].add(new_action)
        mutex_set.add(saved_action)

  """
    Verifica que las los efectos de la nueva accion no interfiera con
    las precondiciones de las acciones existentes y viceversa
  """
  def __interference(self, new_action, mutex_set):
    for saved_action in self.available_actions.keys():
      are_mutex = self.__have_a_common(saved_action.get_preconds(), new_action.get_delete())
      if not are_mutex:
        are_mutex = self.__have_a_common(saved_action.get_delete(), new_action.get_preconds())
      if are_mutex:
        self.available_actions[saved_action].add(new_action)
        mutex_set.add(saved_action)

  """
    verificamos que no haya mutex entre las precondiciones de la nueva accion
    y las aaciones existentes del estado
  """
  def __competing_needs(seld, new_action, mutex_set):
    # No se usa por que no estamos considerando predicados negativos
    pass

  """
    verificamos si es que dos listas tienen algun item en comun
    'son listas de predicados'
  """
  def __have_a_common(self, list1, list2):
    have_a_common = False
    for item in list1:
      if item in list2:
        have_a_common = True
        break
    return have_a_common

  """
    genera un nuevo estado a partir de este estado
  """
  def generate_next_state(self):
    new_state = self.__next_state()
    new_state.__calculate_predicate_mutex() #calculamos que predicados son mutex
    return new_state

  """
    genera el nuevo estado
  """
  def __next_state(self):
    new_state = State()
    # copy predicates without mutex or prev_actions
    for name in self.predicates.keys():
      new_state.predicates[name] = {}
      aux = new_state.predicates[name]
      for predicate in self.predicates[name].keys():
        data = self.predicates[name][predicate]
        aux[predicate] = {"mutex": set(), "prev_actions": [], "available_actions": data["available_actions"]}
    # copy actions and update predicate prev
    for action, mutex_set in self.available_actions.items():
      new_state.available_actions[action] = mutex_set
      for predicate_to_add in action.get_add():
        new_state.add_predicate(predicate_to_add)
        new_state.__add_prev_action_to_predicate(predicate_to_add, action)
    return new_state
  """
    calcula los valores mutex de todos los predicados del estado
  """
  def __calculate_predicate_mutex(self):
    all_predicates = self.__get_all_predicates()
    length = len(all_predicates)
    for i in range(length):
      predicate1 = all_predicates[i]
      for j in range( i+1, length ):
        predicate2 = all_predicates[j]
        if self.__are_predicate_mutex(predicate1, predicate2):
          self.__set_predicate_mutex(predicate1, predicate2)

  """
    VERIFICA si ambos predicados son mutex
  """
  def __are_predicate_mutex(self, predicate1, predicate2):
    prev_actions1 = self.predicates[predicate1[0]][predicate1]["prev_actions"]
    prev_actions2 = self.predicates[predicate2[0]][predicate2]["prev_actions"]
    all_action_are_mutex = True
    for checking_action1 in prev_actions1:
      mutex_set = self.available_actions[checking_action1]
      for checking_action2 in prev_actions2:
        if not checking_action2 in mutex_set:
          if not self.__lista_have_mutex(checking_action1.get_preconds(), checking_action2.get_preconds()):
            all_action_are_mutex = False
            break
      if not all_action_are_mutex:
        break
    return all_action_are_mutex

  """
    establece los valores de mutex de ambos predicados entre ellos
  """
  def __set_predicate_mutex(self, predicate1, predicate2):
    self.predicates[predicate1[0]][predicate1]["mutex"].add(predicate2)
    self.predicates[predicate2[0]][predicate2]["mutex"].add(predicate1)

  """
    dada dos listas de predicados, verifica si alguno de los predicados
    de la lista1 tiene mutex con alguno otro de la segunda lista
  """
  def __lista_have_mutex(self, predicate_list1, predicate_list2):
    have_mutex = False
    for predicate1 in predicate_list1:
      mutex_set =  self.predicates[predicate1[0]][predicate1]["mutex"]
      for predicate2 in predicate_list2:
        if predicate2 in mutex_set:
          have_mutex = True
          break
      if have_mutex:
        break

  """
    obtenemos todos los predicados del estado en una lista
  """
  def __get_all_predicates(self):
    all_states = []
    for predicate_dict in self.predicates.values():
      converted_list = list(predicate_dict.keys())
      all_states.extend(converted_list)
    return all_states

  """
    de un predicado en su lista de acciones previas se agrega una nueva accion
  """
  def __add_prev_action_to_predicate(self, predicate, action):
    name = predicate[0]
    self.predicates[name][predicate]["prev_actions"].append(action)

  """
    los mismo que arriba pero añadimos a la lista de acciones disponibles
  """
  def __add_available_action_to_predicate(self, precond, action):
    name = precond[0]
    self.predicates[name][precond]["available_actions"].append(action)

  # se encarga de ver si el goal (lista de predicados) está en dicho estado
  def contains_goal(self, goal):
    ans = True
    for predicate in goal:
      name = predicate[0]
      ans = name in self.predicates
      if ans:
        ans = predicate in self.predicates[name].keys()
        if ans:
          mutex_set = self.predicates[name][predicate]["mutex"]
          for mutex_predicate in mutex_set:
            if mutex_predicate in goal:
              ans = False
              break
      if not ans:
        break
    return ans

  #obtiene las acciones previas de un predicado del estado
  def get_prev_actions_from(self, predicate):
    data = self.predicates[predicate[0]][predicate]
    return data["prev_actions"]


  #imprime al estado actual
  def print_state(self):
    print("PREDICADOS DEL ESTADO")
    for name in self.predicates.keys():
      for predicate in self.predicates[name].keys():
        data = self.predicates[name][predicate]
        print(Predicate.parse_tuple(predicate))
        print("\tmutex: " + ' '.join(map(Predicate.parse_tuple, data["mutex"])))
        print("\tprev_actions: " + ' '.join(map(str,data["prev_actions"])))
        print("\tavailable_actions: " + ' '.join(map(str,data["available_actions"])))
        print()
    print("\nACCIONES DE ESE ESTADO")
    for action in self.available_actions.keys():
      print(action.get_complete_action_string())
      cad = ""
      for mutex in self.available_actions[action]:
        cad += mutex.get_main_name() + ", "
      if cad:
        print("Mutex: " + cad)
      print()
    pass

  #compara cuando dos estados son iguales
  def __eq__(self, value) -> bool:
    keysSelf = self.predicates.keys()
    keysOther = value.predicates.keys()
    same = keysSelf == keysOther
    if same:
      for name in keysSelf:
        valuesSelf = self.predicates[name].keys()
        valuesOther = value.predicates[name].keys()
        same = valuesSelf == valuesOther
        if same:
          for predicate in valuesOther:
            mutexSelf = self.predicates[name][predicate]["mutex"]
            mutexOther = value.predicates[name][predicate]["mutex"]
            same = mutexSelf == mutexOther
            if not same:
              break
          if not same:
            break
        else:
          break
    return same
  
  