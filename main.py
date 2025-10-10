from collections import deque

def solicitar_dato(mensaje, tipo_dato, validacion=None):
    while True:
        try:
            dato = tipo_dato(input(mensaje))

            if validacion is None or validacion(dato):
                return dato
            
            else:
                print("El valor ingresado no cumple la condición.")

        except ValueError:
            print("Entrada inválida.")

class Mapa:
    def __init__(self, ancho, alto, lista_obstaculos):
        self.ancho = ancho
        self.alto = alto
        self.mapa = [[0 for _ in range(ancho)] for _ in range(alto)]
        self.posicion_obstaculo = {}
        self.lista_obstaculos = lista_obstaculos # Tipos de obstaculos

    def mostrar_mapa_normal(self):
        valor_emoji = {
            0: "⬜",   # camino libre
            1: "🏢",   # edificio
            2: "💧",   # agua
            3: "⛔",   # zona bloqueada
            8: "🚩",   # inicio
            9: "🏁"    # fin
        }

        for fila in self.mapa:
            print("".join(valor_emoji[celda] for celda in fila))
    
    def mostrar_mapa_camino(self, camino_normal, camino_imprevistos):
        valor_camino = 5 
        valor_camino_imprevisto = 6

        valor_emoji = {
            0: "⬜", 1: "🏢", 2: "💧", 3: "⛔", 5: "🟩", 6: "🟨", 8: "🚩", 9: "🏁"
        }
        camino_nomal_set = set(camino_normal)  # Búsqueda rápida
        camino_imprevisto_set = set(camino_imprevistos)  # Búsqueda rápida

        for i, fila in enumerate(self.mapa):
            fila_str = ""
            for j, celda in enumerate(fila):
                if (i, j) in camino_nomal_set:
                    fila_str += valor_emoji[valor_camino]
                elif (i, j) in camino_imprevisto_set:
                    fila_str += valor_emoji[valor_camino_imprevisto]
                else:
                    fila_str += valor_emoji[celda]
            print(fila_str)

    def agregar_obstaculo(self, posicion, tipo_obs, forma, camino_viable):
        
        fila, colm = posicion

        if tipo_obs not in self.posicion_obstaculo:
            self.posicion_obstaculo[tipo_obs] = []
        
        self.mapa[fila][colm] = tipo_obs
        self.posicion_obstaculo[tipo_obs].append(posicion)

        for x, y in forma:
            nueva_fila, nueva_colm = fila + x, colm + y # Recorrer vecinos
            nueva_posicion = (nueva_fila, nueva_colm)

            if self.verificar_posicion(nueva_posicion, camino_viable):
                    self.mapa[nueva_fila][nueva_colm] = tipo_obs
                    self.posicion_obstaculo[tipo_obs].append(nueva_posicion)
    
    def limpiar_zona(self, posicion, forma):
        fila, colm = posicion
        self.mapa[fila][colm] = 0

        for x, y in forma:

            aux_fila, aux_col = fila + x, colm + y # Recorrer vecinos

            if self.verificar_posicion((aux_fila, aux_col), self.lista_obstaculos):
                    
                tipo_obs = self.mapa[aux_fila][aux_col]
                self.posicion_obstaculo[tipo_obs].remove((aux_fila, aux_col))
                self.mapa[aux_fila][aux_col] = 0

    def verificar_posicion(self, posicion, camino_viable):
        fila, colm = posicion

        if 0 <= fila < self.alto and 0 <= colm < self.ancho and self.mapa[fila][colm] in camino_viable:
            return True
    
        return False

    def solicitar_posicion(self, camino_viable):
        while True:

            fila = solicitar_dato("Ingrese la fila: ", int)
            colm = solicitar_dato("Ingrese la columna: ", int)

            if self.verificar_posicion((fila, colm), camino_viable):
                return (fila, colm)
            
            else:
                print("Posición inválida.")
    
    def liberar_zona(self, tipo_obs):
        posiciones_a_eliminar = []

        for fila, colm in self.posicion_obstaculo.get(tipo_obs, []):

            if self.mapa[fila][colm] == tipo_obs:
                self.mapa[fila][colm] = 0
            
            else:
                posiciones_a_eliminar.append((fila, colm))
        if posiciones_a_eliminar:
            for pos in posiciones_a_eliminar:
                self.posicion_obstaculo[tipo_obs].remove(pos)
    
    def bloquear_zonas(self, tipo_obs):

        for fila, colm in self.posicion_obstaculo.get(tipo_obs, []):

            if self.mapa[fila][colm] == 0:
                self.mapa[fila][colm] = tipo_obs
            
            else:
                self.posicion_obstaculo[tipo_obs].remove((fila, colm))
    


class BuscarCamino():
    def __init__(self, instancia_mapa, direcciones, inicio=None, fin=None):
        self.instancia_mapa = instancia_mapa
        self.direcciones = direcciones
        self.camino = []
        self.inicio = inicio
        self.fin = fin

    def buscar_bfs(self, camino_viable):

        cola = deque([self.inicio])
        visitado = set()
        visitado.add(self.inicio)
        padre = {self.inicio: None}

        while cola:
            actual = cola.popleft()
            fila_actual, colm_actual = actual

            if (actual) == (self.fin):
                return self.reconstruir_camino(padre)

            for x, y in self.direcciones:

                vecino = (fila_actual + x, colm_actual + y)

                if vecino not in visitado and self.instancia_mapa.verificar_posicion(vecino, camino_viable):
                    visitado.add(vecino)
                    cola.append(vecino)
                    padre[vecino] = (actual)

        return None  # No se encontró camino

    def reconstruir_camino(self, padre):
        camino = []
        actual = self.fin

        while actual is not None:
            camino.append(actual)
            actual = padre[actual]

        camino.reverse()
        return camino
    
    def agregar_inicio(self, inicio):
        self.inicio = inicio

    def agregar_fin(self, fin):
        self.fin = fin

    def buscar_caminos(self, camino_normal, camino_imprevistos):
        camino1 = self.buscar_bfs(camino_normal)
        camino2 = self.buscar_bfs(camino_imprevistos)

        if camino1 == camino2 and camino1 is None:
            print("No se encontró ningún camino.")
            self.instancia_mapa.mostrar_mapa_normal()
            return
        
        elif camino1 == camino2 and camino1 is not None:
            print("No se encontro ningun camino mas eficiente que el normal.")
            self.instancia_mapa.mostrar_mapa_camino(camino1, [])
            return
        
        if camino1 is None and camino2 is not None:
            print("No se encontro ningun camino sin imprevistos, se muestra el camino con imprevistos.")
            self.instancia_mapa.mostrar_mapa_camino([], camino2)
            return
        
        else:
            print("Se encontraron ambos caminos, se muestran ambos caminos.")
            self.instancia_mapa.mostrar_mapa_camino(camino1, camino2)
        
    def actualizar_mapa(self, instancia_mapa):
        self.instancia_mapa = instancia_mapa

def main():
    # Recorrer en cruz
    forma_cruz = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Recorer en cuadrado
    forma_cuadrado = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    bandera_camino = False

    terreno_normal = [0] #Camino viable
    terreno_imprevistos = [0, 2] #Camino con imprevistos
    lista_obstaculos = [1, 2, 3] #Tipos de obstaculos

    ancho = solicitar_dato("Ingrese el ancho del mapa: ", int, lambda x: x > 0)
    alto = solicitar_dato("Ingrese el alto del mapa: ", int, lambda x: x > 0)
    mapa = Mapa(ancho, alto, lista_obstaculos)
    mapa.mostrar_mapa_normal()

    while True:
        print("--- Menú ---")
        print("1. Editar mapa")
        print("2. Buscar camino")
        print("3. Salir")

        opcion = solicitar_dato("Seleccione una opción: ", int, lambda x: 1 <= x <= 4)

        if opcion == 1:
            print("--- Editar mapa ---")
            print("1. Agregar edificio (cuadrado)")
            print("2. Agregar agua (cruz)")
            print("3. Agregar zona bloqueada (cuadrado)")  
            print("4. Liberar zona bloqueada")
            print("5. Bloquear zonas bloqueadas")
            print("6. Limpiar zona")
            print("7. Volver al menú principal")

            opcion_obstaculo = solicitar_dato("Seleccione una opción: ", int, lambda x: 1 <= x <= 5)

            if opcion_obstaculo in [1, 2, 3]:

                posicion_obstaculo = mapa.solicitar_posicion(terreno_normal)

                if opcion_obstaculo == 1:
                    tipo_obs = 1
                    forma = forma_cuadrado
                    camino_viable = terreno_normal

                elif opcion_obstaculo == 2:
                    tipo_obs = 2
                    forma = forma_cruz
                    camino_viable = terreno_imprevistos

                else:
                    tipo_obs = 3
                    forma = forma_cuadrado
                    camino_viable = terreno_normal

                mapa.agregar_obstaculo(posicion_obstaculo, tipo_obs, forma, camino_viable)
                if bandera_camino:
                    buscador.actualizar_mapa(mapa)
                    buscador.buscar_caminos(terreno_normal, terreno_imprevistos)
                else:
                    mapa.mostrar_mapa_normal()
            
            elif opcion_obstaculo == 4:
                tipo_obs = 4
                mapa.liberar_zona(tipo_obs)
                if bandera_camino:
                    buscador.actualizar_mapa(mapa)
                    buscador.buscar_caminos(terreno_normal, terreno_imprevistos)
                else:
                    mapa.mostrar_mapa_normal()
            
            elif opcion_obstaculo == 5:
                tipo_obs = 4
                mapa.bloquear_zonas(tipo_obs)
                if bandera_camino:
                    buscador.actualizar_mapa(mapa)
                    buscador.buscar_caminos(terreno_normal, terreno_imprevistos)
                else:
                    mapa.mostrar_mapa_normal()
            
            elif opcion_obstaculo == 6:
                posicion_limpiar = mapa.solicitar_posicion(lista_obstaculos)
                mapa.limpiar_zona(posicion_limpiar, forma_cuadrado)
                if bandera_camino:
                    buscador.actualizar_mapa(mapa)
                    buscador.buscar_caminos(terreno_normal, terreno_imprevistos)
                else:
                    mapa.mostrar_mapa_normal()


        elif opcion == 2:
            bandera_camino = True
            print("Ingrese la posición de inicio:")
            posicion_inicio = mapa.solicitar_posicion(terreno_normal)

            print("Ingrese la posición de fin:")
            posicion_fin = mapa.solicitar_posicion(terreno_normal)

            buscador = BuscarCamino(mapa, forma_cruz, posicion_inicio, posicion_fin)

            buscador.buscar_caminos(terreno_normal, terreno_imprevistos)
        
        elif opcion == 3:
            print("Saliendo del programa.")
            break



if __name__ == "__main__":
    main() 


    

    