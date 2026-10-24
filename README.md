# Tarea Grupal G9: Implementación y Mejora del Agente Aspiradora (3x3)

**Asignatura:** Inteligencia Artificial (ICCD523)  
**Tema:** Agentes Inteligentes, Métrica PEAS y Escalamiento a Entorno Bidimensional 3x3

---

## 1. Descripción del Proyecto

En este repositorio se analiza el comportamiento del agente aspiradora reactivo simple (`S2_Capitulo2_Agentes_PEAS.py`) en una cuadrícula $2\times 2$ y se implementa su mejora y escalamiento a un entorno bidimensional de $3\times 3$ (`agente_aspiradora_3x3.py`).

### Ineficiencia identificada en el código base
El agente original (`RandomVacuumAgent`) toma decisiones únicamente con la percepción inmediata (`pos, status`) sin almacenar historial de celdas visitadas y sin contar con una acción de parada (`NoOp`). Como consecuencia:
1. Se desplaza al azar (`random.choice`), revisitando celdas que ya limpió.
2. Nunca decide detenerse por sí mismo, consumiendo energía de forma indefinida.

### Mejoras implementadas
1. **Métrica de Rendimiento PEAS (`VisualEnvironment3x3`):**
   - **$+10$ puntos** por cada celda sucia limpiada efectivamente (`Suck`).
   - **$-1$ punto** de costo energético por cada acción física (`Suck`, `Up`, `Down`, `Left`, `Right`).
   - **$0$ puntos** de costo energético al detenerse (`NoOp`).
2. **Escalamiento a cuadrícula $3\times 3$:** Visualización interactiva con `matplotlib` mostrando el estado de las 9 celdas, puntaje PEAS y energía acumulada en tiempo real.
3. **Agente con Memoria (`MemoryVacuumAgent3x3`):**
   - Registra en un conjunto (`self.visitadas`) las coordenadas ya inspeccionadas/limpias.
   - Selecciona como siguiente destino la celda pendiente más cercana utilizando la **distancia Manhattan**:
     $$d((f_1, c_1), (f_2, c_2)) = |f_1 - f_2| + |c_1 - c_2|$$
   - Al completar las 9 celdas de la cuadrícula $3\times 3$, ejecuta la acción `NoOp` para detenerse de forma óptima sin desperdiciar recursos.

---

## 2. Estructura del Repositorio

- `S2_Capitulo2_Agentes_PEAS.py`: Código base original proporcionado (entorno $2\times 2$, agente reactivo aleatorio).
- `agente_aspiradora_3x3.py`: Simulador interactivo mejorado en cuadrícula $3\times 3$ con métrica PEAS y agente dotado de memoria (`MemoryVacuumAgent3x3`).
- `benchmark_comparativo.py`: Script de evaluación empírica (50 episodios de prueba) que compara `RandomVacuumAgent3x3` vs. `MemoryVacuumAgent3x3` y genera la gráfica `comparacion_peas.png`.
- `comparacion_peas.png`: Gráfica de resultados del benchmark empírico.
- `informe_latex/`: Código fuente en LaTeX (plantilla Springer LNCS) del informe técnico.

---

## 3. Ejecución

### Requisitos
```bash
pip install numpy matplotlib
```

### Ejecutar el simulador visual interactivo (3x3)
```bash
python agente_aspiradora_3x3.py
```

### Ejecutar el benchmark comparativo (para la demostración en clase)
```bash
python benchmark_comparativo.py
```
