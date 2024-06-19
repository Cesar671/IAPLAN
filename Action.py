import Predicate

class Action:
  def __init__(self, name, params = [], preconds = [], add = [], delete = [], duration = 0, cost = 0, persistent = False, interpretation = []):
    self.name = name 
    self.params = params
    self.preconds = preconds
    self.add = add
    self.delete = delete
    self.duration = duration
    self.cost = cost
    self.persistent = persistent
    self.interpretation = interpretation
    self.cad = str(self.name) + " (" 
    self.cad += str(self.params) +")\n"
    self.cad += "\tPRECOND: " + ' '.join(map(Predicate.parse_tuple, self.preconds)) + "\n"
    self.cad += "\tEFFECT ADD: " + ' '.join(map(Predicate.parse_tuple, self.add)) + "\n"
    self.cad += "\tEFFECT DELETE: " + ' '.join(map(Predicate.parse_tuple, self.delete)) + "\n"
    self.cad += "\tDURATION: " + str(self.duration)
    self.cad += "\n\tCOST: " + str(self.cost)

    aux = str(self.name)
    aux += str(self.params)
    aux += str(self.preconds)
    aux += str(self.add)
    aux += str(self.delete)
    aux += str(self.duration)
    self.action_hash = hash(aux)
    
  def __eq__(self, other):
    return self.name == other.name and self.params == other.params and self.preconds == other.preconds and self.add == other.add and self.delete == other.delete and self.duration == other.duration and self.cost == other.cost

  def get_preconds(self):
    return self.preconds

  def get_add(self):
    return self.add

  def get_delete(self):
    return self.delete
  
  def get_cost(self):
    return self.cost

  def get_duration(self):
    return self.duration
  
  def get_main_name(self):
    name = self.name + "("
    first = True
    for param in self.params:
      if first:
        name += param.name
        first = False
      else:
        name += ", " + param.name
    name += ")"
    return name

  def get_complete_action_string(self):
    return self.cad
  
  def get_interpretation(self):
    return " ".join(str(e) for e in self.interpretation)

  def __str__(self):
    return self.get_main_name()
  
  def __hash__(self):
    return self.action_hash