import time
import random
import numpy as np
import matplotlib.pyplot as plt
from agente_aspiradora_3x3 import (
    VisualEnvironment3x3,
    RandomVacuumAgent3x3,
    MemoryVacuumAgent3x3,
)

def evaluar_agente(clase_agente, grids_iniciales, posiciones_iniciales, max_pasos=30):
    puntajes = []
    energias = []
    limpiezas_completas = 0
    historial_puntaje_paso_a_paso = np.zeros(max_pasos)

    inicio = time.perf_counter()

    for grid_ini, pos_ini in zip(grids_iniciales, posiciones_iniciales):
        env = VisualEnvironment3x3(
            initial_grid=grid_ini,
            initial_pos=pos_ini,
            visual=False
        )
        agent = clase_agente()

        for paso in range(max_pasos):
            percept = env.get_percept()
            action = agent.act(percept)
            env.execute_action(action)
            historial_puntaje_paso_a_paso[paso] += env.score

        puntajes.append(env.score)
        energias.append(env.energy_consumed)
        if env.is_completely_clean():
            limpiezas_completas += 1

    tiempo_ms = (time.perf_counter() - inicio) * 1000.0
    n = len(grids_iniciales)
    return {
        "puntaje_promedio": float(np.mean(puntajes)),
        "energia_promedio": float(np.mean(energias)),
        "tasa_exito_pct": (limpiezas_completas / n) * 100.0,
        "tiempo_total_ms": tiempo_ms,
        "curva_puntaje": historial_puntaje_paso_a_paso / n,
    }


if __name__ == "__main__":
    # Fijar semilla para reproducibilidad académica
    np.random.seed(42)
    random.seed(42)

    num_episodios = 50
    max_pasos = 30

    # Generar los mismos 50 entornos iniciales 3x3 para ambos agentes
    grids = [np.random.choice([0, 1], size=(3, 3)) for _ in range(num_episodios)]
    posiciones = [[random.randint(0, 2), random.randint(0, 2)] for _ in range(num_episodios)]

    res_aleatorio = evaluar_agente(RandomVacuumAgent3x3, grids, posiciones, max_pasos)
    res_memoria = evaluar_agente(MemoryVacuumAgent3x3, grids, posiciones, max_pasos)

    print("=" * 68)
    print("   BENCHMARK EMPÍRICO: AGENTE ALEATORIO vs. AGENTE CON MEMORIA (3x3)")
    print(f"   ({num_episodios} episodios de prueba | Horizonte: {max_pasos} pasos por episodio)")
    print("=" * 68)
    print(f"{'Métrica PEAS / Rendimiento':<32} | {'Agente Aleatorio':<15} | {'Agente Memoria':<15}")
    print("-" * 68)
    print(f"{'Puntaje PEAS promedio (pts)':<32} | {res_aleatorio['puntaje_promedio']:>15.2f} | {res_memoria['puntaje_promedio']:>15.2f}")
    print(f"{'Energía consumida promedio':<32} | {res_aleatorio['energia_promedio']:>15.2f} | {res_memoria['energia_promedio']:>15.2f}")
    print(f"{'Entornos 100% limpios (%)':<32} | {res_aleatorio['tasa_exito_pct']:>14.1f}% | {res_memoria['tasa_exito_pct']:>14.1f}%")
    print(f"{'Tiempo de ejecución (50 ep, ms)':<32} | {res_aleatorio['tiempo_total_ms']:>15.2f} | {res_memoria['tiempo_total_ms']:>15.2f}")
    print("=" * 68)

    # Generar gráfico comparativo para el informe LaTeX y la presentación
    pasos_x = np.arange(1, max_pasos + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # Subplot 1: Evolución del puntaje PEAS paso a paso
    ax1.plot(pasos_x, res_memoria["curva_puntaje"], label="Agente con Memoria (3x3)", linewidth=2.5, color="#1f77b4")
    ax1.plot(pasos_x, res_aleatorio["curva_puntaje"], label="Agente Reactivo Aleatorio (3x3)", linewidth=2.5, linestyle="--", color="#d62728")
    ax1.set_title("Evolución del Puntaje PEAS por Paso")
    ax1.set_xlabel("Paso de simulación")
    ax1.set_ylabel("Puntaje PEAS promedio")
    ax1.grid(True, linestyle=":", alpha=0.7)
    ax1.legend()

    # Subplot 2: Comparación de Energía Consumida y Puntaje Final
    metricas = ["Puntaje PEAS Final", "Energía Consumida"]
    vals_aleatorio = [res_aleatorio["puntaje_promedio"], res_aleatorio["energia_promedio"]]
    vals_memoria = [res_memoria["puntaje_promedio"], res_memoria["energia_promedio"]]

    x = np.arange(len(metricas))
    ancho = 0.35
    b1 = ax2.bar(x - ancho / 2, vals_aleatorio, ancho, label="Agente Aleatorio", color="#d62728", alpha=0.85)
    b2 = ax2.bar(x + ancho / 2, vals_memoria, ancho, label="Agente con Memoria", color="#1f77b4", alpha=0.85)
    ax2.set_title("Comparación Promedio (50 Episodios)")
    ax2.set_xticks(x)
    ax2.set_xticklabels(metricas)
    ax2.axhline(0, color="black", linewidth=0.8)
    ax2.grid(True, axis="y", linestyle=":", alpha=0.7)
    ax2.legend()

    for barra in list(b1) + list(b2):
        altura = barra.get_height()
        ax2.annotate(f"{altura:.1f}",
                     xy=(barra.get_x() + barra.get_width() / 2, altura),
                     xytext=(0, 3 if altura >= 0 else -12),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=9, weight="bold")

    plt.tight_layout()
    plt.savefig("comparacion_peas.png", dpi=200)
    print("\nGráfico guardado exitosamente como 'comparacion_peas.png'.")
