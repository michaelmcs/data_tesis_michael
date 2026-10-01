# Contexto del proyecto: tesis de maestría CareER-GPT

Este archivo resume el trabajo realizado en Claude.ai para que Claude Code continúe sin perder contexto. Léelo completo antes de empezar.

## 1. El proyecto

Tesis de Maestría en Informática con mención en Gerencia de Tecnologías de Información y Comunicaciones, Escuela de Posgrado, Universidad Nacional del Altiplano de Puno (UNAP).

Título: CareER-GPT: Arquitectura Híbrida con LoRA sobre LLMs y Modelos Tabulares para la Generación y Rankeo de Rutas Educativas en Postulantes de la Región de Puno.

Autor: Michael Newton Cutipa Santi. Código de matrícula 245310. Proyecto aprobado el 9 de julio de 2026, acta 2025-4136, plataforma PILAR. Asesor: Dr. Renzo Apaza Cutipa. Jurado: Samuel Donato Pérez Quispe (presidente), Charles Ignacio Mendoza Mollocondo, José Pánfilo Tito Lipa.

Arquitectura: un modelo tabular XGBoost estima la probabilidad de ingreso por programa y los ordena; ese ranking calibrado entra como contexto a un LLM ajustado con LoRA que redacta la ruta educativa.

## 2. Objetivos e hipótesis, orden definitivo

Este orden está unificado en todo el borrador y en la matriz de consistencia. No cambiarlo.

| N.º | Objetivo específico | Hipótesis específica |
|---|---|---|
| 1 | Entrenar y evaluar XGBoost para el rankeo de probabilidades de éxito por carrera | AUC-ROC igual o mayor a 0.85 |
| 2 | Transformar el conjunto de datos en pares de instrucción y respuesta | Corpus representativo, coherente y balanceado |
| 3 | Ajustar un LLM con LoRA para generar rutas | Coherencia contextual mayor a 0.80 |
| 4 | Integrar ambos modelos y validar su eficacia comparativa | El híbrido supera en al menos 10 % a cada modelo individual |

## 3. Datos

Bases en `datos/`: `ADMISION_V3.xlsx` y `SIAGIE_V3.xlsx`. Identificador anónimo común: `id_anonimo`.

Periodo usado: 2021-I a 2025-II. Se excluyó 2026 por ser año en curso. Se agregó 2021 para reconstruir postulaciones previas.

Cifras: 48 059 postulaciones de 39 327 personas. Emparejamiento con SIAGIE del 90.0 %. Conjunto analítico: 42 156 postulaciones de 34 648 personas. Tasa de ingreso: 11.49 %.

Unidad de análisis: la postulación. La validación siempre se agrupa por persona. El corte de ingreso se agrupa por `periodo + tipo_proceso + programa`, nunca solo por periodo y programa.

Variables excluidas por fuga de información: puntaje total, puntajes por componente, respuestas por curso, órdenes de mérito y carrera de ingreso.

## 4. Resultados ya obtenidos

Cifras verificadas el 30 de septiembre de 2026 al reejecutar todo el pipeline con el entorno de `requirements.txt`. Las cifras de la versión anterior del borrador no se pudieron reproducir con ninguna versión de pandas o XGBoost probada, por lo que se reemplazaron por estas.

Objetivo 1. XGBoost ajustado: profundidad 3, tasa 0.02, 800 árboles, peso mínimo por hoja 40, submuestreo 0.8, columnas 0.5, regularización L2 de 10. AUC-ROC 0.754 (IC 95 %: 0.747 a 0.761), AUC-PR 0.292 frente a tasa base 0.115. La regresión logística logró 0.755; la diferencia por pliegue es de 0.0014 (t(4) = -2.99, p = .040), sin relevancia práctica. **H1 se rechaza.** Brecha de 7.1 puntos en la tasa de falsos negativos contra colegios rurales (χ² = 18.40, p < .001). Calibración isotónica: Brier de 0.194 a 0.092.

Objetivo 2. Corpus CareER-Dataset de 34 648 pares, particiones 70, 15 y 15 % agrupadas por persona, balanceado (todas las p > .05), coherencia 100 %. **H2 se acepta.** El corpus se regeneró con el modelo actual: usar el `resultados/CareER_Dataset.jsonl` del repositorio en Colab.

Objetivo 4, componente de rankeo, sobre 4 843 ingresantes con validación cruzada: XGBoost MRR 0.353, NDCG@10 0.500; popularidad del programa MRR 0.362, NDCG@10 0.507; aleatorio MRR 0.299. **El XGBoost supera al azar y queda 2.5 % por debajo de la popularidad, diferencia no significativa** (Wilcoxon p = .292, r = .015): ambos métodos son equivalentes. Los textos del borrador que dependen de la significación se redactan de forma condicional según el valor p.

Objetivos 3 y 4, modelo de lenguaje, ejecutado en Colab con GPU Tesla T4 y traído en `resultados_llm.zip`, ya descomprimido en `resultados/`. Qwen2.5-1.5B-Instruct con LoRA, 4 358 144 parámetros entrenables, 375 pasos, 34.8 y 28.5 minutos. Sobre 300 pares de prueba: LLM base, métrica combinada 0.342 y coherencia 0.253; LoRA sin componente tabular, 0.783 y 0.540; CareER-GPT híbrido, 1.000 y 1.000, con el 100 % de rutas idénticas a la referencia. **H3 se acepta** (binomial exacta p < .001). **H4 se acepta en la generación de rutas**: mejora de 192.2 % y 27.7 % (Wilcoxon p < .001, r = .867), pero no en el rankeo. Los valores perfectos se discuten como limitación, porque las referencias tienen estructura fija.

Advertencia: esa corrida de Colab usó el corpus anterior, el del .rar, y no el regenerado. Ambos tienen las mismas 34 648 personas, particiones y perfiles; solo difieren las probabilidades del XGBoost. Para consistencia total, repetir el cuaderno de Colab con el `resultados/CareER_Dataset.jsonl` actual, reemplazar los tres archivos y regenerar el borrador; los textos se recalculan solos.

Todas las cifras exactas están en `resultados/`.

## 5. Estructura de la carpeta y cómo ejecutar

```
datos/          ADMISION_V3.xlsx y SIAGIE_V3.xlsx
plantilla/      plantilla oficial ANEXO 004 de la EPG UNA
documentos/     proyecto aprobado v6, acta 2025-4136 y reporte Turnitin
resultados/     tablas, figuras, métricas y corpus CareER_Dataset.jsonl
pipeline/       scripts de procesamiento, ejecutar desde la raíz
borrador/       generador del borrador sobre la plantilla
colab/          cuaderno para el ajuste con LoRA
```

Todos los scripts usan rutas relativas y se ejecutan desde la raíz del proyecto:

```
python pipeline/01_preprocesamiento.py      # une las bases
python pipeline/03_resultados.py            # modelos, pruebas, corpus y figuras
python pipeline/05_figura_importancia.py    # reetiqueta y colorea la figura de importancia
python pipeline/06_ranking.py               # evaluación del rankeo
python pipeline/07_figuras_conceptuales.py  # figuras de LoRA, arquitectura y entrenamiento
python borrador/generar_borrador.py         # genera Borrador_Tesis_CareER-GPT_EPG_UNA.docx
```

Dependencias: `pip install -r requirements.txt`, con Python 3.11. Las versiones están fijadas porque pandas 3 y otras versiones de XGBoost cambian ligeramente las cifras del modelo tabular.

Estado: el borrador ya se genera completo, con 18 tablas, 7 figuras y 18 ecuaciones, incluidos los resultados del modelo de lenguaje. Solo faltan las cuatro referencias de la tarea 4 y el enlace del repositorio en el Anexo 2.

## 6. Tareas pendientes, en este orden

### Tarea 1. Verificar el equipo

Ejecutar `nvidia-smi`. El ajuste con QLoRA usa bitsandbytes, que requiere GPU NVIDIA con CUDA y al menos 8 GB de VRAM.

Si el equipo es una Mac con chip Apple M1 a M4 y 16 GB o más de memoria, se puede ajustar con `mlx-lm` y su comando de LoRA, usando el mismo corpus convertido al formato de mensajes. Con GPU AMD o Intel no intentar el entrenamiento local: usar Google Colab con el cuaderno de `colab/`.

### Tarea 2. Entrenar con LoRA (objetivos 3 y 4)

Adaptar el cuaderno de Colab a un script local: quitar `google.colab` y `files.upload`, leer `resultados/CareER_Dataset.jsonl`. Modelo `Qwen/Qwen2.5-1.5B-Instruct`, disponible en https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct. Configuración: r 16, alfa 32, dropout 0.05, módulos q, k, v y o, 4 bits NF4, una época, 6 000 pares, lote efectivo 16, tasa 2e-4 coseno.

Tres condiciones sobre la misma partición de prueba: LLM base sin ajuste, LLM con LoRA sin probabilidades del componente tabular, y CareER-GPT híbrido. Métricas: ROUGE-L, BERTScore con `lang='es'`, coherencia y métrica combinada.

Advertencia documentada: el ROUGE-L entre referencias de personas distintas es 0.836 porque comparten estructura. Por eso la métrica decisiva de H3 es la coherencia, contrastada con prueba binomial exacta unilateral frente a 0.80.

Si el entrenamiento se hace en Colab, el usuario traerá `resultados_llm.zip` con `resultados_llm.json`, `generaciones.csv` y `fig_perdida.png`; descomprimirlo en `resultados/`.

### Tarea 3. Insertar los resultados del modelo de lenguaje en el borrador

En `borrador/contenido2.py` hay textos marcados entre corchetes como pendientes: objetivo 3 en resultados, subsección "Calidad de las rutas generadas" del objetivo 4, conclusiones 3 y 4, resumen y abstract, y el párrafo final de la discusión. Reemplazarlos con los valores de `resultados_llm.json`, agregar una tabla por condición y la curva de pérdida como Figura 7, y regenerar con `python borrador/generar_borrador.py`.

### Tarea 4. Referencias que debe completar el usuario

Behr (2020), Cuentas Yupanqui (2024), Velasquez (2023) y Moreira et al. (2024) están incompletas. Pedirle los datos; no inventarlos.

### Tarea 5. En Word

Al abrir el borrador, presionar Ctrl+A y luego F9 para actualizar índices y numeración. Las ecuaciones solo se visualizan en Word, no en LibreOffice.

## 7. Reglas de trabajo, obligatorias

1. **Nunca inventar resultados.** Si algo no se pudo ejecutar, queda marcado como pendiente.
2. No alterar el formato de la plantilla oficial: usar solo sus estilos (Ttulo2, Ttulo3, Ttulo4, NORML12, NORML3, NORML4L5, TITTBFG, Notas, CONTTBFB, proobjhip, CONCLUT1, RECOMENT1, BIBLIOGRAFIA).
3. Tablas en APA 7: sin sombreado, sin bordes verticales, líneas solo arriba, bajo los encabezados y al final.
4. Figuras a color.
5. Redacción del usuario: no usar la barra `/` como separador, ni el guion largo, ni el guion como viñeta. Español con tildes y ñ correctas. Decimales con punto, como en el proyecto aprobado.
6. Consultar con el usuario antes de cambiar algo que el jurado aprobó.
