from contenido import *

# ------------------------------------------------------------ 3.5 métodos por objetivo
# Cada bloque: (título nivel 3, [(título nivel 4, [párrafos o ('eq', clave)])])
METODOS = [
 ('Objetivo específico 1: modelo tabular para el rankeo de probabilidades', [
  ('Descripción de variables', [
    'La variable dependiente es el ingreso, codificada como 1 cuando la condición final del postulante fue ingresó y '
    '0 en caso contrario. Como predictores se emplearon exclusivamente variables conocidas antes del examen: 30 '
    'numéricas, entre ellas los promedios por área curricular de tercero a quinto de secundaria, el promedio de quinto '
    'grado, la tendencia de las notas, las áreas desaprobadas, la repitencia, los perfiles cuantitativo y verbal, la '
    'edad, los años desde el egreso, las postulaciones previas, los índices de servicios básicos y de equipamiento '
    'tecnológico del hogar y la tasa previa de ingreso del programa. Además, se emplearon 26 categóricas, entre ellas el tipo de proceso, '
    'el programa postulado, el área y la gestión del colegio, la UGEL, la lengua materna, el nivel educativo y la '
    'ocupación de los padres, el rango de ingreso familiar y la preparación preuniversitaria.',
    'Se excluyeron de los predictores el puntaje total, los puntajes por componente, las respuestas por curso, los '
    'órdenes de mérito y la carrera de ingreso, por ser información generada durante o después del examen, cuya '
    'inclusión produciría fuga de información. La tasa previa de ingreso de cada programa se calculó únicamente con '
    'procesos anteriores al de cada postulación.']),
  ('Descripción detallada del uso de materiales, equipos e insumos', [
    'Los insumos fueron las bases de admisión y del SIAGIE. El historial escolar, registrado en formato largo con un '
    'registro por grado, se transformó a formato ancho con una fila por estudiante, y en los grados repetidos se conservó '
    'el último año cursado. Las calificaciones en escala literal se utilizaron en su equivalente vigesimal. El '
    'procesamiento se realizó en Python 3 con las bibliotecas Pandas, NumPy, SciPy, Scikit-learn y XGBoost, en una '
    'estación de trabajo con 16 GB de memoria RAM.',
    'El modelo XGBoost se entrenó con ponderación de la clase minoritaria para compensar el desbalance. Sus '
    'hiperparámetros se seleccionaron mediante una búsqueda con validación cruzada agrupada de tres pliegues: '
    'profundidad máxima de 3, tasa de aprendizaje de 0.02, 800 árboles, peso mínimo por hoja de 40, submuestreo de '
    'filas de 0.8, de columnas de 0.5 y regularización L2 de 10. Como referencias se utilizaron un clasificador trivial '
    'y una regresión logística con ponderación de clases.']),
  ('Aplicación de prueba estadística inferencial', [
    'Para identificar las variables asociadas al ingreso se aplicó la prueba U de Mann-Whitney en las variables '
    'numéricas (Mann y Whitney, 1947), con el delta de Cliff como tamaño del efecto (Cliff, 1993):',
    ('eq', 'CLIFF'),
    'donde x_i y y_j son las observaciones de ingresantes y no ingresantes, y n₁ y n₂ los tamaños de cada grupo. Los '
    'valores absolutos de 0.147, 0.33 y 0.474 delimitan efectos pequeños, medianos y grandes. En las variables '
    'categóricas se aplicó la prueba chi cuadrado de independencia, con la V de Cramér (Cramér, 1946):',
    ('eq', 'CRAMER'),
    'donde n es el número de observaciones y k el menor número de categorías entre las dos variables.',
    'El desempeño se estimó mediante validación cruzada de cinco pliegues estratificada y agrupada por persona. La '
    'métrica principal fue el AUC-ROC, que equivale a la probabilidad de que el modelo asigne un puntaje mayor a un '
    'ingresante que a un no ingresante elegidos al azar (Hanley y McNeil, 1982):',
    ('eq', 'AUC'),
    'Su intervalo de confianza al 95 % se obtuvo por remuestreo bootstrap de 1 000 réplicas. Se complementó con el '
    'AUC-PR, más informativo que el AUC-ROC cuando las clases están desbalanceadas (Saito y Rehmsmeier, 2015), y con '
    'la precisión, la sensibilidad y el F1 en el umbral que maximiza este último:',
    ('eq', 'F1'),
    'Las probabilidades se calibraron mediante regresión isotónica ajustada sobre las predicciones fuera de pliegue '
    '(Zadrozny y Elkan, 2002), y la calidad de la calibración se evaluó con el puntaje de Brier (Brier, 1950), donde '
    'p_i es la probabilidad estimada y y_i el resultado observado:',
    ('eq', 'BRIER'),
    'La hipótesis específica 1 se contrastó mediante la prueba t de Student para una muestra sobre el AUC-ROC de los '
    'cinco pliegues frente al valor de 0.85, con α = 0.05. La diferencia con la regresión logística se evaluó mediante '
    'la prueba t para muestras relacionadas. La equidad se evaluó comparando la tasa de falsos negativos entre colegios '
    'rurales y urbanos mediante la prueba chi cuadrado.']),
 ]),
 ('Objetivo específico 2: corpus de instrucción y respuesta', [
  ('Descripción de variables', [
    'Cada par se compone de una instrucción, que describe el perfil del postulante mediante descriptores verbales y '
    'las probabilidades de ingreso de sus tres programas mejor rankeados, y de una respuesta de referencia con la ruta '
    'educativa sugerida. Las variables evaluadas fueron la representatividad del corpus, su coherencia y su balance '
    'entre particiones.']),
  ('Descripción detallada del uso de materiales, equipos e insumos', [
    'Las variables numéricas se tradujeron a descriptores verbales. Por ejemplo, un promedio igual o mayor a 16 se '
    'describió como alto desempeño, de 13 a menos de 16 como desempeño satisfactorio, de 11 a menos de 13 como '
    'desempeño en proceso y menor a 11 como desempeño en inicio. Para cada persona se tomó su postulación más reciente '
    'y se estimó con el modelo tabular la probabilidad de ingreso en los diez programas más demandados de su área '
    'académica, conservándose los tres de mayor probabilidad. Debido a que la ponderación de la clase minoritaria desplaza las salidas del modelo hacia valores altos, las probabilidades se calibraron mediante regresión isotónica ajustada sobre las predicciones fuera de pliegue, de modo que correspondan a frecuencias de ingreso observadas.',
    'La respuesta de referencia se construyó mediante reglas: recomienda el programa de mayor probabilidad, presenta '
    'las dos alternativas siguientes, relaciona el área curricular de mayor rendimiento con las opciones y sugiere '
    'reforzar la de menor rendimiento. El corpus se exportó en formato JSONL compatible con Hugging Face.']),
  ('Aplicación de prueba estadística inferencial', [
    'La representatividad y el balance se evaluaron mediante la prueba chi cuadrado, comparando la distribución del '
    'área del colegio, el sexo y el área del programa entre el corpus y la población, y entre las particiones de '
    'entrenamiento, validación y prueba, con α = 0.05. La coherencia se midió como el porcentaje de pares en que el '
    'programa recomendado coincide con el de mayor probabilidad consignado en la instrucción.']),
 ]),
 ('Objetivo específico 3: ajuste del modelo de lenguaje con LoRA', [
  ('Descripción de variables', [
    'La variable es la calidad de las rutas generadas, medida por su coincidencia léxica y semántica con las '
    'respuestas de referencia del conjunto de prueba.']),
  ('Descripción detallada del uso de materiales, equipos e insumos', [
    'Se utiliza el modelo de lenguaje de código abierto Qwen2.5-1.5B-Instruct, de 1 500 millones de parámetros, '
    'elegido por su desempeño en español y porque, cuantizado en 4 bits, puede ajustarse en una unidad de '
    'procesamiento gráfico T4 de 16 GB disponible en Google Colab. El ajuste se implementa con las bibliotecas '
    'Transformers, PEFT y bitsandbytes de Hugging Face.',
    'La configuración de LoRA fue: rango r = 16, factor de escala α = 32 y tasa de abandono de 0.05, aplicada a las '
    'cuatro proyecciones del mecanismo de atención (consultas, claves, valores y salida) en las 28 capas del modelo, lo '
    'que representa alrededor de 4.4 millones de parámetros entrenables, cerca del 0.3 % del total. El entrenamiento '
    'se realizó durante una época sobre 6 000 pares, con tamaño de lote efectivo de 16, tasa de aprendizaje de '
    '2 × 10⁻⁴ con programación coseno y calentamiento del 3 %, optimizador AdamW paginado de 8 bits, precisión mixta '
    'y longitud máxima de 512 elementos.',
    'Cada par se formateó con la plantilla de conversación del modelo, con un mensaje de sistema que define el rol de '
    'orientador vocacional, la instrucción como mensaje del usuario y la ruta de referencia como respuesta. La pérdida '
    'se calculó únicamente sobre la respuesta. La Figura 3 resume el proceso. Al finalizar, los adaptadores se '
    'guardaron por separado y pueden fusionarse con el modelo base para la inferencia.',
    ('fig', 'fig_entrenamiento.png', 'Proceso de ajuste fino del modelo de lenguaje con QLoRA',
     'NF4: NormalFloat de 4 bits. CE: entropía cruzada. Elaboración propia.'),
    'Para las rutas se empleó decodificación voraz, sin muestreo aleatorio, con un máximo de 200 elementos generados, '
    'de modo que los resultados sean reproducibles.']),
  ('Aplicación de prueba estadística inferencial', [
    'La calidad léxica de las rutas se evalúa con ROUGE-L, basado en la subsecuencia común más larga entre la ruta '
    'generada y la de referencia (Lin, 2004):',
    ('eq', 'ROUGE'),
    'donde R y P son la sensibilidad y la precisión de la subsecuencia común más larga. La similitud semántica se '
    'evalúa con BERTScore, que compara las representaciones contextuales de cada elemento de ambos textos mediante '
    'similitud coseno (Zhang et al., 2020):',
    ('eq', 'BERTR'),
    ('eq', 'BERTF'),
    'donde x y x̂ son la ruta de referencia y la generada, y P_BERT se define de forma análoga a R_BERT intercambiando '
    'ambos textos.',
    'Debido a que las respuestas de referencia comparten una estructura común, el ROUGE-L entre referencias de '
    'personas distintas alcanza 0.836, por lo que las métricas de coincidencia textual tienden a ser altas aunque el '
    'contenido sea incorrecto. Por ello, la coherencia contextual de la hipótesis específica 3 se operacionalizó como '
    'la proporción de rutas en las que el programa recomendado en primer lugar es el de mayor probabilidad del '
    'ranking y los programas se mencionan en el orden correcto. La hipótesis se contrasta mediante la prueba binomial '
    'exacta unilateral frente a una proporción de 0.80, con α = 0.05.']),
 ]),
 ('Objetivo específico 4: integración y validación comparativa', [
  ('Descripción de variables', [
    'La variable es el desempeño comparativo de la arquitectura integrada frente a sus componentes, evaluado en dos '
    'dimensiones: la calidad del rankeo de programas, que corresponde al componente tabular, y la calidad de las rutas '
    'generadas, que corresponde a la integración con el componente lingüístico.']),
  ('Descripción detallada del uso de materiales, equipos e insumos', [
    'El rankeo se evaluó sobre los ingresantes del conjunto analítico mediante validación cruzada agrupada por persona, '
    'de modo que cada postulante fue ordenado por un modelo que no lo vio durante el entrenamiento. Para cada '
    'ingresante se consideraron como candidatos los diez programas más demandados de su área académica y el programa '
    'al que ingresó, que se tomó como el programa relevante. El ordenamiento del XGBoost se comparó con dos '
    'referencias: un orden aleatorio y un orden por popularidad, según la tasa histórica de ingreso de cada programa '
    'calculada en el pliegue de entrenamiento.',
    'La calidad del rankeo se midió con la ganancia acumulada descontada normalizada (Järvelin y Kekäläinen, 2002), '
    'donde rel_i vale 1 si el programa de la posición i es el relevante y 0 en otro caso, e IDCG@k es el valor máximo '
    'alcanzable:',
    ('eq', 'DCG'),
    ('eq', 'NDCG'),
    'y con el rango recíproco medio (Voorhees, 1999), donde rank_q es la posición del programa relevante para el '
    'postulante q:',
    ('eq', 'MRR'),
    'Se reportan además los aciertos en la primera posición y entre las tres primeras.',
    'Para la calidad de las rutas se comparan tres condiciones sobre la misma partición de prueba: el modelo de '
    'lenguaje base sin ajuste, que recibe el perfil y el ranking, el modelo ajustado con LoRA sin el componente '
    'tabular, entrenado y evaluado con el perfil pero sin las probabilidades, y la arquitectura híbrida CareER-GPT, '
    'ajustada con LoRA y alimentada con el ranking calibrado. Para cada ruta se calcula una métrica combinada como el '
    'promedio de ROUGE-L, BERTScore F1 y coherencia. Los experimentos se registran con control de versiones en Git.']),
  ('Aplicación de prueba estadística inferencial', [
    'La diferencia entre el rango recíproco del XGBoost y el de la referencia por popularidad se evaluó con la prueba '
    'de rangos con signo de Wilcoxon para muestras relacionadas (Wilcoxon, 1945). Para contrastar si la arquitectura '
    'híbrida supera en al menos 10 % a cada modelo individual en la métrica combinada, se evalúa la normalidad de las '
    'diferencias con la prueba de Shapiro-Wilk y se aplica la prueba t de Student para muestras relacionadas si se '
    'cumple, o la prueba de Wilcoxon en caso contrario, con α = 0.05.']),
 ]),
]

# ------------------------------------------------------------ Capítulo IV
tp_rows = [[r.periodo, n(r.postulaciones), n(r.ingresantes), f'{r.tasa:.2f}'] for r in TP.itertuples()]
tp_rows.append(['Total', n(TP.postulaciones.sum()), n(TP.ingresantes.sum()), f'{TP.ingresantes.sum()/TP.postulaciones.sum()*100:.2f}'])
tr_rows = [[r.tipo_proceso.capitalize().replace('Examen general', 'Examen general').replace('Examen extraordinario', 'Examen extraordinario').replace('Ceprauna', 'CEPREUNA').replace('Cepreuna', 'CEPREUNA'),
            n(r.postulaciones), n(r.ingresantes), f'{r.tasa:.2f}'] for r in TR.itertuples()]

num_rows = [[r.variable, f'{r.ingreso_media:.2f} ({r.ingreso_de:.2f})', f'{r.no_media:.2f} ({r.no_de:.2f})',
             pv(r.p), f'{r.delta:.3f}'] for r in TN.itertuples()]
cat_rows = [[r.variable, f'{r.chi2:.2f}', str(int(r.gl)), pv(r.p), f'{r.V:.3f}'] for r in TC.itertuples()]
mod_rows = [[et] + [f3(getattr(r, c)) for r in M.itertuples()] for et, c in [('AUC-ROC','auc'),('AUC-PR','aucpr'),('Exactitud','exactitud'),('Precisión','precision'),('Sensibilidad','sensibilidad'),('F1','f1')]]
fold_rows = [[str(r.pliegue), n(r.n), f4(r.auc_xgb), f4(r.aucpr_xgb), f4(r.auc_lr), f4(r.aucpr_lr)] for r in F.itertuples()]
fold_rows.append(['Media (DE)', '', f'{F.auc_xgb.mean():.4f} ({F.auc_xgb.std():.4f})', f'{F.aucpr_xgb.mean():.4f}',
                  f'{F.auc_lr.mean():.4f} ({F.auc_lr.std():.4f})', f'{F.aucpr_lr.mean():.4f}'])
eq_rows = [[r.grupo.capitalize(), n(r.n), f'{r.tasa_real:.2f}', f3(r.auc), f'{r.tfn:.2f}', f'{r.tfp:.2f}'] for r in Q.itertuples()]
cor_rows = [[r.particion.capitalize().replace('Validacion', 'Validación'), n(r.pares), f'{r.palabras_instr:.1f}', f'{r.palabras_resp:.1f}'] for r in CO.itertuples()]
cor_rows.append(['Total', n(CO.pares.sum()), '', ''])
rep_rows = [[r.variable, f'{r.chi2_part:.2f}', pv(r.p_part)] for r in RP.itertuples()]

imp = pd.read_csv(S + 't_importancia.csv')
_ART = {'Perfil verbal': 'del perfil verbal', 'Equipamiento TIC del hogar': 'del equipamiento tecnológico del hogar',
        'Tasa previa de ingreso del programa': 'de la tasa previa de ingreso del programa',
        'Preparación preuniversitaria': 'de la preparación preuniversitaria', 'Perfil cuantitativo': 'del perfil cuantitativo',
        'Programa postulado': 'del programa postulado', 'Tipo de proceso de admisión': 'del tipo de proceso de admisión',
        'Estudió en CEPREUNA': 'del estudio previo en CEPREUNA'}
_sig = [_ART.get(e, 'de ' + e) for e in imp.etiqueta.iloc[2:7]]
SIGUEN = ', '.join(_sig[:-1]) + ' y ' + _sig[-1]
RK = pd.read_csv(S + 't_ranking.csv'); RJ = json.load(open(S + 'ranking.json'))
RQ = pd.read_csv(S + 't_ranking_equidad.csv'); RQ = RQ[RQ.area_colegio.isin(['RURAL', 'URBANA'])]
rk_rows = [[r.metodo, f3(r.MRR), f3(r.NDCG5), f3(r.NDCG10), f3(r.Hit1), f3(r.Hit3)] for r in RK.itertuples()]
rq_rows = [[r.area_colegio.capitalize(), f3(r.MRR), f3(r.NDCG5), f3(r.NDCG10), f3(r.Hit1), f3(r.Hit3)] for r in RQ.itertuples()]
rx = RK[RK.metodo == 'XGBoost'].iloc[0]; rp_ = RK[RK.metodo == 'Popularidad del programa'].iloc[0]; ra = RK[RK.metodo == 'Aleatorio'].iloc[0]
if RJ['wilcoxon_p'] < .05:
    WIL = (f'La diferencia fue estadísticamente significativa según la prueba de Wilcoxon (W = {n(RJ["wilcoxon_W"])}, '
           f'p {"< .001" if RJ["wilcoxon_p"] < .001 else "= " + pv(RJ["wilcoxon_p"])}), aunque con un tamaño del efecto '
           f'pequeño (r = {RJ["r_efecto"]:.3f}).')
    ORDENA = 'ordene mejor que'
else:
    WIL = (f'No obstante, la diferencia no fue estadísticamente significativa según la prueba de Wilcoxon '
           f'(W = {n(RJ["wilcoxon_W"])}, p = {pv(RJ["wilcoxon_p"])}), con un tamaño del efecto despreciable '
           f'(r = {RJ["r_efecto"]:.3f}), por lo que ambos métodos ordenan los programas de forma equivalente.')
    ORDENA = 'ordene al menos tan bien como'

RES_INTRO = ('Los resultados se presentan por objetivo específico. En primer lugar se caracteriza la población de '
             'estudio y, a continuación, se exponen los resultados de cada objetivo con el contraste de su hipótesis.')

# ------------------------------------------------------------ resultados del modelo de lenguaje
import math as _m, re as _re2
LL = json.load(open(S + 'resultados_llm.json')); GEN = pd.read_csv(S + 'generaciones.csv').fillna('')
LC = LL['config']; LT = LL['entrenamiento']; LM = LL['metricas']; LP = LL['pruebas']
NE = LC['n_eval']
CB, CS, CH = 'LLM base sin ajuste', 'LLM + LoRA sin componente tabular', 'CareER-GPT híbrido'
ET = {CB: 'LLM base sin ajuste', CS: 'LLM con LoRA sin componente tabular', CH: 'CareER-GPT híbrido'}
def _perd(h):
    tr = [x['loss'] for x in h if 'loss' in x]; ev = [x['eval_loss'] for x in h if 'eval_loss' in x]
    return tr[0], tr[-1], ev[0], ev[-1], max(x['step'] for x in h if 'step' in x)
PH, PS = _perd(LL['historial']['hibrido']), _perd(LL['historial']['solo_llm'])
def ci(v): return [f'{v[0]:.3f}', f'[{v[1]:.3f}, {v[2]:.3f}]']
def fl(x): return f'{x:.4f}'
ent_rows = [[et, n(LT[k]['parametros_entrenables']), f'{LT[k]["minutos"]:.1f}', fl(pp[0]), fl(pp[1]), fl(pp[3])]
            for et, k, pp in [('CareER-GPT híbrido', 'hibrido', PH), ('LLM con LoRA sin componente tabular', 'solo_llm', PS)]]
met_rows = [[ET[c], ci(LM[c]['rougeL']), ci(LM[c]['bertscore']), ci(LM[c]['coherencia']), ci(LM[c]['combinada'])]
            for c in (CB, CS, CH)]
H3 = LP['H3']; K3 = round(H3['coherencia'] * H3['n'])
def _r(w, n_):  # tamaño del efecto r de la prueba de Wilcoxon a partir de la aproximación normal
    z = (w - n_ * (n_ + 1) / 4) / _m.sqrt(n_ * (n_ + 1) * (2 * n_ + 1) / 24); return z, abs(z) / _m.sqrt(n_)
# Wilcoxon descarta las diferencias nulas: el híbrido coincide con la referencia en todos los pares que lo hacen,
# por lo que solo hay diferencia cero cuando el rival también reproduce la referencia
_col = {CB: 'base', CS: 'solo_llm'}
H4 = {}
for c in (CB, CS):
    t = LP['H4_vs_' + c]
    n_ef = NE - int(((GEN[_col[c]].str.strip() == GEN.referencia.str.strip()) & (GEN.hibrido.str.strip() == GEN.referencia.str.strip())).sum())
    z, r = _r(t['estadistico'], n_ef); H4[c] = dict(t, z=z, r=r, n_ef=n_ef)
h4_rows = [[ET[c], f'{LM[CH]["combinada"][0]:.3f}', f'{LM[c]["combinada"][0]:.3f}', f'{H4[c]["mejora_pct"]:.1f}',
            n(H4[c]['estadistico']), pv(H4[c]['p']), f'{H4[c]["r"]:.3f}']
           for c in (CB, CS)]
H4_OK = all(H4[c]['mejora_pct'] >= 10 and H4[c]['p'] < .05 for c in (CB, CS))
def _frases(t):  # una viñeta por oración
    return ['• ' + x for x in _re2.split(r'(?<=\.)\s+(?=[A-ZÁÉÍÓÚÑ])', _re2.sub(r'\s+', ' ', str(t)).strip())]
def _lineas(t):  # respeta la estructura de listas del modelo base y descarta el elemento final incompleto
    out = []
    for ln in str(t).replace('**', '').splitlines():
        ln = ln.strip()
        if not ln: continue
        ln = _re2.sub(r'^[-*]\s+', '• ', ln)
        out.append(ln)
    if out and len(_re2.sub(r'[\d.•\s]', '', out[-1])) == 0: out = out[:-1]
    return out
_g = GEN.iloc[0]
gen_rows = [['Respuesta de referencia', _frases(_g.referencia)], ['LLM base sin ajuste', _lineas(_g.base)],
            ['LLM con LoRA sin componente tabular', _frases(_g.solo_llm)], ['CareER-GPT híbrido', _frases(_g.hibrido)]]
IDENT_H = (GEN.hibrido.str.strip() == GEN.referencia.str.strip()).mean() * 100
IDENT_SOLO = (GEN.solo_llm.str.strip() == GEN.referencia.str.strip()).mean() * 100

RESUMEN = RESUMEN.replace('[Completar con los resultados del ajuste con LoRA y de la integración híbrida.]',
    f'El modelo de lenguaje ajustado con LoRA alcanzó una coherencia contextual de {H3["coherencia"]:.3f}, superior al '
    f'umbral de 0.80, y la arquitectura híbrida superó en {H4[CS]["mejora_pct"]:.1f} % al modelo ajustado sin '
    'componente tabular en la calidad de las rutas generadas (p < .001).')
ABSTRACT = ABSTRACT.replace('[Complete with the results of LoRA fine-tuning and hybrid integration.]',
    f'The LoRA fine-tuned language model reached a contextual coherence of {H3["coherencia"]:.3f}, above the 0.80 '
    f'threshold, and the hybrid architecture outperformed the fine-tuned model without the tabular component by '
    f'{H4[CS]["mejora_pct"]:.1f}% in the quality of the generated pathways (p < .001).')

RES = [
 ('h3', 'Caracterización de la población de estudio'),
 ('p3', f'El conjunto analítico comprendió {n(P["analizables"])} postulaciones, de las cuales {n(P["ingresantes"])} '
        f'terminaron en ingreso, lo que representa una tasa de {P["tasa_ingreso"]:.2f} %. Como se observa en la Tabla 2, '
        f'la tasa de ingreso osciló entre {TP.tasa.min():.2f} % y {TP.tasa.max():.2f} % según el proceso, sin una '
        'tendencia sostenida en el periodo. La Tabla 3 muestra que la tasa difiere según la modalidad: fue mayor en '
        'CEPREUNA y en el examen extraordinario que en el examen general, lo que justifica incluir el tipo de proceso '
        'como predictor.'),
 ('tbl3', 'Postulaciones e ingresantes por proceso de admisión, Universidad Nacional del Altiplano, 2021-I a 2025-II',
  ['Proceso', 'Postulaciones', 'Ingresantes', 'Tasa de ingreso (%)'], tp_rows,
  'Postulaciones con resultado y con historial escolar emparejado. Elaboración propia con datos de la Oficina de '
  'Admisión de la UNAP y del SIAGIE.'),
 ('tbl3', 'Postulaciones e ingresantes por modalidad de admisión, Universidad Nacional del Altiplano, 2021-I a 2025-II',
  ['Modalidad', 'Postulaciones', 'Ingresantes', 'Tasa de ingreso (%)'], tr_rows, 'Elaboración propia.'),

 ('h3', 'Objetivo específico 1: modelo tabular para el rankeo de probabilidades'),
 ('h4', 'Variables asociadas al ingreso'),
 ('p4', 'La Tabla 4 muestra que los ingresantes presentaron promedios de secundaria significativamente mayores que '
        f'los no ingresantes en todas las áreas curriculares (p < .001). El mayor tamaño del efecto correspondió al '
        f'promedio de quinto grado, con un delta de Cliff de {TN.delta.iloc[0]:.3f}, magnitud media, seguido del '
        f'promedio de secundaria ({TN.delta.iloc[1]:.3f}). Los ingresantes acumularon también menos áreas '
        'desaprobadas. En cambio, la edad, los años desde el egreso, las postulaciones anteriores y el tamaño del hogar '
        'no se asociaron con el ingreso (p > .05).'),
 ('tbl4', 'Comparación de variables numéricas según resultado de admisión, 2021-I a 2025-II',
  ['Variable', 'Ingresó, media (DE)', 'No ingresó, media (DE)', 'p', 'Delta de Cliff'], num_rows,
  'Prueba U de Mann-Whitney. Calificaciones en escala vigesimal. DE: desviación estándar.'),
 ('p4', f'Entre las variables categóricas (Tabla 5), la preparación preuniversitaria mostró la asociación más fuerte '
        f'con el ingreso (V = {TC.V.iloc[0]:.3f}), seguida del acceso a internet, el estudio previo en CEPREUNA y la '
        'disponibilidad de computadora en el hogar. El área y la gestión del colegio y el ingreso familiar se '
        'asociaron de forma significativa pero débil, mientras que el sexo, la lengua materna y el nivel educativo de '
        'la madre no mostraron asociación significativa. En conjunto, el rendimiento escolar previo y el acceso a '
        'recursos de preparación y tecnológicos son los factores que mejor diferencian a los ingresantes.'),
 ('tbl4', 'Asociación entre variables categóricas y resultado de admisión, 2021-I a 2025-II',
  ['Variable', 'Chi cuadrado', 'gl', 'p', 'V de Cramér'], cat_rows, 'Prueba chi cuadrado de independencia. gl: grados de libertad.'),

 ('h4', 'Desempeño predictivo del modelo'),
 ('p4', f'La Tabla 6 compara el modelo XGBoost con las referencias. El clasificador trivial, que predice siempre que el '
        f'postulante no ingresa, obtiene una exactitud de {M.exactitud.iloc[0]*100:.2f} % sin identificar a ningún '
        'ingresante, lo que demuestra que la exactitud no es una métrica adecuada en este problema. El XGBoost alcanzó '
        f'un AUC-ROC de {f3(xg.auc)} y un AUC-PR de {f3(xg.aucpr)}, equivalente a {xg.aucpr/M.aucpr.iloc[0]:.1f} veces la '
        f'tasa base. En el umbral que maximiza el F1 ({C["umbral"]:.3f}) identificó al {xg.sensibilidad*100:.1f} % de los '
        f'ingresantes, con una precisión de {xg.precision*100:.1f} %.'),
 ('tbl4', 'Desempeño del modelo XGBoost y de los modelos de referencia, validación cruzada agrupada por persona',
  ['Métrica', 'Clasificador trivial', 'Regresión logística', 'XGBoost'], mod_rows,
  f'Predicciones fuera de pliegue de {n(P["analizables"])} postulaciones. Precisión, sensibilidad y F1 en el umbral que '
  'maximiza el F1 de cada modelo. El clasificador trivial predice siempre que el postulante no ingresa.'),
 ('p4', f'La Tabla 7 muestra que el desempeño fue estable entre pliegues, con una desviación estándar del AUC-ROC de '
        f'{H["auc_de"]:.4f}. La regresión logística obtuvo un AUC-ROC ligeramente superior al del XGBoost, con una '
        f'diferencia media de {abs(H["mejora_vs_lr"]):.4f} que, '
        f'{"aunque estadísticamente significativa" if H["p_vs_lr"] < .05 else "sin significación estadística"} (t(4) = '
        f'{H["t_vs_lr"]:.2f}, p = {pv(H["p_vs_lr"])}), carece de relevancia práctica. La Figura 4 presenta las curvas '
        'correspondientes.'),
 ('tbl4', 'AUC-ROC y AUC-PR por pliegue de validación cruzada',
  ['Pliegue', 'n', 'AUC-ROC XGB', 'AUC-PR XGB', 'AUC-ROC RL', 'AUC-PR RL'],
  fold_rows, 'XGB: XGBoost. RL: regresión logística. DE: desviación estándar.'),
 ('fig4', 'Curvas ROC y de precisión y sensibilidad del modelo XGBoost y de la regresión logística', 'fig_roc_pr.png',
  'La línea punteada indica el desempeño de un clasificador aleatorio en la curva ROC y la tasa base en la curva de precisión y sensibilidad. Elaboración propia.'),
 ('p4', f'Contraste de la hipótesis específica 1. El AUC-ROC del XGBoost fue {f3(H["auc"])}, con un intervalo de '
        f'confianza al 95 % de {f3(H["ic_inf"])} a {f3(H["ic_sup"])}, que no incluye el valor de 0.85. La prueba t para '
        f'una muestra no permite afirmar que el AUC-ROC supere dicho umbral (t(4) = {H["t"]:.2f}, p > .999). En '
        'consecuencia, se rechaza la hipótesis específica 1: el modelo tabular discrimina de manera moderada, '
        'claramente superior al azar, pero por debajo del umbral planteado.'),

 ('h4', 'Importancia de las variables'),
 ('p4', f'La Figura 5 muestra que el promedio de quinto de secundaria ({imp.ganancia_rel.iloc[0]:.1f} % de la ganancia) '
        f'y el promedio de secundaria ({imp.ganancia_rel.iloc[1]:.1f} %) fueron los predictores de mayor peso, seguidos '
        f'{SIGUEN}. Estos resultados son consistentes con el análisis bivariado de las Tablas 4 y 5.'),
 ('fig4', 'Importancia relativa de los doce principales predictores del modelo XGBoost', 'fig_importancia.png',
  'Ganancia relativa acumulada en las divisiones de los árboles. Los colores indican el tipo de variable. Elaboración propia.'),

 ('h4', 'Equidad entre colegios rurales y urbanos'),
 ('p4', f'La Tabla 8 muestra que el modelo discrimina con similar eficacia en ambos grupos, con AUC-ROC de '
        f'{f3(rur.auc)} en el área rural y {f3(urb.auc)} en la urbana. Sin embargo, la tasa de falsos negativos fue de '
        f'{rur.tfn:.2f} % en los colegios rurales frente a {urb.tfn:.2f} % en los urbanos, una brecha de '
        f'{E["brecha_tfn"]:.2f} puntos estadísticamente significativa (χ² = {E["chi2"]:.2f}, p < .001). Es decir, entre '
        'quienes efectivamente ingresaron, el modelo asignó baja probabilidad con mayor frecuencia a los procedentes de '
        'colegios rurales, por lo que su uso orientador sin corrección desalentaría de forma desproporcionada a este '
        'grupo.'),
 ('tbl4', 'Métricas de desempeño y error por área del colegio de procedencia',
  ['Área', 'n', 'Tasa de ingreso (%)', 'AUC-ROC', 'TFN (%)', 'TFP (%)'], eq_rows,
  'TFN: tasa de falsos negativos. TFP: tasa de falsos positivos. Se excluyen las postulaciones sin registro del área del colegio.'),

 ('h4', 'Rankeo de programas'),
 ('p4', 'A partir del modelo final se estimó, para cada postulante, la probabilidad de ingreso en los programas de su '
        'área académica, lo que permite ordenarlos. La Tabla 9 presenta un caso ilustrativo del rankeo obtenido, que '
        'constituye la entrada del modelo de lenguaje. La calibración isotónica redujo el puntaje de Brier de '
        f'{R["calibracion"]["brier_sin"]:.3f} a {R["calibracion"]["brier_con"]:.3f} y llevó la probabilidad media '
        f'estimada de {R["calibracion"]["media_sin"]:.3f} a {R["calibracion"]["media_con"]:.3f}, igual a la tasa observada, '
        'por lo que las probabilidades presentadas al postulante reflejan frecuencias reales de ingreso.'),
 ('rank', None),

 ('h3', 'Objetivo específico 2: corpus de instrucción y respuesta'),
 ('p3', f'Se generó el corpus CareER-Dataset con {n(K["pares"])} pares de instrucción y respuesta, uno por persona. La '
        'Tabla 10 muestra su distribución en las particiones, con longitudes medias de instrucción y respuesta '
        f'prácticamente idénticas entre ellas. El vocabulario de las respuestas comprende {n(K["vocab"])} términos '
        f'distintos y el programa recomendado en primer lugar abarca {K["top1_distintos"]} programas diferentes.'),
 ('tbl3', 'Distribución del corpus CareER-Dataset por partición',
  ['Partición', 'Pares', 'Palabras por instrucción (media)', 'Palabras por respuesta (media)'], cor_rows,
  'Particiones agrupadas por persona. Elaboración propia.'),
 ('p3', 'Como se observa en la Tabla 11, no se encontraron diferencias significativas entre las particiones en la '
        'distribución del área del colegio, el sexo ni el área del programa (p > .05), lo que confirma que el corpus '
        'está balanceado. Dado que incluye a la totalidad de personas analizables, reproduce la distribución de la '
        f'población. La coherencia fue de {K["coherencia_top1"]:.1f} %: en todos los pares el programa recomendado '
        'coincide con el de mayor probabilidad consignado en la instrucción. La Tabla 12 presenta un par de ejemplo.'),
 ('tbl3', 'Balance del corpus entre particiones de entrenamiento, validación y prueba',
  ['Variable', 'Chi cuadrado', 'p'], rep_rows, 'Prueba chi cuadrado de independencia.'),
 ('par', None),
 ('p3', 'Contraste de la hipótesis específica 2. El corpus resultó representativo de la población, coherente en el '
        '100 % de los pares y balanceado entre particiones, por lo que se acepta la hipótesis específica 2.'),

 ('h3', 'Objetivo específico 3: ajuste del modelo de lenguaje con LoRA'),
 ('h4', 'Entrenamiento del modelo con LoRA'),
 ('p4', f'El ajuste se ejecutó en una GPU {LL["gpu"]} de Google Colab sobre {n(LC["max_train"])} pares de la partición de '
        f'entrenamiento, durante {LC["epocas"]} época y {PH[4]} pasos de optimización. Los adaptadores LoRA sumaron '
        f'{n(LT["hibrido"]["parametros_entrenables"])} parámetros entrenables, cerca del 0.3 % del modelo, y el '
        f'entrenamiento tomó {LT["hibrido"]["minutos"]:.1f} minutos en la condición híbrida y '
        f'{LT["solo_llm"]["minutos"]:.1f} minutos en la condición sin componente tabular. Como muestran la Tabla 13 y la '
        f'Figura 6, en la condición híbrida la pérdida de validación descendió a {fl(PH[3])} al final del entrenamiento, '
        'mientras que en la condición sin componente tabular se estabilizó en '
        f'{fl(PS[3])}. La cercanía entre la pérdida de entrenamiento y la de validación en ambas condiciones indica que '
        'no hubo sobreajuste. La pérdida residual de la condición sin componente tabular corresponde a las '
        'probabilidades y programas que el modelo no puede inferir sin el ranking.'),
 ('tbl4', 'Parámetros, tiempo y pérdida del ajuste con LoRA por condición',
  ['Condición', 'Parámetros entrenables', 'Tiempo (min)', 'Pérdida inicial', 'Pérdida final de entrenamiento',
   'Pérdida final de validación'], ent_rows,
  f'Pérdida de entropía cruzada calculada solo sobre la respuesta. Entrenamiento de {LC["epocas"]} época con '
  f'{n(LC["max_train"])} pares, r = {LC["r"]}, α = {LC["alpha"]} y lote efectivo de 16 en una GPU {LL["gpu"]}.', [1285, 1150, 950, 850, 1450, 1400]),
 ('fig4', 'Pérdida de entrenamiento y de validación durante el ajuste con LoRA', 'fig_perdida.png',
  'Las líneas tenues corresponden a la pérdida de entrenamiento y las líneas con marcadores a la de validación, '
  'evaluada cada 50 pasos. Elaboración propia.'),
 ('h4', 'Calidad de las rutas generadas'),
 ('p4', f'Se generaron rutas para {NE} pares de la partición de prueba, correspondientes a personas no vistas durante '
        f'el entrenamiento. El modelo CareER-GPT obtuvo un ROUGE-L de {LM[CH]["rougeL"][0]:.3f}, un BERTScore F1 de '
        f'{LM[CH]["bertscore"][0]:.3f} y una coherencia de {LM[CH]["coherencia"][0]:.3f}, y el {IDENT_H:.1f} % de sus rutas '
        'coincidió literalmente con la respuesta de referencia. Este resultado se explica porque las referencias del '
        'corpus se construyeron con una estructura fija a partir del ranking del componente tabular, de modo que el '
        'modelo aprendió a trasladar con exactitud las probabilidades y los programas recibidos a una ruta redactada. La '
        'Tabla 14 presenta un ejemplo de las rutas generadas en cada condición.'),
 ('tblx', 'Ejemplo de rutas generadas por condición para un postulante de la partición de prueba',
  ['Condición', 'Ruta generada'], gen_rows,
  'Rutas completas, presentadas por oraciones para facilitar su lectura. La respuesta del modelo base termina '
  'incompleta porque alcanzó el máximo de 200 elementos generados. Se eliminaron sus símbolos de formato. '
  'Elaboración propia.'),
 ('p4', f'Contraste de la hipótesis específica 3. La coherencia contextual del modelo ajustado con LoRA en la '
        f'arquitectura híbrida fue de {H3["coherencia"]:.3f}, con {K3} de {H3["n"]} rutas coherentes, valor superior al '
        f'umbral de 0.80 según la prueba binomial exacta unilateral (p {"< .001" if H3["p"] < .001 else "= " + pv(H3["p"])}). '
        + ('En consecuencia, se acepta la hipótesis específica 3. ' if H3['p'] < .05 and H3['coherencia'] > .8 else
           'En consecuencia, se rechaza la hipótesis específica 3. ') +
        f'Cabe precisar que el modelo ajustado sin el componente tabular alcanzó una coherencia de '
        f'{LM[CS]["coherencia"][0]:.3f}, y la diferencia con la arquitectura híbrida corresponde al aporte del ranking.'),
 ('h3', 'Objetivo específico 4: integración y validación comparativa'),
 ('h4', 'Calidad del rankeo de programas'),
 ('p4', f'Se evaluó el rankeo sobre {n(RJ["n"])} ingresantes, con un promedio de {RJ["candidatos_medio"]:.1f} programas '
        'candidatos por persona. La Tabla 15 y la Figura 7 muestran que el XGBoost superó al orden aleatorio en todas las '
        f'métricas, con un MRR de {f3(rx.MRR)} frente a {f3(ra.MRR)}, y ubicó el programa de ingreso en la primera posición '
        f'en el {rx.Hit1*100:.1f} % de los casos, frente al {ra.Hit1*100:.1f} % esperado al azar. Sin embargo, el orden por '
        f'popularidad, basado solo en la tasa histórica de ingreso de cada programa, obtuvo un MRR de {f3(rp_.MRR)}, '
        f'superior al del XGBoost en {abs(RJ["mejora_mrr"]):.1f} %. {WIL}'),
 ('tbl4', 'Calidad del rankeo de programas del XGBoost y de los métodos de referencia',
  ['Método', 'MRR', 'NDCG@5', 'NDCG@10', 'Acierto@1', 'Acierto@3'], rk_rows,
  f'Evaluación con validación cruzada agrupada por persona sobre {n(RJ["n"])} ingresantes. Para el orden aleatorio se '
  'reportan los valores esperados exactos. Acierto@k: proporción de casos en que el programa de ingreso se ubica entre '
  'las k primeras posiciones.'),
 ('fig4', 'Comparación de las métricas de rankeo entre métodos', 'fig_ranking.png', 'Elaboración propia.'),
 ('p4', 'La Tabla 16 muestra que, a diferencia de lo observado en la clasificación, el rankeo no perjudicó a los '
        'postulantes de colegios rurales: sus métricas fueron iguales o ligeramente superiores a las de los urbanos.'),
 ('tbl4', 'Calidad del rankeo del XGBoost según el área del colegio de procedencia',
  ['Área', 'MRR', 'NDCG@5', 'NDCG@10', 'Acierto@1', 'Acierto@3'], rq_rows,
  'Se excluyen los ingresantes sin registro del área del colegio.'),
 ('h4', 'Calidad de las rutas generadas por la arquitectura integrada'),
 ('p4', f'La Tabla 17 compara las tres condiciones sobre los mismos {NE} pares de prueba. El modelo base sin ajuste '
        f'obtuvo una métrica combinada de {LM[CB]["combinada"][0]:.3f}: generó textos extensos, con formato propio y sin '
        f'respetar el orden del ranking, con una coherencia de {LM[CB]["coherencia"][0]:.3f}. El modelo ajustado sin el '
        f'componente tabular alcanzó {LM[CS]["combinada"][0]:.3f}. Reprodujo la estructura de la ruta, con un ROUGE-L de '
        f'{LM[CS]["rougeL"][0]:.3f}, cercano al de 0.836 que comparten referencias de personas distintas, pero al no '
        f'conocer las probabilidades recomendó un programa distinto o en otro orden en el {(1 - LM[CS]["coherencia"][0]) * 100:.1f} % de los casos. La '
        f'arquitectura híbrida alcanzó {LM[CH]["combinada"][0]:.3f}, con intervalos de confianza que no se superponen con '
        'los de las otras condiciones.'),
 ('tbl4', 'Calidad de las rutas generadas según la condición experimental',
  ['Condición', 'ROUGE-L', 'BERTScore F1', 'Coherencia', 'Métrica combinada'], met_rows,
  f'Media e intervalo de confianza al 95 % entre corchetes, estimado mediante 1 000 remuestreos bootstrap, sobre '
  f'{NE} pares de la partición de prueba. La métrica combinada es el promedio de ROUGE-L, BERTScore F1 y coherencia.', [1685, 1350, 1350, 1350, 1350]),
 ('p4', f'La Tabla 18 presenta el contraste de la mejora. Las diferencias por par no siguieron una distribución '
        'normal según la prueba de Shapiro-Wilk (p < .001), por lo que se aplicó la prueba de rangos con signo de '
        f'Wilcoxon unilateral. La arquitectura híbrida superó al modelo base en {H4[CB]["mejora_pct"]:.1f} % y al modelo '
        f'ajustado sin componente tabular en {H4[CS]["mejora_pct"]:.1f} %, en ambos casos con p < .001 y un tamaño del '
        f'efecto grande ('
        + (f'r = {H4[CB]["r"]:.3f} en ambas comparaciones' if f'{H4[CB]["r"]:.3f}' == f'{H4[CS]["r"]:.3f}'
           else f'r = {H4[CB]["r"]:.3f} y r = {H4[CS]["r"]:.3f}, respectivamente') + ').'),
 ('tbl4', 'Contraste de la mejora de la arquitectura híbrida frente a cada modelo individual',
  ['Comparación frente a', 'Híbrido', 'Rival', 'Mejora (%)', 'W', 'p', 'r'], h4_rows,
  f'Valores medios de la métrica combinada sobre {NE} pares. Prueba de rangos con signo de Wilcoxon unilateral para '
  'muestras relacionadas, aplicada porque las diferencias no siguieron una distribución normal según la prueba de '
  'Shapiro-Wilk (p < .001). r: tamaño del efecto calculado como z dividido entre la raíz cuadrada de n, excluidos '
  'los pares con diferencia nula.', [2085, 850, 800, 900, 900, 800, 750]),
 ('p4', 'Contraste de la hipótesis específica 4. '
        + (f'En la calidad de las rutas generadas, la arquitectura híbrida superó a cada modelo individual en más del '
           f'10 % con diferencias estadísticamente significativas, por lo que se acepta la hipótesis específica 4 en '
           f'esta dimensión. ' if H4_OK else
           'En la calidad de las rutas generadas, la arquitectura híbrida no superó a cada modelo individual en al menos '
           '10 % con significación estadística, por lo que se rechaza la hipótesis específica 4 en esta dimensión. ') +
        'En la dimensión del rankeo, el ordenamiento que la arquitectura entrega es el del componente tabular, que no '
        'superó a la referencia por popularidad. Por ello, la ventaja de la integración radica en traducir el ranking '
        'a una ruta comprensible y fiel a las probabilidades, y no en mejorar el orden de los programas.'),
]

DISC = [
    f'El modelo tabular alcanzó un AUC-ROC de {f3(H["auc"])}, superior al valor de 0.69 que Carballo-Mendívil et al. '
    '(2025) obtuvieron con XGBoost al predecir la deserción desde la inscripción con información previa al ingreso. '
    'Ambos estudios coinciden en que, con variables disponibles antes del inicio de los estudios, la capacidad '
    'predictiva es moderada: el resultado depende de factores que no están registrados en las bases administrativas, '
    'como el desempeño en el propio examen, la motivación o la preparación específica. Por ello, el umbral de 0.85 '
    'planteado en la hipótesis específica 1 resultó optimista para este tipo de información.',
    'Los predictores de mayor peso, el rendimiento escolar previo, el acceso a tecnología y la preparación '
    'preuniversitaria, concuerdan con Guadalupe y Rodriguez (2025), quienes identificaron los factores académicos y '
    'socioeconómicos como determinantes, y con Carballo-Mendívil et al. (2025), que destacaron el promedio de '
    'bachillerato y las condiciones económicas. También son coherentes con Yatco y Jacha (2024), para quienes las '
    'variables sociodemográficas permiten anticipar trayectorias de riesgo.',
    'La equivalencia práctica entre XGBoost y la regresión logística es consistente con Aguilar-Reyes et al. (2025), '
    'que compararon modelos de regresión y árboles de clasificación en el estudio del rendimiento académico, y matiza lo '
    'señalado por Fang et al. (2024) sobre la ventaja de los árboles de decisión en datos tabulares: cuando la relación '
    'entre predictores y resultado es predominantemente aditiva, un modelo lineal regularizado puede ser igual de '
    'eficaz y más interpretable. Aun así, el XGBoost ofrece una mayor sensibilidad en su umbral óptimo, lo que resulta '
    'preferible en orientación vocacional, donde descartar a quien sí podría ingresar es el error más costoso.',
    'La brecha en la tasa de falsos negativos entre colegios rurales y urbanos constituye el hallazgo de mayor '
    'implicancia práctica. Mientras los estudios de deserción revisados reportan métricas globales, este resultado '
    'muestra que una capacidad discriminativa equivalente entre grupos no garantiza errores equivalentes. Dado que la '
    'falta de orientación es un factor clave del abandono (Cisneros-Bravo et al., 2023; Rodas, 2024), un sistema que '
    'subestime sistemáticamente a los postulantes rurales podría ampliar la desigualdad que pretende reducir.',
    f'En el rankeo, el hecho de que la tasa histórica de ingreso de cada programa {ORDENA} el modelo '
    'personalizado indica que la probabilidad de ingreso depende más del programa que de la interacción entre el '
    'perfil del postulante y el programa. El XGBoost aprendió principalmente efectos aditivos, lo que es coherente con '
    'su equivalencia frente a la regresión logística. Este resultado matiza lo reportado por Millan (2025), para quien '
    'los sistemas híbridos superan a los enfoques simples, y sugiere que en orientación vocacional la personalización '
    'debe demostrarse frente a referencias simples y no solo frente al azar. Como aspecto favorable, el rankeo no '
    'reprodujo la brecha territorial observada en la clasificación.',
    'Respecto al corpus, la estrategia de traducir variables numéricas a descriptores verbales y construir respuestas '
    'de referencia a partir del rankeo sigue la lógica de Armando et al. (2023), que destacaron la calidad del corpus '
    'como factor clave del ajuste con LoRA, y de Mena (2023) y Dettmers et al. (2023), que mostraron la viabilidad del '
    'ajuste cuantizado con recursos limitados.',
    f'El ajuste con LoRA entrenó cerca del 0.3 % de los parámetros de un modelo de 1 500 millones y, en '
    f'{LT["hibrido"]["minutos"]:.0f} minutos de una GPU {LL["gpu"]}, bastó para que el modelo aprendiera a redactar '
    'rutas fieles al ranking. Este resultado concuerda con Hu et al. (2021), quienes mostraron que la adaptación de '
    'bajo rango es competitiva frente al ajuste fino tradicional con una fracción del costo computacional, y con '
    'Dettmers et al. (2023), para quienes la cuantización en 4 bits no degrada el ajuste. A diferencia de Mena (2023), '
    'que identificó la memoria de video como una limitación importante al ajustar modelos de 7 mil millones de '
    'parámetros, el uso de un modelo de 1 500 millones permitió entrenar en infraestructura gratuita, lo que favorece '
    'la replicación en universidades con recursos limitados.',
    f'La comparación entre condiciones muestra que el aporte del componente tabular no está en la forma del texto, que '
    f'el modelo aprendió aun sin probabilidades, con un ROUGE-L de {LM[CS]["rougeL"][0]:.3f}, sino en su contenido: '
    f'sin el ranking, la coherencia descendió a {LM[CS]["coherencia"][0]:.3f}, y con él alcanzó '
    f'{LM[CH]["coherencia"][0]:.3f}. Que el modelo sin probabilidades acierte el orden en el '
    f'{LM[CS]["coherencia"][0] * 100:.1f} % de los casos sugiere que el ranking puede inferirse en buena medida a partir '
    'del área de interés del perfil, lo que es coherente con el hallazgo del rankeo: la probabilidad de ingreso depende '
    'más del programa que del perfil individual. Este hallazgo coincide con Martínez Sixto et al. (2025), quienes encontraron que la '
    'efectividad de un modelo de lenguaje depende en gran medida de la calidad y relevancia del contexto que recibe, '
    'y respalda lo planteado por Millan (2025) sobre la ventaja de los enfoques híbridos. En cambio, matiza lo '
    'señalado por Castejon (2025), para quien una ingeniería de instrucciones adecuada elimina las alucinaciones: el '
    'modelo base recibió la misma instrucción con el ranking y, aun así, generó textos extensos que no respetaron el '
    'orden de los programas, lo que indica que en esta tarea la instrucción por sí sola no bastó y fue necesario el '
    'ajuste fino.',
    f'Los valores máximos de la arquitectura híbrida, con el {IDENT_H:.1f} % de rutas idénticas a la referencia, deben '
    'interpretarse con cautela. Las respuestas de referencia se construyeron con una estructura fija a partir del '
    'ranking, por lo que el resultado demuestra que el modelo traslada con exactitud la información del componente '
    'tabular, pero no mide la calidad pedagógica de la orientación ni su utilidad percibida por los postulantes. Esta '
    'es la principal limitación del componente lingüístico y justifica validar las rutas con especialistas en '
    'orientación vocacional y con los propios postulantes, y ampliar el corpus con respuestas redactadas por '
    'orientadores, en línea con Armando et al. (2023), que destacaron la calidad del corpus como factor clave.',
]

CONCL = [
    f'El modelo tabular XGBoost estimó la probabilidad de ingreso por programa con una capacidad discriminativa '
    f'moderada, con un AUC-ROC de {f3(H["auc"])} y un AUC-PR de {f3(H["aucpr"])}, {xg.aucpr/M.aucpr.iloc[0]:.1f} veces la '
    'tasa base, sin alcanzar el umbral de 0.85, por lo que se rechaza la hipótesis específica 1. El rendimiento en '
    'secundaria, en particular en quinto grado, el acceso a tecnología en el hogar y la preparación preuniversitaria '
    f'fueron los principales predictores, y se identificó una brecha de {E["brecha_tfn"]:.1f} puntos en la tasa de falsos '
    'negativos en perjuicio de los postulantes de colegios rurales.',
    f'La transformación de los datos en pares de instrucción y respuesta produjo un corpus de {n(K["pares"])} pares, '
    'representativo de la población, coherente en el 100 % de los casos y balanceado entre particiones, por lo que se '
    'acepta la hipótesis específica 2.',
    f'El ajuste fino con LoRA, que entrenó cerca del 0.3 % de los parámetros del modelo Qwen2.5-1.5B-Instruct, permitió '
    f'generar rutas educativas con una coherencia contextual de {H3["coherencia"]:.3f}, superior al umbral de 0.80 '
    f'(prueba binomial exacta, p {"< .001" if H3["p"] < .001 else "= " + pv(H3["p"])}), con un ROUGE-L de '
    f'{LM[CH]["rougeL"][0]:.3f} y un BERTScore F1 de {LM[CH]["bertscore"][0]:.3f}, por lo que '
    + ('se acepta' if H3['p'] < .05 and H3['coherencia'] > .8 else 'se rechaza') + ' la hipótesis específica 3. La '
    'coherencia alcanza su valor máximo cuando el modelo recibe el ranking del componente tabular: sin él, fue de '
    f'{LM[CS]["coherencia"][0]:.3f}.',
    f'En la validación comparativa, el componente de rankeo superó al orden aleatorio, con un MRR de {f3(rx.MRR)} frente '
    f'a {f3(ra.MRR)}, pero no al orden por popularidad del programa, que alcanzó {f3(rp_.MRR)}'
    f'{", con el que resultó estadísticamente equivalente" if RJ["wilcoxon_p"] >= .05 else ""}, sin generar brecha '
    f'territorial. En la calidad de las rutas, la arquitectura híbrida alcanzó una métrica combinada de '
    f'{LM[CH]["combinada"][0]:.3f} y superó en {H4[CB]["mejora_pct"]:.1f} % al modelo base y en {H4[CS]["mejora_pct"]:.1f} % '
    'al modelo ajustado sin componente tabular, con diferencias significativas (Wilcoxon, p < .001), por lo que '
    + ('se acepta la hipótesis específica 4 en la dimensión de generación de rutas, mientras que en la dimensión del '
       'rankeo la mejora no se verifica.' if H4_OK else
       'no se verifica la mejora planteada en la hipótesis específica 4.'),
]
RECOM = [
    'A futuras investigaciones, incorporar variables de interacción entre el perfil del postulante y las exigencias de '
    'cada programa, o emplear algoritmos de aprendizaje para ranking que optimicen directamente el NDCG, y exigir que '
    'todo sistema de recomendación supere a una referencia por popularidad antes de su implementación.',
    'A la Universidad Nacional del Altiplano, incorporar en los procesos de admisión el registro sistemático de '
    'variables de preparación y de acceso a tecnología, y establecer mecanismos formales de vinculación con el SIAGIE, '
    'para disponer de información previa al examen que permita mejorar la capacidad predictiva de los sistemas de '
    'orientación.',
    'A quienes implementen sistemas de orientación basados en inteligencia artificial, evaluar las métricas de error '
    'por grupo territorial además de las métricas globales, y aplicar umbrales diferenciados o técnicas de '
    'recalibración que reduzcan la brecha en la tasa de falsos negativos antes de su uso con postulantes.',
    'A futuras investigaciones, validar el corpus de respuestas de referencia con especialistas en orientación '
    'vocacional y replicar la arquitectura en otras universidades de la región, como la Universidad Nacional de '
    'Juliaca, para evaluar su capacidad de generalización.',
]

BIB = [
 'Aguilar-Reyes, J. E., Mejía-Peñafiel, E. F., Morocho-Barrionuevo, T. P., y Velasco-Castelo, G.-M. (2025). Estudio del rendimiento académico mediante la comparación de modelos de regresión y árboles de clasificación. Telos: Revista de Estudios Interdisciplinarios en Ciencias Sociales, 27(1), 94-115. https://doi.org/10.36390/telos271.08',
 'Alejandro, S. Y. (2024). Orientación vocacional y profesional: la inteligencia artificial y su impacto en la educación. Revista Scientific, 9(34), 285-300. https://doi.org/10.29394/scientific.issn.2542-2987.2024.9.34.13.285-300',
 'Armando, J., Caranqui, L., y Riofrío, D. (2023). URKU: Adaptación de LLaMA 2 para la generación de texto en kichwa usando técnicas de Low-Rank Adaptation (LoRA) [Tesis de maestría, Universidad San Francisco de Quito]. http://bit.ly/COPETheses',
 'Balarezo, M., Pia, M., Hurtado, A., Alfredo, W., Churata, G., Francis, H., Atiquipa, S., Franklin, E., Felix, T., y Erick, R. (2024). Diseño de un asistente inteligente RAG para la Comisión de Eliminación de Barreras Burocráticas de INDECOPI-2024 [Tesis de maestría, Universidad Peruana de Ciencias Aplicadas]. http://hdl.handle.net/10757/684330',
 'Carballo-Mendívil, B., Arellano-González, A., Ríos-Vázquez, N. J., y Lizardi-Duarte, M. del P. (2025). Predicting student dropout from day one: XGBoost-based early warning system using pre-enrollment data. Applied Sciences, 15(16). https://doi.org/10.3390/app15169202',
 'Castejon, F. (2025). SoroIA: Diseño e implementación de un sistema conversacional basado en modelos grandes de lenguaje para el Museo Sorolla [Tesis de maestría, Universidad Politécnica de Madrid]. https://oa.upm.es/90917/1/TFM_FEDERICO_CASTEJON_LOZANO.pdf',
 'Cen, C., Luo, G., Tian, Y., Fu, B., Chen, Y., Huang, S., Jiang, T., y Huang, G. (2024). Enhancing the dissemination of Cantonese Opera among youth via Bilibili: A study on intangible cultural heritage transmission. Humanities and Social Sciences Communications, 11(1). https://doi.org/10.1057/s41599-024-03537-w',
 'Chen, T., y Guestrin, C. (2016). XGBoost: A scalable tree boosting system. En Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 785-794). https://doi.org/10.1145/2939672.2939785',
 'Cisneros-Bravo, B. E., Rodríguez-Aguilar, R. M., Niño-Membrillo, Y. E., y Cuevas-Rasgado, A. D. (2023). Falta de orientación vocacional como factor en la deserción universitaria. Caso de estudio: zona Oriente del Estado de México. RIDE Revista Iberoamericana para la Investigación y el Desarrollo Educativo, 14(27). https://doi.org/10.23913/ride.v14i27.1715',
 'Dettmers, T., Pagnoni, A., Holtzman, A., y Zettlemoyer, L. (2023). QLoRA: Efficient finetuning of quantized LLMs. En Advances in Neural Information Processing Systems 36. https://doi.org/10.48550/arXiv.2305.14314',
 'Escalante López, J. I., Medina Valderrama, C. J., y Vásquez Muñoz, A. (2023). La deserción universitaria: un problema no resuelto en el Perú. Hacedor - AIAPÆC, 7(1), 60-72. https://doi.org/10.26495/rch.v7i1.2421',
 'Escobar-Mamani, F., y Cuentas Yupanqui, S. R. (2024). Situación académica de estudiantes con matrícula regular y en riesgo académico en la Universidad Nacional del Altiplano, 2023-II. Journal of Humanities Titicaca, 2(1), 66-88. https://doi.org/10.70123/jht.7',
 'Fang, X., Xu, W., Tan, F. A., Zhang, J., Hu, Z., Qi, Y., Nickleach, S., Socolinsky, D., Sengamedu, S., y Faloutsos, C. (2024). Large language models (LLMs) on tabular data: Prediction, generation, and understanding. A survey. Transactions on Machine Learning Research. http://arxiv.org/abs/2402.17944',
 'Fernandez, J. M., Petrocelli, D., Matuk, R., Lanson, D., Zamudio, E., Cagnina, L., Gil Costa, V., y Errecalde, M. (2025). Fine-tuning y adaptación de modelos de lenguaje abiertos en infraestructura HPC para aplicaciones de dominio específico. SEDICI, Universidad Nacional de La Plata. http://sedici.unlp.edu.ar/handle/10915/183892',
 'Ferreyra, M. M., Avitabile, C., Botero Álvarez, J., Haimovich Paz, F., y Urzúa, S. (2017). Momento decisivo: la educación superior en América Latina y el Caribe. Banco Mundial. https://doi.org/10.1596/978-1-4648-1014-5',
 'Flores Meléndez, M., Góngora Cortés, J. J., López Cabrera, M. V., y Eraña Rojas, I. E. (2020). The «call» of medicine. Use of new mentoring models for vocational orientation. Educación Médica, 21(2), 145-148. https://doi.org/10.1016/j.edumed.2018.11.008',
 'Gao, D., Chen, S., Yang, Z., Yang, L., Gao, H., Wu, M., Yu, S., Xuan, Q., Zhang, W., Yang, L., y Cai, X. (2025). MLoRA+: Transformer-fusion mixture-of-LoRA network for multi-domain click-through rate prediction. Expert Systems with Applications, 297. https://doi.org/10.1016/j.eswa.2025.129486',
 'García, G., y Serradilla, F. (2021). Modelos de Transformers para la clasificación de texto [Tesis de maestría, Universidad Politécnica de Madrid].',
 'Guadalupe, V., y Rodriguez, C. (2025). Modelo predictivo basado en machine learning para la reducción de la deserción estudiantil en las universidades privadas del Perú: caso Universidad Privada San Juan Bautista [Tesis doctoral, Universidad Nacional Federico Villarreal].',
 'Hu, E. J., Shen, Y., Wallis, P., Allen-Zhu, Z., Li, Y., Wang, S., Wang, L., y Chen, W. (2021). LoRA: Low-rank adaptation of large language models. arXiv. https://doi.org/10.48550/arXiv.2106.09685',
 'Jardon, M., Granizo, J., Yaselga, W., y Cocha, M. (2024). Impacto de los asistentes virtuales de inteligencia artificial en el rendimiento académico de estudiantes universitarios. Revista Social Fronteriza, 4. https://doi.org/10.59814/resofro.2024.4(4)e338',
 'Kung, T. H., Cheatham, M., Medenilla, A., Sillos, C., De Leon, L., Elepaño, C., Madriaga, M., Aggabao, R., Diaz-Candido, G., Maningo, J., y Tseng, V. (2023). Performance of ChatGPT on USMLE: Potential for AI-assisted medical education using large language models. PLOS Digital Health, 2(2), e0000198. https://doi.org/10.1371/journal.pdig.0000198',
 'Li, Y., Li, Z., Zhang, K., Dan, R., Jiang, S., y Zhang, Y. (2023). ChatDoctor: A medical chat model fine-tuned on a large language model Meta-AI (LLaMA) using medical domain knowledge. Cureus. https://doi.org/10.7759/cureus.40895',
 'Liu, Z., Liu, Z., Feng, R., Feng, P., Chu, J., y Peng, X. (2025). LoRA-TCN: A pre-trained/fine-tuning learning paradigm for drift adaptation. Sensors and Actuators B: Chemical, 446. https://doi.org/10.1016/j.snb.2025.138644',
 'Martínez Sixto, L., Fernández y Fernández, C. A., y Millán Hernández, C. E. (2025). Comparación del desempeño de LLMs en la generación de diagramas de clases UML mediante un sistema RAG. Revista de Investigación en Tecnologías de la Información, 13(31), 64-79. https://doi.org/10.36825/riti.13.31.007',
 'Mena, S. (2023). Usos y aplicaciones de modelos de lenguaje masivos en español [Tesis de maestría, Universidad San Francisco de Quito].',
 'Millan, M. (2025). Estudio comparativo de sistemas de recomendación mediante filtrado colaborativo, basado en contenido y propuestas híbridas [Tesis de maestría, Universidad Loyola Andalucía]. https://repositorio.uloyola.es/bitstream/handle/20.500.12412/6735/TFM%20Mar%C3%ADa%20Mill%C3%A1n.pdf',
 'Muñoz Pilozo, A. G., Villalva Pilozo, A. M., Medina Castro, A. R., y Pilozo Mendoza, J. J. (2024). Factores determinantes en el éxito del proceso de enseñanza-aprendizaje. Revista Scientific, 9(33), 45-63. https://doi.org/10.29394/scientific.issn.2542-2987.2024.9.33.2.45-63',
 'Nass, O., Skuliabina, O., Bapiyev, I., Dnekeshev, A., Bekenova, S., y Bekenova, A. (2023). Blended learning as a promising direction of informatization of higher education. E3S Web of Conferences, 389. https://doi.org/10.1051/e3sconf/202338908003',
 'Navarro Forero, C. A., Hernández, M. A., y Viloria, K. T. (2025). Nuevas rutas de aprendizaje: adaptación de contenidos académicos a formatos audiovisuales para mejorar la preparación de los estudiantes. https://doi.org/10.26507/paper.4223',
 'Negueruela Gómez, I. (2024). Análisis y evaluación de LLMs con técnicas RAG para el desarrollo y despliegue de un asistente virtual [Trabajo de fin de estudios, Universidad de Cantabria]. https://repositorio.unican.es/xmlui/handle/10902/33837',
 'Ramos-Rivera, R. E., Santana Mancilla, P. C., García-Mancilla, J., y Gaytán-Lugo, L. S. (2025). Modelos de lenguaje en educación: inteligencia artificial generativa para optimizar el análisis del desempeño docente. Innovación Académica, Universidad Autónoma de Nuevo León, 1(2), 70-81. https://doi.org/10.29105/innoacad.v1i2.36',
 'Rodas, A. (2024). Orientación vocacional y deserción universitaria en una universidad de Lima - 2024 [Tesis de maestría, Universidad César Vallejo].',
 'Rodriguez, Y. (2023). Inteligencia artificial y rendimiento académico de los estudiantes de educación superior en la región Puno, 2022 [Tesis de maestría, Universidad Alas Peruanas].',
 'Sabando Moreira, P. A., y Zambrano Montenegro, D. F. (2024). Técnicas de machine learning para predecir la deserción estudiantil universitaria: una revisión sistemática de la literatura. Revista Científica Multidisciplinar G-nerando, 5(2), 997-1023. https://doi.org/10.60100/rcmg.v5i2.245',
 'Sancho Escrivá, J. V., Fanjul Peyró, C., De la Iglesia Vayá, M., Montell, J. A., y Escartí Fabra, M. J. (2020). Aplicación de la inteligencia artificial con procesamiento del lenguaje natural para textos de investigación cualitativa en la relación médico-paciente con enfermedad mental mediante el uso de tecnologías móviles. Revista de Comunicación y Salud, 10(1), 19-41. https://doi.org/10.35669/rcys.2020.10(1).19-41',
 'Singhal, K., Azizi, S., Tu, T., Mahdavi, S. S., Wei, J., Chung, H. W., Scales, N., Tanwani, A., Cole-Lewis, H., Pfohl, S., Payne, P., Seneviratne, M., Gamble, P., Kelly, C., Babiker, A., Schärli, N., Chowdhery, A., Mansfield, P., Demner-Fushman, D., … Natarajan, V. (2023). Large language models encode clinical knowledge. Nature, 620(7972), 172-180. https://doi.org/10.1038/s41586-023-06291-2',
 'Song, Y., Lv, C., Zhu, K., y Qiu, X. (2025). LoRA fine-tuning of Llama3 large model for intelligent fishery field. Discover Computing, 28(1). https://doi.org/10.1007/s10791-025-09663-6',
 'Superintendencia Nacional de Educación Superior Universitaria. (2020). II Informe bienal sobre la realidad universitaria en el Perú. SUNEDU.',
 'Torres-Delgado, G., Ramos-Pulido, S., y Hernández-Gress, N. (2024). Satisfaction with research-based learning and academic performance by big data analysis. Engineering Proceedings, 74(1). https://doi.org/10.3390/engproc2024074074',
 'Velasquez Velasquez, S. D. (2023). La inteligencia artificial aplicada al sector educativo: una revisión sistemática de la literatura [Trabajo de investigación de bachiller, Universidad Católica Santo Toribio de Mogrovejo]. http://hdl.handle.net/20.500.12423/6921',
 'Yatco, W., y Jacha, J. (2024). Modelo machine learning para predicción de deserción estudiantil [Tesis de segunda especialidad, Universidad Peruana Unión].',
 'Yupanquin, L. A. (2024). Perfil del egresado y la formación profesional en estudiantes del último año de arquitectura de la Universidad Femenina del Sagrado Corazón, 2020 [Tesis de maestría, Universidad Nacional de Educación Enrique Guzmán y Valle]. https://repositorio.une.edu.pe/server/api/core/bitstreams/0a198466-0baf-4299-897b-90a22a49c958/content',
 'Zavala Guirado, M. A., González Castro, I., Tapia Ruelas, C. S., Cota Valenzuela, L. V., y Durón Ramos, M. F. (2024). Propiedades psicométricas de una escala para medir la práctica docente universitaria en la modalidad híbrida. RIDE Revista Iberoamericana para la Investigación y el Desarrollo Educativo, 14(28). https://doi.org/10.23913/ride.v14i28.1878',
 'Zhang, H., Li, Z., y Liu, J. (2026). SceneLLM: Implicit language reasoning in LLM for dynamic scene graph generation. Pattern Recognition, 170. https://doi.org/10.1016/j.patcog.2025.111992',
 'Zhang, J. C., Xiong, Y. J., Xia, C. M., Zhu, D. H., y Zhan, H. J. (2025). LoRA2: Multi-scale low-rank approximations for fine-tuning large language models. Neurocomputing, 650. https://doi.org/10.1016/j.neucom.2025.130859',
 'Zheng, L., Chiang, W.-L., Sheng, Y., Zhuang, S., Wu, Z., Zhuang, Y., Lin, Z., Li, Z., Li, D., Xing, E. P., Zhang, H., Gonzalez, J. E., y Stoica, I. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. http://arxiv.org/abs/2306.05685',
]

BIB = sorted(BIB + ['Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. Monthly Weather Review, 78(1), 1-3. https://doi.org/10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2', 'Cliff, N. (1993). Dominance statistics: Ordinal analyses to answer ordinal questions. Psychological Bulletin, 114(3), 494-509. https://doi.org/10.1037/0033-2909.114.3.494', 'Cramér, H. (1946). Mathematical methods of statistics. Princeton University Press.', 'Hanley, J. A., y McNeil, B. J. (1982). The meaning and use of the area under a receiver operating characteristic (ROC) curve. Radiology, 143(1), 29-36. https://doi.org/10.1148/radiology.143.1.7063747', 'Järvelin, K., y Kekäläinen, J. (2002). Cumulated gain-based evaluation of IR techniques. ACM Transactions on Information Systems, 20(4), 422-446. https://doi.org/10.1145/582415.582418', 'Lin, C.-Y. (2004). ROUGE: A package for automatic evaluation of summaries. En Text Summarization Branches Out (pp. 74-81). Association for Computational Linguistics.', 'Mann, H. B., y Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. The Annals of Mathematical Statistics, 18(1), 50-60. https://doi.org/10.1214/aoms/1177730491', 'Saito, T., y Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets. PLOS ONE, 10(3), e0118432. https://doi.org/10.1371/journal.pone.0118432', 'Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., y Polosukhin, I. (2017). Attention is all you need. En Advances in Neural Information Processing Systems 30 (pp. 5998-6008).', 'Voorhees, E. M. (1999). The TREC-8 question answering track report. En Proceedings of the Eighth Text REtrieval Conference (pp. 77-82). National Institute of Standards and Technology.', 'Wilcoxon, F. (1945). Individual comparisons by ranking methods. Biometrics Bulletin, 1(6), 80-83. https://doi.org/10.2307/3001968', 'Zadrozny, B., y Elkan, C. (2002). Transforming classifier scores into accurate multiclass probability estimates. En Proceedings of the Eighth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (pp. 694-699). https://doi.org/10.1145/775047.775151', 'Zhang, T., Kishore, V., Wu, F., Weinberger, K. Q., y Artzi, Y. (2020). BERTScore: Evaluating text generation with BERT. En International Conference on Learning Representations. https://doi.org/10.48550/arXiv.1904.09675'], key=lambda x: x.lower().replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ä','a'))

MATRIZ_HDR = ['Problema', 'Hipótesis', 'Objetivos', 'Variables', 'Dimensiones e indicadores', 'Metodología']
MATRIZ = [
 [['General:', PG], ['General:', HG], ['General:', OG],
  ['Independiente:', 'Arquitectura híbrida CareER-GPT, basada en modelos tabulares y modelos de lenguaje ajustados con LoRA.'],
  ['Variable independiente:', 'Componente tabular XGBoost. Componente lingüístico ajustado con LoRA. Integración híbrida.'],
  ['Enfoque:', 'cuantitativo.', 'Tipo:', 'aplicada.', 'Nivel:', 'predictivo.', 'Diseño:', 'preexperimental.']],
 [['Específicos:'] + [f'P{i+1}. {x}' for i, x in enumerate(PE)],
  ['Específicas:'] + [f'H{i+1}. {x}' for i, x in enumerate(HE)],
  ['Específicos:'] + [f'O{i+1}. {x}' for i, x in enumerate(OE)],
  ['Dependiente:', 'Precisión en la generación y el rankeo de rutas educativas personalizadas.'],
  ['Variable dependiente:', 'H1: AUC-ROC igual o mayor a 0.85, AUC-PR y F1.', 'H2: representatividad, coherencia y balance del corpus.',
   'H3: ROUGE-L y BERTScore, coherencia igual o mayor a 0.80.', 'H4: NDCG@5, NDCG@10 y MRR, con mejora igual o mayor a 10 %.',
   'Equidad: tasa de falsos negativos por área del colegio.'],
  ['Población:', f'{n(P["postulaciones"])} postulaciones de {n(P["personas"])} personas, procesos 2021-I a 2025-II.',
   'Muestra:', f'censal, con un conjunto analítico de {n(P["analizables"])} postulaciones.',
   'Técnicas e instrumentos:', 'análisis documental de registros de admisión y del SIAGIE, validación cruzada, U de Mann-Whitney, chi cuadrado, t de Student y Wilcoxon.']],
]
