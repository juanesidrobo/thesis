# Cumplimiento del objetivo específico 1 — WP1

## Uso y alcance de este documento

Este documento contiene:

1. **Una sección académica preliminar**, redactada con los avances documentados del proyecto.
2. **Una matriz de correspondencia entre el objetivo y WP1**.
3. **Los resultados y anexos que deben existir para declarar el objetivo completado**.
4. **Los pendientes y criterios de aceptación**.

Es una base para la monografía, no una declaración de cumplimiento total. La información procede del anteproyecto, la base de conocimiento, las entrevistas y los antecedentes de observación discutidos. Los artículos no se consideran verificados a texto completo solo por estar enumerados en la base; las mediciones del registrador no se consideran realizadas por existir un firmware.

**Estado de referencia:** entrevistas inicial con el agrónomo de Corsavida, E1 con Oscar Castillo y E2 con Yuri Mena sistematizadas; fotografías iniciales disponibles según el equipo; revisión bibliográfica estructurada; registrador ESP32/BME280/DS3231 preparado y sensores probados por separado según el equipo. No se ha aportado en este contexto un informe de identificación taxonómica local, una serie ambiental de campo final ni un catálogo completo revisado.

---

# Parte I. Sección académica preliminar para la monografía

## 1. Caracterización biológica y agronómica de *Tetranychus urticae* y su contexto de observación en plantas madre de cítricos bajo cubierta

### 1.1. Objetivo y alcance de la caracterización

El primer objetivo específico del proyecto consiste en:

> **Caracterizar el ciclo biológico de la araña *Tetranychus urticae* en plantas madre de cítricos bajo cubierta, para identificar la presencia y sus efectos visibles en las plantas.**

Para abordarlo se desarrolla el paquete de trabajo WP1, denominado **Caracterización del entorno y levantamiento del conocimiento**, compuesto por revisión de literatura, observación directa en plantas madre, entrevistas con expertos y estructuración de la base de conocimiento agrícola [AP].

La caracterización se plantea como una integración **documental, experta y descriptiva local**. La literatura y las entrevistas permiten describir los estadios de la especie, los parámetros de desarrollo, la reproducción, el comportamiento y las condiciones asociadas con su establecimiento. La observación local permite documentar organismos, ubicación, síntomas y contexto de manejo en el vivero, diferenciando estos registros de los resultados experimentales publicados.

En este alcance no se pretende medir experimentalmente la duración de todos los estadios en Corsavida. Las duraciones de laboratorio se conservan junto con el hospedero, las condiciones del estudio y la definición del parámetro; no se presentan como mediciones realizadas en las plantas madre del proyecto. Esta distinción permite construir conocimiento contextualizado para WP2 sin atribuir a la observación local resultados que no se han obtenido.

La confirmación de la especie del material local constituye una condición crítica de interpretación. Hasta disponer de identificación especializada, la descripción bibliográfica de *T. urticae* se mantiene separada de los registros de ácaros fotografiados en el vivero.

### 1.2. Desarrollo metodológico de WP1

#### 1.2.1. Revisión de literatura — WP1.1

La actividad WP1.1 del anteproyecto contempla revisión sistemática de arquitecturas cognitivas y métodos directos de detección in situ. Para fundamentar la caracterización se ha organizado además una base bibliográfica biológica y agronómica. Este componente complementario no debe confundirse con el proceso de selección del estado del arte tecnológico [AP, BK].

El archivo `Base de conocimiento CSV.txt` reúne un catálogo de referencias, una matriz de extracción de hallazgos, reglas candidatas y respuestas sintetizadas a diez grupos de preguntas: biología general, ciclo de vida, microclima, alimentación, reproducción, comportamiento, interacción con cítricos, monitoreo, variables del sistema y relaciones biológicas.

El catálogo contiene 52 identificadores, A001–A052. El equipo confirmó que **A001 es una fila de ejemplo**, por lo que se excluye como evidencia. Los 51 registros restantes son referencias candidatas con pertinencia y grado de verificación diferentes; su número no equivale al de estudios incluidos en una revisión sistemática validada.

La matriz de extracción contiene hospedero, página o figura, evidencia parafraseada, dato cuantitativo, unidad, cita, interpretación y aplicación propuesta. Esta estructura permite enlazar un hallazgo con su fuente. Su depuración requiere distinguir resultados propios del artículo, información citada en la introducción e inferencias del equipo. Asimismo, las reglas candidatas deben conservarse separadas de los hallazgos publicados.

Entre las fuentes prioritarias se encuentran A017 y A021 para desarrollo e interacción con hospederos cítricos; A011 para efectos de alimentación sobre hojas cítricas; A023 para daño y detección óptica; A041 para selección de superficie foliar y luz; y A019 para monitoreo y umbrales económicos en clementinos productivos. Los originales de A017, A019, A021 y A041 están disponibles según confirmación del equipo, pero esa disponibilidad no sustituye el cotejo de cada dato [BK].

Los estudios de otros hospederos se utilizan como antecedentes contextuales y no como parámetros automáticos de plantas madre. En particular, los resultados de papaya, fríjol, calabacín, tomate o vid deben conservar su contexto al explicar variación de desarrollo, fecundidad, daño o ubicación.

**Para documentar WP1.1 como actividad finalizada**, deben incorporarse también los registros de búsqueda y selección —bases, fechas, cadenas, criterios y decisiones— y referencias completas de los estudios utilizados. La matriz de extracción demuestra trabajo de organización, pero por sí sola no acredita la ejecución completa de una revisión sistemática.

#### 1.2.2. Entrevistas con expertos — WP1.3

Se han sistematizado tres entrevistas con funciones complementarias:

| Fuente | Perfil y contexto | Contribución al objetivo | Límite principal |
|---|---|---|---|
| ENT-01 | Geovanny Agredo Sarria, agrónomo vinculado al manejo de Corsavida | Inspección, ubicación observada, síntomas, plantas madre y manejo local | Algunas respuestas agrupan estados o proporcionan estimaciones sin medición asociada |
| ENT-02 / E1 | Oscar Castillo, profesional en manejo agroforestal y gerente de Corsavida; entrevista identificada como 21 de septiembre | Contexto de producción, varetas, riego, sombreado, operación y observación de problemas | Alterna arañita roja, blanca y ácaros no especificados; no confirma taxonomía |
| ENT-03 / E2 | Yuri Mena, ingeniera agrónoma con maestría/doctorado y experiencia en ácaros de papaya; afiliación declarada ICA; 10 de octubre de 2026 | Estadios, reproducción, daños celulares, límites de extrapolación e identificación | No confirmó la especie local ni parámetros propios de plantas madre de cítricos |

La tabla E2 conserva en Notion el título histórico «Ingeniero Agrónomo Agrosavia», pero la entrevistada declaró trabajar en el ICA. Ese título de organización no debe utilizarse como afiliación institucional en la monografía [ENT-03].

Las respuestas se organizan por temas y se distinguen como completas, parciales o no respondidas. La sistematización de E1 comprende 51 registros, de los cuales 26 pertenecían al cuestionario y 25 surgieron durante la conversación. E2 comprende 57 registros, con 35 preguntas existentes y 22 añadidas. Estas cantidades describen **preguntas registradas**, no entrevistas independientes, observaciones de campo ni réplicas experimentales.

Los testimonios se conservan con sus localizadores y alcance. Una coincidencia conceptual entre expertos no se interpreta automáticamente como validación cuantitativa de un umbral. Se diferencia también lo planteado espontáneamente por un participante de las cifras introducidas por el equipo y aceptadas o discutidas posteriormente.

La autorización de grabación y uso académico debe conservarse según los acuerdos del proyecto. En E2 existe aceptación verbal en la transcripción; la existencia de un documento firmado todavía debe comprobarse.

#### 1.2.3. Observación local — WP1.2

El equipo informó la existencia de una visita inicial a Corsavida en la que, con acompañamiento del agrónomo, se observaron ácaros y se tomaron fotografías mediante teléfono y accesorio de aumento declarado 200×. Estas imágenes constituyen evidencia inicial de observación y permiten reconocer las necesidades de captura y catalogación [OBS-01].

La documentación local debe vincular cada imagen con la planta, hoja, superficie, estrato, fecha, método y fundamento de identificación. La vista ampliada permite observar organismos, mientras que la imagen de hoja completa y el contexto de planta permiten describir efectos visibles y localización. El aumento declarado del accesorio no constituye una escala dimensional calibrada.

La entrevista E2 introdujo una duda explícita sobre la identidad del ejemplar mostrado. Entre 41:38 y 44:31, Yuri Mena propuso considerar *Panonychus citri* y recomendó recolectar machos y hembras para identificación especializada. En consecuencia, el registro local debe conservarse como **identificación inicial de campo pendiente de confirmación**, sin presentar la imagen como prueba definitiva de *T. urticae* ni como confirmación de *P. citri* [ENT-03].

La próxima observación se organiza para cubrir hojas maduras y jóvenes, estratos inferior, medio y superior y superficies haz/envés, conforme a disponibilidad y acceso. La selección es descriptiva y busca cubrir situaciones; no se presenta como estimación de prevalencia del vivero sin un diseño específico.

Se ha preparado un registrador con ESP32-WROOM-32, BME280 y DS3231 para conservar temperatura y humedad relativa del aire, fecha/hora y archivos originales. El BME280 proporciona además presión atmosférica auxiliar. La guía y el firmware prevén registro periódico y muestras identificadas asociadas manualmente con fotografías [MET-01].

**La preparación del registrador y la compilación del firmware son avances instrumentales, no resultados ambientales de campo.** Para concluir WP1.2 deben existir archivos recuperados, instalación documentada, observaciones y catálogo revisado. Hasta aportar esos archivos, no corresponde incluir medias, rangos o relaciones locales entre ambiente y población.

#### 1.2.4. Estructuración del conocimiento agrícola — WP1.4

La base existente organiza fuentes, hallazgos, preguntas y 17 reglas candidatas. También se cuenta con un modelo preliminar de dominio que relaciona vivero, cubierta, planta, estrato, hoja, ubicación, observación y contexto ambiental [BK, MD].

Para preparar los insumos de WP2 se adopta la cadena:

```text
Fuente → Hallazgo o testimonio → Interpretación contextual → Regla candidata
```

Esta separación impide que un tratamiento experimental, una hipótesis o una recomendación del equipo se conviertan directamente en un hecho agronómico local. Cada afirmación requiere identidad del organismo, hospedero, condiciones, variable, unidad, localizador y estado de verificación.

Las entidades principales incluyen planta madre, hoja, estrato, superficie foliar, organismo, estadio, síntoma, imagen, observación, medición ambiental, instalación del sensor, evento de manejo y fuente de conocimiento. Se distinguen **presencia, identificación, daño, densidad y riesgo**, pues no representan el mismo resultado.

El resultado requerido en WP1 es conocimiento organizado y trazable para la posterior formalización. Una ontología implementada o un detector entrenado no son requisitos implícitos para declarar terminado este paquete; sí lo son el modelo de dominio, las definiciones y la procedencia de las relaciones propuestas.

### 1.3. Resultados preliminares de la caracterización

#### 1.3.1. Ciclo biológico y rasgos observables

La literatura organizada y la explicación de E2 permiten estructurar el ciclo de *T. urticae* en huevo, larva, protoninfa, deutoninfa y adulto, con periodos quiescentes entre estados activos. La larva posee tres pares de patas, mientras que los estados posteriores presentan cuatro pares. Las exuvias son recubrimientos desprendidos durante muda, no equivalentes a cadáveres [BK, ENT-03].

| Componente | Conocimiento documentado | Qué falta para su ficha definitiva |
|---|---|---|
| Huevo | Forma redondeada y descripción translúcida/cristalina en E2; oviposición asociada al envés | Rasgos y duración con fuente específica, condiciones y evidencia visual revisada |
| Larva | Tres pares de patas; transición posterior mediante muda | Duración contextualizada y posibilidad real de reconocerla con el equipo |
| Protoninfa | Estadio posterior a larva | Rasgos diferenciales y duración verificada |
| Deutoninfa | Estadio posterior a protoninfa | Rasgos diferenciales y duración verificada |
| Quiescencia | Periodos inmóviles asociados a mudas | Definición, alimentación/actividad y duración según fuente |
| Adulto | Dimorfismo descrito por E2; macho utilizado en identificación especializada | Ficha de reconocimiento, longevidad y reproducción con parámetros bien definidos |

El cuadro describe información documental y experta. **No acredita que todas esas etapas se hayan observado o identificado en las plantas madre locales.** La ficha final debe mostrar por separado «descrito en fuentes» y «observado en campo».

La duración no se expresa mediante un único rango general que mezcle hospederos. En A017 la extracción reporta aproximadamente 11,52 y 8,00 días bajo tratamientos combinados diferentes en hojas de clementina; ese dato requiere cotejar su definición en el original. En E2 se reportan 8,8 días de huevo a adulto en papaya, en laboratorio a 26 °C y 56 % HR. Ambos se conservan como resultados contextualizados, no como tiempos medidos en Corsavida [BK, ENT-03].

En la versión final se separarán desarrollo huevo–adulto, preoviposición, huevo–primera oviposición, oviposición, longevidad adulta y longevidad total. Esta separación es necesaria porque la base actual contiene valores de parámetros distintos bajo denominaciones parcialmente coincidentes.

#### 1.3.2. Reproducción

E2 aportó para su estudio en papaya una preoviposición cercana a un día, oviposición promedio de seis días con máximo de catorce, fecundidad promedio de cuarenta huevos y máximo observado de ciento trece. Las cifras deben enlazarse con la tesis o tabla original para verificar condiciones, dispersión y población analizada [ENT-03].

No se adopta una fecundidad universal de 95 huevos, pues ese valor dependía de A001, ejemplo excluido. Tampoco se iguala un máximo observado con promedio ni se multiplica directamente población local a partir de tasas obtenidas en otros cultivos [BK].

La explicación oral de partenogénesis necesita depuración: E2 alterna producción de machos, descendencia femenina y ejemplos generales de ácaros. La descripción específica de arrenotoquia y fecundación en *T. urticae* se completará con una fuente especializada, preservando el testimonio como tal. Las cifras de longevidad total y adulta también requieren aclaración antes de incorporarse a reglas.

#### 1.3.3. Ambiente, hospedero y ubicación

Los testimonios y varios hallazgos bibliográficos relacionan condiciones cálidas y relativamente secas con desarrollo y aumentos de población. No obstante, los rangos sugeridos en entrevistas no constituyen umbrales locales validados; los resultados que cambian simultáneamente temperatura y HR no permiten atribuir todo el efecto a una sola variable [BK, ENT-01, ENT-02, ENT-03].

La ubicación presenta una diferencia relevante. ENT-01 y E1 mencionan cogollos y tejidos tiernos, en una conversación que incluye ácaros rojos y blancos. E2 describe para *T. urticae* preferencia por hojas maduras y progresión de abajo hacia arriba al deteriorarse el alimento. Esta diferencia se conserva como cuestión abierta, relacionada potencialmente con especie, edad de hoja, contexto y etapa de infestación; no se resuelve por mayoría de entrevistados.

La identificación especializada y la observación con estratos y superficies documentados permitirán interpretar esa discrepancia. En tanto no se resuelva, no se recomienda excluir de la inspección ni cogollos ni hojas maduras.

#### 1.3.4. Alimentación y efectos visibles

La extracción de A011 y la exposición de E2 describen alimentación mediante perforación de células y consumo de su contenido. Este mecanismo se relaciona con pérdida localizada de coloración, punteado clorótico y, en ataques mayores descritos, deterioro y necrosis. Otras entrevistas mencionan curvatura y defoliación; cada efecto debe conservar el organismo y contexto a los que se atribuyó [BK, ENT-01, ENT-02, ENT-03].

Para el análisis visual se diferencian:

| Evidencia | Qué permite registrar | Qué no demuestra por sí sola |
|---|---|---|
| Organismo fotografiado | Presencia de un organismo visible | Identidad específica sin procedimiento suficiente |
| Huevos/estructuras compatibles | Indicio a revisar | Especie o viabilidad confirmadas |
| Exuvias | Estructuras asociadas a muda si se reconocen | Organismo vivo o individuo muerto |
| Tela | Estructura compatible con actividad de ciertos ácaros | Confirmación exclusiva de *T. urticae* |
| Punteado/decoloración | Efecto visible documentable | Causa exclusiva ni presencia actual |
| Sin detección | Resultado del método y esfuerzo utilizado | Ausencia absoluta en hoja/planta |

La detección directa del organismo mediante macrofotografía se distingue de la detección de síntomas y de cambios espectrales. Una hoja sin clorosis puede contener organismos visibles mediante aumento; por eso los estudios espectrales no se convierten en requisito automático de hardware para este objetivo.

La entrevista E2 no estableció el efecto cuantitativo sobre brotes o varetas de plantas madre. Los efectos sobre frutos y rendimiento de papaya no permiten concluir por sí solos una reducción de material de propagación cítrico. Ese componente debe describirse mediante evidencia pertinente o limitarse explícitamente.

#### 1.3.5. Implicaciones para el monitoreo

La información reunida respalda un procedimiento de inspección documentada, acompañado de contexto ambiental y validación de identificación. E2 recomienda observación de plantas marcadas y monitoreo aproximado cada ocho días como criterio de experiencia. No fijó un tamaño de muestra, unidad poblacional o umbral de acción para plantas madre locales [ENT-03].

El protocolo de la próxima visita combina mediciones periódicas del BME280 con muestras identificadas cercanas a las capturas. La transcripción manual de T/HR en el dashboard es aceptable si conserva muestra original, hora e instalación. La medición caracteriza el aire del punto, no el envés ni las condiciones acumuladas que experimentó el organismo antes de la fotografía [MET-01].

### 1.4. Triangulación y conocimiento resultante

| Tema | Literatura/base | Entrevistas | Situación de integración |
|---|---|---|---|
| Estadios | Extracción disponible, fichas incompletas | E2 aporta secuencia y larva de seis patas | Conocimiento estructurado; completar fuentes y rasgos |
| Duración | Valores de múltiples hospederos y parámetros | E2 contextualiza papaya; ENT-01 estima ciclo | No fusionar en constante local |
| Identificación | Requiere fuentes diagnósticas | E2 solicita laboratorio y plantea *P. citri* | Pendiente crítico |
| Ubicación | Estudios de distintos hospederos y morfologías | Cogollos frente a hojas maduras | Contrastar con especie y observación |
| Ambiente | Relaciones y tratamientos experimentales | Acuerdo general sobre calor; distinta interpretación de humedad | Hipótesis contextual, no umbral validado |
| Daño | Fuentes directas en cítricos y otras indirectas | Punteado, amarillamiento y otros efectos | Construir catálogo con alcance de identificación |
| Brotes/varetas | Evidencia específica por completar | Manejo local y límite reconocido por E2 | No cuantificado |
| Reglas | R1–R17 candidatas | Contraste conceptual iniciado | Depuración y clasificación pendientes |

La triangulación no busca eliminar todas las diferencias, sino explicar su alcance y determinar qué afirmaciones pueden sostenerse. Una discrepancia documentada es un resultado útil; una conclusión única sin fundamento no lo es.

### 1.5. Estado de cumplimiento y limitaciones

Con la evidencia disponible, el objetivo presenta **avance sustancial en fundamentación documental y levantamiento experto**, así como evidencia fotográfica inicial e instrumentos preparados para continuar la observación. Sin embargo, **todavía no corresponde declararlo completamente cumplido**.

Los puntos que impiden una conclusión definitiva son:

1. Identificación taxonómica del material local no confirmada.
2. Fichas del ciclo y parámetros numéricos todavía por depurar/cotejar.
3. Catálogo local sin consolidación completa de ubicación, método e identificación.
4. Registro ambiental de campo previsto, no aportado aún como resultado recuperado.
5. Reglas candidatas con extrapolaciones y errores pendientes de revisión.
6. Síntesis y anexos finales todavía por consolidar y revisar con el director.

La identificación tiene especial importancia: si el material corresponde a otro taxón, deberá discutirse el alcance con el director y decidir cómo obtener evidencia de la especie objetivo o ajustar formalmente el proyecto. No se sustituirá automáticamente el nombre de la especie en el anteproyecto ni se relabelarán todas las imágenes por una sospecha visual.

### 1.6. Conclusión preliminar del objetivo

WP1 ha permitido organizar una base de conocimiento, recuperar experiencia agronómica local y especializada, describir los componentes esenciales del ciclo de *T. urticae* y reconocer las condiciones que deben registrarse para interpretar su presencia y efectos visibles. También ha identificado una incertidumbre taxonómica que condiciona la interpretación de los registros locales.

El avance obtenido constituye un insumo para WP2, pero el cierre académico requiere completar la verificación del material, la observación trazable y la depuración de afirmaciones. El producto final deberá distinguir explícitamente **conocimiento publicado, testimonio experto y resultado local**, conservando sus condiciones y límites.

---

# Parte II. Cómo debe verse completado el objetivo

## 2. Correspondencia entre WP1, evidencia actual y resultado final

| Actividad | Lo que existe | Resultado que debe quedar entregado | Estado actual |
|---|---|---|---|
| **WP1.1. Revisión sistemática tecnológica** | Estado del arte en anteproyecto y matrices de referencias | Estrategia/selección trazables, referencias y síntesis crítica de detección y conocimiento | Avance documentado; comprobar expediente completo |
| **Fundamentación biológica complementaria** | 51 referencias candidatas excluyendo ejemplo A001; extracción P1–P10 | Fichas biológicas verificadas y contextualizadas, no acumulación de resúmenes | Avanzada, pendiente de depuración |
| **WP1.2. Trabajo de campo** | Visita/fotografías iniciales informadas; guía y registrador preparado | Observaciones de plantas madre, catálogo revisado, identificación y contexto medido/documentado | Parcial; identificación y consolidación críticas |
| **WP1.3. Entrevistas** | ENT-01, E1 y E2 sistematizadas | Perfil, soporte de uso, transcripción, matriz temática y triangulación | Avanzado; aclaraciones y soportes pendientes |
| **WP1.4. Base agrícola** | Hallazgos, R1–R17 y modelo preliminar | Diccionario, modelo de dominio y afirmaciones con procedencia/estado | Parcial; formalización documental pendiente |

No debe asignarse un porcentaje de cumplimiento solamente por contar referencias, preguntas o fotografías. La suficiencia se determina por cobertura y calidad de evidencia frente al objetivo.

## 3. Paquete final de entrega de WP1

### D1. Informe de revisión y matriz bibliográfica

Debe contener:

- Protocolo y registros de búsqueda de la revisión tecnológica.
- Registro de búsqueda biológica complementaria y criterio de pertinencia.
- Referencias completas y archivos/localizadores.
- A001 excluido y dependencias corregidas.
- Hallazgos críticos cotejados con originales.
- Matriz que distinga hospedero, ambiente, método y aplicabilidad.

**Criterio:** cada afirmación relevante de la sección puede remontarse a su fuente y contexto. Si un artículo no se recuperó o un dato no pudo verificarse, se señala; no se declara lectura completa.

### D2. Caracterización del ciclo y reproducción

Una ficha o tabla por estadio con:

```text
estadio → rasgos → actividad/alimentación → transición
        → duración y definición del parámetro
        → hospedero/condiciones → fuente
        → observado localmente: sí/no/no determinado
```

Separar media, rango, máximo, error o dispersión. No sumar duraciones de experimentos incompatibles para construir un «ciclo de Corsavida».

**Criterio:** secuencia completa, reconocimiento explicado, mecanismos reproductivos verificados y parámetros bien definidos. No es obligatorio observar localmente cada estadio si el alcance documental-descriptivo se conserva y el límite se explicita.

### D3. Expediente de entrevistas y triangulación

- Perfil y afiliación real de cada participante.
- Registro/transcripción y autorización según exigencias del proyecto.
- Respuestas completas, parciales y pendientes.
- Localizadores de tiempo/página.
- Matriz literatura–ENT-01–E1–E2–observación local.
- Discrepancias y decisiones interpretativas.
- Aclaraciones puntuales sobre reproducción, longevidad y alcance normativo.

**Criterio:** testimonio e interpretación no se mezclan y una misma entrevista copiada en distintas páginas no se cuenta como nueva evidencia.

Si E3 continúa pendiente, revisar con el director su aporte faltante. El número de entrevistas no define por sí solo suficiencia: la cuarta solo es imprescindible si cubre una necesidad no cubierta o forma parte de un compromiso metodológico que debe mantenerse.

### D4. Evidencia local e identificación

- Registro de visita y selección de plantas/hojas.
- Identificadores, ubicación, variedad cuando se conoce y estado de planta madre.
- Procedimiento/esfuerzo de inspección.
- Imágenes originales, vistas contextuales y macros.
- Identificación especializada, método y alcance del material examinado.
- Observaciones de síntomas, estructuras y confusores.
- Eventos de manejo y límites del periodo.

**Criterio:** existe evidencia local atribuible de forma defendible al objeto del objetivo; no se declara confirmación de especie por color o tamaño. Si no se obtiene, se documenta la limitación y se acuerda con el director cómo resolver el alcance antes de concluir.

### D5. Contexto ambiental y asociación con imágenes

- Esquema/montaje del nodo y configuración.
- Instalación, periodo, reloj, unidades y comprobaciones.
- CSV original y eventos, sin limpieza destructiva.
- Tabla foto–muestra con desfase temporal y alcance espacial.
- Resumen de calidad y resultados descriptivos del periodo medido.

**Criterio:** T/HR son datos medidos y recuperables, no cifras copiadas sin origen. La presión se conserva como auxiliar. No se exige registro continuo de semanas ni correlación causal para una caracterización descriptiva, pero la sesión ejecutada debe documentarse si se usa como resultado.

### D6. Base agrícola lista para WP2

- Diccionario: variable, definición, unidad, método, escala y valores desconocidos.
- Modelo de dominio con entidades/relaciones.
- Preguntas de competencia.
- Fuentes, hallazgos, interpretaciones y reglas en registros separados.
- R1–R17 clasificadas: contextual, candidata, revisada, pendiente o excluida.
- Restricciones de especie/hospedero y evidencias contradictorias.

**Criterio:** el conocimiento puede convertirse en ontología/grafo sin perder procedencia ni transformar incertidumbre en hecho. No se exige implementar el razonador dentro de WP1.

### D7. Capítulo y anexos de cierre

- Texto académico con metodología, resultados, triangulación y límites.
- Figuras/tablas con captions que indiquen origen.
- Bibliografía formal y enlaces/IDs de anexos.
- Matriz de cobertura del objetivo.
- Revisión y aceptación documentada por el director.

**Criterio:** la conclusión responde qué se caracterizó, con qué evidencia y hasta dónde se puede afirmar.

## 4. Qué añadir a la sección después de completar la visita

No rellenar estas tablas con valores propuestos o de literatura. Completar exclusivamente con archivos de campo comprobados.

### Tabla de ejecución

| Campo | Resultado a completar |
|---|---|
| Fecha y duración real | Pendiente de evidencia |
| Vivero, cubierta y sector | Pendiente de ficha final |
| Plantas observadas y criterio de selección | Pendiente de registros |
| Hojas/estratos/superficies examinadas | Pendiente de registros |
| Método y esfuerzo de búsqueda | Pendiente de protocolo ejecutado |
| Organismos/estadios identificados | Pendiente de revisión y reporte |
| Fotografías obtenidas/utilizables | Pendiente de catálogo |
| Identificación taxonómica | Pendiente crítico |
| Instalación y periodo ambiental | Pendiente de manifiesto/CSV |
| Lecturas válidas e incidencias | Pendiente de revisión de calidad |

### Tabla ambiental por instalación

| Instalación | Periodo | Muestras válidas/esperadas* | T mínima/media/máxima | HR mínima/media/máxima | Limitaciones |
|---|---|---|---|---|---|
| Por completar | Por completar | Por completar | Por completar | Por completar | Por completar |

\* Definir oportunidades de muestreo, pausas, reinicios y criterios de validez. Muestras de captura puntual y periódicas no se mezclan indiscriminadamente para calcular medias temporales.

### Tabla de observaciones y catálogo

| Observación | Planta/hoja | Estrato/superficie | Identificación y fundamento | Efecto visible | Imagen | Muestra ambiental asociada |
|---|---|---|---|---|---|---|
| Por completar | Por completar | Por completar | Por completar | Por completar | Por completar | Por completar |

Las fotografías repetidas de un mismo individuo/hoja y una muestra compartida no son réplicas independientes. El denominador biológico debe estar definido antes de informar densidades o porcentajes.

## 5. Figuras recomendadas para la versión final

1. **Secuencia del ciclo biológico**, con fuentes y condiciones de las cifras; no utilizar dibujos de internet sin atribución/licencia pertinente.
2. **Mapa del vivero y punto de medición**, altura, sector y plantas observadas.
3. **Montaje del registrador** y protección del elemento ambiental.
4. **Panel planta–hoja–macro**, vinculando escala de observación y códigos.
5. **Ejemplares/estructuras revisados**, diferenciando organismo, exuvia, huevo compatible y caso dudoso.
6. **Síntomas documentados**, con estado de identificación y límites de atribución.
7. **Serie T/HR del periodo real**, con eventos y huecos visibles.
8. **Modelo de dominio y trazabilidad** entre observaciones y conocimiento.

El caption de una foto debe decir lo sustentado: por ejemplo «ácaro observado pendiente de identificación», y no «adulto de *T. urticae*» mientras esa afirmación no esté respaldada.

---

# Parte III. Pendientes, aceptación y cierre

## 6. Pendientes priorizados

| Prioridad | Acción | Evidencia de terminado |
|---|---|---|
| **P0** | Acordar y ejecutar identificación del material local | Informe o registro especializado con método y ejemplares vinculados |
| **P1** | Recuperar diapositivas, tesis/tablas y cartilla de Yuri | Material recibido y localizadores de cifras |
| **P1** | Depurar ciclo, reproducción y longevidad | Fichas verificadas y preguntas aclaradas |
| **P1** | Excluir dependencias de A001 | Síntesis/reglas sin respaldo en el ejemplo |
| **P1** | Ejecutar y documentar observación local | Registros, catálogo y archivos recuperados |
| **P1** | Resolver o contextualizar ubicación cogollos/hojas maduras | Triangulación por especie, hospedero y observación |
| **P2** | Completar protocolo bibliográfico y referencias | Expediente reproducible de búsqueda/selección |
| **P2** | Depurar R1–R17 | Estado, fuente, contexto y razón de cada regla |
| **P2** | Consolidar diccionario/modelo | Variables y relaciones con procedencia |
| **P2** | Redactar capítulo y revisar con Fulvio | Versión de entrega y observaciones resueltas |

La visita, el registrador y el catálogo pueden avanzar mientras se coordina la identificación; las etiquetas taxonómicas y conclusiones específicas se mantienen pendientes. No es necesario paralizar todo el proyecto ni cerrar el objetivo sin resolver esa condición.

## 7. Lista de aceptación

- [ ] El alcance documental–experto–descriptivo está acordado con el director.
- [ ] WP1.1 conserva protocolo de búsqueda/selección y fuentes utilizadas.
- [ ] A001 está excluido y sus dependencias corregidas.
- [ ] Hay fichas completas de estadios, transiciones y reproducción.
- [ ] Duraciones y fecundidades mantienen definición, hospedero y condiciones.
- [ ] Los datos de papaya no se presentan como resultados de cítricos locales.
- [ ] Las entrevistas tienen perfiles, soportes, localizadores y análisis.
- [ ] La afiliación de Yuri se registra correctamente como declarada en ICA.
- [ ] Existe verificación defendible del taxón en material local, o una resolución formal del alcance con el director.
- [ ] Fotografías y observaciones están vinculadas con plantas/hojas y método.
- [ ] Se distinguen organismo, síntoma, exuvia, confusor y no detección.
- [ ] Los registros ambientales utilizados tienen origen, hora, unidades y ubicación.
- [ ] Las asociaciones foto–ambiente señalan desfase y alcance espacial.
- [ ] Las discrepancias están explicadas o conservadas como incertidumbres.
- [ ] R1–R17 y demás afirmaciones tienen procedencia, contexto y estado.
- [ ] El modelo de dominio distingue presencia, daño y riesgo.
- [ ] El capítulo incluye resultados propios y límites, no solo antecedentes.
- [ ] Los anexos y originales se pueden recuperar.
- [ ] El director revisó la cobertura y el cierre.

## 8. Cómo redactar la conclusión cuando sí esté completado

La conclusión final debe mencionar resultados concretos y evidencia real, no limitarse a «se realizaron entrevistas y se revisaron artículos».

**Plantilla, no declaración actual de cumplimiento:**

> El objetivo específico 1 se abordó mediante la integración de revisión documental, entrevistas a expertos y observación en plantas madre de cítricos bajo cubierta. La caracterización permitió describir los estadios y las transiciones de *Tetranychus urticae*, contextualizar sus parámetros de desarrollo y reproducción e identificar los elementos observables pertinentes para el monitoreo. La evidencia local, respaldada por [informe/método de identificación] y por [catálogo y registros de observación], documentó [ubicaciones, estadios y efectos efectivamente encontrados]. El ambiente se describió mediante [periodo e instalación reales], conservando la vinculación temporal y espacial con las observaciones. Los hallazgos se organizaron en [diccionario/modelo/matriz] como insumo para WP2, diferenciando conocimiento publicado, testimonio y evidencia local. Las duraciones de desarrollo utilizadas corresponden a sus fuentes y condiciones de origen; no se presentan como estimaciones experimentales locales. Las limitaciones [especificar] delimitan la aplicación de los resultados.

Reemplazar los corchetes solo cuando existan los entregables. Si la identificación o evidencia de la especie no se resuelve, utilizar una conclusión de avance/limitación o acordar modificación formal, no la plantilla de cumplimiento total.

## 9. Fuentes y trazabilidad de este borrador

Los códigos siguientes son localizadores de trabajo, **no referencias bibliográficas formales**. Antes de incorporarlo a la monografía, sustituirlos por citas completas o referencias a anexos y mantener los IDs de artículos para trazabilidad interna.

| Código | Fuente |
|---|---|
| **AP** | `documentacion/anteproyecto/main_anteproyecto.tex`, objetivo en línea 336 y WP1 en líneas 355–360 |
| **BK** | `Base de conocimiento CSV.txt`: catálogo A001–A052, extracción, R1–R17 y síntesis P1–P10; A001 confirmado como ejemplo |
| **ENT-01** | [Primera entrevista con agrónomo](https://app.notion.com/p/399a494a338880f38539cc52817dc3c7); tabla y transcripción indicada por el equipo |
| **ENT-02 / E1** | [E1 Ingeniero Agroforestal](https://www.notion.so/3d6a494a338880cd9346d2900d6f7881), Oscar Castillo; transcripción `Agroforestal 21 Septiembre.pdf` revisada previamente y sistematizada |
| **ENT-03 / E2** | [E2](https://www.notion.so/3d7a494a338880dc8915c879541c4082), transcripción aportada «Reunión Tesis Tetranychus Urticae», 10/10/2026, Yuri Mena; especial atención 26:16–33:28 y 41:38–44:31 |
| **OBS-01** | Visita inicial y fotografías originales informadas por el equipo; imagen compartida y pendiente de catalogación/identificación definitiva |
| **MD** | Modelo preliminar en [notas de reuniones](https://app.notion.com/p/eef6ecb2d6844f0eae38e210147d3cd1), especialmente reunión del 28 de agosto |
| **MET-01** | [Guía de medición](GUIA_PRIMERA_MEDICION_INVERNADERO.md) y [sketch](scripts/registrador_invernadero/registrador_invernadero.ino); instrumentos y procedimiento preparados, no resultados de campo |

### Recomendación de anexos

- Anexo A: estrategia y selección bibliográfica.
- Anexo B: matriz de hallazgos y fichas biológicas.
- Anexo C: instrumentos, transcripciones y autorizaciones.
- Anexo D: identificación y documentación de muestras.
- Anexo E: protocolo ejecutado, planillas y catálogo.
- Anexo F: montaje, CSV ambientales, eventos y asociaciones.
- Anexo G: diccionario, modelo de dominio y reglas candidatas.

**Síntesis de cierre:** lo ya realizado sustenta una sección académica sólida de avance. Para presentarla como cumplimiento completo, el paso determinante es convertir el conocimiento y los registros existentes en evidencia verificada, contextualizada y localmente atribuible a la especie objetivo.
