from Planner import Planner
from Types import Persona, Taxi, Ubicacion, Recepcionista, Doctor
from AbstractAction import AbstractAction

goal = [("Diagnosticado", Persona.P1)]

init = [("En", Persona.P1, Ubicacion.C1),
        ("Libre", Taxi.T1)]

constants = [("Ruta", Ubicacion.C1, Ubicacion.U1, 5),
             ("Ruta", Ubicacion.C1, Ubicacion.U2, 4),
             ("Ruta", Ubicacion.U1, Ubicacion.H1, 3),
             ("Ruta", Ubicacion.U2, Ubicacion.H1, 6),
             ("Ruta", Ubicacion.U1, Ubicacion.C1, 7),
             ("Ruta", Ubicacion.U2, Ubicacion.C1, 8),
             ("Ruta", Ubicacion.H1, Ubicacion.U1, 6),
             ("Ruta", Ubicacion.H1, Ubicacion.U2, 5),
             ("Trabaja", Doctor.D1, Ubicacion.H1),
             ("Trabaja", Doctor.D2, Ubicacion.H2),
             ("Trabaja", Doctor.D3, Ubicacion.H3),
             ("Trabaja", Recepcionista.R1, Ubicacion.H1),
             ("Trabaja", Recepcionista.R2, Ubicacion.H2),
             ("Trabaja", Recepcionista.R3, Ubicacion.H3)]

actions = []

actions.append(
    AbstractAction(
        "PedirTaxi",
        params={"p": Persona, "t": Taxi, "u": Ubicacion},
        preconds=[("En", "p", "u"), ("Libre", "t")],
        add=[("En", "t", "u"), ("Pasajero", "p", "t")],
        delete=[("En", "p", "u"), ("Libre", "t")],
        duration=5,
        interpretation=["La persona", "p", "está pidiendo un taxi", "t", "a la ubicación", "u"]
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
        interpretation=["La persona", "p", "está bajando del taxi", "t", "en la ubicación", "u"]
    )
)

actions.append(
    AbstractAction(
        "PedirConsulta",
        params={"p": Persona, "r": Recepcionista, "u": Ubicacion},
        preconds=[("En", "p", "u"), ("Trabaja", "r", "u")],
        add=[("Ficha", "r", "p")],
        delete=[],
        duration=5,
        interpretation=["La persona", "p", "está sacando una ficha de consulta a la recepcionista", "r",
                        ", quien trabaja en", "u"]
    )
)

actions.append(
    AbstractAction(
        "Atender",
        params={"d": Doctor, "p": Persona, "u": Ubicacion},
        preconds=[("En", "p", "u"), ("Trabaja", "d", "u"), ("Trabaja", "r", "u"), ("Ficha", "r", "p")],
        add=[("Diagnosticado", "p")],
        delete=[("Ficha", "r", "p")],
        duration=20,
        interpretation=["El doctor", "d", "está atendiendo a la persona", "p", "en", "u"]
    )
)

actions.append(
    AbstractAction(
        "Conducir",
        params={"t": Taxi, "p": Persona, "u1": Ubicacion, "u2": Ubicacion},
        preconds=[("En", "t", "u1"), ("Pasajero", "p", "t"), ("Ruta", "u1", "u2", "d")],
        add=[("En", "t", "u2")],
        delete=[("En", "t", "u1")],
        duration="d",
        interpretation=["El taxista", "t", "está llevando a la persona", "p", "de", "u1", "a", "u2"]
    )
)

planner = Planner(init, goal, actions, constants)
planner.start_plann()
new_init = planner.get_last_state_predicates()
new_goal = [("En", Persona.P1, Ubicacion.C1)]
planner = Planner(new_init, new_goal, actions, constants, optimize_money=True)
planner.start_plann()
