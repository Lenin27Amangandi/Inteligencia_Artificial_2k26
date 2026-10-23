import matplotlib.pyplot as plt
import numpy as np
import random
import time

class VisualEnvironment2x2:
    def __init__(self, filas=2, columnas=2):
        # Cuadrícula: 0 = Limpio, 1 = Sucio
        self.grid = np.random.choice([0, 1], size=(filas, columnas))
        # Posición inicial aleatoria (fila, columna)
        self.agent_pos = [random.randint(0, filas - 1),
                          random.randint(0, columnas - 1)]

        # Configuración del gráfico interactivo
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

    def render(self, step, action):
        self.ax.clear()
        filas, columnas = self.grid.shape

        # Dibujar la cuadrícula (colores cambian según limpieza)
        self.ax.matshow(self.grid, cmap='Blues', vmin=0, vmax=1.5)

        # Dibujar al agente como un punto rojo grande
        self.ax.plot(self.agent_pos[1], self.agent_pos[0], 'ro', markersize=40)

        # Etiquetas de estado
        for i in range(filas):
            for j in range(columnas):
                estado = "SUCIO" if self.grid[i, j] == 1 else "LIMPIO"
                self.ax.text(j, i, estado, ha='center', va='center',
                             color='black', weight='bold', fontsize=12)

        self.ax.set_title(f"Paso: {step} | Acción: {action}", pad=20)
        self.ax.set_xticks(range(columnas))
        self.ax.set_yticks(range(filas))
        self.ax.grid(which='minor', color='black', linestyle='-', linewidth=2)

        plt.draw()
        plt.pause(1.5) # Pausa para visualizar la animación

    def get_percept(self):
        return self.agent_pos.copy(), self.grid[self.agent_pos[0], self.agent_pos[1]]

    def execute_action(self, action):
        filas, columnas = self.grid.shape

        if action == 'Suck':
            self.grid[self.agent_pos[0], self.agent_pos[1]] = 0
        elif action == 'Up' and self.agent_pos[0] > 0:
            self.agent_pos[0] -= 1
        elif action == 'Down' and self.agent_pos[0] < filas - 1:
            self.agent_pos[0] += 1
        elif action == 'Left' and self.agent_pos[1] > 0:
            self.agent_pos[1] -= 1
        elif action == 'Right' and self.agent_pos[1] < columnas - 1:
            self.agent_pos[1] += 1

    def is_completely_clean(self):
        return np.sum(self.grid) == 0

class RandomVacuumAgent:
    def __init__(self, filas=2, columnas=2):
        # Memoria de las casillas visitadas
        self.visited = np.zeros((filas, columnas), dtype=bool)

    def act(self, percept):
        pos, status = percept
        fila, columna = pos
        filas, columnas = self.visited.shape

        # Adaptar la memoria si cambia el tamaño del entorno
        if fila >= filas or columna >= columnas:
            return 'Stop'

        # Recordar la casilla actual
        self.visited[fila, columna] = True

        # Regla principal: Si está sucio, limpia
        if status == 1:
            return 'Suck'

        # Buscar movimientos que lleven a casillas no visitadas
        movimientos_posibles = []
        if fila > 0 and not self.visited[fila - 1, columna]:
            movimientos_posibles.append('Up')
        if fila < filas - 1 and not self.visited[fila + 1, columna]:
            movimientos_posibles.append('Down')
        if columna > 0 and not self.visited[fila, columna - 1]:
            movimientos_posibles.append('Left')
        if columna < columnas - 1 and not self.visited[fila, columna + 1]:
            movimientos_posibles.append('Right')

        # Elegir una casilla nueva si existe
        if movimientos_posibles:
            return random.choice(movimientos_posibles)

        # Si no hay vecinos nuevos, buscar cualquier casilla sin visitar
        pendientes = np.argwhere(~self.visited)

        if len(pendientes) == 0:
            return 'Stop'

        destino = pendientes[0]
        if fila < destino[0]:
            return 'Down'
        if fila > destino[0]:
            return 'Up'
        if columna < destino[1]:
            return 'Right'
        if columna > destino[1]:
            return 'Left'

        return 'Stop'

if __name__ == "__main__":
    env = VisualEnvironment2x2(filas=3, columnas=3)
    agent = RandomVacuumAgent(filas=3, columnas=3)

    energia = 0
    movimientos = 0
    limpiezas = 0

    env.render(step=0, action="Inicio")

    for paso in range(1, env.grid.size * 4 + 1):
        percept = env.get_percept()
        action = agent.act(percept)

        if action == 'Stop':
            break

        env.execute_action(action)

        # Métrica PEAS: energía y acciones realizadas
        if action == 'Suck':
            energia += 2
            limpiezas += 1
        else:
            energia += 1
            movimientos += 1

        env.render(step=paso, action=action)

        if env.is_completely_clean() and np.all(agent.visited):
            break

    # Evaluación del rendimiento
    porcentaje_limpieza = np.count_nonzero(env.grid == 0) / env.grid.size * 100

    print("Porcentaje de limpieza:", porcentaje_limpieza, "%")
    print("Movimientos:", movimientos)
    print("Acciones de limpieza:", limpiezas)
    print("Energía consumida:", energia)

    plt.ioff()
    plt.show()