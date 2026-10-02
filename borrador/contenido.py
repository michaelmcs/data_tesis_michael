import json, pandas as pd
import os as _os
S = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'resultados') + _os.sep
R = json.load(open(S + 'resultados.json'))
P = R['poblacion']; H = R['h1']; C = R['confusion']; E = R['equidad']; K = R['corpus']
M = pd.read_csv(S + 't_modelos.csv'); F = pd.read_csv(S + 't_pliegues.csv'); Q = pd.read_csv(S + 't_equidad.csv')
TN = pd.read_csv(S + 't_p1_numericas.csv'); TC = pd.read_csv(S + 't_p1_categoricas.csv')
TP = pd.read_csv(S + 't_periodo.csv'); TR = pd.read_csv(S + 't_proceso.csv')
CO = pd.read_csv(S + 't_corpus.csv'); RP = pd.read_csv(S + 't_representatividad.csv')
xg = M[M.modelo == 'XGBoost'].iloc[0]; lr = M[M.modelo == 'Regresión logística'].iloc[0]
rur = Q[Q.grupo == 'RURAL'].iloc[0]; urb = Q[Q.grupo == 'URBANA'].iloc[0]
EJ = R['ejemplo_par']

def n(x, d=0):
    return f'{x:,.{d}f}'.replace(',', ' ')
def f3(x): return f'{x:.3f}'
def f4(x): return f'{x:.4f}'
def pv(p): return '< .001' if p < .001 else f'{p:.3f}'.lstrip('0')

TITULO = ('CAREER-GPT: ARQUITECTURA HÍBRIDA CON LORA SOBRE LLMS Y MODELOS TABULARES PARA LA GENERACIÓN '
          'Y RANKEO DE RUTAS EDUCATIVAS EN POSTULANTES DE LA REGIÓN DE PUNO')

ACRONIMOS = [
    ('AUC-PR', 'Área bajo la curva de precisión y sensibilidad'),
    ('AUC-ROC', 'Área bajo la curva característica operativa del receptor'),
    ('CEPREUNA', 'Centro Preuniversitario de la Universidad Nacional del Altiplano'),
    ('DRE', 'Dirección Regional de Educación'),
    ('EPG', 'Escuela de Posgrado'),
    ('IA', 'Inteligencia artificial'),
    ('LLM', 'Modelo de lenguaje grande (Large Language Model)'),
    ('LoRA', 'Adaptación de bajo rango (Low-Rank Adaptation)'),
    ('MRR', 'Rango recíproco medio (Mean Reciprocal Rank)'),
    ('NDCG', 'Ganancia acumulada descontada normalizada'),
    ('PEFT', 'Ajuste fino eficiente en parámetros'),
    ('PLN', 'Procesamiento de lenguaje natural'),
    ('QLoRA', 'Adaptación de bajo rango cuantizada'),
    ('SIAGIE', 'Sistema de Información de Apoyo a la Gestión de la Institución Educativa'),
    ('TFN', 'Tasa de falsos negativos'),
    ('UGEL', 'Unidad de Gestión Educativa Local'),
    ('UNAP', 'Universidad Nacional del Altiplano de Puno'),
    ('XGBoost', 'Potenciación extrema del gradiente (Extreme Gradient Boosting)'),
]

RESUMEN = (
    'La orientación vocacional en el Perú se apoya en instrumentos que no aprovechan el historial académico de los '
    'postulantes, lo que se asocia con elecciones de carrera poco informadas y con la deserción universitaria. El '
    'objetivo fue desarrollar y validar CareER-GPT, una arquitectura híbrida que combina un modelo tabular XGBoost, '
    'para rankear la probabilidad de ingreso por programa, con un modelo de lenguaje grande ajustado mediante LoRA, '
    'para generar rutas educativas personalizadas. El estudio fue cuantitativo, aplicado y de diseño preexperimental. '
    f'Se integraron los registros de admisión de la Universidad Nacional del Altiplano de 2021-I a 2025-II con el '
    f'historial de secundaria del SIAGIE, y se analizaron {n(P["analizables"])} postulaciones de {n(P["personas_analizables"])} '
    f'personas mediante validación cruzada agrupada por persona. El modelo tabular alcanzó un AUC-ROC de {f3(H["auc"])} '
    f'(IC 95 %: {f3(H["ic_inf"])} a {f3(H["ic_sup"])}) y un AUC-PR de {f3(H["aucpr"])}, frente a una tasa base de '
    f'{f3(M.aucpr.iloc[0])}; no alcanzó el umbral hipotético de 0.85. El promedio de quinto de secundaria, el equipamiento '
    'tecnológico del hogar y la preparación preuniversitaria fueron los predictores de mayor peso. Se identificó una '
    f'brecha de {E["brecha_tfn"]:.1f} puntos en la tasa de falsos negativos en perjuicio de los postulantes de colegios '
    f'rurales. En el rankeo de programas superó al azar, pero no a la ordenación por la tasa histórica de ingreso. '
    f'El corpus de instrucción y respuesta reunió {n(K["pares"])} pares balanceados entre particiones. '
    '[Completar con los resultados del ajuste con LoRA y de la integración híbrida.] Se concluye que el componente '
    'tabular discrimina de manera moderada y que su uso orientador requiere controles de equidad territorial.')
PALABRAS = 'Palabras clave: equidad algorítmica, LoRA, modelos de lenguaje, orientación vocacional, XGBoost.'

ABSTRACT = (
    'Vocational guidance in Peru relies on instruments that do not use applicants\' academic records, which is associated '
    'with poorly informed career choices and university dropout. The aim was to develop and validate CareER-GPT, a hybrid '
    'architecture that combines an XGBoost tabular model, to rank the probability of admission by program, with a large '
    'language model fine-tuned through LoRA, to generate personalized educational pathways. The study was quantitative, '
    'applied and pre-experimental. Admission records of the Universidad Nacional del Altiplano from 2021-I to 2025-II were '
    f'linked with secondary school records from SIAGIE, and {P["analizables"]:,} applications from '
    f'{P["personas_analizables"]:,} individuals were analyzed using person-grouped cross-validation. The tabular model '
    f'reached an AUC-ROC of {f3(H["auc"])} (95% CI: {f3(H["ic_inf"])} to {f3(H["ic_sup"])}) and an AUC-PR of '
    f'{f3(H["aucpr"])}, against a base rate of {f3(M.aucpr.iloc[0])}; it did not reach the hypothesized threshold of 0.85. '
    'The fifth-grade average, household technological equipment and pre-university preparation were the most influential '
    f'predictors. A gap of {E["brecha_tfn"]:.1f} points in the false negative rate was found against applicants from rural '
    f'schools. In program ranking it outperformed random ordering but not ordering by historical admission rate. '
    f'The instruction-response corpus comprised {K["pares"]:,} pairs balanced across partitions. [Complete with the '
    'results of LoRA fine-tuning and hybrid integration.] The tabular component discriminates moderately, and its use for '
    'guidance requires territorial fairness controls.')
KEYWORDS = 'Keywords: algorithmic fairness, language models, LoRA, vocational guidance, XGBoost.'

INTRO = [
    'La transición de la educación secundaria a la universidad es la etapa más vulnerable de la trayectoria académica, '
    'y en ella se concentra buena parte de la deserción universitaria. En el Perú, y de manera particular en la región '
    'de Puno, la decisión de a qué programa postular suele tomarse sin información personalizada sobre las '
    'probabilidades reales de éxito, pese a que las instituciones acumulan registros históricos que podrían orientar '
    'esa decisión. El presente estudio se inscribe en el programa de Maestría en Informática con mención en Gerencia de '
    'Tecnologías de Información y Comunicaciones de la Escuela de Posgrado de la Universidad Nacional del Altiplano, '
    'en la línea de investigación Inteligencia de negocios y datos, sublínea BI, Big Data, aprendizaje automático y '
    'visualización de datos.',
    'El propósito de la investigación fue desarrollar y validar CareER-GPT, una arquitectura híbrida de inteligencia '
    'artificial que combina un modelo tabular, encargado de estimar y ordenar la probabilidad de ingreso de un '
    'postulante en cada programa de estudios, con un modelo de lenguaje grande ajustado mediante adaptación de bajo '
    'rango, encargado de traducir ese ordenamiento en una ruta educativa personalizada y comprensible. Para ello se '
    'integraron los registros de los procesos de admisión de la Universidad Nacional del Altiplano con el historial '
    'académico de educación secundaria registrado en el SIAGIE.',
    'Metodológicamente, el estudio adoptó un enfoque cuantitativo, de tipo aplicado y diseño preexperimental. El '
    'componente tabular se evaluó mediante validación cruzada agrupada por persona, con métricas adecuadas al '
    'desbalance de clases y con una auditoría de equidad entre colegios rurales y urbanos; el componente generativo se '
    'evaluó con métricas de procesamiento de lenguaje natural; y la arquitectura integrada se comparó con sus '
    'componentes individuales.',
    'El informe se organiza en cuatro capítulos. El Capítulo I presenta la revisión de literatura, con el marco teórico '
    'y los antecedentes internacionales, nacionales y locales. El Capítulo II expone el planteamiento del problema, la '
    'justificación, los objetivos y las hipótesis. El Capítulo III describe los materiales y métodos por objetivo '
    'específico. El Capítulo IV presenta los resultados y su discusión. Finalmente se exponen las conclusiones, las '
    'recomendaciones, la bibliografía y los anexos.',
]

MARCO = [
    ('Arquitectura híbrida', [
        'Una arquitectura híbrida combina dos o más métodos, técnicas o arquitecturas distintos para integrar sus '
        'fortalezas y compensar sus limitaciones. En los sistemas de recomendación, por ejemplo, la integración del '
        'filtrado colaborativo con el filtrado basado en contenido ofrece recomendaciones más precisas y '
        'personalizadas, especialmente cuando un solo enfoque resulta insuficiente, como en el arranque en frío o ante '
        'la escasez de datos (Millan, 2025).',
        'Cuando la arquitectura combina modelos de lenguaje de gran tamaño con modelos tabulares, se integra la '
        'capacidad de comprensión contextual de los primeros con la capacidad analítica sobre datos estructurados de '
        'los algoritmos tabulares. Esta colaboración permite procesar de forma conjunta información estructurada y no '
        'estructurada, lo que mejora la adaptabilidad y la precisión en tareas de predicción y clasificación en '
        'dominios como la medicina, la educación o las finanzas (Zheng et al., 2023).']),
    ('Adaptación de bajo rango (LoRA)', [
        'Según Song et al. (2025) y Zhang et al. (2025), LoRA es una técnica para ajustar modelos de lenguaje '
        'preentrenados de gran escala, como los basados en la arquitectura Transformer, a tareas específicas sin '
        'modificar todos sus parámetros. En lugar de recalibrar cada peso, introduce matrices de descomposición de bajo '
        'rango en las capas del modelo, lo que reduce considerablemente la cantidad de parámetros entrenables y hace el '
        'ajuste más eficiente en memoria y cómputo, manteniendo la efectividad del modelo en la tarea. La técnica '
        'resulta especialmente útil en modelos muy grandes, en los que un ajuste completo es poco práctico (Gao et al., '
        '2025; Liu et al., 2025). Su variante cuantizada, QLoRA, permite además ajustar modelos de varios miles de '
        'millones de parámetros en una sola unidad de procesamiento gráfico (Dettmers et al., 2023).',
        'Formalmente, dada una matriz de pesos preentrenada W₀ de dimensión d × k, LoRA no la modifica, sino que '
        'representa su actualización como el producto de dos matrices de bajo rango, B de dimensión d × r y A de '
        'dimensión r × k, con r mucho menor que d y k (Hu et al., 2021). La salida de la capa se calcula como:',
        ('eq', 'LORA'),
        'donde α es un factor de escala que controla la magnitud de la adaptación. La matriz A se inicializa de forma '
        'aleatoria y B en cero, de modo que al inicio del entrenamiento ΔW = BA = 0 y el modelo conserva exactamente su '
        'comportamiento original. El número de parámetros entrenables se reduce de d × k a:',
        ('eq', 'PARAM'),
        'Por ejemplo, en una capa de atención con d = k = 1 536 y r = 16, se pasa de 2 359 296 a 49 152 parámetros '
        'entrenables, es decir, el 2.1 %. La Figura 1 representa este mecanismo.',
        ('fig', 'fig_lora.png', 'Esquema de la adaptación de bajo rango (LoRA) en una capa del modelo',
         'Los pesos preentrenados permanecen congelados y solo se entrenan las matrices A y B. Elaboración propia con base en Hu et al. (2021).'),
        'QLoRA extiende este esquema cuantizando los pesos congelados del modelo base en 4 bits con el tipo de dato '
        'NormalFloat, diseñado para pesos con distribución normal, y aplicando una doble cuantización de las constantes '
        'de escala; los adaptadores A y B se mantienen en mayor precisión (Dettmers et al., 2023).']),
    ('Modelos de lenguaje grandes', [
        'Singhal et al. (2023) definen un modelo de lenguaje grande como una forma avanzada de inteligencia artificial '
        'capaz de comprender y generar lenguaje natural a partir del entrenamiento con grandes volúmenes de texto. '
        'Estos modelos funcionan como arquitecturas fundacionales versátiles, aplicables en campos como la atención '
        'sanitaria, y muestran un potencial significativo en razonamiento, recuperación de información y respuesta a '
        'preguntas, aunque requieren evaluaciones exhaustivas para evitar errores y sesgos (Negueruela Gómez, 2024; '
        'H. Zhang et al., 2026).',
        'Estos modelos se basan en la arquitectura Transformer, cuyo componente central es el mecanismo de atención, '
        'que pondera la relevancia de cada elemento de la secuencia respecto de los demás (Vaswani et al., 2017):',
        ('eq', 'ATTN'),
        'donde Q, K y V son las matrices de consultas, claves y valores obtenidas por proyección lineal de la entrada, y '
        'd_k es la dimensión de las claves. LoRA se aplica precisamente sobre las matrices de proyección de este '
        'mecanismo.',
        'Un modelo de lenguaje causal se entrena para predecir cada elemento de la secuencia a partir de los anteriores, '
        'minimizando la entropía cruzada:',
        ('eq', 'CE'),
        'donde x es la instrucción, y_t el elemento de la respuesta en la posición t, T la longitud de la respuesta y θ '
        'los parámetros entrenables. En el ajuste fino supervisado la pérdida se calcula solo sobre la respuesta, no '
        'sobre la instrucción.']),
    ('Ajuste fino', [
        'El ajuste fino es el proceso mediante el cual se reentrena parcialmente un modelo de lenguaje previamente '
        'entrenado, con el objetivo de adaptar su conocimiento general a un dominio o tarea específica. El enfoque '
        'conserva los parámetros esenciales del modelo y los ajusta con un conjunto de datos especializado, lo que '
        'mejora su precisión y pertinencia en contextos como la medicina o la educación (Li et al., 2023).']),
    ('Modelos tabulares', [
        'Los modelos tabulares son algoritmos de aprendizaje automático especializados en datos estructurados, '
        'organizados en tablas con variables bien definidas. Detectan patrones entre las columnas, que representan '
        'características, y las filas, que representan instancias, lo que les permite realizar tareas de predicción y '
        'clasificación cuando la información tiene una estructura relacional clara, como en bases de datos médicas, '
        'financieras o educativas (Zavala Guirado et al., 2024). Entre ellos destaca XGBoost, un sistema de '
        'potenciación del gradiente sobre árboles de decisión, diseñado para ser escalable y regularizado (Chen y '
        'Guestrin, 2016).',
        'XGBoost construye un conjunto de K árboles de forma secuencial, donde cada árbol corrige los errores de los '
        'anteriores, minimizando una función objetivo que combina la pérdida de predicción con un término de '
        'regularización (Chen y Guestrin, 2016):',
        ('eq', 'XGB1'),
        ('eq', 'XGB2'),
        'donde l es la función de pérdida logística, ŷ_i la predicción para la observación i, T el número de hojas del '
        'árbol, w el vector de pesos de las hojas, y γ y λ los parámetros que penalizan la complejidad para evitar el '
        'sobreajuste.']),
    ('Generación de rutas educativas', [
        'La generación de rutas educativas es un proceso basado en el análisis de datos académicos, personales y '
        'vocacionales, cuyo objetivo es recomendar itinerarios de formación personalizados. La combinación de modelos '
        'predictivos tabulares con modelos de lenguaje permite identificar patrones de rendimiento, intereses y riesgos, '
        'y diseñar trayectorias adaptadas al perfil y al contexto de cada estudiante (Cen et al., 2024; Nass et al., '
        '2023).']),
    ('Aprendizaje en contexto', [
        'El aprendizaje en contexto es la capacidad de los modelos de lenguaje de gran escala para resolver nuevas '
        'tareas a partir de ejemplos o instrucciones incluidos en la entrada, sin modificar sus parámetros internos. Se '
        'basa en los mecanismos de atención y constituye una alternativa flexible al ajuste tradicional (Kung et al., '
        '2023).']),
    ('Rankeo de rutas educativas', [
        'El rankeo de rutas educativas consiste en ordenar las alternativas de formación de un estudiante según un '
        'criterio de pertinencia, como la probabilidad estimada de éxito en cada programa. La integración de modelos '
        'predictivos tabulares con modelos de lenguaje permite identificar patrones de rendimiento académico, '
        'inclinaciones de interés y riesgos de abandono, y presentar las alternativas ordenadas de acuerdo con las '
        'características y antecedentes individuales (Fernandez et al., 2025; Navarro Forero et al., 2025).']),
    ('Orientación vocacional', [
        'Según Cisneros-Bravo et al. (2023) y Alejandro (2024), la orientación vocacional es un proceso educativo y '
        'psicológico que ayuda a los estudiantes a explorar sus intereses, valores y habilidades, para tomar decisiones '
        'académicas acordes con su proyecto de vida. En la actualidad este proceso incorpora herramientas tecnológicas '
        'e inteligencia artificial para ofrecer asesoramiento personalizado y mejorar la retención universitaria (Flores '
        'Meléndez et al., 2020).']),
    ('Perfil del estudiante', [
        'El perfil del estudiante describe sus habilidades, intereses, motivaciones, rendimiento académico y '
        'capacidades tecnológicas. Esta información es fundamental para orientar las decisiones educativas y adaptar el '
        'proceso de aprendizaje, y puede ser procesada mediante modelos de lenguaje y análisis de datos para construir '
        'itinerarios específicos para cada contexto (Yupanquin, 2024).']),
    ('Éxito académico y retención estudiantil', [
        'El éxito académico es el grado en que los estudiantes alcanzan las metas de aprendizaje establecidas por el '
        'sistema educativo, y se manifiesta en un rendimiento constante, satisfacción personal y capacidad sostenida '
        'para cursar estudios universitarios (Aguilar-Reyes et al., 2025). En esta investigación, el éxito se '
        'operacionaliza como el ingreso a la universidad en el programa postulado.',
        'La retención estudiantil comprende las estrategias institucionales y personales orientadas a que los '
        'estudiantes culminen sus estudios. Ambos aspectos dependen de factores vocacionales, académicos y '
        'tecnológicos, y pueden fortalecerse con modelos de inteligencia artificial que anticipan riesgos y '
        'personalizan la intervención educativa (Muñoz Pilozo et al., 2024; Sabando Moreira y Zambrano Montenegro, 2024).']),
    ('Desempeño académico', [
        'El desempeño académico es el resultado del proceso de aprendizaje reflejado en el nivel de rendimiento del '
        'estudiante, y se mide mediante calificaciones, evaluaciones, logro de objetivos y desarrollo de competencias '
        '(Jardon et al., 2024). Desde un enfoque integral, no depende solo de las habilidades cognitivas, sino también '
        'de la motivación, de la adecuación entre intereses y carrera elegida y de las condiciones institucionales '
        '(Escalante López et al., 2023). La literatura reciente destaca además la autoeficacia, la gestión del tiempo y '
        'la percepción del apoyo institucional como factores de la perseverancia (Rodas, 2024).']),
    ('Deserción estudiantil', [
        'La deserción es el abandono del proceso educativo antes de su culminación. Según Torres-Delgado et al. (2024), '
        'es un fenómeno multicausal en el que se entrelazan factores académicos, sociales, familiares y personales que '
        'afectan la decisión de dejar los estudios.']),
    ('Inteligencia artificial', [
        'La inteligencia artificial es la rama de la informática dedicada al diseño, desarrollo y aplicación de '
        'sistemas capaces de realizar tareas que antes requerían inteligencia humana, como el razonamiento lógico, el '
        'aprendizaje a partir de datos, la comprensión del lenguaje natural y la toma de decisiones (Ramos-Rivera et '
        'al., 2025; Sancho Escrivá et al., 2020).']),
    ('Equidad algorítmica', [
        'La equidad algorítmica estudia si un modelo predictivo distribuye sus errores de manera homogénea entre grupos '
        'de población. En contextos de orientación, un indicador relevante es la tasa de falsos negativos, que mide la '
        'proporción de personas que efectivamente logran el resultado pero a quienes el modelo asigna una baja '
        'probabilidad; una tasa mayor en un grupo implica que el sistema desalentaría de forma desproporcionada a sus '
        'integrantes con potencial. Por ello, la evaluación de modelos con fines educativos debe complementar las '
        'métricas globales con métricas desagregadas por grupo.',
        ('eq', 'TFN'),
        'donde FN son los falsos negativos y VP los verdaderos positivos de cada grupo.']),
]

ANT_INT = [
    'García y Serradilla (2021) tuvieron como objetivo desarrollar técnicas de clasificación de textos que alcanzaran '
    'el estado del arte sin requerir grandes recursos computacionales, y ampliar los modelos de lenguaje para el '
    'español ante la escasez de recursos para esta lengua. Emplearon modelos basados en la arquitectura Transformer y '
    'BERT, y obtuvieron resultados alineados con el estado del arte, que evidencian la eficiencia de modelos abiertos de '
    'tamaño moderado. Concluyeron que existe un interés insuficiente de la industria y la academia por los modelos '
    'neuronales en español, lo que representa un nicho para el desarrollo de recursos en este idioma.',
    'Mena (2023) se propuso evaluar modelos de lenguaje masivos en español, comparar LLaMA2-Chat, Mistral y Falcon, y '
    'estudiar su adaptación para generar chatbots en Ecuador. Probó modelos de 7 mil millones de parámetros ajustados '
    'mediante QLoRA. Los tres modelos mejoraron tras el ajuste, con Mistral destacando en tareas complejas y Falcon en '
    'tareas creativas, aunque algunos modelos ajustados mostraron respuestas imprecisas. Concluyó que la memoria de '
    'video fue una limitación importante, que el ajuste fue exitoso y que Mistral obtuvo el mejor desempeño global, y '
    'recomendó explorar RAG y mezcla de expertos.',
    'Hu et al. (2021) aplicaron la adaptación de bajo rango para entrenar parámetros específicos de la tarea sin '
    'modificar los pesos preentrenados. Demostraron que LoRA es competitivo en tareas de comprensión del lenguaje '
    'natural, como GLUE y WikiSQL, frente al ajuste fino tradicional, y concluyeron que reduce significativamente los '
    'requisitos de memoria, el costo computacional y el tiempo de entrenamiento sin afectar el rendimiento.',
    'Dettmers et al. (2023) propusieron QLoRA, un método que retropropaga gradientes a través de un modelo cuantizado '
    'en 4 bits hacia adaptadores de bajo rango. Con esta técnica ajustaron un modelo de 65 mil millones de parámetros en '
    'una sola unidad de procesamiento gráfico de 48 GB, y su mejor modelo alcanzó un desempeño cercano al de ChatGPT en '
    'el benchmark de Vicuna. Concluyeron que la cuantización no degrada el desempeño del ajuste fino de 16 bits y que '
    'democratiza el ajuste de modelos grandes.',
    'Armando et al. (2023), en la investigación titulada "URKU: Adaptación de LLaMA 2 para la generación de texto en '
    'kichwa usando técnicas de Low-Rank Adaptation (LoRA)", tuvieron como propósito adaptar LLaMA 2 al kichwa, crear un '
    'corpus de alta calidad y establecer un benchmark para la evaluación, generación y traducción de textos. El modelo '
    'URKU superó a modelos previos en generación de texto en kichwa, y los autores concluyeron que constituye un avance '
    'para la inclusión lingüística y la preservación cultural en idiomas con recursos limitados.',
    'Castejon (2025) diseñó, implementó y evaluó un sistema conversacional que permite consultar en lenguaje natural la '
    'información del Museo Sorolla, con preguntas estructuradas por categorías de uso. El clasificador de intención '
    'alcanzó una precisión global de 88 % y un F1 de 0.88, con 0.94 en la clase SQL; el componente RAG obtuvo una '
    'relevancia de contexto de 0.98 y una fidelidad de 0.67. Concluyó que el sistema, que integra LLM, RAG y Text2SQL, '
    'funciona eficazmente y que una ingeniería de instrucciones adecuada elimina las alucinaciones.',
    'Fang et al. (2024) realizaron una revisión extensa de los modelos de lenguaje grandes aplicados a datos tabulares '
    'en predicción, generación de datos y comprensión de tablas. Analizaron técnicas, métricas y enfoques, y compararon '
    'estos modelos con los árboles de decisión en conjuntos grandes y heterogéneos. Encontraron una gran capacidad de '
    'los LLM para tareas complejas, con debilidades en generalización e interpretabilidad, y concluyeron que se '
    'requiere más investigación para mejorar su rendimiento y adaptabilidad.',
    'Fernandez et al. (2025) estudiaron el ajuste fino de modelos de lenguaje para convertirlos en tutores de '
    'matemática y física en educación básica, entrenándolos con problemas específicos como los del conjunto GSM8K. Los '
    'resultados mostraron que el ajuste fino mejora la precisión en la resolución de problemas y la claridad con que '
    'el modelo explica los conceptos, lo que lo convierte en una herramienta educativa valiosa en ciencias.',
    'En otro estudio, Fernandez et al. (2025) optimizaron grandes modelos de lenguaje mediante técnicas de ajuste '
    'eficiente sobre infraestructura de alto rendimiento, como el supercomputador Clementina XXI, con el objetivo de '
    'mejorar la eficiencia computacional y el rendimiento en seguridad, biología y educación. Emplearon LoRA, QLoRA, '
    'ajuste con adaptadores y mezcla de expertos, evaluaron la eficacia de estas técnicas y establecieron repositorios '
    'abiertos para la reproducibilidad, reduciendo el costo y la duración del entrenamiento.',
    'Ramos-Rivera et al. (2025) analizaron la aplicación de modelos de lenguaje grandes para mejorar el análisis de las '
    'respuestas abiertas en la evaluación del desempeño docente. Mediante modelos específicos de dominio, modelos de '
    'lenguaje pequeños y modelos en la nube con menos iteraciones de entrenamiento, buscaron mitigar las alucinaciones. '
    'Los resultados indicaron que los LLM reducen sustancialmente el tiempo de procesamiento de las evaluaciones y '
    'mejoran la toma de decisiones en las instituciones educativas.',
    'Millan (2025), en el estudio "Estudio comparativo de sistemas de recomendación mediante filtrado colaborativo, '
    'basado en contenido y propuestas híbridas", comparó el rendimiento de los tres tipos de sistemas con datos de '
    'Goodreads que incluyeron 93 398 libros, 34 919 254 interacciones y 2 389 900 reseñas. Los modelos híbridos mejoraron '
    'la calidad de las recomendaciones al superar la sobreespecialización y la escasez de datos, y concluyó que '
    'combinan eficientemente ambos enfoques con mejoras en precisión, diversidad y adaptabilidad.',
    'Martínez Sixto et al. (2025) evaluaron el desempeño de seis modelos de lenguaje grandes dentro de un sistema de '
    'generación aumentada por recuperación para producir diagramas de clases UML a partir de historias de usuario. '
    'Entre los modelos evaluados figuraron Gemini 2.5 Pro, Claude Sonnet 4, GPT-4 y Llama 3.2. Claude Sonnet 4, Gemini '
    '2.5 Pro y GPT-4 obtuvieron el mejor desempeño, y el estudio mostró que la efectividad de RAG depende en gran medida '
    'de la calidad y relevancia del contexto recuperado.',
    'Cisneros-Bravo et al. (2023) exploraron cómo la falta de orientación vocacional influye en la deserción '
    'universitaria. Mediante una metodología mixta encuestaron a 231 estudiantes de bachillerato: el 36.8 % no había '
    'recibido orientación vocacional y el 87 % manifestó interés en contar con herramientas de orientación. Concluyeron '
    'que la falta de orientación es un factor clave de la deserción y que deben fortalecerse estas herramientas en el '
    'nivel medio superior.',
    'Carballo-Mendívil et al. (2025) diseñaron un sistema de alerta temprana para predecir la deserción universitaria '
    'desde la inscripción, con información académica, socioeconómica y demográfica de cerca de 40 000 estudiantes de '
    'una universidad pública de México. Siguiendo la metodología CRISP-DM, el algoritmo XGBoost obtuvo un AUC-ROC de '
    '0.69 y una sensibilidad de 88 %. La edad, el promedio de bachillerato y las condiciones económicas y familiares '
    'fueron determinantes, y el modelo permitió identificar estudiantes en riesgo antes del inicio del ciclo.',
]
ANT_NAC = [
    'Balarezo et al. (2024) diseñaron un asistente conversacional basado en arquitectura RAG para optimizar la '
    'búsqueda, recuperación y análisis de resoluciones históricas de la Comisión de Eliminación de Barreras '
    'Burocráticas del INDECOPI. El diseño optimizó la búsqueda contextual, redujo los tiempos de revisión, análisis y '
    'redacción, y mejoró la precisión de las respuestas frente a los buscadores tradicionales; concluyeron que su '
    'implementación es viable, pertinente y beneficiosa.',
    'Yatco y Jacha (2024), en la investigación "Modelo de machine learning para predicción de deserción estudiantil", '
    'desarrollaron un modelo predictivo de la deserción en el Perú con datos de la Encuesta Nacional de Hogares y una '
    'amplia gama de variables sociodemográficas. El modelo mostró potencial para la identificación temprana de '
    'estudiantes en riesgo, y los autores recomendaron explorar modelos híbridos y técnicas de aprendizaje profundo.',
    'Guadalupe y Rodriguez (2025), en el estudio "Modelo predictivo basado en machine learning para la reducción de la '
    'deserción estudiantil en las universidades privadas del Perú: caso Universidad Privada San Juan Bautista", '
    'desarrollaron un modelo predictivo con enfoque cuantitativo y diseño preexperimental longitudinal. El modelo '
    'anticipó eficazmente la deserción, y concluyeron que los factores personales, académicos y socioeconómicos son '
    'determinantes y que las intervenciones específicas pueden mejorar la retención.',
    'Rodas (2024), en la investigación "Orientación vocacional y deserción universitaria en una universidad de Lima '
    '- 2024", exploró la relación entre ambas variables con enfoque cuantitativo y diseño no experimental en una '
    'muestra de 103 estudiantes de ingeniería. Encontró una correlación inversa significativa: a mayor orientación '
    'vocacional, menor deserción, además de la influencia de factores externos, institucionales, académicos y '
    'personales.',
    'Velasquez Velasquez (2023) realizó una revisión sistemática de la literatura sobre inteligencia artificial aplicada al '
    'sector educativo, siguiendo la propuesta de Kitchenham, con el fin de proporcionar una estructura para futuras '
    'investigaciones. Entre los resultados destacaron las aplicaciones de tutores inteligentes.',
]
ANT_LOC = [
    'Rodriguez (2023) analizó la relación entre la inteligencia artificial y el rendimiento académico de los '
    'estudiantes de la Universidad Nacional del Altiplano, en la región Puno, mediante un enfoque cuantitativo, diseño '
    'no experimental descriptivo y encuestas aplicadas a una muestra censal de 82 estudiantes. Encontró que la '
    'inteligencia artificial tiene un efecto positivo en el rendimiento académico, principalmente en lo referido al '
    'aprendizaje automático, la tecnología de código abierto y los dispositivos portátiles, y concluyó que puede '
    'contribuir a mejorar la calidad de la educación en la región.',
]

IDENT = [
    'La deserción universitaria constituye uno de los problemas estructurales más serios de los sistemas de educación '
    'superior. La evidencia internacional coincide en que el abandono se concentra en los primeros años de estudio, '
    'cuando los estudiantes enfrentan las mayores dificultades de adaptación académica, emocional y vocacional, lo que '
    'convierte la transición de la secundaria a la universidad en el periodo más vulnerable de la trayectoria. El '
    'fenómeno implica pérdidas personales y familiares, y costos para las instituciones y la sociedad.',
    'En América Latina la magnitud del problema es particularmente alta. Según el Banco Mundial, cerca de la mitad de '
    'la población de 25 a 29 años que inició estudios superiores no llegó a culminarlos (Ferreyra et al., 2017), y las '
    'cifras de deserción en el primer año, antes de la pandemia, rondaban el 31 % en Colombia, el 21 % en Chile y el 33 % '
    'en el Perú (Behr et al., 2020, como se citó en Escalante López et al., 2023).',
    'En el caso peruano, según el II Informe Bienal sobre la Realidad Universitaria de la SUNEDU, alrededor del 15.8 % '
    'de los estudiantes abandonó las aulas universitarias entre 2012 y 2018 (Superintendencia Nacional de Educación '
    'Superior Universitaria, 2020), y la limitada disponibilidad de herramientas de orientación vocacional basadas en '
    'evidencia agrava este panorama. Escalante López et al. (2023) señalan que la deserción sigue siendo un problema no '
    'resuelto, asociado a factores económicos, familiares, vocacionales y motivacionales, y que la falta de orientación '
    'y de estrategias preventivas limita la permanencia.',
    'En la región de Puno el panorama se intensifica por las desigualdades socioeconómicas y geográficas del Altiplano '
    'y por el limitado acceso a información vocacional personalizada. La deserción y el bajo rendimiento representan '
    'desafíos críticos para la Universidad Nacional del Altiplano (Escobar-Mamani y Cuentas Yupanqui, 2024), institución en la que la '
    'inteligencia artificial ha mostrado potencial para mejorar el rendimiento académico (Rodriguez, 2023).',
    'Entre las causas del problema destaca la ausencia de sistemas predictivos que aprovechen los datos académicos '
    'históricos de los postulantes: aunque la universidad y el sistema educativo regional registran los resultados de '
    'admisión y el historial de secundaria, esa información no se utiliza para orientar a quienes postulan. Sus efectos '
    'se manifiestan en elecciones vocacionales poco informadas, bajo rendimiento y mayor abandono. Las variables '
    'involucradas son, por un lado, la arquitectura híbrida de inteligencia artificial propuesta y, por otro, la '
    'precisión en la generación y el rankeo de rutas educativas personalizadas.',
    'En este contexto, una arquitectura híbrida que combine modelos tabulares con modelos de lenguaje grandes ajustados '
    'mediante LoRA podría estimar las probabilidades de éxito de cada postulante por programa y traducirlas en rutas '
    'educativas personalizadas y comprensibles, lo que da lugar a las interrogantes de la investigación.',
]
ENUNC = ('A partir de la situación descrita, la investigación se orienta a determinar en qué medida la arquitectura '
         'propuesta optimiza la generación y el rankeo de rutas educativas, a través de las siguientes preguntas.')
PG = ('¿En qué medida una arquitectura híbrida de inteligencia artificial que combine modelos tabulares y modelos de '
      'lenguaje grandes ajustados con LoRA puede optimizar la generación y el rankeo de rutas educativas personalizadas '
      'para postulantes universitarios de la región de Puno?')
PE = [
    '¿Qué variables académicas, demográficas y socioeducativas predicen mejor la probabilidad de éxito académico por '
    'carrera, y con qué capacidad discriminativa lo hace el modelo tabular XGBoost?',
    '¿Cómo transformar los datos de los postulantes en entradas textuales representativas, coherentes y balanceadas '
    'para el entrenamiento del modelo de lenguaje?',
    '¿Qué efectividad tiene el ajuste fino con LoRA para generar rutas educativas relevantes y contextualizadas?',
    '¿Cuál es el desempeño de la arquitectura híbrida comparada con sus modelos individuales?',
]
JUST = [
    'La deserción universitaria es un desafío serio en la educación superior peruana, especialmente en la región de '
    'Puno, donde existen marcadas desigualdades en el acceso a información y apoyo para elegir una carrera. La brecha '
    'entre las capacidades de los postulantes y las rutas educativas que eligen incide en la deserción y en la falta de '
    'coincidencia entre habilidades, intereses y trayectorias formativas (Rodas, 2024). Con frecuencia los postulantes '
    'eligen una carrera sin información previa adecuada, lo que conduce a su abandono o a cambios de programa.',
    'Desde el punto de vista práctico, la investigación se justifica en la necesidad de herramientas tecnológicas '
    'escalables que no solo estimen la probabilidad de éxito de un postulante, sino que ofrezcan itinerarios '
    'personalizados y comprensibles para una decisión informada. Una orientación vocacional basada en evidencia '
    'favorece la elección de programas acordes con las capacidades del estudiante, lo que contribuye a la retención y '
    'fortalece la capacidad de orientación de las universidades de la región.',
    'Desde el punto de vista teórico y metodológico, el estudio cubre un vacío en la aplicación de arquitecturas '
    'híbridas de inteligencia artificial en educación, particularmente en contextos con recursos computacionales '
    'limitados. La combinación de la adaptación de bajo rango con modelos de lenguaje grandes ofrece un enfoque '
    'replicable y escalable, e incorpora además una auditoría de equidad territorial que permite verificar que el '
    'sistema no perjudique a los postulantes de zonas rurales, aspecto escasamente explorado en la orientación '
    'vocacional apoyada en inteligencia artificial.',
]
OBJ_INTRO = ('Los objetivos expresan la intención del estudio y se formulan en correspondencia con los problemas y las '
             'hipótesis de investigación.')
OG = ('Desarrollar y validar la arquitectura híbrida CareER-GPT, basada en LoRA sobre modelos de lenguaje grandes y '
      'modelos tabulares, para la generación y el rankeo de rutas educativas personalizadas en postulantes de la región '
      'de Puno.')
OE = [
    'Entrenar y evaluar un modelo tabular XGBoost para el rankeo de probabilidades de éxito por carrera.',
    'Preparar y transformar el conjunto de datos de postulantes en pares de instrucción y respuesta para el '
    'entrenamiento del modelo de lenguaje.',
    'Ajustar un modelo de lenguaje grande mediante LoRA para la generación automática de rutas educativas '
    'contextualizadas.',
    'Integrar ambos modelos en una arquitectura unificada y validar su eficacia comparativa.',
]
HG = ('La arquitectura híbrida CareER-GPT, basada en LoRA sobre modelos de lenguaje grandes y modelos tabulares, genera '
      'y rankea rutas educativas personalizadas con una precisión significativamente alta para los postulantes de la '
      'región de Puno.')
HE = [
    'El modelo tabular XGBoost alcanza un AUC-ROC de al menos 0.85 en la estimación de la probabilidad de éxito por '
    'carrera.',
    'La transformación del conjunto de datos de postulantes en pares de instrucción y respuesta permite generar un '
    'corpus representativo, coherente y balanceado del perfil académico y vocacional, adecuado para el entrenamiento '
    'del modelo de lenguaje.',
    'El ajuste fino con LoRA permite al modelo de lenguaje generar rutas educativas con coherencia contextual superior '
    'al 80 %.',
    'La integración híbrida supera el rendimiento de cada modelo por separado en al menos un 10 % en métricas '
    'combinadas de clasificación, ranking y fidelidad.',
]

LUGAR = [
    'La investigación se desarrolló en la Universidad Nacional del Altiplano de Puno, ubicada en la ciudad de Puno, '
    'provincia y región de Puno, Perú, a una altitud aproximada de 3 827 m s. n. m., en las coordenadas '
    '15°50′24″ S y 70°01′19″ O. La universidad es la principal institución pública de educación superior de la región '
    'y recibe postulantes de sus trece provincias, tanto de zonas urbanas como rurales.',
    'La región de Puno presenta marcadas desigualdades socioeconómicas y geográficas: una parte importante de su '
    'población reside en zonas rurales altoandinas, con predominio de las lenguas quechua y aimara y con acceso '
    'desigual a servicios básicos y tecnológicos. Estas condiciones hacen de la región un escenario pertinente para '
    'estudiar sistemas de orientación vocacional que, además de ser precisos, no reproduzcan las brechas territoriales.',
]
POBL = [
    f'La población está conformada por la totalidad de postulaciones registradas en la Universidad Nacional del '
    f'Altiplano de Puno en los procesos de admisión comprendidos entre 2021-I y 2025-II, que suman {n(P["postulaciones"])} '
    f'postulaciones correspondientes a {n(P["personas"])} personas distintas, en todas las modalidades de admisión. La '
    'información se obtuvo de la Oficina de Admisión, con autorización del Vicerrectorado Académico, y del historial de '
    'educación secundaria registrado en el SIAGIE, vinculados mediante un identificador anónimo común.',
    'El periodo difiere del consignado en el proyecto aprobado, que se formuló con una estimación previa a la entrega '
    'de los datos. Se incorporaron los procesos de 2021 porque permiten reconstruir las postulaciones previas de '
    'quienes volvieron a postular a partir de 2022, variable considerada en el modelo, y se excluyeron los procesos de '
    '2026 por corresponder a un año lectivo en curso.',
    'Criterios de inclusión: postulaciones con resultado registrado en el examen y con historial académico de '
    'educación secundaria emparejable en el SIAGIE. Criterios de exclusión: postulantes ausentes al examen y '
    'postulaciones sin historial escolar. La conformación del conjunto analítico se presenta en la Tabla 1.',
]
MUESTRA = [
    'Dado que se trabajó con la totalidad de los registros disponibles que cumplen los criterios de elegibilidad, el '
    'estudio adoptó un diseño censal y no se aplicó técnica de muestreo ni fórmula de cálculo muestral. La unidad de '
    'análisis es la postulación, porque una misma persona puede postular en más de un proceso y cada postulación '
    'constituye un evento con resultado propio.',
    f'El conjunto analítico comprende {n(P["analizables"])} postulaciones de {n(P["personas_analizables"])} personas, '
    f'con una tasa de ingreso de {P["tasa_ingreso"]:.2f} %. Para la validación de los modelos, este conjunto se dividió '
    'en cinco pliegues estratificados y agrupados por persona, de modo que ninguna persona aparezca simultáneamente en '
    'entrenamiento y prueba; para el modelo de lenguaje, los pares se dividieron en 70 % para entrenamiento, 15 % para '
    'validación y 15 % para prueba, también agrupados por persona.',
]
METODO = [
    'El estudio adoptó un enfoque cuantitativo, de tipo aplicado y de nivel predictivo, con diseño preexperimental: la '
    'arquitectura propuesta constituye la intervención, cuyo desempeño se evalúa sobre datos históricos y se compara '
    'con modelos de referencia. Las variables de estudio son la arquitectura híbrida CareER-GPT, como variable '
    'independiente, y la precisión en la generación y el rankeo de rutas educativas, como variable dependiente, medida '
    'mediante la capacidad discriminativa del modelo tabular, la calidad textual de las rutas generadas y la equidad '
    'algorítmica entre zonas rurales y urbanas. Se consideraron como variables intervinientes la calidad del conjunto '
    'de datos histórico y la capacidad computacional disponible.',
    'La Figura 2 presenta la arquitectura propuesta. El componente tabular estima, para cada postulante, la '
    'probabilidad de ingreso en cada programa, la calibra y ordena los programas; ese ordenamiento se incorpora a la '
    'instrucción que recibe el componente lingüístico, un modelo de lenguaje ajustado con LoRA que genera la ruta '
    'educativa en lenguaje natural.',
    ('fig', 'fig_arquitectura.png', 'Arquitectura híbrida CareER-GPT',
     'La integración opera en cascada: la salida calibrada del componente tabular es el contexto del componente lingüístico. Elaboración propia.'),
]
