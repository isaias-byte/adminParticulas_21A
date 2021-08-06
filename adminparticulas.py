from types import ClassMethodDescriptorType
from .particula import Particula
import json
from pprint import pformat
from collections import deque
from queue import Empty, PriorityQueue

class AdminParticulas:
    def __init__(self):
        self.__particulas = []
        self.__grafo = dict()
        self.__vertice = dict() #usamos un vértice auxiliar para el algoritmo de Kruskal
        self.__rango = dict() #usamos un rango para las uniones en el algoritmo de Kruskal

    def grafo_aux_dijkstra_camino(self, grafo:dict):
        for arista, tupl in self.__grafo.items():
            origen = arista
            ponderacion = ""
            #print(arista)

            arista_o_d = ponderacion

            if origen in grafo:
                grafo[origen].append(arista_o_d)
            else:
                grafo[origen] = arista_o_d

    def grafo_aux_dijkstra_distancia(self, grafo:dict):
        for arista, tupl in self.__grafo.items():
            origen = arista
            ponderacion = 10000
            #print(arista)

            arista_o_d = ponderacion

            if origen in grafo:
                grafo[origen].append(arista_o_d)
            else:
                grafo[origen] = arista_o_d


    def algoritmo_dijkstra(self, origen):
        try:
            arreglo_distancias = dict() #Se contruye un arreglo de distancias
            self.grafo_aux_dijkstra_distancia(arreglo_distancias) #Se agrega inf a todas las posiciones
            arreglo_distancias[origen] = 0 #Se agrega el valor de 0 al nodo origen
            #print(pformat(arreglo_distancias))
            arreglo_camino = dict() #Se cre aun arreglo para guardar el camino 
            self.grafo_aux_dijkstra_camino(arreglo_camino) #Se llenan las posiciones con valores vacíos
            #print(pformat(arreglo_caminos))
            lista = PriorityQueue()
            lista.put((0, origen))

            while not lista.empty(): #Mientras la cola de Prioridad no esté vacía
                nodo = lista.get() #Extraemos el nodo
                #print(nodo)
                for des, dist in self.__grafo[nodo[1]]: #Por cada arista del nodo que sacamos
                    #colaPrioridad.put((dist, (nodo, des)))
                    #print(des)
                    nueva_distancia = dist + nodo[0] #Sacamos la nueva distancia
                    if nueva_distancia < arreglo_distancias[des]: #Si la nueva distancia es menor que la distancia del arreglo
                        arreglo_distancias[des] = nueva_distancia #Se coloca la nuea distancia en el arreglo de distancias
                        arreglo_camino[des] = nodo[1] #En el arreglo de caminos se agrega la posicion del nodo destino la conexión del padre del nodo
                        lista.put((nueva_distancia, des)) #Se agrega a la cola de Prioridad el nodo destino con la nueva distancia
            print("Arreglo de distancias:")
            print(pformat(arreglo_distancias))
            print("Arreglo de caminos:")
            print(pformat(arreglo_camino))
            return arreglo_camino
        except:
            return 0



    def union(self, origen, destino, lista:PriorityQueue):
        orige = self.find_set(origen)
        destin = self.find_set(destino)
        
        if orige != destin:
            if self.__rango[orige] > self.__rango[destin]:
                self.__vertice[destin] = orige
            else:
                self.__vertice[orige] = destin
            if self.__rango[orige] == self.__rango[destin]:
                self.__rango[destin] += 1

    def make_set(self, arista):
        self.__vertice[arista] = arista
        self.__rango[arista] = 0

    def find_set(self, arista):
        if self.__vertice[arista] != arista:
            self.__vertice[arista] = self.find_set(self.__vertice[arista])
        return self.__vertice[arista]

    def algoritmo_kruskal(self):
        grafoResultante = dict() #Se define  el grafo resultante
        lista = PriorityQueue()
        self.__vertice.clear()
        
        for particula in self.__particulas: #se agrega a la lista las particulas
            origen = (particula.origen_x, particula.origen_y)
            destino = (particula.destino_x, particula.destino_y)
            ponderacion = particula.velocidad * -1
            lista.put((ponderacion, (origen, destino)))
        
        for arista, tupl in self.__grafo.items(): #Make_Set a todos los nodos del grafo
            self.make_set(arista)
        
        #print(self.__vertice)

        while not lista.empty():
            arista = lista.get() #Sacamos el mayor valor de la lista 
            velocidad = arista[0] 
            tuplaAux = arista[1]
            origen = tuplaAux[0]
            destino = tuplaAux[1]
            origenAux = self.find_set(origen)
            destinoAux = self.find_set(destino)
            if origenAux != destinoAux: #Si el find_set de origen es distinto del find_set de destino
                arista_o_d = (destino, velocidad) #Agregamos la arista al grafo resultante
                arista_d_o = (origen, velocidad)

                if origen in grafoResultante:
                    grafoResultante[origen].append(arista_o_d)
                else:
                    grafoResultante[origen] = [arista_o_d]
                if destino in grafoResultante:
                    grafoResultante[destino].append(arista_d_o)
                else:
                    grafoResultante[destino] = [arista_d_o]
                
                self.union(origen, destino, lista) #Hacemos una unión en donde se encunetren los conjuntos
                                                    #de origen y destino

            #print(origenAux)
            print("Arista:", arista)
            #print(lista)
            print(self.__vertice)
        
        #print(pformat(grafoResultante, width=40, indent=1))
        return grafoResultante

    def algoritmo_prim(self, origen:tuple):
        try:
            visitados = [] #lista de visitados
            colaPrioridad = PriorityQueue() #se define la cola de prioridad
            grafoResultante = dict() #se define el grafo resultante

            visitados.append(origen) #se agrega nodo inicial a la lista

            for des, dist in self.__grafo[origen]: #se agregan adyacentes del nodo origen a la cola de Prioridad
                colaPrioridad.put((dist, (origen, des)))
                
            
            while not colaPrioridad.empty():
                arista = colaPrioridad.get()
                distancia = arista[0]
                tuplaAux = arista[1]
                origenAux = tuplaAux[0]
                destino = tuplaAux[1]
                #print(destino)

                if destino not in visitados:
                    visitados.append(destino) #agregamos nodo destino a la lista de visitados
                    for des, dist in self.__grafo[destino]: #agregamos adyacentes de destino 
                        if des not in visitados:           #que no han sido visitados a cola prioridad
                            colaPrioridad.put((dist, (destino, des)))
                    #agregamos la arista(distancia, (origen,destino)) al grafo resultante
                    
                    #arista_o_d = (distancia, (destino, origenAux))
                    #arista_d_o = (distancia, (origenAux, destino))
                    arista_o_d = (destino, distancia)
                    arista_d_o = (origenAux, distancia)

                    if origenAux in grafoResultante:
                        grafoResultante[origenAux].append(arista_o_d)
                    else:
                        grafoResultante[origenAux] = [arista_o_d]
                    if destino in grafoResultante:
                        grafoResultante[destino].append(arista_d_o)
                    else:
                        grafoResultante[destino] = [arista_d_o]
                    
            print(pformat(grafoResultante, width=40, indent=1))
            
            return grafoResultante
        except:
            return 0

    def recorrido_profundidad(self, origen:tuple):
        try:
            visitados = []
            pila = deque()
            recorrido = []

            visitados.append(origen)
            pila.append(origen)

            while pila:
                vertice = pila[-1]
                #print(vertice)
                recorrido.append(vertice)
                pila.pop()
                

                #adyacentes = self.__grafo[vertice]
                for ady, tupl in self.__grafo[vertice]:
                    if ady not in visitados:
                        visitados.append(ady)
                        pila.append(ady)
                        #print(ady)

            #return recorrido
            return "".join(
                str(vertice) + '\n' for vertice in recorrido 
            )
        except:
            return 0
        
    def recorrido_amplitud(self, origen:tuple):
        try:
            visitados = []
            cola = deque()
            recorrido = []

            visitados.append(origen)
            cola.append(origen)

            while cola:
                vertice = cola[0]
                #print(vertice)
                recorrido.append(vertice)
                cola.popleft()

                #adyacentes = self.__grafo[vertice]
                for ady, tupl in self.__grafo[vertice]:
                    if ady not in visitados:
                        visitados.append(ady)
                        cola.append(ady)
                        #print(ady)

            #return recorrido
            return "".join(
                str(vertice) + '\n' for vertice in recorrido 
            )
        except:
            return 0

    def imprimir_grafo(self):
        self.__grafo.clear()
        for particula in self.__particulas:
            origen = (particula.origen_x, particula.origen_y)
            destino = (particula.destino_x, particula.destino_y)
            ponderacion = int(particula.distancia)

            arista_o_d = (destino, ponderacion)
            arista_d_o = (origen, ponderacion)

            if origen in self.__grafo:
                self.__grafo[origen].append(arista_o_d)
            else:
                self.__grafo[origen] = [arista_o_d]
            if destino in self.__grafo:
                self.__grafo[destino].append(arista_d_o)
            else:
                self.__grafo[destino] = [arista_d_o]
        
        #cad = '\n' + "Representación de lista de adyacencia:" + '\n'
        cad = pformat(self.__grafo, width=40, indent=1)
        #print(cad)
        return cad
        
        #return pprint.pformat(self.__grafo, width=40, indent=1)

    def agregar_final(self, particula: Particula):
        self.__particulas.append(particula)
    
    def agregar_inicio(self, particula: Particula):
        self.__particulas.insert(0, particula)

    def mostrar(self):
        for particula in self.__particulas:
            print(particula)
    
    def ordenar_particulas_id(self):
        self.__particulas.sort()

    def ordenar_particulas_distancia(self):
        self.__particulas.sort(key=lambda particula: particula.distancia, reverse=True)

    def ordenar_particulas_velocidad(self):
        self.__particulas.sort(key=lambda particula: particula.velocidad, reverse=False)

    def __str__(self):
        return "".join(
            str(particula) + '\n' for particula in self.__particulas
        )

    def __len__(self):
        return len(self.__particulas)

    def __iter__(self):
        self.cont = 0

        return self

    def __next__(self):
        if self.cont < len(self.__particulas):
            particula = self.__particulas[self.cont]
            self.cont += 1

            return particula
        else:
            raise StopIteration

    def guardarParticulas(self, ubicacion):
        try:
            with open(ubicacion, "w") as archivo:
                lista = [particula.to_dict() for particula in self.__particulas]
                #print(lista)
                json.dump(lista, archivo, indent=5)
            return 1
        except:
            return 0

    def abrir(self, ubicacion):
        try:
            with open(ubicacion, "r") as archivo:
                lista = json.load(archivo)
                self.__particulas = [Particula(**particula) for particula in lista]
            return 1
        except:
            return 0