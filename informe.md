```markdown
# Informe Teórico: Aplicación de Fundamentos de Big Data
**Asignatura:** Manejo Masivo de Datos  
**Primer Parcial**

---

## 5. Las 5 V del Big Data aplicadas al proyecto

| V | Relación con el sistema de sensores | Ejemplo concreto | Escenario |
| :--- | :--- | :--- | :--- |
| **Volumen** | Cantidad masiva de registros generados y almacenados por los sensores. | El dataset actual con 100,000 mediciones simuladas almacenadas en disco. | **CSV Actual** |
| **Velocidad** | Inmediatez con la que los sensores toman y transmiten las lecturas. | Transmisión continua de mediciones cada 1 segundo por miles de sensores en tiempo real. | **Futura Ampliación** |
| **Variedad** | Diversidad en los tipos y formatos de datos que ingresan al sistema. | Incorporación de datos estructurados (temperatura), no estructurados (fotos HD) y semiestructurados (reportes). | **Futura Ampliación** |
| **Veracidad** | Nivel de precisión, ruido o incerteza en las lecturas recolectadas. | Fallas de calibración en sensores o pérdida de lecturas por interrupción de señal de red. | **Futura Ampliación** |
| **Valor** | Utilidad estratégica o económica para evitar fallas o paros en la producción. | Detectar patrones de sobrecalentamiento antes de que una máquina falle para reducir costos de reparación. | **CSV Actual y Futura Ampliación** |

---

## 6. Tipos de datos y procesamiento tradicional

### Clasificación:
1. **El CSV de sensores:** **Estructurado**. Posee columnas y filas con tipos de datos estandarizados.
2. **Un mensaje JSON enviado por un sensor:** **Semiestructurado**. Utiliza pares clave-valor organizados sin requerir un esquema relacional estricto.
3. **Una fotografía de una máquina:** **No estructurado**. Formato binario sin estructura de campos.
4. **El texto libre de un reporte de mantenimiento:** **No estructurado**. Lenguaje natural no tabulado.

### ¿Por qué 100,000 registros no lo convierten automáticamente en Big Data?
Porque ocupa únicamente unos pocos megabytes de memoria (alrededor de 3 a 5 MB) y puede ser procesado por una computadora convencional en milisegundos utilizando Pandas en memoria RAM. No supera la capacidad de una sola máquina ni exige procesamiento distribuido.

### Limitaciones al escalar a miles de sensores por segundo:
- **Desbordamiento de memoria RAM:** Pandas carga el archivo entero en memoria; con terabytes de información colapsaría.
- **Cuello de botella en I/O:** Escribir miles de registros por segundo en archivos locales bloquea el disco rígido/SSD.
- **Procesamiento Monohilo:** El script actual se ejecuta en un solo núcleo, volviéndose incapaz de procesar peticiones simultáneas masivas.

---

## 7. Batch y Streaming

- **Procesamiento realizado:** **Batch (por lotes)**. El programa analiza un archivo de datos históricos estático que ya estaba completamente guardado en disco.

### Decisiones según latencia:
1. **Alertas en pocos segundos (> 85 °C):**
   - **Enfoque:** **Streaming**.
   - **Justificación:** Requiere una latencia casi nula. Las lecturas deben evaluarse según llegan en el flujo de datos (event-driven) usando motores como Apache Flink o Spark Streaming.
2. **Resumen al terminar el día:**
   - **Enfoque:** **Batch**.
   - **Justificación:** Es un cómputo programado sobre datos estáticos acumulados durante 24 horas, donde no se requiere respuesta inmediata.

---

## 8. Arquitecturas Lambda y Kappa

### Escenario A
- **Elección:** **Arquitectura Lambda**.
- **Justificación:** Combina una capa por lotes (*Batch Layer*) para mantener la precisión recomputando el historial completo y una capa rápida (*Speed Layer*) para métricas en tiempo real con baja latencia.

```text
               ┌──> Speed Layer (Streaming en tiempo real) ──┐
Fuente Datos ──┼─────────────────────────────────────────────┼──> Serving Layer
               └──> Batch Layer (Procesamiento por lotes) ───┘
```

## 9. Analítica descriptiva, predictiva y prescriptiva

1. **Analítica Descriptiva (Valores obtenidos del dataset):**
   - **Hallazgo 1:** Se procesaron un total de **100,000 registros** distribuidos entre **40 sensores distintos** a lo largo de 4 plantas industriales. Las temperaturas promedio se mantuvieron muy estables por planta: Planta 1 (66.62 °C), Planta 2 (66.53 °C), Planta 3 (66.77 °C) y Planta 4 (66.67 °C).
   - **Hallazgo 2:** Se registraron **6,954 lecturas con alerta** (temperatura mayor a 85 °C). Existió un empate en la temperatura máxima absoluta registrada con **104.99 °C** (alcanzada en 4 lecturas distintas por los sensores S023, S019, S014 y S030 en Planta 2 y Planta 3). La **Planta 3** fue la que concentró la mayor cantidad de alertas de sobrecalentamiento, acumulando un total de **1,777 alertas**.

2. **Analítica Predictiva:**
   - **Pregunta:** ¿Existe una correlación entre el incremento sostenido de vibración (mm/s) y un pico crítico de temperatura (> 85 °C) dentro de las 24 horas previas a una falla mecánica?
   - **Datos adicionales necesarios:** Histórico de fallas o paradas técnicas reales de las máquinas, registro de mantenimientos previos, horas continuas de operación de cada equipo y especificaciones de tolerancia del fabricante.

3. **Analítica Prescriptiva:**
   - **Acción propuesta:** Reducir automáticamente la carga de trabajo de la máquina asociada al sensor en alerta o detener temporalmente el equipo y generar una orden de inspección preventiva prioritaria.
   - **Información a revisar antes de decidir:** Tendencia de la temperatura en los últimos 10 minutos (para descartar falsos positivos por lecturas atípicas isoladas), disponibilidad de equipos de respaldo en la planta para asumir la producción y presencia de personal de mantenimiento en el turno.