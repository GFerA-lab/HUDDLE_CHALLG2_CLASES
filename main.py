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
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.mapa = [[0 for _ in range(ancho)] for _ in range(alto)]
        self.posicion_obstaculo = {}

    def mostrar_mapa(self):
        valor_emoji = {
            0: "⬜",   # camino libre
            1: "🏢",   # edificio
            2: "💧",   # agua
            3: "⛔",   # zona bloqueada
            5: "🟦",   # camino junto
            6: "🟩",   # camino sin imprevistos
            7: "🟨",   # camino alternativo
            8: "🚩",   # inicio
            9: "🏁"    # fin
        }

        for fila in self.mapa:
            print("".join(valor_emoji[celda] for celda in fila))

    def agregar_obstaculo(self, fila, colm, tipo_obs, forma, camino_viable):

        self.mapa[fila][colm] = tipo_obs
        self.posicion_obstaculo[tipo_obs].append((fila,colm))

        for x, y in forma:
            nueva_fila, nueva_colm = fila + x, colm + y # Recorrer vecinos
            nueva_posicion = (nueva_fila, nueva_colm)

            if self.verificar_posicion(nueva_posicion, camino_viable):
                    self.mapa[nueva_fila][nueva_colm] = tipo_obs
                    self.posicion_obstaculo[tipo_obs].append(nueva_posicion)
    
    def limpiar_zona(self, fila, colm, forma):
        for x, y in forma:
            aux_fila, aux_col = fila + x, colm + y # Recorrer vecinos

            if 0 <= aux_fila < self.alto and 0 <= aux_col < self.ancho:
                if self.mapa[aux_fila][aux_col] != 0:

                    tipo_obs = self.mapa[aux_fila][aux_col]

                    if (aux_fila, aux_col) in self.posicion_obstaculo.get(tipo_obs, []):
                        self.posicion_obstaculo[tipo_obs].remove((aux_fila, aux_col))
                        self.mapa[aux_fila][aux_col] = 0

    def verificar_posicion(self, posicion, camino_viable):
        fila, colm = posicion

        if 0 <= fila < self.alto and 0 <= colm < self.ancho and self.mapa[fila][colm] in camino_viable:
            return True
    
        return False
    


class BuscarCamino():
    def __init__(self, instancia_mapa, direcciones):
        self.instancia_mapa = instancia_mapa
        self.direcciones = direcciones

    def buscar_bfs(self, inicio, fin, camino_viable):

        cola = deque([inicio])
        visitado = set()
        visitado.add(inicio)
        padre = {}

        while cola:
            actual = cola.popleft()
            fila_actual, colm_actual = actual

            if (actual) == (fin):
                return self.reconstruir_camino(padre, fin)

            for x, y in self.direcciones:

                vecino = (fila_actual + x, colm_actual + y)

                if vecino not in visitado and self.instancia_mapa.verificar_posicion(vecino, camino_viable):
                    visitado.add(vecino)
                    cola.append(vecino)
                    padre[vecino] = (actual)

        return None  # No se encontró camino

    def reconstruir_camino(self, padre, fin):
        camino = []
        actual = fin

        while actual is not None:
            camino.append(actual)
            actual = padre[actual]

        camino.reverse()
        return camino

def main():
    forma_cruz = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    forma_cuadrado = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    terreno_normal = [0]
    terreno_imprevistos = [0, 2]

    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    

    