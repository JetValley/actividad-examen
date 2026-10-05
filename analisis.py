import os
import pandas as pd


def analizar_sensores():
    # Rutas relativas
    ruta_csv = os.path.join("data", "sensores_industriales.csv")
    ruta_salida = os.path.join("resultados", "alertas.csv")

    # Verificar que el CSV exista
    if not os.path.exists(ruta_csv):
        print(f"Error: No se encuentra el archivo en la ruta '{ruta_csv}'.")
        print(
            "Asegúrate de colocar 'sensores_industriales.csv' dentro de la carpeta 'data/'."
        )
        return

    # Leer el dataset
    df = pd.read_csv(ruta_csv)

    print("=" * 60)
    print("ANÁLISIS DE SENSORES INDUSTRIALES - RESUMEN EJECUTIVO")
    print("=" * 60)

    # 1. Cantidad de registros y sensores distintos
    total_registros = len(df)
    sensores_unicos = df["id_sensor"].nunique()
    print(f"1. Total de registros: {total_registros:,}")
    print(f"   Total de sensores distintos: {sensores_unicos}")
    print("-" * 60)

    # 2. Temperatura promedio de cada planta
    print("2. Temperatura promedio por planta (°C):")
    temp_promedio = df.groupby("planta")["temperatura_c"].mean()
    for planta, temp in temp_promedio.items():
        print(f"   - Planta {planta}: {temp:.2f} °C")
    print("-" * 60)

    # 3. Temperatura máxima, sensor y fecha correspondientes (maneja empates)
    max_temp = df["temperatura_c"].max()
    registros_max = df[df["temperatura_c"] == max_temp]
    print(f"3. Temperatura máxima registrada: {max_temp} °C")
    for _, row in registros_max.iterrows():
        print(
            f"   - Sensor: {row['id_sensor']} | Planta: {row['planta']} | Fecha/Hora: {row['fecha_hora']}"
        )
    print("-" * 60)

    # 4. Contar lecturas con temperatura mayor que 85 °C
    df_alertas = df[df["temperatura_c"] > 85]
    total_alertas = len(df_alertas)
    print(f"4. Total de lecturas con alerta (Temp > 85 °C): {total_alertas}")
    print("-" * 60)

    # 5. Identificar la planta con más alertas (maneja empates)
    if total_alertas > 0:
        conteo_alertas = df_alertas["planta"].value_counts()
        max_alertas_val = conteo_alertas.max()
        plantas_top_alertas = conteo_alertas[
            conteo_alertas == max_alertas_val
        ].index.tolist()

        print(
            f"5. Planta(s) con más alertas de temperatura ({max_alertas_val} alertas):"
        )
        for p in plantas_top_alertas:
            print(f"   - Planta: {p}")
    else:
        print("5. No se registraron alertas de temperatura.")
    print("-" * 60)

    # 6. Exportar lecturas con alerta a resultados/alertas.csv
    os.makedirs("resultados", exist_ok=True)
    df_alertas.to_csv(ruta_salida, index=False)
    print(
        f"6. Se exportaron {total_alertas} registros a la ruta: '{ruta_salida}'"
    )
    print("=" * 60)


if __name__ == "__main__":
    analizar_sensores()