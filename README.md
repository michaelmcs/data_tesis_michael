# CareER-GPT

Datos y programas de la tesis de maestría **CareER-GPT: Arquitectura Híbrida con LoRA sobre LLMs y Modelos Tabulares para la Generación y Rankeo de Rutas Educativas en Postulantes de la Región de Puno**.

Autor: Michael Newton Cutipa Santi. Maestría en Informática con mención en Gerencia de Tecnologías de Información y Comunicaciones, Escuela de Posgrado, Universidad Nacional del Altiplano de Puno.

## Contenido

| Carpeta | Contenido |
|---|---|
| `datos/` | Bases anonimizadas de admisión y del SIAGIE, unidas por un identificador anónimo |
| `pipeline/` | Programas en Python de preprocesamiento, modelos, pruebas estadísticas y rankeo |
| `resultados/` | Tablas, figuras, métricas y el corpus CareER-Dataset en formato JSONL |
| `colab/` | Cuaderno de Google Colab para el ajuste del modelo de lenguaje con LoRA |
| `borrador/` | Programas que generan el borrador de tesis sobre la plantilla oficial |
| `plantilla/` | Plantilla del borrador de tesis de la EPG UNA |
| `documentos/` | Proyecto aprobado y acta de aprobación |

## Cómo reproducir los resultados

Se requiere Python 3.11. Desde la raíz del repositorio:

```
pip install -r requirements.txt
python pipeline/01_preprocesamiento.py
python pipeline/03_resultados.py
python pipeline/05_figura_importancia.py
python pipeline/06_ranking.py
python pipeline/07_figuras_conceptuales.py
python borrador/generar_borrador.py
```

Las versiones de las bibliotecas están fijadas en `requirements.txt` porque otras versiones de pandas y XGBoost cambian ligeramente las cifras del modelo tabular.

El ajuste del modelo de lenguaje requiere una GPU NVIDIA y se ejecuta con el cuaderno de `colab/`, subiendo el archivo `resultados/CareER_Dataset.jsonl`. Sus resultados se guardan en `resultados/resultados_llm.json`, `resultados/generaciones.csv` y `resultados/fig_perdida.png`.
