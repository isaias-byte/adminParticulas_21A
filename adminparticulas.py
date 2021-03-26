from particula import Particula

class AdminParticulas:
    def __init__(self):
        self.__particulas = []

    def agregar_final(self, particula: Particula):
        self.__particulas.append(particula)
    
    def agregar_inicio(self, particula: Particula):
        self.__particulas.insert(0, particula)

    def mostrar(self):
        for particula in self.__particulas:
            print(particula)

p = Particula(1, 16, 3, 57, 7, 290, 0, 0, 255)
p2 = Particula(2, 91, 40, 177, 59, 107, 255, 255, 255)
p3 = Particula(3, 60, 20, 70, 30, 107, 0, 143, 57)

adminParticulas = AdminParticulas()
adminParticulas.agregar_final(p)
adminParticulas.agregar_inicio(p2)
adminParticulas.agregar_inicio(p3)
adminParticulas.mostrar()