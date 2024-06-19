from Planner import Planner
from Types import Persona, Taxi, Ubicacion, Recepcionista, Doctor
from AbstractAction import AbstractAction

persona = Persona.P3
ubicacion = Ubicacion.CCE

goal = [("Diagnosticado", persona)]
goal_2 = [("En", persona, ubicacion)]

init = [("En", persona, ubicacion), ("Libre", Taxi.T1), ("Libre", Taxi.T2)]

# ("Ruta, U1, U2, Tiempo, Dinero")
constants = [("Ruta", Ubicacion.CAD, Ubicacion.Pt1, 6, 14.5),
             ("Ruta", Ubicacion.Pt1, Ubicacion.CAD, 6, 14.5),

             ("Ruta", Ubicacion.CAD, Ubicacion.Pt10, 17, 27),
             ("Ruta", Ubicacion.Pt10, Ubicacion.CAD, 17, 27),

             ("Ruta", Ubicacion.Pt1, Ubicacion.Pt12, 4, 7),
             ("Ruta", Ubicacion.Pt12, Ubicacion.Pt1, 4, 7),

             ("Ruta", Ubicacion.Pt1, Ubicacion.Pt2, 2.5, 5.5),
             ("Ruta", Ubicacion.Pt2, Ubicacion.Pt1, 2.5, 5.5),

             ("Ruta", Ubicacion.Pt12, Ubicacion.Pt10, 3, 5),
             ("Ruta", Ubicacion.Pt10, Ubicacion.Pt12, 3, 5),

             ("Ruta", Ubicacion.Pt2, Ubicacion.CAL, 12, 14),
             ("Ruta", Ubicacion.CAL, Ubicacion.Pt2, 12, 14),

             ("Ruta", Ubicacion.Pt2, Ubicacion.Pt5, 1, 2.5),
             ("Ruta", Ubicacion.Pt5, Ubicacion.Pt2, 1, 2.5),

             ("Ruta", Ubicacion.Pt2, Ubicacion.Pt3, 3, 5.5),
             ("Ruta", Ubicacion.Pt3, Ubicacion.Pt2, 3, 5.5),

             ("Ruta", Ubicacion.Pt5, Ubicacion.Pt4, 3.5, 4),
             ("Ruta", Ubicacion.Pt4, Ubicacion.Pt5, 3.5, 4),

             ("Ruta", Ubicacion.Pt11, Ubicacion.Pt9, 2.5, 3),
             ("Ruta", Ubicacion.Pt9, Ubicacion.Pt11, 2.5, 3),

             ("Ruta", Ubicacion.Pt9, Ubicacion.Pt10, 4, 3),
             ("Ruta", Ubicacion.Pt10, Ubicacion.Pt9, 4, 3),

             ("Ruta", Ubicacion.Pt10, Ubicacion.Pt13, 22, 28),
             ("Ruta", Ubicacion.Pt13, Ubicacion.Pt10, 22, 28),

             ("Ruta", Ubicacion.Pt9, Ubicacion.Pt13, 24, 23),
             ("Ruta", Ubicacion.Pt13, Ubicacion.Pt9, 24, 23),

             ("Ruta", Ubicacion.Pt3, Ubicacion.Pt4, 2, 3),
             ("Ruta", Ubicacion.Pt4, Ubicacion.Pt4, 2, 3),

             ("Ruta", Ubicacion.Pt4, Ubicacion.Pt6, 4, 5),
             ("Ruta", Ubicacion.Pt6, Ubicacion.Pt4, 4, 5),

             ("Ruta", Ubicacion.Pt6, Ubicacion.Pt7, 3, 3.5),
             ("Ruta", Ubicacion.Pt7, Ubicacion.Pt6, 3, 3.5),

             ("Ruta", Ubicacion.Pt7, Ubicacion.Pt8, 2, 2),
             ("Ruta", Ubicacion.Pt8, Ubicacion.Pt7, 2, 2),

             ("Ruta", Ubicacion.Pt3, Ubicacion.HOli, 12, 15.5),
             ("Ruta", Ubicacion.HOli, Ubicacion.Pt3, 12, 15.5),

             ("Ruta", Ubicacion.Pt4, Ubicacion.HOli, 10, 14),
             ("Ruta", Ubicacion.HOli, Ubicacion.Pt4, 10, 14),

             ("Ruta", Ubicacion.Pt6, Ubicacion.Pt19, 15, 16),
             ("Ruta", Ubicacion.Pt19, Ubicacion.Pt6, 15, 16),

             ("Ruta", Ubicacion.Pt13, Ubicacion.HVied, 4, 3),
             ("Ruta", Ubicacion.HVied, Ubicacion.Pt13, 4, 3),

             ("Ruta", Ubicacion.Pt14, Ubicacion.HVied, 0.5, 1.5),
             ("Ruta", Ubicacion.HVied, Ubicacion.Pt14, 0.5, 1.5),

             ("Ruta", Ubicacion.HOli, Ubicacion.CCE, 5, 9.5),
             ("Ruta", Ubicacion.CCE, Ubicacion.HOli, 5, 9.5),

             ("Ruta", Ubicacion.Pt19, Ubicacion.Pt15, 13, 13),
             ("Ruta", Ubicacion.Pt15, Ubicacion.Pt19, 13, 13),

             ("Ruta", Ubicacion.Pt15, Ubicacion.Pt16, 1, 1),
             ("Ruta", Ubicacion.Pt16, Ubicacion.Pt15, 1, 1),

             ("Ruta", Ubicacion.Pt16, Ubicacion.Pt17, 2, 3),
             ("Ruta", Ubicacion.Pt17, Ubicacion.Pt16, 2, 3),

             ("Ruta", Ubicacion.CCE, Ubicacion.Pt20, 5, 4.5),
             ("Ruta", Ubicacion.Pt20, Ubicacion.CCE, 5, 4.5),

             ("Ruta", Ubicacion.Pt20, Ubicacion.Pt18, 25, 17),
             ("Ruta", Ubicacion.Pt18, Ubicacion.Pt20, 25, 17),

             ("Ruta", Ubicacion.Pt19, Ubicacion.Pt20, 2, 2),
             ("Ruta", Ubicacion.Pt20, Ubicacion.Pt19, 2, 2),

             ("Ruta", Ubicacion.Pt11, Ubicacion.Pt5, 4, 5),
             ("Ruta", Ubicacion.Pt5, Ubicacion.Pt11, 4, 5),

             ("Ruta", Ubicacion.Pt12, Ubicacion.Pt11, 1, 2.5),
             ("Ruta", Ubicacion.Pt11, Ubicacion.Pt12, 1, 2.5),

             ("Ruta", Ubicacion.HUni, Ubicacion.Pt9, 1, 3.5),

             ("Ruta", Ubicacion.Pt9, Ubicacion.Pt7, 2, 3),

             ("Ruta", Ubicacion.Pt8, Ubicacion.HUni, 0.25, 2),

             ("Ruta", Ubicacion.HVied, Ubicacion.HSSU, 0.5, 0.5),

             ("Ruta", Ubicacion.HSSU, Ubicacion.Pt17, 2, 3),

             ("Ruta", Ubicacion.Pt14, Ubicacion.Pt15, 3, 3),

             ("Ruta", Ubicacion.Pt16, Ubicacion.Pt14, 1, 2),

             ("Ruta", Ubicacion.Pt18, Ubicacion.Pt16, 7, 7),

            ("Trabaja", Doctor.D1, Ubicacion.HVied, 15),
            ("Trabaja", Doctor.D2, Ubicacion.HOli, 30),
            ("Trabaja", Doctor.D3, Ubicacion.HUni, 20),
            ("Trabaja", Doctor.D4, Ubicacion.HSSU, 25),
            ("Trabaja", Recepcionista.R1, Ubicacion.HVied, 30, 50),
            ("Trabaja", Recepcionista.R2, Ubicacion.HOli, 10, 80),
            ("Trabaja", Recepcionista.R3, Ubicacion.HUni, 10, 70),
            ("Trabaja", Recepcionista.R4, Ubicacion.HSSU, 90, 0)]

actions = []

actions.append(
    AbstractAction(
        "PedirTaxi",
        params={"p": Persona, "t": Taxi, "u": Ubicacion},
        preconds=[("En", "p", "u"), ("Libre", "t")],
        add=[("En", "t", "u"), ("Pasajero", "p", "t")],
        delete=[("En", "p", "u"), ("Libre", "t")],
        duration=5,
        interpretation=["p", "está pidiendo un taxi", "a la ubicación", "u"]
    )
)

actions.append(
    AbstractAction(
        "BajarTaxi",
        params={"p": Persona, "t": Taxi, "u": Ubicacion},
        preconds=[("En", "t", "u"), ("Pasajero", "p", "t")],
        add=[("En", "p", "u"), ("Libre", "t")],
        delete=[("En", "t", "u"), ("Pasajero", "p", "t")],
        duration=1,
        interpretation=["p", "está bajando del taxi", "t", "en la ubicación", "u"]
    )
)

actions.append(
  AbstractAction(
    "PedirConsulta",
    params = {"p": Persona, "r": Recepcionista, "u": Ubicacion},
    preconds = [("En", "p", "u"), ("Trabaja", "r", "u", "d", "c")],
    add = [("Ficha", "r", "p")],
    delete = [],
    duration = "d",
    cost = "c",
    interpretation = ["La persona", "p", "está sacando una ficha de consulta a la recepcionista", "r", ", quien trabaja en", "u"]
  )
)

actions.append(
  AbstractAction(
    "Atender",
    params = {"d": Doctor, "p": Persona, "u": Ubicacion},
    preconds = [("En", "p", "u"), ("Trabaja", "d", "u", "d1"), ("Trabaja", "r", "u", "d2", "c"), ("Ficha", "r", "p")],
    add = [("Diagnosticado", "p")],
    delete = [("Ficha", "r", "p")],
    duration = "d1",
    interpretation = ["El doctor", "d", "está atendiendo a la persona", "p", "en", "u"]
  )
)

actions.append(
  AbstractAction(
    "Conducir",
    params = {"t": Taxi, "p": Persona, "u1": Ubicacion, "u2": Ubicacion},
    preconds = [("En", "t", "u1"), ("Pasajero", "p", "t"), ("Ruta", "u1", "u2", "d", "c")],
    add = [("En", "t", "u2")],
    delete = [("En", "t", "u1")],
    duration = "d",
    cost = "c",
    interpretation = ["El taxista", "t", "está llevando a la persona", "p", "de", "u1", "a", "u2"]
  )
)

planner = Planner(init, goal, actions, constants)
planner.start_plann()
new_init = planner.get_last_state_predicates()
planner_2 = Planner(new_init, goal_2, actions, constants, optimize_money=True)
planner_2.total_cost = planner.total_cost
planner_2.total_time = planner.total_time
planner_2.start_plann()

