# actividad-examen
actividad del examen 1er parcial.

# Análisis de Sensores Industriales — Manejo Masivo de Datos

## Objetivo del Proyecto
Este proyecto analiza un conjunto de datos simulados de mediciones de sensores industriales (temperatura y vibración) instalados en cuatro plantas operativas. El objetivo es obtener métricas agregadas, identificar valores máximos de temperatura y aislar lecturas críticas (> 85 °C) para respaldar la toma de decisiones.

## Descripción de los Datos
> **Nota:** Los datos procesados provienen del archivo simulado `sensores_industriales.csv` (100,000 mediciones aproximadamente).

Estructura de las columnas:
- `id_registro`: Identificador único de la lectura.
- `fecha_hora`: Fecha y hora del registro.
- `id_sensor`: Identificador único del sensor.
- `planta`: Planta industrial donde está ubicado el sensor.
- `temperatura_c`: Temperatura registrada (°C).
- `vibracion_mm_s`: Nivel de vibración registrado (mm/s).

## Requisitos Previos
- Python 3.8 o superior.

## Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone <URL_DE_TU_REPOSITORIO>
   cd <NOMBRE_DE_TU_CARPETA>