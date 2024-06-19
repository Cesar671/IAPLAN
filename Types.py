from enum import Enum

class Persona(Enum):
  P1 = "Adrian Crespo"
  P2 = "Alejandro"

class Recepcionista(Enum):
  R1 = "Carmen Rosales"
  R2 = "Pamela lolas"
  R3 = "Adriana loza"

class Doctor(Enum):
  D1 = "Doctor Chochoa"
  D2 = "Doctor Muerte"
  D3 = "Doctor Strange"

# puntos del grafo
class Ubicacion(Enum):
  U1 = 1
  U2 = 2
  U3 = 3
  U4 = 4
  U5 = 5
  C1 = "Hogar Dulce Hogar"
  C2 = 7
  H1 = "Hospital Vietma"
  H2 = "Clinica los Olivos"
  H3 = "Hospital Univalle"

class Taxi(Enum):
  T1 = "Josias"
  T2 = 2
