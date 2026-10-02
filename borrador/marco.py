"""Marco teórico del borrador, organizado de lo general a lo específico.

Cada subtítulo es una tupla (título, [párrafos o ('eq', clave) o ('fig', archivo, título, nota)]). Las citas se escriben en
texto plano con el formato autor y año, y el generador las convierte en citas de Mendeley.
"""

MARCO = [
    ('Arquitectura híbrida', [
        'Una arquitectura híbrida combina dos o más métodos, técnicas o arquitecturas distintos para integrar sus '
        'fortalezas y compensar sus limitaciones. En los sistemas de recomendación, por ejemplo, la integración del '
        'filtrado colaborativo con el filtrado basado en contenido ofrece recomendaciones más precisas y '
        'personalizadas, especialmente cuando un solo enfoque resulta insuficiente, como en el arranque en frío o ante '
        'la escasez de datos (Millán Gordillo, 2025).',
        'Cuando la arquitectura combina modelos de lenguaje de gran tamaño con modelos tabulares, se integra la '
        'capacidad de comprensión contextual de los primeros con la capacidad analítica sobre datos estructurados de '
        'los algoritmos tabulares. Esta colaboración permite procesar de forma conjunta información estructurada y no '
        'estructurada, lo que mejora la adaptabilidad y la precisión en tareas de predicción y clasificación en '
        'dominios como la medicina, la educación o las finanzas (Zheng et al., 2023).',
        'Fang et al. (2024) señalan que los modelos de lenguaje, aunque muestran una gran capacidad para tareas '
        'complejas, presentan debilidades en la generalización e interpretabilidad cuando trabajan directamente sobre '
        'datos tabulares, y comparan su desempeño con el de los modelos basados en árboles de decisión. Por ello, una alternativa consiste en '
        'distribuir las responsabilidades: el modelo tabular realiza la estimación numérica sobre los datos '
        'estructurados y el modelo de lenguaje recibe ese resultado como contexto para redactar una respuesta en '
        'lenguaje natural. Este es el esquema que adopta la presente investigación, en el que la probabilidad de '
        'ingreso por programa se calcula fuera del modelo de lenguaje y este se limita a comunicarla.']),

    ('Inteligencia artificial y aprendizaje automático', [
        'La inteligencia artificial es la rama de la informática dedicada al diseño, desarrollo y aplicación de '
        'sistemas capaces de realizar tareas que antes requerían inteligencia humana, como el razonamiento lógico, el '
        'aprendizaje a partir de datos, la comprensión del lenguaje natural y la toma de decisiones (Ramos-Rivera et '
        'al., 2025; Sancho Escrivá et al., 2020).',
        'El aprendizaje automático es el área de la inteligencia artificial que construye modelos a partir de datos, '
        'sin programar reglas de forma explícita. En el aprendizaje supervisado, el modelo aprende una función que '
        'relaciona un conjunto de variables de entrada, llamadas predictores, con una variable de salida conocida en '
        'los datos históricos. Cuando la salida es una cantidad continua se trata de un problema de regresión, y '
        'cuando es una categoría, como ingresar o no ingresar a la universidad, se trata de un problema de '
        'clasificación. En este último caso, la mayoría de los algoritmos no entregan solo una categoría, sino una '
        'puntuación o probabilidad de pertenencia a la clase de interés (Hastie et al., 2009).',
        'La construcción de un modelo supervisado sigue un procedimiento general. Primero se define la variable '
        'objetivo y se identifican los predictores que estarán disponibles en el momento en que se usará el modelo. '
        'Luego se preparan los datos, lo que incluye la integración de fuentes, el tratamiento de valores faltantes y '
        'la construcción de variables derivadas. A continuación se separan los datos en subconjuntos para entrenar y '
        'para evaluar, se ajustan los hiperparámetros del algoritmo con datos de validación y, finalmente, se estima '
        'el desempeño con observaciones que el modelo no utilizó durante el entrenamiento (Hastie et al., 2009).',
        'El principal riesgo de este procedimiento es el sobreajuste, que ocurre cuando el modelo memoriza '
        'particularidades de los datos de entrenamiento en lugar de aprender patrones generalizables, de modo que su '
        'desempeño en datos nuevos es inferior al observado durante el entrenamiento. El equilibrio entre un modelo '
        'demasiado simple, que no capta la relación, y uno demasiado complejo, que se ajusta al ruido, se conoce como '
        'el compromiso entre sesgo y varianza, y se controla mediante la regularización y la evaluación con datos '
        'independientes (Hastie et al., 2009).',
        'Un problema relacionado es la fuga de información, que se produce cuando el modelo utiliza durante el '
        'entrenamiento datos que no estarían disponibles en el momento real de la predicción. Kaufman et al. (2012) '
        'muestran que la fuga produce estimaciones de desempeño optimistas que no se sostienen al implementar el '
        'modelo, y que suele originarse en variables registradas después del evento que se quiere predecir. En la '
        'predicción del ingreso universitario, el puntaje del examen o el orden de mérito son ejemplos de este tipo de '
        'variables, por lo que deben excluirse de los predictores.']),

    ('Modelos tabulares', [
        'Los modelos tabulares son algoritmos de aprendizaje automático especializados en datos estructurados, '
        'organizados en tablas con variables bien definidas. Detectan patrones entre las columnas, que representan '
        'características, y las filas, que representan instancias, lo que les permite realizar tareas de predicción y '
        'clasificación cuando la información tiene una estructura relacional clara, como en bases de datos médicas, '
        'financieras o educativas (Zavala Guirado et al., 2024).',
        'El árbol de decisión es el bloque básico de muchos de estos modelos. Se construye mediante una partición '
        'recursiva de los datos: en cada nodo, el algoritmo evalúa las posibles divisiones de cada variable y elige '
        'aquella que separa mejor las observaciones según la variable objetivo, de acuerdo con un criterio de '
        'impureza o de pérdida. El proceso se repite en cada subconjunto hasta alcanzar una profundidad máxima o un '
        'número mínimo de observaciones por nodo, y cada hoja final asigna una predicción. Los árboles son fáciles de '
        'interpretar y capturan interacciones entre variables, pero un árbol individual es inestable, porque pequeños '
        'cambios en los datos pueden modificar su estructura (Hastie et al., 2009).',
        'Para superar esa inestabilidad se combinan muchos árboles en un ensamble. Existen dos estrategias '
        'principales. En el bosque aleatorio, cada árbol se entrena de forma independiente con una muestra '
        'aleatoria de las observaciones y de las variables, y la predicción final promedia los árboles, lo que reduce '
        'la varianza (Breiman, 2001). En la potenciación del gradiente, en cambio, los árboles se construyen de forma '
        'secuencial y cada nuevo árbol se especializa en corregir los errores que aún comete el conjunto (Friedman, '
        '2001).',
        'Friedman (2001) describe la potenciación del gradiente como un descenso por gradiente en el espacio de las '
        'funciones. El procedimiento comienza con una predicción inicial igual para todas las observaciones, por '
        'ejemplo, el logaritmo de la razón de probabilidades de la clase positiva. En cada iteración se calcula, para '
        'cada observación, el gradiente negativo de la función de pérdida respecto de la predicción actual, que '
        'indica en qué dirección y cuánto debe corregirse. Se ajusta un árbol pequeño que aproxima esos gradientes, '
        'se multiplica su aporte por una tasa de aprendizaje menor que uno y se suma al modelo. Repetir este paso '
        'cientos de veces produce un modelo aditivo de muchos árboles débiles cuyo conjunto es muy preciso, y la tasa '
        'de aprendizaje reducida, junto con un número suficiente de árboles, mejora la generalización.',
        'XGBoost es una implementación escalable y regularizada de la potenciación del gradiente sobre árboles de '
        'decisión (Chen y Guestrin, 2016). Construye un conjunto de K árboles de forma secuencial, donde cada árbol '
        'corrige los errores de los anteriores, minimizando una función objetivo que combina la pérdida de predicción '
        'con un término de regularización:',
        ('eq', 'XGB1'),
        ('eq', 'XGB2'),
        'donde l es la función de pérdida logística, ŷ_i la predicción para la observación i, T el número de hojas del '
        'árbol, w el vector de pesos de las hojas, y γ y λ los parámetros que penalizan la complejidad para evitar el '
        'sobreajuste.',
        'Chen y Guestrin (2016) introducen varias mejoras sobre la potenciación clásica. En lugar de usar solo el '
        'gradiente, aproximan la pérdida con información de primer y segundo orden, lo que permite calcular de forma '
        'exacta el peso óptimo de cada hoja y la ganancia de cada posible división. Una división solo se realiza si '
        'su ganancia supera el umbral γ, lo que poda ramas poco útiles, y el parámetro λ contrae los pesos de las '
        'hojas hacia cero. Además, el algoritmo incorpora el submuestreo de filas y columnas en cada árbol, la '
        'búsqueda aproximada de divisiones mediante cuantiles ponderados y un tratamiento propio de los valores '
        'faltantes, que aprende en cada nodo hacia qué rama enviar las observaciones sin dato. Estas características, '
        'junto con su eficiencia computacional, lo han convertido en uno de los algoritmos de referencia para datos '
        'tabulares.',
        'La regresión logística es el modelo de referencia clásico para la clasificación binaria. Estima el logaritmo '
        'de la razón de probabilidades de la clase positiva como una combinación lineal de los predictores, y sus '
        'coeficientes indican la dirección y magnitud de la asociación de cada variable con el resultado. Con '
        'regularización, controla el sobreajuste incluso con muchas variables categóricas codificadas. Aunque no '
        'captura interacciones de forma automática, su interpretabilidad la convierte en un punto de comparación '
        'obligado para evaluar si un modelo más complejo aporta una mejora real (Hastie et al., 2009).']),

    ('Validación y evaluación de modelos predictivos', [
        'La validación cruzada de k pliegues estima el desempeño de un modelo con datos que no utilizó para '
        'entrenar. El conjunto de datos se divide en k partes de tamaño similar, el modelo se entrena k veces '
        'dejando fuera una parte distinta en cada ocasión, y se evalúa sobre la parte excluida. Al final, cada '
        'observación recibe una predicción de un modelo que no la vio, y el promedio de los k resultados ofrece una '
        'estimación más estable que una única partición (Hastie et al., 2009). La validación estratificada conserva '
        'en cada pliegue la proporción de la clase minoritaria, y la validación agrupada asigna todas las '
        'observaciones de una misma unidad, como una persona que postuló varias veces, al mismo pliegue. Esta última '
        'condición evita una forma de fuga de información en la que el modelo reconoce a la persona en lugar de '
        'aprender patrones generales (Kaufman et al., 2012).',
        'En la clasificación binaria, las predicciones se resumen en una matriz de confusión que cruza la clase real '
        'con la predicha y distingue verdaderos positivos, falsos positivos, verdaderos negativos y falsos negativos. '
        'A partir de ella se calculan la exactitud, que es la proporción de aciertos, la sensibilidad, que es la '
        'proporción de positivos identificados, y la precisión, que es la proporción de predicciones positivas que '
        'son correctas (Fawcett, 2006). Cuando la clase de interés es poco frecuente, la exactitud resulta engañosa, '
        'porque un clasificador que siempre predice la clase mayoritaria obtiene un valor alto sin identificar a '
        'ningún caso positivo (Saito y Rehmsmeier, 2015).',
        'La curva característica operativa del receptor representa la sensibilidad frente a la tasa de falsos '
        'positivos para todos los umbrales posibles, y el área bajo esta curva resume la capacidad discriminativa del '
        'modelo en un solo valor. Hanley y McNeil (1982) mostraron que esta área equivale a la probabilidad de que el '
        'modelo asigne una puntuación mayor a una observación positiva elegida al azar que a una negativa elegida al '
        'azar. Un valor de 0.5 corresponde a un clasificador aleatorio y un valor de 1 a una discriminación perfecta. '
        'Fawcett (2006) advierte que esta métrica no depende del umbral ni de la proporción de clases, lo que es una '
        'ventaja para comparar modelos, pero también una limitación, porque no informa sobre la calidad de las '
        'predicciones positivas.',
        'Por ello, en problemas desbalanceados se recomienda complementarla con la curva de precisión y '
        'sensibilidad, que muestra cuántas de las predicciones positivas son correctas a medida que se identifican '
        'más casos. A diferencia del área bajo la curva característica operativa del receptor, el área bajo esta '
        'curva debe compararse con la proporción de positivos en los datos, que es el valor esperado de un '
        'clasificador aleatorio, y es más sensible a las mejoras en la identificación de la clase minoritaria (Saito y '
        'Rehmsmeier, 2015).']),

    ('Calibración de probabilidades', [
        'Un modelo está bien calibrado cuando sus probabilidades coinciden con las frecuencias observadas: entre los '
        'casos a los que asigna una probabilidad de 0.2, aproximadamente el 20 % debería pertenecer a la clase '
        'positiva. La capacidad discriminativa y la calibración son propiedades distintas, porque un modelo puede '
        'ordenar correctamente a las personas y, al mismo tiempo, sobrestimar o subestimar sus probabilidades '
        '(Niculescu-Mizil y Caruana, 2005). Cuando las probabilidades se comunican a las personas, como en la '
        'orientación vocacional, la calibración es indispensable para que la cifra tenga un significado real.',
        'La calidad de la calibración se evalúa con el puntaje de Brier, que es el error cuadrático medio entre la '
        'probabilidad estimada y el resultado observado, y cuyo valor menor indica mejores predicciones (Brier, 1950), '
        'así como con la curva de calibración, que compara la probabilidad media estimada con la proporción observada '
        'en grupos de observaciones ordenadas por su probabilidad. Niculescu-Mizil y Caruana (2005) mostraron que los '
        'modelos basados en la potenciación de árboles tienden a producir probabilidades distorsionadas. Además, '
        'ponderar la clase minoritaria para compensar el desbalance desplaza las probabilidades hacia la clase '
        'positiva, por lo que el modelo sobrestima la probabilidad real.',
        'La calibración isotónica corrige esas distorsiones mediante una función escalonada y no decreciente que '
        'transforma las puntuaciones del modelo en probabilidades. El procedimiento ordena las observaciones según su '
        'puntuación y ajusta la función que mejor reproduce las frecuencias observadas, con la única restricción de '
        'que una puntuación mayor no puede recibir una probabilidad menor. Como conserva el orden, no altera la '
        'capacidad discriminativa del modelo (Zadrozny y Elkan, 2002). Al no suponer una forma funcional, requiere '
        'una cantidad suficiente de datos y, con pocos casos, puede sobreajustarse (Niculescu-Mizil y Caruana, '
        '2005).']),

    ('Equidad algorítmica', [
        'La equidad algorítmica estudia si un modelo predictivo distribuye sus errores de manera homogénea entre grupos '
        'de población. En contextos de orientación, un indicador relevante es la tasa de falsos negativos, que mide la '
        'proporción de personas que efectivamente logran el resultado pero a quienes el modelo asigna una baja '
        'probabilidad. Una tasa mayor en un grupo implica que el sistema desalentaría de forma desproporcionada a sus '
        'integrantes con potencial. Por ello, la evaluación de modelos con fines educativos debe complementar las '
        'métricas globales con métricas desagregadas por grupo.',
        ('eq', 'TFN'),
        'donde FN son los falsos negativos y VP los verdaderos positivos de cada grupo.',
        'Hardt et al. (2016) formalizan este criterio como igualdad de oportunidades: un clasificador la cumple '
        'cuando la tasa de verdaderos positivos, y por tanto la de falsos negativos, es igual en todos los grupos '
        'protegidos. Los autores muestran que el criterio depende solo de la distribución conjunta de la predicción, '
        'el resultado real y la pertenencia al grupo, de modo que puede auditarse sin conocer el funcionamiento '
        'interno del modelo, y que es posible corregir un clasificador ya entrenado ajustando umbrales por grupo. Su '
        'propuesta traslada además el costo de una mala clasificación desde el grupo desfavorecido hacia quien toma '
        'la decisión, que puede responder mejorando la precisión de la clasificación.']),

    ('Procesamiento de lenguaje natural y arquitectura Transformer', [
        'El procesamiento de lenguaje natural estudia la representación y el tratamiento computacional del lenguaje '
        'humano. Su primer paso es la tokenización, que divide el texto en unidades llamadas elementos o tokens. Los '
        'modelos actuales utilizan unidades de subpalabra obtenidas mediante la codificación por pares de bytes, que '
        'parte de caracteres individuales y fusiona de forma iterativa los pares más frecuentes del corpus hasta '
        'alcanzar un vocabulario de tamaño fijo. Así, las palabras frecuentes se representan como un solo elemento y '
        'las raras se descomponen en fragmentos conocidos, lo que permite procesar cualquier palabra, incluidos '
        'nombres propios y términos técnicos, sin elementos desconocidos (Sennrich et al., 2016).',
        'Cada elemento se convierte en un vector numérico denso, llamado incrustación, al que se suma información '
        'sobre su posición en la secuencia. La arquitectura Transformer procesa estos vectores mediante una pila de '
        'bloques idénticos, cada uno compuesto por un mecanismo de atención y una red neuronal de propagación hacia '
        'adelante, con conexiones residuales y normalización entre ellos (Vaswani et al., 2017). A diferencia de las '
        'redes recurrentes, que leen el texto palabra por palabra, el Transformer procesa toda la secuencia en '
        'paralelo, lo que acelera el entrenamiento y facilita capturar relaciones entre palabras distantes.',
        'El componente central es el mecanismo de atención, que pondera la relevancia de cada elemento de la secuencia '
        'respecto de los demás (Vaswani et al., 2017):',
        ('eq', 'ATTN'),
        'donde Q, K y V son las matrices de consultas, claves y valores obtenidas por proyección lineal de la entrada, y '
        'd_k es la dimensión de las claves. En términos prácticos, cada elemento formula una consulta, la compara con '
        'las claves de los demás para decidir a cuáles prestar atención y combina sus valores en esa proporción. La '
        'atención se calcula en paralelo en varias cabezas, cada una con sus propias proyecciones, y sus resultados se '
        'concatenan y proyectan con una matriz de salida. Las cuatro matrices de proyección, de consultas, claves, '
        'valores y salida, son precisamente las que adapta LoRA en esta investigación.']),

    ('Modelos de lenguaje grandes', [
        'Singhal et al. (2023) definen un modelo de lenguaje grande como una forma avanzada de inteligencia artificial '
        'capaz de comprender y generar lenguaje natural a partir del entrenamiento con grandes volúmenes de texto. '
        'Estos modelos funcionan como arquitecturas fundacionales versátiles, aplicables en campos como la atención '
        'sanitaria, y muestran un potencial significativo en razonamiento, recuperación de información y respuesta a '
        'preguntas, aunque requieren evaluaciones exhaustivas para evitar errores y sesgos (Negueruela Gómez, 2024; '
        'H. Zhang et al., 2026).',
        'Existen dos estrategias principales de preentrenamiento. En la primera, el modelo aprende a recuperar '
        'palabras ocultas a partir del contexto anterior y posterior, lo que produce representaciones bidireccionales '
        'útiles para tareas de comprensión, como la clasificación de textos (Devlin et al., 2019). En la segunda, que '
        'es la de los modelos generativos, el modelo es causal: solo puede ver los elementos anteriores y aprende a '
        'predecir el siguiente, lo que le permite generar texto de forma continua (Brown et al., 2020). Un modelo de '
        'lenguaje causal se entrena minimizando la entropía cruzada:',
        ('eq', 'CE'),
        'donde x es la instrucción, y_t el elemento de la respuesta en la posición t, T la longitud de la respuesta y θ '
        'los parámetros entrenables. En el ajuste fino supervisado la pérdida se calcula solo sobre la respuesta, no '
        'sobre la instrucción.',
        'Brown et al. (2020) mostraron que el aumento de escala de estos modelos mejora de forma notable su desempeño '
        'en tareas para las que no fueron entrenados de manera específica. Su modelo de 175 mil millones de '
        'parámetros resolvió tareas de traducción, respuesta a preguntas y razonamiento a partir de unos pocos '
        'ejemplos en el texto de entrada, sin modificar sus parámetros, aunque también identificaron conjuntos de '
        'datos en los que este enfoque seguía siendo insuficiente.',
        'La familia Qwen2.5 es un ejemplo reciente de modelos de lenguaje de pesos abiertos. Según su informe técnico, '
        'sus modelos se preentrenaron con 18 billones de elementos, más del doble que la versión anterior, y se '
        'publicaron en varios tamaños, en versiones base y ajustadas por instrucciones. Su etapa posterior al '
        'preentrenamiento combinó un ajuste fino supervisado con más de un millón de ejemplos y aprendizaje por '
        'refuerzo en varias etapas, lo que mejoró el seguimiento de instrucciones y el análisis de datos '
        'estructurados (Qwen Team, 2024). Su disponibilidad en tamaños pequeños, como el de 1 500 millones de '
        'parámetros, permite ajustarlos con recursos computacionales limitados.']),

    ('Ajuste por instrucciones', [
        'Un modelo preentrenado solo para predecir el siguiente elemento no necesariamente sigue las indicaciones de '
        'un usuario. El ajuste por instrucciones consiste en continuar el entrenamiento con una colección de tareas '
        'redactadas como instrucciones en lenguaje natural, acompañadas de su respuesta esperada. Wei et al. (2021) '
        'aplicaron este procedimiento a un modelo de 137 mil millones de parámetros con más de 60 tareas y mostraron '
        'que mejora de forma sustancial su desempeño en tareas no vistas durante el ajuste, y que el número de tareas, '
        'la escala del modelo y la redacción en lenguaje natural son determinantes de ese resultado.',
        'Ouyang et al. (2022) añadieron una segunda etapa de alineación con preferencias humanas. Primero ajustaron el '
        'modelo con demostraciones escritas por personas y luego lo entrenaron mediante aprendizaje por refuerzo a '
        'partir de comparaciones entre respuestas. Las respuestas de su modelo de 1 300 millones de parámetros fueron '
        'preferidas por evaluadores humanos frente a las del modelo original de 175 mil millones, lo que muestra que '
        'el ajuste orientado a la tarea puede compensar una gran diferencia de tamaño.',
        'Los modelos ajustados por instrucciones utilizan una plantilla de conversación que distingue los roles de '
        'sistema, usuario y asistente. El mensaje de sistema define el comportamiento general del modelo, el del '
        'usuario contiene la instrucción y el del asistente, la respuesta. Respetar esta plantilla durante el ajuste '
        'fino permite aprovechar el comportamiento aprendido en el preentrenamiento y en la alineación.']),

    ('Aprendizaje en contexto', [
        'El aprendizaje en contexto es la capacidad de los modelos de lenguaje de gran escala para resolver nuevas '
        'tareas a partir de ejemplos o instrucciones incluidos en la entrada, sin modificar sus parámetros internos. Se '
        'basa en los mecanismos de atención y constituye una alternativa flexible al ajuste tradicional (Kung et al., '
        '2023).',
        'Brown et al. (2020) distinguen tres modalidades: sin ejemplos, en la que el modelo recibe solo la '
        'descripción de la tarea, con un ejemplo y con pocos ejemplos. Su ventaja es que no requiere entrenamiento '
        'adicional. Sus limitaciones son que el número de ejemplos está restringido por la longitud máxima de la '
        'entrada, que el resultado depende de la redacción de la instrucción y que el modelo no siempre respeta un '
        'formato de respuesta preciso. Cuando la tarea exige reproducir de manera consistente una estructura y unos '
        'datos determinados, como un orden de programas con sus probabilidades, el ajuste fino resulta más '
        'confiable.']),

    ('Ajuste fino', [
        'El ajuste fino es el proceso mediante el cual se reentrena parcialmente un modelo de lenguaje previamente '
        'entrenado, con el objetivo de adaptar su conocimiento general a un dominio o tarea específica. El enfoque '
        'conserva los parámetros esenciales del modelo y los ajusta con un conjunto de datos especializado, lo que '
        'mejora su precisión y pertinencia en contextos como la medicina o la educación (Li et al., 2023).',
        'El ajuste fino completo actualiza todos los parámetros del modelo. Además de los pesos, debe almacenar en '
        'memoria sus gradientes y los estados del optimizador, lo que multiplica la memoria necesaria y obliga a '
        'guardar una copia completa del modelo por cada tarea. Houlsby et al. (2019) propusieron como alternativa el '
        'ajuste eficiente en parámetros: mantener congelado el modelo original e insertar módulos pequeños, llamados '
        'adaptadores, que son los únicos que se entrenan. En la evaluación GLUE, los adaptadores alcanzaron un '
        'desempeño a menos de 0.4 % del ajuste completo entrenando solo el 3.6 % de los parámetros por tarea.',
        'El procedimiento del ajuste fino supervisado es el mismo con independencia de la técnica. Cada par de '
        'instrucción y respuesta se da formato con la plantilla del modelo y se tokeniza. El modelo procesa el par '
        'completo, pero la pérdida se calcula solo sobre los elementos de la respuesta. Los pares se agrupan en lotes, '
        'se calcula el gradiente de la pérdida y un optimizador actualiza los parámetros entrenables. El optimizador '
        'más utilizado es AdamW, que adapta el tamaño del paso a cada parámetro y aplica la penalización de los pesos '
        'de forma separada de ese paso, lo que mejora la generalización (Loshchilov y Hutter, 2017). La tasa de '
        'aprendizaje suele aumentar de forma gradual al inicio, en una etapa de calentamiento, y luego disminuir según '
        'una curva coseno. Durante el entrenamiento se monitorea la pérdida en un conjunto de validación, porque una '
        'pérdida de validación que deja de bajar mientras la de entrenamiento sigue bajando indica sobreajuste.']),

    ('Adaptación de bajo rango (LoRA)', [
        'Según Song et al. (2025) y J. C. Zhang et al. (2025), LoRA es una técnica para ajustar modelos de lenguaje '
        'preentrenados de gran escala, como los basados en la arquitectura Transformer, a tareas específicas sin '
        'modificar todos sus parámetros. En lugar de recalibrar cada peso, introduce matrices de descomposición de bajo '
        'rango en las capas del modelo, lo que reduce considerablemente la cantidad de parámetros entrenables y hace el '
        'ajuste más eficiente en memoria y cómputo, manteniendo la efectividad del modelo en la tarea. La técnica '
        'resulta especialmente útil en modelos muy grandes, en los que un ajuste completo es poco práctico (Gao et al., '
        '2026; Liu et al., 2026).',
        'Hu et al. (2021) parten de la hipótesis de que el cambio que necesitan los pesos para adaptarse a una tarea '
        'tiene un rango intrínseco bajo, es decir, puede representarse con muy pocas dimensiones. Por ello, dada una '
        'matriz de pesos preentrenada W₀ de dimensión d × k, LoRA no la modifica, sino que representa su actualización '
        'como el producto de dos matrices de bajo rango, B de dimensión d × r y A de dimensión r × k, con r mucho menor '
        'que d y k. La salida de la capa se calcula como:',
        ('eq', 'LORA'),
        'donde α es un factor de escala que controla la magnitud de la adaptación. La matriz A se inicializa de forma '
        'aleatoria y B en cero, de modo que al inicio del entrenamiento ΔW = BA = 0 y el modelo conserva exactamente su '
        'comportamiento original. El número de parámetros entrenables se reduce de d × k a:',
        ('eq', 'PARAM'),
        'Por ejemplo, en una capa de atención con d = k = 1 536 y r = 16, se pasa de 2 359 296 a 49 152 parámetros '
        'entrenables, es decir, el 2.1 %. La Figura 1 representa este mecanismo.',
        ('fig', 'fig_lora.png', 'Esquema de la adaptación de bajo rango (LoRA) en una capa del modelo',
         'Los pesos preentrenados permanecen congelados y solo se entrenan las matrices A y B. Elaboración propia con base en Hu et al. (2021).'),
        'La aplicación de LoRA sigue un procedimiento definido. Primero se congelan todos los pesos del modelo base. '
        'Luego se eligen los módulos que recibirán adaptadores, generalmente las proyecciones del mecanismo de '
        'atención, y se fijan tres hiperparámetros: el rango r, que determina la capacidad de la adaptación, el factor '
        'de escala α, que regula su intensidad, y una tasa de abandono que actúa como regularización. Durante el '
        'entrenamiento, el gradiente solo actualiza las matrices A y B. Al terminar, los adaptadores pueden guardarse '
        'por separado, con un tamaño de pocos megabytes, o fusionarse con los pesos originales sumando el producto BA a '
        'W₀ (Hu et al., 2021).',
        'Esta última propiedad distingue a LoRA de los adaptadores de Houlsby et al. (2019): una vez fusionado, el '
        'modelo tiene exactamente la misma arquitectura que el original, por lo que no añade latencia en la '
        'inferencia. Hu et al. (2021) reportaron que, frente al ajuste completo de un modelo de 175 mil millones de '
        'parámetros, LoRA redujo 10 000 veces el número de parámetros entrenables y 3 veces la memoria de la unidad de '
        'procesamiento gráfico, con una calidad igual o superior en varios modelos de referencia.']),

    ('Ajuste cuantizado con QLoRA', [
        'Aunque LoRA reduce los parámetros entrenables, el modelo base congelado debe permanecer en memoria. QLoRA '
        'resuelve esta limitación almacenando ese modelo en 4 bits y propagando los gradientes a través de él hacia '
        'los adaptadores LoRA, que se mantienen en mayor precisión (Dettmers et al., 2023). Con este procedimiento, '
        'sus autores ajustaron un modelo de 65 mil millones de parámetros en una sola unidad de procesamiento gráfico '
        'de 48 GB, conservando el desempeño del ajuste en 16 bits.',
        'Dettmers et al. (2023) introducen tres componentes. El primero es el tipo de dato NormalFloat de 4 bits, '
        'cuyos 16 valores posibles se distribuyen según los cuantiles de una distribución normal, que es la forma que '
        'suelen tener los pesos de las redes neuronales, lo que lo hace óptimo desde la teoría de la información para '
        'ese tipo de pesos. El segundo es la doble cuantización, que también cuantiza las constantes de escala usadas '
        'en la primera cuantización para reducir aún más la memoria. El tercero son los optimizadores paginados, que '
        'trasladan temporalmente los estados del optimizador a la memoria del procesador central cuando la unidad '
        'gráfica se queda sin espacio, lo que evita interrupciones por picos de memoria.',
        'Durante el entrenamiento, cada bloque de pesos se descuantiza a 16 bits en el momento de calcular la capa y se '
        'descarta después, de modo que en memoria solo permanece la versión de 4 bits. Esta combinación permite '
        'ajustar modelos de varios miles de millones de parámetros en unidades gráficas de 16 GB, como las disponibles '
        'de forma gratuita en servicios de computación en la nube.']),

    ('Generación de texto y decodificación', [
        'Un modelo de lenguaje genera texto de forma autorregresiva: en cada paso calcula una distribución de '
        'probabilidad sobre todo el vocabulario para el siguiente elemento, elige uno, lo añade a la secuencia y '
        'repite el proceso hasta producir un elemento de fin o alcanzar una longitud máxima. La regla con la que se '
        'elige cada elemento se denomina estrategia de decodificación.',
        'La decodificación voraz elige siempre el elemento más probable, por lo que es determinista: la misma entrada '
        'produce siempre la misma salida. Las estrategias de muestreo, en cambio, eligen al azar según las '
        'probabilidades, lo que aumenta la diversidad. Holtzman et al. (2019) mostraron que maximizar la probabilidad '
        'en la generación abierta tiende a producir textos repetitivos y poco naturales, y propusieron el muestreo de '
        'núcleo, que solo considera el conjunto mínimo de elementos que acumula la mayor parte de la probabilidad. Sin '
        'embargo, cuando la tarea exige reproducir información precisa y la evaluación debe ser reproducible, como en '
        'la redacción de una ruta a partir de un ranking dado, la decodificación voraz es la opción adecuada.']),

    ('Evaluación de texto generado', [
        'La evaluación automática de texto compara la salida del modelo con una o más respuestas de referencia. Las '
        'métricas de coincidencia léxica, como ROUGE, cuentan las palabras o secuencias de palabras compartidas, y su '
        'variante ROUGE-L se basa en la subsecuencia común más larga, que premia que las palabras aparezcan en el '
        'mismo orden aunque no sean contiguas (Lin, 2004). Estas métricas son simples y reproducibles, pero penalizan '
        'las paráfrasis correctas y pueden ser altas en textos que comparten una estructura aunque difieran en el '
        'contenido relevante.',
        'Las métricas semánticas, como BERTScore, comparan las representaciones contextuales de cada palabra '
        'generadas por un modelo de lenguaje preentrenado, de modo que reconocen sinónimos y reformulaciones (T. Zhang '
        'et al., 2020). Ninguna de las dos familias verifica la exactitud de los datos que contiene el texto, por lo '
        'que en tareas con información crítica se complementan con métricas específicas de la tarea, como comprobar '
        'que el programa recomendado sea el correcto. Una alternativa más reciente es emplear un modelo de lenguaje '
        'avanzado como evaluador: Zheng et al. (2023) encontraron que este enfoque alcanza un acuerdo superior al 80 % '
        'con las preferencias humanas, similar al acuerdo entre personas, aunque presenta sesgos de posición, de '
        'extensión y de autopreferencia que deben controlarse.']),

    ('Corpus de instrucción y respuesta', [
        'Un corpus de instrucción y respuesta es un conjunto de pares en los que la instrucción describe una tarea y '
        'su contexto, y la respuesta muestra el resultado esperado. Es el insumo del ajuste fino supervisado, y su '
        'calidad determina en gran medida el comportamiento del modelo ajustado (León Caranqui, 2023). Para tareas '
        'sobre datos estructurados, el corpus se construye mediante la serialización de cada registro, es decir, su '
        'conversión a una descripción textual de sus atributos, una práctica habitual cuando los modelos de lenguaje '
        'deben trabajar con datos tabulares (Fang et al., 2024).',
        'La construcción del corpus debe cuidar tres propiedades. La primera es la representatividad, que el corpus '
        'refleje la diversidad de la población a la que se aplicará el modelo. La segunda es la coherencia, que cada '
        'respuesta sea consistente con la información de su instrucción. La tercera es la independencia entre '
        'particiones, que una misma persona no aparezca a la vez en los datos de entrenamiento y en los de prueba, '
        'para que la evaluación mida la capacidad de generalizar y no la memorización (Kaufman et al., 2012).']),

    ('Generación de rutas educativas', [
        'La generación de rutas educativas es un proceso basado en el análisis de datos académicos, personales y '
        'vocacionales, cuyo objetivo es recomendar itinerarios de formación personalizados. La combinación de modelos '
        'predictivos tabulares con modelos de lenguaje permite identificar patrones de rendimiento, intereses y riesgos, '
        'y diseñar trayectorias adaptadas al perfil y al contexto de cada estudiante (Cen et al., 2024; Nass et al., '
        '2023).']),

    ('Rankeo de rutas educativas', [
        'El rankeo de rutas educativas consiste en ordenar las alternativas de formación de un estudiante según un '
        'criterio de pertinencia, como la probabilidad estimada de éxito en cada programa. La integración de modelos '
        'predictivos tabulares con modelos de lenguaje permite identificar patrones de rendimiento académico, '
        'inclinaciones de interés y riesgos de abandono, y presentar las alternativas ordenadas de acuerdo con las '
        'características y antecedentes individuales (Fernández et al., 2025; Navarro Forero et al., 2025).',
        'Desde el punto de vista técnico, el enfoque más directo es el puntual: un modelo estima una puntuación para '
        'cada par formado por la persona y la alternativa, y las alternativas se ordenan de mayor a menor puntuación. '
        'La calidad del ordenamiento se evalúa con métricas de recuperación de información que dan más valor a los '
        'aciertos en las primeras posiciones. El rango recíproco medio considera la posición en que aparece la '
        'alternativa correcta (Voorhees, 1999), y la ganancia acumulada descontada normalizada reduce el valor de cada '
        'acierto según su posición y lo compara con el ordenamiento ideal (Järvelin y Kekäläinen, 2002).',
        'En los sistemas de recomendación, la ordenación por popularidad, que presenta a todos los usuarios las mismas '
        'alternativas según su frecuencia o éxito histórico, es una referencia exigente, porque captura la parte del '
        'resultado que no depende de la persona. Un sistema personalizado solo aporta valor si supera esa referencia '
        'y no únicamente al azar (Millán Gordillo, 2025).']),

    ('Orientación vocacional', [
        'Según Cisneros-Bravo et al. (2023) y Alejandro Jaramillo (2024), la orientación vocacional es un proceso '
        'educativo y psicológico que ayuda a los estudiantes a explorar sus intereses, valores y habilidades, para tomar '
        'decisiones académicas acordes con su proyecto de vida. En la actualidad este proceso incorpora herramientas '
        'tecnológicas e inteligencia artificial para ofrecer asesoramiento personalizado y mejorar la retención '
        'universitaria (Flores Meléndez et al., 2020).',
        'Cisneros-Bravo et al. (2023) identifican la falta de orientación vocacional como un factor de la deserción '
        'universitaria, y Rodas Zegarra de Escalante (2024) encontró una relación inversa entre ambas variables: a '
        'mayor orientación, menor deserción. En este marco, la información sobre la probabilidad de ingreso a cada '
        'programa no sustituye la exploración de intereses, sino que la complementa, al permitir que el postulante '
        'contraste sus preferencias con una expectativa realista.']),

    ('Perfil del estudiante', [
        'El perfil del estudiante describe sus habilidades, intereses, motivaciones, rendimiento académico y '
        'capacidades tecnológicas. Esta información es fundamental para orientar las decisiones educativas y adaptar el '
        'proceso de aprendizaje, y puede ser procesada mediante modelos de lenguaje y análisis de datos para construir '
        'itinerarios específicos para cada contexto (Yupanqui Sanchez, 2024).']),

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
        '(Jardón Gallegos et al., 2024). Desde un enfoque integral, no depende solo de las habilidades cognitivas, sino también '
        'de la motivación, de la adecuación entre intereses y carrera elegida y de las condiciones institucionales '
        '(Escalante López et al., 2023). La literatura reciente destaca además la autoeficacia, la gestión del tiempo y '
        'la percepción del apoyo institucional como factores de la perseverancia (Rodas Zegarra de Escalante, 2024).']),

    ('Deserción estudiantil', [
        'La deserción es el abandono del proceso educativo antes de su culminación. Según Torres-Delgado et al. (2024), '
        'es un fenómeno multicausal en el que se entrelazan factores académicos, sociales, familiares y personales que '
        'afectan la decisión de dejar los estudios.',
        'En la UNA-Puno, Escobar-Mamani y Cuentas Yupanqui (2024) analizaron a los 18 435 estudiantes matriculados en '
        'el semestre 2023-II y encontraron que 1 690 de ellos, el 9.17 %, se encontraban en riesgo académico por estar '
        'en tercera o cuarta matrícula de una asignatura, con una proporción significativamente mayor en varones. Los '
        'autores consideran la deserción y el bajo rendimiento como desafíos críticos para la institución, lo que '
        'refuerza la pertinencia de herramientas que apoyen decisiones vocacionales mejor informadas desde el ingreso.']),
]
