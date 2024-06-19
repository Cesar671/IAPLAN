from Action import Action
import Predicate
from enum import Enum
from Types import Ubicacion


class AbstractAction:

    def __init__(self, name, params={}, preconds=[], add=[], delete=[], duration=1, cost=0, interpretation=[]):
        self.name = name
        self.params = params
        self.preconds = preconds
        self.add = add
        self.delete = delete
        self.duration = duration
        self.cost = cost
        self.interpretation = interpretation

    def possible_actions(self, state):
        i = 0
        options = []
        empty = False
        while i < len(self.preconds) and not empty:
            precond = self.preconds[i]
            predicates = self.__predicates_that_match(precond, state)

            if i == 0:  # primera vez que llena las opciones
                options = predicates
            else:
                options = self.__merge(options, predicates, state)
            empty = not options
            i += 1
        return self.__format_result(options)

    def __format_result(self, options):
        result = []
        for option in options:
            variables = option["variable_values"]
            # Checking to have only one predicate oftype "En"
            add = [self.__translate_variables(variables, x) for x in self.add]
            delete = [self.__translate_variables(variables, x) for x in self.delete]
            for predicate in add:
                if predicate[0] == "En":
                    for u in Ubicacion:
                        if u != predicate[2]:
                            new_predicate = (predicate[0], predicate[1], u)
                            if new_predicate not in delete:
                                delete.append(new_predicate)
            # Creating the interpretation
            new_interpretation = []
            for string in self.interpretation:
                if string in variables.keys():
                    var = variables[string]
                    new_interpretation.append(var.value if isinstance(var, Enum) else var)
                else:
                    new_interpretation.append(string)
            result.append(
                Action(
                    self.name,
                    params=[variables[x] for x in self.params.keys()],
                    preconds=[self.__translate_variables(variables, x) for x in self.preconds],
                    add=add,
                    delete=delete,
                    duration=variables[self.duration] if self.duration in variables else self.duration,
                    cost=variables[self.cost] if self.cost in variables else self.cost,
                    interpretation=new_interpretation
                )
            )
        return result

    @staticmethod
    def create_presistent_action(predicate):
        delete = []
        if predicate[0] == "En":
            for u in Ubicacion:
                if u != predicate[2]:
                    new_predicate = (predicate[0], predicate[1], u)
                    delete.append(new_predicate)
        return Action(
            "persistent_" + Predicate.parse_tuple(predicate, "_", "_"),
            params=[],
            preconds=[predicate],
            add=[predicate],
            delete=delete,
            duration=0,
            cost=0,
            persistent=True
        )

    def __translate_variables(self, variables, predicate):
        translated = []
        for elem in predicate:
            if elem in variables:
                translated.append(variables[elem])
            else:
                translated.append(elem)
        return tuple(translated)

    def __predicates_that_match(self, precond, state):
        predicates = []
        name = precond[0]
        if name in state.predicates:
            for predicate in state.predicates[name].keys():
                if len(precond) == len(predicate):
                    result = self.__get_match(precond, predicate)
                    if not result is None:
                        predicates.append(result)
        return predicates

    def __get_match(self, precond, predicate):
        result = {"predicate": [predicate], "variable_values": {}}
        i = 1  # Empieza en 1 por que el 0 es el nombre
        match = True
        while i < len(precond) and match:
            precond_var = precond[i]
            predicate_val = predicate[i]
            if precond_var in self.params:
                match = self.params[precond_var] == type(predicate_val)
                if match:
                    result["variable_values"][precond_var] = predicate_val
            else:
                result["variable_values"][precond_var] = predicate_val
            i += 1
        if not match:
            result = None
        return result

    def __merge(self, old_results, new_results, state):
        results = []
        for old_res in old_results:
            for new_res in new_results:
                if not self.__are_mutex(old_res["predicate"], new_res["predicate"][0], state):
                    candidate_result = self.__copy_result(old_res)
                    variable_values = candidate_result["variable_values"]
                    failed = False
                    for key_name in new_res["variable_values"].keys():
                        if not failed:
                            if key_name in variable_values:
                                failed = variable_values[key_name] != new_res["variable_values"][key_name]
                            else:
                                variable_values[key_name] = new_res["variable_values"][key_name]
                    if not failed:
                        candidate_result["predicate"].append(new_res["predicate"][0])
                        results.append(candidate_result)
        return results

    def __copy_result(self, old_res):
        return {"predicate": old_res["predicate"].copy(),
                "variable_values": {k: v for k, v in old_res["variable_values"].items()}}

    def __are_mutex(self, predicate_list, new_predicate, state):
        ans = False
        for predicate in predicate_list:
            if state.are_mutex(new_predicate, predicate):
                ans = True
                break
        return ans
