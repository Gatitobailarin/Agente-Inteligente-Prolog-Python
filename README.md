# MediMind AI: Agente Inteligente para Diagnóstico y Seguimiento Médico Personalizado

MediMind AI es un proyecto universitario que integra Prolog como motor de inferencia y Python como interfaz gráfica para diagnosticar enfermedades probables, explicar el razonamiento, generar recomendaciones, clasificar urgencia y administrar historial dinámico del paciente.

## Arquitectura del sistema

```text
Python (CustomTkinter)
        ↓
Puente PySwip
        ↓
SWI-Prolog
        ↓
Base de hechos y hechos dinámicos
        ↓
Reglas de inferencia
        ↓
Diagnóstico + explicación + seguimiento
```

## Características innovadoras

1. Predicción preventiva de progresión clínica.
2. Comparación de diagnósticos alternativos por porcentaje de coincidencia.
3. Explicación textual del razonamiento seguido por el agente.
4. Clasificación de urgencia médica mediante puntaje acumulado.
5. Aprendizaje dinámico de síntomas durante la ejecución.
6. Gestión de historial con borrado lógico y físico.

## Archivos del proyecto

- `medimind_ai.pl`: base de conocimiento, reglas, hechos dinámicos y consultas.
- `main.py`: interfaz gráfica moderna en CustomTkinter y comunicación con Prolog.
- `README.md`: documentación técnica, reglas, arquitectura, pruebas e instrucciones.

## Base de conocimiento en Prolog

### Síntomas implementados

Se incluyen 25 síntomas:

- fiebre
- tos
- dificultad_respiratoria
- dolor_garganta
- congestion_nasal
- estornudos
- dolor_cabeza
- fatiga
- dolor_muscular
- nauseas
- vomitos
- diarrea
- dolor_pecho
- sensibilidad_luz
- erupcion_cutanea
- picazon_ojos
- perdida_olfato
- sed_excesiva
- miccion_frecuente
- vision_borrosa
- dolor_abdominal
- escalofrios
- rigidez_cuello
- sibilancias
- presion_arterial_alta

### Enfermedades implementadas

Se modelan 8 enfermedades base:

- gripe
- covid19
- alergia
- migrana
- gastroenteritis
- neumonia
- diabetes
- hipertension

## Hechos dinámicos

```prolog
:- dynamic historial/7.
:- dynamic sintoma_aprendido/1.
:- dynamic enfermedad_aprendida/4.
:- dynamic consulta_realizada/4.
:- dynamic historial_logico/8.
```

### Explicación del hecho dinámico

- `historial/7` guarda paciente, síntomas, diagnóstico, porcentaje, nivel, riesgo y marca temporal.
- `sintoma_aprendido/1` permite aprender nuevos síntomas en tiempo real.
- `enfermedad_aprendida/4` deja abierta la expansión futura del sistema.
- `consulta_realizada/4` soporta estadísticas de uso.
- `historial_logico/8` conserva respaldo tras un borrado lógico.

## Reglas de inferencia

### 1. `porcentaje_coincidencia/5`

Cuenta cuántos síntomas requeridos por una enfermedad coinciden con los síntomas del paciente y calcula un porcentaje. Esta regla permite un diagnóstico gradual, no binario.

### 2. `nivel_confianza/2`

Clasifica el diagnóstico según el porcentaje:

- `confirmado`: 80% o más.
- `probable`: entre 50% y 79%.
- `preventivo`: entre 25% y 49%.

### 3. `diagnostico_principal/7`

Evalúa todas las enfermedades, genera candidatos con coincidencia mínima del 25% y selecciona la de mayor porcentaje. También construye una explicación sobre síntomas activados y nivel de inferencia.

### 4. `posibles_enfermedades/2`

Devuelve todas las enfermedades compatibles con el conjunto de síntomas, no solo la principal. Sirve para análisis diferencial.

### 5. `riesgo_urgencia/3`

Suma factores de urgencia de las enfermedades que tengan coincidencia relevante y clasifica la urgencia en `baja`, `media`, `alta` o `critica`.

### 6. `explicacion_diagnostico/2`

Genera una narrativa explicable con enfermedad, porcentaje, nivel, riesgo y urgencia estimada. Esta regla satisface el requisito de explicabilidad del agente.

### 7. `recomendacion_medica/2`

Combina tratamiento base de la enfermedad con una recomendación derivada del nivel de riesgo.

### 8. `prediccion_preventiva/2`

Es la característica innovadora principal. Detecta patrones incompletos que podrían evolucionar a cuadros más graves o específicos, por ejemplo un patrón respiratorio que aún no llega a compromiso total.

### 9. `comparar_diagnosticos/2`

Entrega una lista comparativa de diagnósticos alternativos con sus porcentajes de coincidencia para justificar por qué uno fue el principal y no otro.

### 10. `registrar_consulta/2`

Guarda cada consulta en el historial y en la tabla estadística dinámica.

## Consultas funcionales implementadas

1. Obtener diagnóstico principal: `diagnostico_principal/7`.
2. Obtener posibles enfermedades relacionadas: `posibles_enfermedades/2`.
3. Obtener nivel de riesgo y urgencia: `riesgo_urgencia/3`.
4. Obtener recomendación médica: `recomendacion_medica/2`.
5. Consultar historial de pacientes: `consultar_historial/2`.
6. Agregar síntomas nuevos dinámicamente: `agregar_sintoma_dinamico/1`.
7. Eliminar síntomas aprendidos: `eliminar_sintoma_aprendido/1`.
8. Mostrar enfermedades registradas: `mostrar_enfermedades/1`.
9. Mostrar tratamientos disponibles: `mostrar_tratamientos/1`.
10. Mostrar estadísticas de consultas realizadas: `estadisticas_consultas/2`.
11. Comparar diagnósticos alternativos: `comparar_diagnosticos/2`.
12. Obtener predicción preventiva: `prediccion_preventiva/2`.

## Borrado lógico y físico

### Borrado lógico

Se implementa con `borrado_logico_historial/2`.

Funcionamiento:

1. Busca cada registro del paciente en `historial/7`.
2. Copia el registro a `historial_logico/8` agregando un motivo.
3. Retira el hecho activo de `historial/7` con `retract`.
4. Conserva un rastro auditivo del dato eliminado.

Esto representa un borrado lógico porque el dato deja de estar operativo, pero permanece almacenado como respaldo o evidencia histórica.

### Borrado físico

Se implementa con `borrado_fisico_historial/1`.

Funcionamiento:

1. Elimina todos los hechos de `historial/7` del paciente.
2. Elimina también `historial_logico/8` del paciente.
3. Elimina `consulta_realizada/4` asociada.

Esto es borrado físico porque desaparece por completo la información del sistema en ejecución.

## Interfaz en Python

La interfaz fue diseñada con `CustomTkinter` y contiene:

- Campo para nombre del paciente.
- Lista de síntomas con `CheckBox`.
- Botón para diagnosticar.
- Botón para ver historial.
- Botón para agregar síntomas.
- Botón para eliminar síntomas aprendidos.
- Botones para borrado lógico y físico del historial.
- Área de resumen diagnóstico.
- Área de explicación del diagnóstico.
- Área de recomendaciones y predicción preventiva.
- Área de historial de consultas.
- Área de catálogo, tratamientos y estadísticas.

## Comunicación Python-Prolog

El flujo de comunicación es el siguiente:

1. Python recoge los síntomas seleccionados.
2. Convierte la selección a una lista Prolog, por ejemplo `[fiebre,tos,dificultad_respiratoria]`.
3. PySwip ejecuta consultas como `diagnostico_principal/7` y `explicacion_diagnostico/2`.
4. Python recupera variables de respuesta.
5. La interfaz muestra diagnóstico, riesgo, explicaciones, historial y recomendaciones.

## Diagrama de funcionamiento

```text
[Usuario]
   ↓ ingresa nombre y sintomas
[Interfaz Python - CustomTkinter]
   ↓ arma consulta Prolog
[PySwip]
   ↓ envia hechos y consultas
[SWI-Prolog]
   ↓ evalua coincidencias, reglas y dinamica
[Motor de inferencia]
   ↓ devuelve diagnostico, explicacion, riesgo y recomendacion
[Interfaz Python]
   ↓ registra historial y presenta resultados
[Seguimiento y estadisticas]
```

## Casos de prueba

### Caso 1: posible COVID-19 confirmado

Síntomas:

```text
[fiebre, tos, dificultad_respiratoria, perdida_olfato, fatiga]
```

Resultado esperado:

- Diagnóstico principal: `covid19`.
- Nivel: `confirmado`.
- Riesgo: `alto`.
- Urgencia: `alta` o `critica` según combinaciones concurrentes.

### Caso 2: diagnóstico preventivo respiratorio

Síntomas:

```text
[fiebre, tos]
```

Resultado esperado:

- Diagnóstico preventivo hacia `covid19` o `gripe`.
- Activación de `prediccion_preventiva/2`.

### Caso 3: alergia respiratoria

Síntomas:

```text
[congestion_nasal, estornudos, picazon_ojos, dolor_garganta]
```

Resultado esperado:

- Diagnóstico principal: `alergia`.
- Nivel: `confirmado`.
- Riesgo: `bajo`.

### Caso 4: gastroenteritis

Síntomas:

```text
[diarrea, vomitos, nauseas, dolor_abdominal, fiebre]
```

Resultado esperado:

- Diagnóstico principal: `gastroenteritis`.
- Recomendación de rehidratación.

### Caso 5: diabetes probable

Síntomas:

```text
[sed_excesiva, miccion_frecuente, fatiga, vision_borrosa]
```

Resultado esperado:

- Diagnóstico principal: `diabetes`.
- Riesgo alto.
- Seguimiento clínico continuo.

### Caso 6: borrado lógico y físico

1. Registrar una consulta del paciente `ana`.
2. Ejecutar `borrado_logico_historial(ana, solicitud_usuario).`
3. Verificar que el historial activo desaparece y el respaldo queda en `historial_logico/8`.
4. Ejecutar `borrado_fisico_historial(ana).`
5. Verificar eliminación completa.

## Ejemplos de consultas Prolog

```prolog
?- diagnostico_principal([fiebre,tos,dificultad_respiratoria,perdida_olfato,fatiga], E, P, N, R, T, EX).

?- posibles_enfermedades([fiebre,tos], Lista).

?- riesgo_urgencia([fiebre,tos,dificultad_respiratoria], Nivel, Puntaje).

?- recomendacion_medica([diarrea,vomitos,nauseas,dolor_abdominal], R).

?- registrar_consulta(juan, [fiebre,tos,dolor_garganta,fatiga]).

?- consultar_historial(juan, H).

?- agregar_sintoma_dinamico(dolor_articular).

?- eliminar_sintoma_aprendido(dolor_articular).

?- mostrar_enfermedades(L).

?- mostrar_tratamientos(T).

?- estadisticas_consultas(Total, Pacientes).
```

## Instrucciones de ejecución paso a paso

### Requisitos

- Python 3.10 o superior.
- SWI-Prolog instalado.
- Paquetes Python: `pyswip` y `customtkinter`.

### Instalación

1. Instalar SWI-Prolog.
2. Instalar dependencias Python:

```bash
pip install pyswip customtkinter
```

3. Colocar `main.py` y `medimind_ai.pl` en la misma carpeta.

### Ejecución

1. Abrir terminal en la carpeta del proyecto.
2. Ejecutar:

```bash
python main.py
```

3. Escribir el nombre del paciente.
4. Seleccionar síntomas.
5. Presionar `Diagnosticar`.
6. Revisar explicación, recomendación y predicción preventiva.
7. Consultar historial o aplicar borrado según el caso.

## Valor académico del proyecto

Este proyecto demuestra:

- Representación del conocimiento en Prolog.
- Construcción de un sistema basado en reglas.
- Uso de inferencia lógica con coincidencia parcial.
- Integración Python-Prolog mediante PySwip.
- Gestión de hechos dinámicos con `dynamic`, `assertz`, `retract` y `retractall`.
- Explicabilidad del razonamiento del agente.
- Consultas complejas y análisis diferencial.
- Innovación mediante predicción preventiva y comparación diagnóstica.

## Observaciones finales

MediMind AI no sustituye a un profesional de la salud. Es un sistema académico de apoyo a la decisión que ilustra técnicas de IA simbólica, inferencia lógica y explicabilidad en un contexto clínico.
