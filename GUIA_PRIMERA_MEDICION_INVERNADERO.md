# Primera medición en el invernadero — ESP32, BME280 y RTC

> **Versión vigente: 2.0.0-minimal.** [Sketch Arduino](scripts/registrador_invernadero/registrador_invernadero.ino). Utilizar el procedimiento breve inmediatamente siguiente. **Las secciones 1–28 se conservan como historial del diseño anterior:** LittleFS, CSV, contexto, diagnóstico y registro periódico ya no están implementados en el sketch actual. No ejecutar los comandos de esas secciones con esta versión.

## Procedimiento vigente — solo medir y mostrar

### Qué contiene ahora

La página local tiene únicamente dos botones:

1. **Verificar / ajustar RTC con el teléfono.**
2. **Registrar muestra.**

Cada muestra muestra ID, fecha/hora Colombia y UTC, **temperatura del BME280, humedad relativa y presión local**. El resultado queda fijo hasta solicitar otra lectura. También se imprime como JSON en serial a 115200.

No hay campos de visita, observación ni contexto. No hay muestreo automático, LittleFS, EEPROM, archivos CSV, descargas o conexión al dashboard. Todo el contexto se registra manualmente en la otra app. No se utiliza la temperatura del DS3231 como temperatura ambiental ni se calcula altitud.

**«Registrar muestra» significa obtener una lectura y mostrarla, no guardarla permanentemente.** Solo la última respuesta permanece en RAM. Un reinicio borra esa respuesta y reinicia el contador con un identificador de arranque distinto. Una recarga de página recupera la última muestra del nodo si este no se reinició. Anotar o guardar en dashboard antes de pedir otra muestra.

### Cableado, sin cambios

```text
ESP32 3V3 ──────┬──── BME280 VCC
                └──── DS3231 VCC
ESP32 GND ──────┬──── BME280 GND
                └──── DS3231 GND
ESP32 GPIO21 ───┬──── BME280 SDA
                └──── DS3231 SDA
ESP32 GPIO22 ───┬──── BME280 SCL
                └──── DS3231 SCL
```

Alimentación principal por USB-C del ESP32. Mantener pull-ups a 3,3 V y BME280 separado del calor del ESP32. Identificar el circuito del portapila antes de instalar CR2032; no cargar una pila no recargable. El arreglo eléctrico que ya funcionó no necesita cambios.

### Cargar y usar

1. Abrir `scripts/registrador_invernadero/registrador_invernadero.ino`.
2. Mantener la placa ESP32 Dev Module, puerto y bibliotecas BME280/RTClib que ya funcionaron.
3. Compilar/cargar. No hace falta crear ni formatear un filesystem. La nueva versión no usa ni borra archivos existentes; un borrado total o cambio de particiones desde el IDE sí puede afectar datos anteriores.
4. Conectar Android B a `TESIS-NODO-01`; contraseña configurada en `AP_PASSWORD` del sketch. Mantener conexión aunque Android indique que no hay Internet.
5. Abrir `http://192.168.4.1`, o la IP que indique serial. **Recargar la página después de actualizar el firmware** para no seguir usando la interfaz anterior.
6. Comprobar hora correcta del teléfono y pulsar el primer botón. Se envía UTC al DS3231, sin Internet. Repetir después de cada reinicio del ESP32.
7. Pulsar **Registrar muestra**. El programa realiza una medición forzada nueva; no muestra una lectura periódica antigua.
8. Revisar que el sensor indique OK. B dicta T/HR, hora e ID de muestra; A fotografía y anota en el dashboard o planilla.
9. El resultado queda fijo; pedir otra muestra cuando corresponda a una nueva observación o cuando cambien condiciones.

La interfaz exige ajustar/verificar el reloj antes de obtener muestras. Si sensor o conexión fallan, se indica el error y no se presenta la lectura anterior como una adquisición nueva. Cada pulsación nueva solicita una lectura nueva; no hay cola persistente de reintentos ni historial de muestras.

### Flujo de campo mínimo

```text
Android B: conectar al ESP32 → ajustar RTC → registrar muestra
                    ↓ dicta T/HR + hora + ID
Android A: tomar foto → anotar contexto y valores en dashboard
```

Objetivo operativo: fotografía cercana a la lectura —por ejemplo, dentro de 30 segundos—, con hora real anotada. El sensor puede permanecer fijo y protegido; indicar que es ambiente del punto de referencia, no temperatura de la hoja. Una muestra puede acompañar varias imágenes del mismo grupo breve, dejando constancia de que comparten el dato.

Si A no tiene Internet y el dashboard no trabaja offline, conservar fotos en galería y datos en planilla para cargarlos después. **Esta versión no ofrece un respaldo de archivos en el ESP32.** No dejarlo instalado esperando encontrar una serie histórica al regresar.

### Serial opcional

Monitor a 115200, terminación nueva línea:

```text
STATUS
TIME <epoch_UTC_actual>
CAPTURE
```

`TIME` es alternativa al ajuste con el teléfono; no usar hora de compilación. `CAPTURE` obtiene la muestra y la imprime; `STATUS` consulta estado y última respuesta en RAM. No existen `FORMAT`, `DIAG`, `CONTEXT`, `FILES`, `DUMP`, `PAUSE` o `RESUME` en esta versión.

### Prueba antes de ir

- [ ] Página muestra solo dos botones, sin interfaz antigua en caché.
- [ ] RTC verificado con fecha/hora correcta.
- [ ] Cada pulsación produce ID nuevo y T/HR/presión.
- [ ] Lectura fija y transcripción completada antes de la siguiente.
- [ ] Fallo de red/sensor no confunde una lectura anterior con una nueva.
- [ ] Flujo de fotos y anotaciones ensayado con ambos Android sin Internet.

---

## Historial del diseño extendido — no corresponde al firmware mínimo actual

## 1. Propósito y decisiones de esta guía

Construir un registrador ambiental con el equipo disponible y ejecutar una visita que produzca **mediciones e imágenes vinculadas, interpretables y recuperables** para el objetivo 1 / WP1.

**Equipo identificado mediante las especificaciones aportadas:** ESP32-WROOM-32 de 30 pines con interfaz USB–serie CP2102 y conector USB-C; módulo BME280 versión 3,3 V; módulo RTC DS3231 con EEPROM AT24C32. Se dispone de dos teléfonos Android, accesorio macro de aumento declarado 200× y un dashboard con base de datos para fotografías. La pila CR2032 no está incluida.

**Todavía por comprobar físicamente:** pinout serigrafiado y revisión de la placa, tamaño real de flash y particiones, circuito de carga/pull-ups del módulo RTC, dirección del BME280, disponibilidad de microSD, alimentación y funciones reales del dashboard. Esta guía no presume que el dashboard ya importe CSV, trabaje offline o registre todos los campos propuestos. Las especificaciones de tienda son información de partida, no una verificación del montaje ni un certificado metrológico.

### Resultado mínimo de la visita

1. Una serie de temperatura y humedad relativa del aire de un punto identificado.
2. Presión atmosférica como variable auxiliar del BME280, claramente diferenciada.
3. Un registro de instalación y de eventos: movimientos, riego, fallas y manejo conocido.
4. Observaciones de plantas y hojas con fotografías originales y códigos de vínculo.
5. Un paquete de datos original, respaldado, con incidencias y límites documentados.

**La visita no medirá la duración individual del ciclo del ácaro ni validará umbrales de infestación.** Una serie ambiental corta caracteriza ese punto y periodo, no el ambiente de todo el vivero ni el microclima exacto de cada hoja.

---

## 2. Arquitectura que sí podemos construir ahora

```text
BME280 ── I²C ──┐
                ├── ESP32 ── archivo CSV local ── descarga y respaldo
RTC ───── I²C ──┘       │                              │
                        └── estado y descarga          └── vinculación con dashboard
                            por USB o página local

Android: fotografías originales + observaciones + hora/códigos
```

### Configuración inicial recomendada

- Un nodo ambiental **fijo** durante la sesión principal.
- Lectura cada **60 segundos**, configurable y registrada en el manifiesto.
- BME280 en modo de medición forzada si la biblioteca permite configurarlo correctamente; medir y dejarlo en reposo entre muestras.
- RTC como referencia temporal persistente; ESP32 para programación de intervalos y diagnóstico.
- Registro local independiente de Wi-Fi.
- LED de estado o mensajes por USB; página local de descarga si se implementa.
- Fotografías con la cámara del teléfono y posterior carga al dashboard.
- T y HR por fotografía asociadas mediante una muestra identificada —preferiblemente recién adquirida cerca de la captura—, manteniendo también el registro periódico. Ver secciones 13 y 22.
- Ningún control automático de riego ni alerta biológica en esta primera versión.

El BME280 mide **temperatura de su elemento sensor**, que puede aproximar la del aire si se instala correctamente; **HR del aire**, no humedad del sustrato; y presión atmosférica. No mide temperatura foliar, agua en bolsas, iluminación, población de ácaros ni especies.

---

## 3. Identificar los componentes antes de conectar

Fotografiar ambas caras de cada módulo y anotar referencias. No trabajar solamente con nombres comerciales.

| Componente | Comprobar | Decisión |
|---|---|---|
| ESP32 | Modelo de placa, módulo, pinout, flash y pines reservados | Elegir pines reales de I²C y alimentación |
| BME280 | Marcado, etiquetas, regulador y esquema del breakout | Confirmar que es BME280 y no BMP280 |
| RTC | DS3231, DS1307, PCF8523 u otro; tensión; pull-ups; circuito de batería | Seleccionar biblioteca y conexión compatibles |
| Alimentación | Fuente/batería, tensión de entrada de la placa y estabilidad | Probar autonomía real |
| Almacenamiento | Flash libre, partición o microSD disponible | Elegir una de las rutas de la sección 5 |

### BME280 frente a BMP280

El BMP280 no mide humedad. Comprobar inicialización, identificación del chip y disponibilidad de HR; no confiar solo en la etiqueta de la tienda. El identificador esperado del BME280 es habitualmente `0x60`; corroborarlo con la documentación del componente y biblioteca. Un escáner I²C detecta una dirección, **no confirma por sí solo la identidad del sensor**.

### RTC identificado: DS3231 + AT24C32

- Usar `RTC_DS3231` de RTClib; comprobar `begin()`, `lostPower()` y fecha plausible. Su termómetro interno no reemplaza al BME280.
- Alimentar el módulo inicialmente a **3,3 V**, conforme al rango declarado, compartiendo GND y bus con el BME280. Verificar que las pull-ups estén referidas a 3,3 V.
- La AT24C32 es una memoria de **32 kbit = 4.096 bytes**, no 32 kB. Es distinta del reloj y de la flash del ESP32; no será el almacenamiento principal de CSV.
- DS3231: dirección habitual `0x68`; AT24C32: habitualmente `0x57` en este módulo, modificable por A0/A1/A2. Comprobar las direcciones reales.
- Comprar la CR2032 indicada únicamente después de comprobar que el módulo no intenta cargarla. Algunos módulos comerciales incorporan un circuito de carga para otra química. **Una pila no recargable no debe conectarse a un circuito que la cargue.** La ficha comercial no basta para determinar ese circuito; consultar esquema, fotografías o medición por personal competente.
- Sin pila, el nodo puede registrar durante una sesión alimentada, pero no debe confiar en persistencia de hora tras desconexión; comprobar y ajustar al encender. Para la visita se recomienda respaldo de hora probado.

---

## 4. Cableado y construcción física

### Diagrama del montaje completo: ambos módulos en el mismo bus

**Sí: BME280 y DS3231 se conectan a GPIO21 y GPIO22 simultáneamente, en paralelo.** I²C utiliza dos señales compartidas:

- **SDA:** datos; en este montaje GPIO21.
- **SCL:** reloj de comunicación; en este montaje GPIO22.

Además, cada módulo necesita **alimentación y tierra**. Por tanto, no se usan únicamente dos conexiones: cada módulo tiene cuatro conexiones básicas. El ESP32 selecciona el dispositivo por su **dirección I²C**, no utilizando un par de GPIO diferente para cada sensor.

```text
                          ESP32-WROOM-32
                       Placa de desarrollo
                      ┌────────────────────┐
 Fuente USB 5 V ──────►│ Conector USB-C     │
                      │                    │
                      │ 3V3   ●────────────┼──────┬──────────────────────┐
                      │ GND   ●────────────┼──────┼──┬───────────────────┼──┐
                      │ GPIO21●────────────┼──────┼──┼──┬────────────────┼──┼──┐
                      │ GPIO22●────────────┼──────┼──┼──┼──┬─────────────┼──┼──┼──┐
                      └────────────────────┘      │  │  │  │             │  │  │  │
                                                  │  │  │  │             │  │  │  │
                                         ┌────────┴──┴──┴──┴───┐ ┌───────┴──┴──┴──┴─────┐
                                         │ VCC GND SDA SCL     │ │ VCC GND SDA SCL      │
                                         │                    │ │                      │
                                         │ BME280 — 3,3 V      │ │ DS3231 + AT24C32     │
                                         │ I²C: 0x76 o 0x77    │ │ RTC I²C: 0x68        │
                                         │                    │ │ EEPROM: usual 0x57   │
                                         └────────────────────┘ └──────────────────────┘
```

**Lectura del dibujo:** cada señal se ramifica hacia ambos módulos. Los cruces de líneas no representan conexiones entre señales; solo se conectan las ramas indicadas. Si el diagrama se ve desalineado en el visor, usar la tabla de cableado siguiente como referencia definitiva.

#### Diagrama por señal, sin cruces

```text
ESP32 3V3 ──────┬──────── BME280 VCC
                └──────── DS3231 VCC

ESP32 GND ──────┬──────── BME280 GND
                └──────── DS3231 GND

ESP32 GPIO21 ───┬──────── BME280 SDA (puede llamarse SDI)
                └──────── DS3231 SDA

ESP32 GPIO22 ───┬──────── BME280 SCL (puede llamarse SCK)
                └──────── DS3231 SCL
```

#### Lista exacta de conexiones

| Origen en ESP32 | Destino en BME280 | Destino en DS3231 | Función |
|---|---|---|---|
| **3V3** | **VCC** | **VCC** | Alimentar ambos módulos a 3,3 V |
| **GND** | **GND** | **GND** | Tierra común |
| **GPIO21** | **SDA / SDI** | **SDA** | Datos I²C compartidos |
| **GPIO22** | **SCL / SCK** | **SCL** | Reloj I²C compartido |

Esto equivale a cuatro redes compartidas y, por ejemplo, **ocho cables hacia los módulos** si se hacen dos ramas por cada red. No unir SDA con SCL ni unir alimentación con señales. En protoboard se puede usar un punto común por señal y rieles de alimentación; verificar si los rieles están partidos y necesitan puente.

### ¿Cómo distingue el ESP32 a los dispositivos?

| Dispositivo | Dirección esperada | Uso en el programa |
|---|---|---|
| BME280 | **0x76**, confirmada en tu ensayo; alternativa 0x77 | T, HR y presión |
| DS3231 | **0x68** | Fecha y hora |
| AT24C32 del módulo RTC | Habitualmente **0x57** | No utilizada por este sketch |

No hay conflicto entre esas direcciones. La EEPROM puede aparecer en un escáner aunque no se utilice. El sketch consulta BME280 y RTC **secuencialmente sobre el mismo bus**; funcionan juntos durante la visita, sin que ambas transacciones se ejecuten literalmente al mismo instante.

El reloj **SCL del bus** es generado por el ESP32 y no es el pin **SQW** del DS3231. No conectar SQW al GPIO22. Los pines **SQW** y **32K** del RTC se dejan sin conexión en esta versión.

### Alimentación, ubicación y pines adicionales

- Alimentar la placa ESP32 por **USB-C**, y desde su pin **3V3** alimentar los módulos. La entrada USB de 5 V no significa que deban alimentar el BME280 a 5 V.
- Usar las etiquetas de la placa: **21 / IO21 / GPIO21** y **22 / IO22 / GPIO22**. No contar posiciones del conector: una placa de 30 pines puede cambiar su distribución según fabricante.
- Verificar orden de pines en cada módulo: el dibujo es **eléctrico**, no una reproducción a escala de su serigrafía. Si VCC está a la derecha de tu módulo, conectarlo allí, no donde aparece en el dibujo.
- Mantener BME280 separado físicamente de ESP32/RTC y batería. El dibujo agrupa componentes para mostrar conexiones, no recomienda pegarlos entre sí.
- Si BME280 expone **CS/CSB y SDO**, mantener la configuración I²C que funcionó en el ensayo individual. Habitualmente CSB se lleva a VDDIO para I²C y SDO selecciona 0x76/0x77; verificar si ya existen resistencias en el módulo antes de agregar conexiones. Si solo expone cuatro pines, esos ajustes normalmente están resueltos en la placa.
- Las pull-ups de SDA/SCL deben referirse a **3,3 V**. Muchos módulos ya las incorporan; no agregar un juego por cada dispositivo sin evaluar la resistencia equivalente. Si el bus no tiene pull-ups, un único par de aproximadamente 4,7 kΩ a 3V3 es un punto de partida para el cableado corto a 100 kHz, sujeto a comprobación.
- La pila del RTC va en su portapila, **no al pin 3V3 del ESP32**. Su compatibilidad con el circuito del módulo se comprueba como se explica en la sección 3.

### Comprobación después de unirlos

1. Desconectar USB y revisar los ocho destinos contra la tabla.
2. Confirmar alimentación de 3,3 V, tierra común y que SDA/SCL no estén intercambiados.
3. Reconectar y cargar el sketch integrado de la sección 27.
4. Abrir serial a 115200 y comprobar **BME=ok** y **RTC=ok**.
5. Verificar hora explícitamente y solicitar una muestra.
6. Comprobar T/HR del **BME280**, fecha/hora del **DS3231** y registro CSV. La temperatura interna del RTC no se utiliza como ambiente.

No hace falta otro ESP32, otro bus, multiplexor ni GPIO adicionales para estos dos módulos con direcciones distintas. USB alimenta el nodo; la flash interna guarda el CSV y no requiere cableado externo.

### Interfaz I²C

| ESP32 | BME280 | RTC |
|---|---|---|
| GND | GND | GND |
| GPIO21 — SDA | SDA / SDI según módulo | SDA |
| GPIO22 — SCL | SCL / SCK según módulo | SCL |
| 3V3 | VCC 3,3 V | VCC 3,3 V |

**Configuración adoptada para el ESP32-WROOM-32:** SDA = GPIO21 y SCL = GPIO22, comprobando esas etiquetas en la placa de 30 pines. Orientarse por GPIO serigrafiado, no por el número de posición de un pin. No copiar esta asignación a una placa C3/S3 diferente.

- Los GPIO del ESP32 trabajan a 3,3 V; no exponerlos a pull-ups de 5 V.
- Verificar dónde están conectadas las resistencias pull-up de cada módulo. Si un RTC necesita 5 V y eleva el bus a 5 V, hace falta adaptar niveles o modificar el montaje según su esquema.
- No alimentar un chip BME280 desnudo a 5 V; ciertos breakouts tienen regulador, pero eso debe comprobarse.
- En breakouts que exponen CS/CSB y SDO, configurar modo I²C y dirección según documentación; no dejar pines requeridos flotantes.
- Direcciones habituales: BME280 `0x76` o `0x77`; varios RTC usan `0x68`. Confirmar con escáner y pruebas individuales.
- Comenzar a 100 kHz, con cables cortos y GND común. No tender I²C por sectores del vivero.
- Revisar conexiones sin energía. Probar primero cada módulo y después el bus compartido.

### Montaje para medir el aire

```text
Protector de radiación ventilado
  └── BME280, separado de superficies calientes
       └── cable corto y fijado
            └── caja de electrónica: ESP32 + RTC + almacenamiento
                 └── alimentación
```

- Mantener BME280 separado del ESP32, regulador, batería y pantalla: su calor sesga temperatura y HR.
- No encerrar el sensor en la misma caja hermética que la electrónica.
- Usar un protector de radiación ventilado, preferiblemente diseñado para ese propósito. Una cubierta improvisada debe documentarse y evaluarse como limitación.
- Evitar sol directo, contacto con hojas, paredes, metal caliente y chorros de agua.
- No aplicar barniz, cinta o adhesivo sobre la abertura del sensor.
- No apoyar el sensor sobre la hoja para intentar medir su temperatura.
- Para dejarlo instalado, reemplazar conexiones sueltas de protoboard por conectores firmes o montaje soldado; fijar cables y caja.

**Una buena ubicación importa más que mostrar muchos decimales.** El BME280 no es impermeable por estar en un módulo.

---

## 5. Almacenamiento: elegir y probar antes de salir

No se ha confirmado microSD. Por eso el registrador no debe diseñarse suponiendo que ya existe.

### Ruta A — Flash interna con LittleFS: mínimo autónomo

Es viable para esta primera visita si la placa dispone de una partición suficiente y el firmware permite descargar archivos.

- Configurar una partición de archivos conocida y registrar su capacidad.
- Guardar CSV en modo append; sincronizar/cerrar cada lectura a este ritmo de muestreo.
- Descargar por USB mediante procedimiento implementado, o por página HTTP local del ESP32.
- Medir espacio disponible; mantener un margen explícito y detener nuevas escrituras con aviso si se alcanza, sin sobrescribir datos anteriores silenciosamente.
- **No formatear automáticamente LittleFS cuando falla el montaje.** La recuperación y el borrado deben ser operaciones explícitas después de respaldar.
- No reprogramar, cambiar particiones o borrar flash antes de descargar y verificar los archivos de campo.
- No usar NVS/Preferences para almacenar toda la serie; reservarlo para configuración pequeña.

### Ruta B — microSD: preferida si se puede incorporar

- Usar tarjeta confiable y módulo compatible con lógica de 3,3 V.
- CSV y FAT32 facilitan extracción con lector. Verificar tamaño/formato admitido por la biblioteca.
- Sincronizar escrituras y ofrecer parada segura antes de retirar la tarjeta.
- La SD facilita capacidad y recuperación, pero FAT sigue siendo vulnerable a cortes de energía.
- Fijar pines SPI según placa y evitar conflictos con I²C/USB/arranque.

### Ruta C — USB a computador: respaldo para visita atendida

Si no hay almacenamiento autónomo implementado, registrar el puerto serie a un archivo en un computador y comprobar el proceso completo.

- Depende del computador, cable y programa de captura.
- No basta con que el monitor serie muestre valores: tiene que guardar un archivo verificable.
- No es una opción para dejar solo el nodo instalado.

### Capacidad orientativa

Con una fila aproximada de 250 bytes y una lectura por minuto:

| Duración | Filas | Tamaño aproximado, sin archivos auxiliares |
|---|---:|---:|
| 6 horas | 360 | 90 kB |
| 24 horas | 1.440 | 360 kB |
| 72 horas | 4.320 | 1,08 MB |

Son cálculos de planificación, no mediciones del tamaño real. Una partición de 1 MB no alcanza cómodamente 72 horas en ese supuesto. Comprobar el CSV real, eventos y margen de almacenamiento. El intervalómetro y los reinicios no deben crear filas duplicadas ni omitir registros sin diagnóstico.

---

## 6. Firmware: requisitos que debe cumplir

Se puede desarrollar en C++ con framework Arduino para ESP32 y dependencias fijadas. Esta guía es un protocolo de construcción; **no implica que el firmware ya exista o esté probado**.

Bibliotecas adoptadas para una primera implementación: `Adafruit BME280 Library`, sus dependencias `Adafruit Unified Sensor` / `Adafruit BusIO`, y `RTClib` con clase `RTC_DS3231`. Usar `Wire`, `LittleFS`, `WiFi` y `WebServer` del core Arduino-ESP32 según las funciones implementadas. Fijar y registrar versiones del core y bibliotecas después del ensayo. La EEPROM no necesita controlador si no se utiliza.

### Configuración persistente

```text
device_id: NODO-01
session_id: UUID o código de la visita
deployment_id: UUID o código del periodo de instalación
sample_interval_seconds: 60
timezone_display: America/Bogota
sensor_address: 0x76 o 0x77 comprobada
firmware_version: versión del programa
schema_version: versión del CSV
```

Configuración inicial adoptada: modo forzado, oversampling de temperatura ×1, presión ×1 y humedad ×1, filtro IIR desactivado. Es suficiente como punto de partida para el piloto; documentar cualquier cambio. Ejecutar `takeForcedMeasurement()` antes de leer y comprobar su resultado. La biblioteca debe esperar la conversión; no presentar registros antes de que termine ni tratar los máximos de velocidad del bus como frecuencia necesaria de muestreo.

### Arranque

1. Mostrar identificador y versión.
2. Comprobar almacenamiento sin borrarlo.
3. Comprobar sensor y su identidad.
4. Comprobar RTC, bandera de pérdida de hora si existe y plausibilidad de fecha.
5. Crear `boot_id` nuevo y registrar causa de reinicio cuando esté disponible.
6. Abrir archivo e iniciar adquisición o mostrar fallo explícito.

### Ciclo de adquisición

```text
Cada 60 segundos, con programación monotónica:
  obtener RTC y estado de hora
  iniciar/esperar medición de BME280
  leer temperatura, HR y presión
  validar valores finitos y estado de respuesta
  construir registro con secuencia y uptime
  escribir y sincronizar
  registrar estado de escritura
  actualizar indicador y última lectura
```

- Programar intervalos con un reloj monotónico (`millis`/temporizador), no mediante igualdad de segundos del RTC.
- No bloquear el muestreo esperando Wi-Fi.
- Descargar archivos no debe alterar el intervalo sin dejar un evento.
- No resetear la hora en cada arranque a la fecha de compilación.
- Una falla de lectura genera una fila con valores vacíos y estado de error; no reutilizar la última medición como si fuera nueva.
- Una falla de almacenamiento se muestra y registra por un canal alternativo cuando sea posible.
- Si hay muestras retrasadas, no inventar valores intermedios; registrar retraso o hueco.

### Indicadores mínimos

| Estado | Indicación sugerida |
|---|---|
| Registro activo | Pulso breve periódico |
| Sensor no disponible | Patrón distinto + mensaje |
| Hora inválida | Aviso específico, continuar con secuencia/uptime |
| Almacenamiento fallido/lleno | Aviso persistente |
| Parado y listo para descarga | Estado claramente distinto |

Un LED aislado no prueba que se están guardando datos: comprobar también contador de filas, última escritura y descarga.

---

## 7. Hora y CSV: contrato de datos

### Sincronización

- Ajustar RTC antes de salir con una referencia confiable y anotar el ajuste.
- Recomendación: guardar UTC en RTC y archivos; mostrar Colombia en el dashboard.
- Si se usa hora local, incluir siempre el offset `-05:00` y documentar esa decisión; no mezclar ambas convenciones.
- Registrar estado y batería del RTC, así como diferencia inicial y final frente a referencia.
- Una pila del RTC conserva la hora, **no alimenta el ESP32**.
- Confirmar que ambos teléfonos tienen hora correcta antes de fotografiar.
- EXIF suele carecer de zona horaria explícita: conservar fuente de hora y verificarla, no asumir UTC.

### CSV propuesto

```csv
schema_version,device_id,session_id,deployment_id,boot_id,sequence,timestamp_utc,uptime_ms,time_status,temperature_c,relative_humidity_pct,pressure_pa,sensor_status
1,NODO-01,VIS-001,DEP-001,BOOT-001,1,2026-10-20T14:00:00Z,60000,valid,27.43,61.20,83540,ok
1,NODO-01,VIS-001,DEP-001,BOOT-001,2,2026-10-20T14:01:00Z,120000,valid,,,,read_error
```

**Ejemplo sintético de formato; fecha y valores no corresponden a una visita realizada.** Usar punto decimal, comas y cabecera única por archivo. La combinación dispositivo + boot + secuencia identifica una muestra; la secuencia reiniciada necesita nuevo boot.

- `pressure_pa`: presión medida en el lugar, en Pa. Si la biblioteca devuelve hPa, convertir explícitamente y documentarlo.
- No convertir a presión al nivel del mar sin método y metadatos; no comparar automáticamente con una aplicación meteorológica que use otro tipo de presión.
- `timestamp_utc` vacío cuando no hay hora válida; guardar uptime y evento para posible reconstrucción posterior.
- Conservar mediciones originales. Redondear solo para visualización; varios decimales no implican esa exactitud.
- HR fuera de 0–100 % y valores no finitos requieren señalamiento y revisión; no corregirlos silenciosamente.

### Manifiesto de instalación

Guardar `manifest.json` o documento equivalente con:

```text
dispositivo, placa, sensor y RTC
firmware y configuración
fuente de alimentación
tipo/capacidad de almacenamiento
ubicación, altura y foto del montaje
fecha/hora de instalación y retirada
fuente de hora y diferencias comprobadas
intervalo esperado
unidades
modo, oversampling y filtro del BME280
protector de radiación y longitud aproximada de cable
incidencias y condiciones de manejo conocidas
```

---

## 8. Ensayo previo: condición para llevar el nodo

### Pruebas de construcción

1. Leer sensor solo y comprobar que hay HR y presión.
2. Leer RTC solo, ajustar y comprobar persistencia de hora sin alimentación principal.
3. Integrar I²C y verificar estabilidad.
4. Registrar al menos dos horas y descargar CSV.
5. Ensayar el equipo montado durante un periodo comparable al previsto; para dejarlo varios días, probar autonomía y almacenamiento con margen suficiente.
6. Probar fallas controladas con datos de prueba: sensor desconectado, reinicio, falta de espacio y descarga interrumpida.
7. Verificar que no se formatean o borran datos al recuperarse.
8. Importar o abrir el CSV y comprobar columnas, unidades y hora.

Para un intervalo de 60 segundos, dos horas contienen aproximadamente 120 muestras; el número exacto depende de si se registra al inicio y al final. Comparar con la programación real, no con una cifra fija sin definición.

### Verificación de medición

- Comparar con un instrumento de referencia prestado si existe, registrando modelo y estado metrológico.
- Colocarlos próximos bajo condiciones similares y esperar estabilización.
- Observar diferencias y cambios durante un periodo, no solo una lectura.
- Sin referencia, documentar comprobación funcional; no afirmar calibración.
- No corregir offset solo para que coincida con una estación lejana o una app meteorológica.
- No usar aliento, inmersión o contacto con la mano como calibración de humedad/temperatura.

### Checklist de autorización operativa

- [ ] Modelo de ESP32 y RTC identificado.
- [ ] Cableado, niveles lógicos y batería del RTC comprobados.
- [ ] BME280 confirmado, incluida HR.
- [ ] Registro sin internet funciona.
- [ ] CSV se recupera y abre correctamente.
- [ ] Reinicio no borra datos ni cambia la hora silenciosamente.
- [ ] Fallos no aparecen como ceros o mediciones repetidas.
- [ ] Fuente de energía probada, incluido apagado automático del power bank.
- [ ] Protector, soporte y caja preparados.
- [ ] Dashboard probado con archivos reales de ambos Android.
- [ ] Plan alternativo de planilla/galería preparado.

---

## 9. Preparación de la visita

### Una semana o los días disponibles antes

1. Confirmar acceso, fecha, duración, personal y restricciones por aplicaciones recientes.
2. Preguntar si el nodo puede permanecer y quién podrá revisarlo.
3. Conocer plantas madre disponibles, identificación y variedades.
4. Acordar ubicación ambiental y preguntas de observación.
5. Acordar manejo de hojas: no arrancarlas sin autorización y sin registrar cambio de condición.
6. Consultar riego, poda y extracción de varetas recientes.
7. Preparar etiquetas legibles, plano básico y planillas.

### Preguntas que se busca responder

- ¿Dónde se observaron organismos durante esta inspección?
- ¿Qué estrato, edad de hoja, superficie y zona corresponden?
- ¿Qué efectos visibles acompañan esas observaciones?
- ¿Qué identificación hizo el experto y con qué fundamento?
- ¿Qué condiciones del punto ambiental se registraron durante esas capturas?
- ¿Es reproducible el método de fotografía y registro?

### Selección descriptiva

Cubrir, cuando estén disponibles, estratos alto/medio/bajo, hojas jóvenes/maduras y haz/envés. No limitar de antemano la búsqueda a cogollos o a estratos bajos: precisamente existe una discrepancia que se quiere documentar.

**Propuesta piloto ajustable:** seis plantas identificadas y dos hojas por estrato disponible, con una duración de inspección objetivo acordada antes de comenzar. Es una meta logística, no cálculo de representatividad. Si hay menos plantas o el acceso limita hojas, registrar el esfuerzo real. Aumentar el número solo si mantiene calidad de inspección y trazabilidad.

No seleccionar únicamente plantas evidentemente dañadas. Incluir casos sin detección durante el procedimiento y describir cómo se seleccionaron. Si se busca estimar prevalencia, hará falta un diseño de muestreo diferente.

---

## 10. Agenda operativa de una visita de 3–4 horas

Adaptar al acceso real y conservar horas efectivas.

| Momento | Actividad | Evidencia |
|---|---|---|
| Inicio | Reunión breve, identificar manejo reciente y sectores | Acta/bitácora |
| Primeros 20–30 min | Instalar nodo, comprobar archivos y esperar estabilización | Instalación, foto, hora y estado |
| En paralelo | Prueba conjunta de registro y fotografía en primeras hojas | Criterios acordados |
| Bloque principal | Observaciones y fotografías con nodo fijo | Registros y originales |
| Últimos 20–30 min | Revisar identificaciones, pendientes y descarga | Revisión con experto y respaldo |
| Cierre | Retirar o formalizar permanencia del nodo | Hora de cierre/acuerdo |

Los 20–30 minutos son una reserva operativa inicial, no tiempo de respuesta garantizado. Registrar cuándo las lecturas parecen estabilizarse y si cambió el entorno. Conservar las lecturas iniciales, señalándolas para análisis.

### Distribución práctica

- Persona A: inspección y fotografía.
- Persona B: códigos, planilla, condiciones y revisión del registrador.
- Revisar juntos las primeras observaciones; intercambiar roles en un pequeño bloque para comprobar que usan los mismos criterios.
- El experto revisa identificación y dudas. No asumir que toda «arañita» sea T. urticae, especialmente cuando se mencionan roja y blanca.

---

## 11. Ubicación y límites con un único sensor

### Sesión principal

Elegir un punto fijo, a altura representativa del follaje, con posición documentada. No atribuirle cobertura de todo el invernadero. Evitar proximidad accidental a ventilador, entrada, techo, suelo o riego que distorsione el propósito; si se elige una de esas zonas deliberadamente, explicarlo.

### Si se quiere explorar otros puntos

- Hacerlo después del bloque principal o en una prueba separada.
- Parar/anotar movimiento, asignar otro `deployment_id`, fotografiar posición y esperar estabilización.
- Medir durante un periodo definido y registrar su hora.
- Interpretar como exploración **no simultánea**: cambios pueden deberse a lugar y hora.
- Una secuencia centro→borde no prueba por sí sola que el borde es más cálido.

Si dejan el nodo, mantener la instalación identificada y no permitir movimientos sin anotarlos.

---

## 12. Fotografías y dashboard: obtener un dataset útil

### Antes de salir

- Probar acceso, carga múltiple y consulta en ambos teléfonos.
- Confirmar campos disponibles y tamaños/formats aceptados.
- Crear visita y plantas conocidas si el dashboard lo permite.
- No dar por hecho soporte offline: comprobarlo. Si no existe, tomar fotos en galería y usar planilla local/papel para subir después.
- Limpiar lente y accesorio; verificar batería y espacio.
- Comprobar hora y evitar apps de mensajería como vía de transferencia de originales.

### Secuencia por observación

1. Identificar planta y hoja.
2. Foto de contexto de planta/estrato cuando sea necesaria.
3. Foto de hoja completa, idealmente indicando superficie.
4. Macro del organismo o región de interés.
5. Segunda macro si aporta enfoque o detalle adicional.
6. Registrar observación y vínculos de archivos antes de cambiar de hoja.

Usar soporte o apoyos que no dañen la planta. Mantener posición durante enfoque y evitar reflejos/LED saturado. Revisar la imagen a tamaño ampliado, no solo la miniatura. Conservar también los casos limitados si documentan el procedimiento, pero separarlos del conjunto utilizable.

### Calidad y aumento

- Registrar «200× declarado por el accesorio»; no inferir tamaño corporal a partir de ese número.
- Para dimensiones, fotografiar una referencia adecuada de escala bajo la misma configuración y calibrar; sin ella, no reportar mm.
- No afirmar que puntos circulares o filamentos son huevos o tela sin revisión.
- Diferenciar organismo, síntomas y evidencia indirecta.
- La foto de hoja completa ayuda a describir daño; la macro ayuda a observar organismos. Ambas tienen propósitos diferentes.
- Si se desprende una hoja, anotar hora y condición: no equivale a observarla in situ.

### Estados de identificación

1. Identificado como objetivo, con fundamento documentado.
2. Ácaro observado, especie pendiente.
3. Otro organismo.
4. No detectado con el método aplicado.
5. No evaluable.

No usar «ausencia» para una fotografía borrosa ni mezclar arañita blanca con T. urticae.

### Vínculo mínimo aunque el dashboard no tenga todos los campos

```text
session_id | observation_id | plant_id | leaf_code
fecha/hora | estrato | edad | superficie | zona
archivo(s) | tipo de captura | calidad | identificación
síntomas | método | esfuerzo de inspección | notas
```

Puede mantenerse como CSV auxiliar y posteriormente importarse o vincularse. No inventar valores para llenar campos faltantes.

---

## 13. Relacionar imágenes y mediciones

**Sí es válido anotar T y HR para cada fotografía en este WP1**, como descripción del contexto ambiental de la observación. La mejora necesaria es que cada anotación apunte a una **lectura original identificable**, con hora, ubicación y estado. No quedarse con dos números aislados en el formulario.

La propuesta es combinar **registro periódico cada 60 segundos + captura puntual solicitada alrededor de cada fotografía o grupo breve de fotografías**. También puede asociarse después la lectura periódica más próxima. Sección 22 define ambos procedimientos.

### Procedimiento

1. Normalizar zona horaria sin modificar originales.
2. Vincular observación a la instalación ambiental pertinente.
3. Asociar la lectura válida más próxima dentro de una tolerancia definida.
4. Guardar diferencia temporal y método de asociación.
5. Si no hay lectura próxima o el reloj está inválido, señalar «sin dato asociado».

Si T/HR se transcriben manualmente en el dashboard, conservar campos separados para la anotación original y la asociación comprobada. Cotejar con el CSV; no sobrescribir silenciosamente una discrepancia. Cuando varias imágenes comparten muestra, señalarlo: no son mediciones ambientales independientes.

Para muestreo de 60 segundos, una tolerancia inicial de ±60 segundos puede servir al piloto si los relojes están comprobados. Es una decisión de procesamiento, no una regla física; no usarla para ocultar incertidumbre de captura. Si la hora de fotografía es aproximada, documentar la precisión temporal.

La lectura es **ambiental de referencia**, no temperatura de hoja. Si la foto es de otro sector, conservar esa separación espacial. Resúmenes de ventanas temporales se guardan como datos derivados, con inicio, final, muestras y método.

---

## 14. Eventos y planillas listas para copiar

### Instalación

| Campo | Valor |
|---|---|
| Visita/prueba | |
| Dispositivo e instalación | |
| Placa / sensor / RTC | |
| Firmware / intervalo | |
| Ubicación / altura / soporte | |
| Protector de radiación | |
| Hora de inicio UTC y local | |
| Fuente de hora / diferencia inicial | |
| Alimentación / almacenamiento | |
| Foto del montaje | |
| Riego / poda / tratamientos conocidos | |
| Hora de retirada / diferencia final | |
| Incidencias | |

### Observación

| Campo | Valor |
|---|---|
| ID observación / visita | |
| Planta / cítrico / variedad si conocida | |
| Hoja y criterio de identificación | |
| Hora / precisión de hora | |
| Estrato / edad / superficie / zona | |
| Método / duración / superficie examinada | |
| Organismo / identificación / fundamento | |
| Conteo visible y si es contable | |
| Síntomas y estructuras | |
| Archivos de planta / hoja / macro | |
| Calidad / iluminación / accesorio | |
| Instalación ambiental de referencia | |
| ID muestra / hora de muestra / T °C / HR % | |
| Método de asociación / desfase temporal / ubicación relativa | |
| Dudas y limitaciones | |

Conteo por imagen no equivale a densidad por hoja ni por m². No sumar automáticamente macros solapadas: podrían mostrar los mismos individuos.

### Eventos

```csv
event_id,session_id,deployment_id,timestamp,event_type,description
```

Tipos: instalación, movimiento, riego, ventilación, sombreado, aplicación, poda, reinicio, sensor_error, storage_error, clock_adjustment, parada y otros.

---

## 15. Descarga, integridad y organización

Al cerrar:

1. Anotar hora final y estado.
2. Detener registro o descargar una instantánea consistente si sigue funcionando.
3. Descargar CSV, manifiesto y eventos.
4. Abrir archivos y revisar primeras/últimas filas.
5. Comparar filas y secuencias con duración y eventos.
6. Copiar originales a dos ubicaciones independientes.
7. Confirmar que imágenes del dashboard pueden recuperarse, no solo visualizarse.
8. Mantener originales de teléfono y nodo hasta verificar respaldos.

Organización sugerida, fuera de Git para originales voluminosos:

```text
VIS-001/
  README_visita.md
  originales/
    sensores/NODO-01/
    imagenes/
    observaciones.csv
    eventos.csv
  derivados/
    mediciones_revisadas.csv
    asociaciones_imagen_ambiente.csv
    resumen_calidad.md
  manifiesto_archivos.csv
```

El manifiesto puede incluir ruta, tamaño y SHA-256 calculado al respaldar. No guardar credenciales en archivos del ensayo.

### Supabase / R2

- Mantener registros estructurados en Supabase y archivos originales en R2, conforme a la plataforma definida.
- Confirmar si existe importador de CSV; si no, conservar archivos y metadatos para carga posterior.
- El firmware no necesita claves administrativas de esos servicios.
- Guardar presión en un campo explícito si el esquema lo permite; si no, preservarla en el CSV y añadir soporte después. No colocarla en la columna de HR.
- Exportar también metadatos y vínculos: las fotos sin sus registros no constituyen el paquete completo.

---

## 16. Revisión de calidad después de la visita

### Revisar

- Continuidad y frecuencia de muestras.
- Reinicios y secuencias repetidas.
- Hora inválida o ajustada.
- Errores de sensor y almacenamiento.
- Valores constantes sospechosos, saltos y exposición a sol/agua.
- Periodos iniciales y movimientos.
- Imágenes huérfanas o registros sin archivos.
- Etiquetas taxonómicas pendientes.
- Incertidumbre de hora y distancia al punto ambiental.

No eliminar un pico porque parece raro: contrastarlo con eventos, montaje y registros. Conservar original y documentar cualquier exclusión analítica.

### Productos derivados posibles

- Gráficas de T/HR por instalación.
- Mínimo, máximo y media del periodo válido, con número de muestras y duración.
- Disponibilidad: muestras válidas / oportunidades de muestreo definidas, explicando periodos excluidos.
- Tabla de observaciones con condición ambiental asociada y distancia temporal.
- Resumen de calidad del catálogo.

No extrapolar la media de tres horas a media diaria ni afirmar correlación biológica a partir de unos pocos organismos seleccionados y un sensor central.

---

## 17. Planes de contingencia

| Situación | Acción |
|---|---|
| No hay internet | Registrar localmente; fotos en galería y planilla; subir después |
| Dashboard no trabaja offline | No perder tiempo intentando cargar; usar IDs y archivos originales |
| Falla RTC | Conservar uptime/secuencia, anotar referencia manual y marcar hora inválida |
| Falla BME280 | Registrar estado de error; no usar última lectura ni cero |
| Falla almacenamiento | Avisar; usar captura USB a archivo si está disponible; no dejarlo solo |
| Batería insuficiente | Usar fuente comprobada o acortar registro; anotar interrupción |
| Sensor mojado | Marcar periodo afectado; recuperar conforme al fabricante, sin secado térmico improvisado |
| No se observa la plaga | Documentar búsqueda, esfuerzo y condiciones; aprovechar protocolo y contexto sin declarar ausencia general |
| Imagen dudosa | Marcar pendiente; solicitar revisión y conservar original |
| Nodo se mueve | Nuevo periodo de instalación y evento |

### Si se deja el nodo

Solo hacerlo si almacenamiento, energía, reloj y descarga ya funcionan de forma autónoma. Acordar responsable operativo, revisión, fecha de retiro y registro de manejo; documentar protección y montaje. Sin autonomía comprobada, llevarlo solo durante la visita atendida.

---

## 18. Lista de equipo para la visita

### Imprescindible

- [ ] ESP32 + BME280 + RTC montados y probados.
- [ ] Almacenamiento local implementado o computador con captura USB validada.
- [ ] Alimentación y cable de repuesto.
- [ ] Protector ventilado, caja y soporte.
- [ ] Dos Android con batería y espacio.
- [ ] Macro, accesorios y material para limpieza de lente.
- [ ] Etiquetas/códigos y planillas.
- [ ] Método de descarga comprobado.
- [ ] Lista de preguntas y protocolo de selección.

### Recomendado si está disponible

- [ ] Instrumento ambiental de comparación documentado.
- [ ] Computador o lector compatible con el almacenamiento elegido.
- [ ] Medidor USB de consumo.
- [ ] Regla/cinta para altura y ubicación.
- [ ] Referencia de escala apropiada para calibración de imágenes.
- [ ] Conectores y soporte de repuesto.

---

## 19. Criterios de visita satisfactoria

- [ ] Instalación y periodo ambiental identificados.
- [ ] Hora y unidades documentadas.
- [ ] Serie original recuperada, con fallas visibles.
- [ ] Fotografías vinculadas a planta/hoja/observación.
- [ ] Superficie, estrato y método registrados.
- [ ] Identificaciones y dudas diferenciadas.
- [ ] Eventos de manejo y movimientos anotados cuando se conocen.
- [ ] Archivos respaldados y comprobados.
- [ ] Resumen de cobertura, calidad y límites preparado.
- [ ] Pendientes concretos para experto, literatura o nueva observación definidos.

**No exigir que todos los datos sean perfectos:** exigir que los datos y sus limitaciones sean trazables. La primera sesión es también un piloto del sistema.

---

## 20. Orden de implementación inmediato

1. Verificar físicamente pinout WROOM-32, DS3231/AT24C32 y módulo BME280 3,3 V.
2. Probar sensor y reloj individualmente.
3. Integrar bus y niveles compatibles.
4. Implementar CSV local y descarga; LittleFS si no hay microSD y cabe la sesión.
5. Añadir estado, eventos y recuperación sin borrar archivos.
6. Construir montaje separado y ventilado.
7. Ensayar energía, reloj y continuidad.
8. Probar flujo de fotos y metadatos del dashboard.
9. Ejecutar ensayo completo antes de ir.
10. Visita con nodo fijo y captura descriptiva.
11. Descargar, respaldar y revisar calidad antes de interpretar.

### Comprobaciones pendientes para implementar

- Foto de ambas caras de módulos y pinout de la placa de 30 pines.
- Circuito de respaldo/carga del DS3231 y disponibilidad de pila apropiada.
- Flash real y partición elegida; no asumir microSD disponible.
- Alimentación y duración prevista de visita/permanencia.
- Campos de T/HR, hora y referencia de muestra disponibles en el dashboard.

---

## 21. Documentación técnica de referencia

- [Bosch Sensortec — BME280, especificaciones y datasheet](https://www.bosch-sensortec.com/products/environmental-sensors/humidity-sensors-bme280/).
- [Bosch — controlador BME280](https://github.com/boschsensortec/BME280_SensorAPI).
- [Arduino-ESP32 — I²C](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/i2c.html).
- [Arduino-ESP32 — ejemplos de archivos y almacenamiento](https://github.com/espressif/arduino-esp32/tree/master/libraries).
- [Espressif — consideraciones de sistemas de archivos](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/file-system-considerations.html).
- [Analog Devices — DS3231](https://www.analog.com/en/products/ds3231.html), RTC identificado para este montaje.

Consultar el datasheet y esquema del **módulo concreto**, además del chip. Este documento define el procedimiento propuesto; no constituye certificado de calibración ni prueba de un montaje todavía no construido.

---

## 22. Dictamen sobre tomar una fotografía y anotar T/HR

### ¿Es un buen enfoque para WP1 / objetivo 1?

**Sí, como caracterización descriptiva local.** Relacionar fotografía, observación biológica y ambiente aporta:

- Evidencia local de presencia e indicios o efectos visibles.
- Ubicación y condiciones de captura.
- Contexto ambiental contemporáneo que puede contrastarse con literatura y testimonios.
- Un conjunto trazable para la futura representación del conocimiento.

Pero una fotografía con 30 °C y 55 % HR **no demuestra** que esas condiciones causaron la presencia, que son óptimas, que el ciclo duró cierto número de días ni que el sensor midió el envés. Tampoco convierte la identificación visual en confirmación de especie. Esas afirmaciones requieren sus fuentes y métodos respectivos.

**La observación local complementa el objetivo; la descripción completa de estadios, reproducción y duraciones sigue sustentándose en literatura y entrevistas verificadas.** No hay que intentar completar todo el ciclo experimentalmente durante esta visita.

### Qué mejorar del enfoque original

| Enfoque sencillo | Problema | Versión recomendada |
|---|---|---|
| Escribir T y H en la foto | No identifica sensor, hora o posición | Añadir referencia de muestra e instalación |
| Leer al subir la foto | La subida puede ocurrir mucho después | Registrar al capturar, no al subir |
| Copiar valor visible sin comprobar edad | Puede ser una lectura anterior | Mostrar edad de lectura o solicitar nueva muestra |
| Mover el sensor para cada foto | Introduce transitorios y confunde lugares | Mantener nodo fijo o trabajar por estaciones estables |
| Muchos macros con misma T/HR | Pseudorreplicación del ambiente | Compartir muestra explícitamente, sin contar réplicas independientes |
| Fotografiar solo individuos fáciles | Sesgo de selección | Registrar selección, búsqueda, casos negativos y dudosos |
| Una macro por planta | Falta contexto de daño/ubicación | Planta/estrato, hoja completa y macro relacionadas |

### Procedimiento preferido: lectura puntual guardada + foto

La pantalla local del registrador tendrá un botón **«Registrar lectura para fotografía»**, además del registro periódico.

1. Identificar visita, planta, hoja y observación.
2. Mantener sensor en el punto documentado; no acercar mano o cara a su abertura.
3. Solicitar una nueva muestra al ESP32.
4. El ESP32 adquiere T/HR/presión, guarda en archivo y devuelve `sample_id`, hora, valores y estados.
5. Confirmar en pantalla **«Guardado en el nodo»**. Una lectura mostrada pero no guardada no se presenta como registro respaldado.
6. Tomar foto procurando una separación temporal corta; objetivo operativo inicial: dentro de 30 segundos. Si se excede, registrar hora real y obtener otra muestra cuando convenga.
7. Registrar ID muestra, hora de captura, instalación y valores en el dashboard o planilla.
8. Para un grupo breve de fotos de la misma observación, puede compartirse muestra si se conserva hora por imagen y se cumple la tolerancia acordada. Si cambia ubicación o transcurre más tiempo, tomar otra.
9. Revisar correspondencia entre nombre de archivo y registro antes de pasar a otra hoja.

El desfase objetivo de 30 segundos es **criterio operativo de esta sesión**, no garantía de correspondencia microclimática. Cambios rápidos por riego, ventilación o movimiento exigen anotación y nueva comprobación. No invalidar retrospectivamente datos sin conservarlos.

### Alternativa: foto + lectura periódica

Si no hay botón de captura implementado:

1. Fotografía con fecha/hora comprobada.
2. Anotar el valor visible, su hora y referencia si existe.
3. Vincular posteriormente al registro periódico válido más cercano, dentro de una tolerancia inicial de ±60 segundos.
4. Registrar `association_method=nearest_periodic` y el desfase.
5. Sin muestra válida, conservar foto y observación como «ambiente no asociado».

No aumentar ficticiamente la resolución temporal mediante interpolación y presentarla como medición original.

### Un nodo: dos modalidades posibles

**A. Nodo fijo de referencia — recomendada para empezar:** se instala y estabiliza en un punto. Todas las imágenes reciben referencia de ese punto, indicando si proceden del mismo sector o de otro. Ventaja: continuidad y pocas manipulaciones. Límite: no mide junto a cada hoja.

**B. Nodo por estación cercana a un grupo de plantas:** se cambia de ubicación por bloques, no por foto. Cada bloque tiene `deployment_id`, posición, altura y estabilización; dentro del bloque se toman las fotos. Puede contextualizar mejor ciertas plantas, pero las comparaciones son secuenciales y la serie tiene transitorios.

Elegir una modalidad antes de ir. Para una visita de 3–4 horas con un único nodo, priorizar A y hacer B solamente como ensayo separado si hay tiempo. La elección debe quedar en el manifiesto.

### Campos de asociación propuestos para dashboard/CSV auxiliar

```text
image_id
original_filename
observation_id
captured_at + capture_time_source
deployment_id
sample_id
sampled_at
temperature_c
relative_humidity_pct
association_method: on_demand / nearest_periodic / manual_unverified
time_difference_seconds
environment_scope: reference_point / nearby_station
sensor_status + time_status + storage_status
notes
```

Propuesta: `time_difference_seconds = hora_captura - hora_muestra`, con signo. Mantener hora y valores originales además de la asociación verificada. Si el dashboard solo tiene T/H/observaciones, usar mientras tanto:

```text
Muestra=NODO-01/BOOT-003/000145; instalación=DEP-001;
hora_muestra=...; hora_foto=...; método=on_demand;
alcance=referencia sector central; estado=guardado;
T=... °C; HR=... %.
```

No es necesario guardar identidad de la persona para este flujo. Sí se necesitan identificadores técnicos de archivo, observación y muestra.

---

## 23. Correcciones a las especificaciones comerciales aportadas

| Afirmación del proveedor | Interpretación para el proyecto |
|---|---|
| BME280 resolución T 0,01 °C / HR 0,008 % | Resolución no equivale a exactitud; mostrar centésimas no permite inferir diferencias fiables de centésimas |
| Temperatura ±1 °C / HR ±3 % | Son referencias sujetas a condiciones del datasheet, no garantía de todo el montaje ni todo el rango |
| Presión «±1 Pa» | No adoptar como exactitud absoluta. Puede existir confusión con ruido/resolución u otra especificación. Bosch distingue exactitud absoluta/relativa y ruido; revisar el datasheet y condiciones. Conservar ±1 Pa como dato comercial no verificado, no como incertidumbre del ensayo |
| I²C hasta 3,4 MHz en BME280 | El bus compartido se fija a 100 kHz; DS3231/EEPROM y cableado condicionan la configuración |
| DS3231 «error sobre 1 minuto» | Incompleto sin periodo. ±2 ppm equivale nominalmente a unos 0,173 s/día; ±3,5 ppm a 0,302 s/día. Un minuto no es el error de cada lectura |
| AT24C32 «32K» | 32 kbit = 4 KiB, no memoria suficiente para CSV extendidos |
| Wi-Fi «2.4 Hz» | Banda de 2,4 GHz |
| Bluetooth «4.1» | WROOM-32/ESP32 clásico suele documentarse Bluetooth 4.2 BR/EDR y BLE; verificar módulo real. No se necesita Bluetooth en esta primera versión |
| «1 DAC» | El ESP32 clásico dispone de dos canales DAC de 8 bits; no se usan aquí |
| Sensor de temperatura integrado ESP32 | No sustituye al sensor del aire; no utilizarlo para T ambiental |
| 12 mA máximos por GPIO según tienda | No generalizar como especificación verificada del chip ni alimentar módulos desde GPIO. Usar rieles de alimentación y LED con resistencia si se incorpora |
| USB-C y «micro USB» en el texto | Compra describe USB-C; confirmar físicamente y usar cable de datos, no solo carga |

El intervalo especificado de presión es un rango de operación, no exactitud. La presión no define riesgo de T. urticae en este protocolo; se conserva como canal auxiliar sin forzar una interpretación agronómica.

### Parámetros registrados en la metodología

Registrar modelo/chip, exactitud publicada con fuente y condiciones, resolución, método de montaje, comprobación funcional y limitaciones. No declarar calibración propia ni utilizar el dato dudoso de presión en cálculos de incertidumbre. La comparación con otra referencia debe conservar resultados, sin ajustar el sensor para que «dé el valor esperado».

---

## 24. Configuración concreta en Arduino IDE

### Preparar el entorno

1. Instalar soporte `esp32` de Espressif en el gestor de placas.
2. Seleccionar **ESP32 Dev Module** como configuración genérica inicial para la placa WROOM-32 descrita, salvo que exista una definición específica confirmada.
3. Conectar USB-C de datos y seleccionar puerto COM del CP2102. Si no aparece, comprobar cable y controlador CP210x.
4. Monitor serie: **115200 baudios**.
5. Velocidad inicial de carga: **115200**, aumentando solo tras comprobar estabilidad.
6. CPU: valor estándar de **240 MHz** para este primer ensayo; no optimizar frecuencia antes de validar registro y consumo.
7. PSRAM: **desactivada/no disponible**, salvo evidencia de que la placa real la incluye. WROOM-32 no implica WROVER con PSRAM.
8. Flash: consultar tamaño real antes de elegir la partición. La publicidad aportada no indica capacidad de flash.
9. Elegir una tabla de particiones compatible con LittleFS y espacio medido; registrar su nombre/tamaños. No seleccionar «sin filesystem» si se utiliza LittleFS.
10. Inicialización del filesystem una sola vez en banco, explícita y registrada. Firmware de campo: montaje sin formateo automático.

### Inspección y arranque sugeridos

```cpp
// Fragmentos de configuración; no constituyen un firmware completo.
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <RTClib.h>
#include <LittleFS.h>

constexpr int SDA_PIN = 21;
constexpr int SCL_PIN = 22;
constexpr uint32_t I2C_HZ = 100000;
constexpr uint32_t PERIOD_MS = 60000;

Adafruit_BME280 bme;
RTC_DS3231 rtc;

void setup() {
  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);
  Wire.setClock(I2C_HZ);

  Serial.printf("Flash detectada: %u bytes\n", ESP.getFlashChipSize());
  bool fsOk = LittleFS.begin(false);  // Nunca formatear automáticamente.
  if (fsOk) {
    Serial.printf("FS total/usado: %u / %u bytes\n",
      (unsigned)LittleFS.totalBytes(), (unsigned)LittleFS.usedBytes());
  }

  bool sensorOk = bme.begin(0x76, &Wire);
  if (!sensorOk) sensorOk = bme.begin(0x77, &Wire);
  if (sensorOk) {
    bme.setSampling(
      Adafruit_BME280::MODE_FORCED,
      Adafruit_BME280::SAMPLING_X1, // temperatura
      Adafruit_BME280::SAMPLING_X1, // presión
      Adafruit_BME280::SAMPLING_X1, // humedad
      Adafruit_BME280::FILTER_OFF);
  }

  bool rtcOk = rtc.begin(&Wire);
  bool clockValid = rtcOk && !rtc.lostPower();
  // Validar además fecha plausible y sincronización real.
  // Mostrar estados; un fallo debe registrarse, no ocultarse.
}
```

Comprobar APIs contra la versión instalada; incluir las variables de estado en el firmware real. Si el RTC perdió la hora, **no establecerla silenciosamente** en el `setup()`. Configurar explícitamente mediante herramienta de banco o comando que reciba UTC y deje un evento. RTClib devuelve fecha sin zona horaria; la convención UTC la fija el proyecto.

### Lectura forzada sugerida

```cpp
// Invocar solo si sensorOk. Guardar estados y hora alrededor de adquisición.
bool measured = bme.takeForcedMeasurement();
if (measured) {
  float t = bme.readTemperature();
  float rh = bme.readHumidity();
  float p = bme.readPressure(); // Pa en esta biblioteca.
  // Validar isfinite(t/rh/p), rangos y estados antes de asociar a foto.
  // Guardar CSV, cerrar/sincronizar y comprobar escritura.
}
```

No confundir «la función retornó valores» con «el archivo se guardó». Registrar `storage_status` en respuesta de captura/estado, y eventos de falla. Comparar número de bytes escritos con lo esperado y revisar archivos descargados.

### Contrato CSV actualizado para capturas puntuales

Actualizar de forma coordinada productor e importador a `schema_version=2`:

```csv
schema_version,device_id,session_id,deployment_id,boot_id,sequence,sample_id,timestamp_utc,uptime_ms,time_status,temperature_c,relative_humidity_pct,pressure_pa,sensor_status,trigger_type,observation_ref,request_id
```

- `sample_id`: por ejemplo `NODO-01/BOOT-003/000145`.
- `trigger_type`: `periodic` o `photo_request`.
- `observation_ref`: opcional, código de observación; no es requisito para almacenar una lectura.
- `request_id`: ID del pedido puntual, utilizado para evitar dobles muestras por reintento.
- Una lectura periódica cercana y una puntual pueden coexistir; son adquisiciones diferentes. No mezclarlas al calcular promedios periódicos sin explicar el método.
- `storage_status` se informa en pantalla/API y en incidencias: una fila que no se pudo escribir no puede certificar su propia escritura.

Mantener posibilidad de leer los CSV versión 1 de la sección 7. No cambiar columnas a mitad de un archivo ni agregar filas versión 2 bajo una cabecera versión 1.

---

## 25. Interfaz local sin añadir pantalla al equipo

Con lo disponible, la opción práctica es una **página local servida por el ESP32 mediante su punto de acceso Wi-Fi**, accesible desde el navegador Android.

### Configuración propuesta

```text
Wi-Fi del nodo: TESIS-NODO-01
Dirección local: la que reporte WiFi.softAPIP(); normalmente 192.168.4.1
Máximo previsto: dos Android
Internet: no requerido para lecturas o descarga local
Contraseña: configurada en banco, no publicar en esta guía
```

El acceso local al equipo no es registro de usuarios ni identifica quién hizo una foto. Android puede advertir que la red no tiene internet; comprobar que permanece conectado y permite abrir la dirección local. No depender de portales cautivos o cambio automático de redes.

### Pantalla

- Hora RTC en UTC y hora Colombia calculada para visualizar.
- T °C, HR %, presión opcional.
- ID y edad de última muestra.
- Estado: sensor, RTC, archivo y espacio.
- Botón «Registrar lectura para fotografía».
- Campo opcional de observación.
- Lista de archivos y descarga.
- Parada segura del registro; evitar borrado o formateo en uso normal.

**GET de estado muestra última lectura; no debe crear mediciones.** El botón ejecuta una solicitud explícita de adquisición y guardado. Implementar una cola única para todas las adquisiciones: dos teléfonos no deben operar simultáneamente el bus o las escrituras sin coordinación.

### Rutas del diseño inicial

| Ruta | Operación |
|---|---|
| `GET /` | Interfaz local |
| `GET /status` | Estados, última muestra, espacio |
| `POST /samples` | Nueva muestra puntual con `request_id` |
| `GET /requests/{id}` | Recuperar resultado de solicitud en caso de reintento |
| `GET /files` | Archivos disponibles |
| `GET /files/{id}` | Descarga controlada de archivo o instantánea |

Validar rutas contra lista de archivos permitidos; no exponer cualquier ruta arbitraria del filesystem. Limitar tamaño de petición y caracteres de identificadores para evitar romper CSV. La respuesta puntual devuelve `sample_id`, hora, T/HR, estados y si fue persistida. Si la red se interrumpe después de guardar, el reintento con el mismo `request_id` recupera el resultado o indica que hace falta reconciliar; no crea duplicados silenciosos.

### Dashboard HTTPS y ESP32 local HTTP

No asumir que el dashboard alojado en internet puede consultar directamente `http://192.168.4.1`: restricciones de navegador, contenido mixto y permisos de red local pueden impedirlo. Para el piloto:

1. Un teléfono fotografía; el otro mantiene la página local y anota la muestra.
2. O usar dos pestañas separadas: página local y dashboard, conservando galería/planilla si no hay internet.
3. Descargar CSV del nodo y luego cambiar a red con internet para cargar en plataforma.

La automatización dashboard–nodo es una mejora posterior que requiere pruebas específicas. Primero garantizar registro local y vínculo manual trazable.

La implementación de la sección 27 usa un contrato más pequeño: `POST /samples` conserva la última respuesta y detecta solicitudes ya guardadas en el CSV del arranque; no implementa `GET /requests/{id}`. La descarga se realiza con `GET /download?file=...`, después de pausar el registro periódico. No depender de las rutas sugeridas aquí si se utiliza ese sketch.

### Efecto térmico de Wi-Fi

La actividad de radio puede aumentar el calor de la placa. Mantener el sensor separado y ensayar el montaje **con el AP activo**, porque será su condición real de trabajo. No encender/apagar radio de forma cambiante sin documentarlo si afecta la instalación. Las mediciones siguen guardándose aunque nadie esté conectado.

---

## 26. Configuración final y materiales adicionales mínimos

| Elemento | Decisión para esta visita |
|---|---|
| CPU | ESP32-WROOM-32 disponible |
| Comunicación de sensores | I²C a 100 kHz, GPIO21/22 |
| Alimentación de módulos | Riel 3,3 V, GND común |
| Alimentación principal | USB-C de la placa mediante fuente/power bank probado |
| Sensor | BME280, dirección comprobada 0x76/0x77 |
| Reloj | DS3231, UTC, batería/módulo compatibles |
| EEPROM | AT24C32 identificada; no usada como logger principal |
| Registro | LittleFS en flash si partición y ensayo lo permiten |
| Muestreo | Cada 60 s + capturas puntuales identificadas |
| Visualización | Página local AP Wi-Fi + USB de diagnóstico |
| Imágenes | Cámara Android/galería con originales; dashboard para metadatos |
| Descarga | CSV/manifiesto/eventos al Android o computador, comprobados |
| Instalación | Nodo fijo en punto definido y BME separado de electrónica |

### Qué conseguir o preparar

- Cable USB-C **de datos** y uno de repuesto.
- Fuente/power bank comprobado para toda la duración; no inferir autonomía de los mAh sin ensayo.
- Pila de respaldo apropiada después de inspeccionar módulo RTC.
- Cables y conectores cortos, soporte y protección ventilada.
- Montaje firme; si se deja el nodo, no usar conexiones sueltas.
- Planilla local/papel y etiquetas.
- microSD es opcional para la primera visita si LittleFS ya registra y descarga. Para varios días, evaluar capacidad y desgaste antes de decidir.

No alimentar el ESP32 simultáneamente desde varias entradas sin comprobar el circuito de la placa. Para este ensayo elegir **USB-C como entrada única**. No aplicar 5 V al pin 3V3 ni alimentar el nodo por GPIO. Comprobar estabilidad al escribir y transmitir.

### EEPROM: por qué no basta

Una fila de 250 bytes permitiría del orden de 16 filas en 4 KiB antes de considerar formato/metadatos: unos minutos a 60 s. Un formato binario compacto tendría otra capacidad, pero exige diseño, gestión de páginas/endurance y recuperación. No dedicar tiempo a ello para esta visita: conservar EEPROM para configuración futura o dejarla sin utilizar.

### Ensayo de fotos y medidas antes de salir

Simular diez fotografías con los dos Android:

1. Registrar códigos de observación.
2. Solicitar muestra y fotografiar dentro del objetivo temporal.
3. Anotar T/HR y referencia.
4. Desconectar internet y repetir con galería/planilla.
5. Interrumpir una solicitud y comprobar reintento.
6. Descargar CSV y cotejar las diez asociaciones.
7. Comprobar que archivos originales, hora y muestra coinciden.

Criterio de terminado: las diez fotos tienen asociación comprobable o una ausencia/limitación explícita; no hay lecturas inventadas, muestras duplicadas por reintento ni valores transcritos sin referencia. Este ensayo prueba el flujo, no la identificación de la especie ni la calibración.

### Entregables de WP1 después de esta visita

1. Registro técnico del montaje y método.
2. Serie ambiental original con unidades, hora y eventos.
3. Catálogo de planta/hoja/macro vinculado a observaciones.
4. Tabla de asociaciones foto–muestra con alcance espacial y desfase.
5. Identificaciones revisadas y casos dudosos diferenciados.
6. Síntesis descriptiva contrastada con entrevistas y literatura.
7. Limitaciones y vacíos pendientes para cierre del objetivo.

**Conclusión operativa:** registrar T/HR por foto es apropiado si representa contexto medido y trazable. La configuración más útil con este equipo es conservar el registro periódico, añadir una adquisición puntual guardada y evitar mover el BME280 con cada captura. Eso produce mejores datos sin requerir nuevos sensores ni comunicación cloud durante la visita.

---

## 27. Paso a paso final — firmware disponible y flujo manual de dos teléfonos

### 27.1. Qué se entrega y qué está comprobado

Archivo: [`scripts/registrador_invernadero/registrador_invernadero.ino`](scripts/registrador_invernadero/registrador_invernadero.ino).

Integra las bibliotecas que ya funcionaron en los ensayos individuales:

- `Wire` en GPIO21/22.
- `Adafruit_BME280`, con búsqueda en 0x76 y 0x77.
- `RTC_DS3231` de RTClib.
- AP Wi-Fi y HTTP local.
- LittleFS y descarga CSV.
- Preferencias pequeñas para conservar códigos de visita e instalación.

**Compilación comprobada:** Arduino-ESP32 3.3.12, Adafruit BME280 2.3.0, Unified Sensor 1.1.15, BusIO 1.17.4 y RTClib 2.1.4, placa `ESP32 Dev Module`. La compilación inicial validada ocupó aproximadamente 1,03 MB de programa y 49 kB de variables globales; no son mediciones del consumo dinámico máximo ni de autonomía.

**Todavía exige prueba física:** sensores integrados, AP en sus Android, RTC, escritura/recuperación de LittleFS, consumo y descarga. Compilar no significa que el montaje ya haya sido validado en el vivero. No se ha cargado el programa al dispositivo desde esta entrega.

### 27.2. Dictamen sobre el flujo que propusieron

**Es adecuado y lo adoptamos para esta primera visita.**

| Dispositivo | Función |
|---|---|
| Android A | Fotografiar; introducir observación y T/HR en dashboard cuando funcione, o en planilla offline |
| Android B | Conectarse a la red del ESP32; solicitar lectura, dictar y comprobar muestra/hora |
| ESP32 | Medir, registrar localmente y servir su página; no necesita Internet |

No automatizamos comunicación entre dashboard y ESP32. La página local de B muestra una lectura manual fija hasta que se solicite otra; el periódico continúa en segundo plano.

**Condición clave:** el Wi-Fi del ESP32 no brinda Internet. Tener esa red no garantiza que se puedan subir fotos a Supabase/R2. Si el dashboard requiere conexión y no hay señal, A toma fotos con la cámara y conserva metadatos en papel o una herramienta ya probada offline. La carga se realiza después; T/HR y hora corresponden a la captura, no al momento de subir.

No asumir persistencia offline del dashboard solo porque permanece abierto. Ensayar específicamente guardar y reabrir en modo avión. Si falla, usar la planilla auxiliar desde el principio.

### 27.3. Cablear ambos sensores juntos

Desconectar alimentación durante cableado:

```text
ESP32 3V3  ─── BME280 VCC 3,3 V
           └── DS3231 VCC 3,3 V
ESP32 GND  ─── BME280 GND
           └── DS3231 GND
ESP32 21   ─── BME280 SDA / SDI
           └── DS3231 SDA
ESP32 22   ─── BME280 SCL / SCK
           └── DS3231 SCL
```

Mantener la configuración CS/SDO que permitió el ensayo del BME280 y verificar pull-ups a 3,3 V. No se utiliza SQW, 32K ni la AT24C32. El puerto USB-C alimenta la placa. Ver secciones 3–4 para batería y montaje.

### 27.4. Abrir y cargar en Arduino IDE

1. Abrir el `.ino` desde su carpeta `registrador_invernadero`. Carpeta y sketch tienen el mismo nombre.
2. Seleccionar **ESP32 Dev Module** y el puerto COM que ya funcionó.
3. Mantener flash y ajustes de carga compatibles con la placa real. Usar esquema con espacio de filesystem; el habitual de 4 MB puede servir **solo si la flash detectada lo confirma**.
4. Instalar/verificar bibliotecas indicadas en 27.1.
5. Cambiar `AP_PASSWORD` al inicio por una contraseña local de al menos ocho caracteres y conservarla para el ensayo. No son credenciales de Supabase/R2. SSID predeterminado: `TESIS-NODO-01`.
6. Verificar/compilar y cargar. Si se requiere BOOT para carga, aplicar el procedimiento de la placa que ya usaron.
7. Abrir monitor serie a **115200**, terminación **Nueva línea** o **Ambos NL y CR**.
8. Leer arranque: modelo lógico, flash, estados BME/RTC/FS e IP del AP.

Los comandos se procesan al recibir nueva línea. El monitor serie puede reiniciar la placa al abrirse: comprobar `boot_id` y volver a verificar la hora cuando suceda.

### 27.5. Preparar LittleFS una sola vez en banco

Si aparece `filesystem_not_mounted`, revisar primero partición y flash. Para una partición nueva/vacía, ejecutar por serial:

```text
FORMAT CONFIRMAR
```

**Este comando elimina todos los archivos del nodo. Solo usarlo para inicialización en banco, después de respaldar cualquier contenido. No se ofrece desde HTTP.** Después reiniciar, verificar FS, ajustar hora y revisar archivos.

El firmware usa `LittleFS.begin(false)`: no destruye los datos automáticamente si hay un problema. La reserva inicial es 32 KiB; cuando no alcanza, las muestras se muestran con `saved=false` y se registra el fallo por serial. No sobrescribe archivos anteriores por falta de espacio.

La muestra y evento iniciales pueden tener hora inválida; se conservan como tales. No son datos biológicos utilizables con hora verificada. No reprogramar ni cambiar particiones después de una visita sin descargar.

### 27.6. Conectar Android B sin internet

1. Encender el nodo.
2. En Wi-Fi de Android, elegir `TESIS-NODO-01` y escribir la contraseña configurada.
3. Si Android avisa «sin Internet», elegir mantener la conexión. Durante el ensayo comprobar que no cambie automáticamente a otra Wi-Fi; los ajustes varían por teléfono.
4. Abrir el navegador e introducir **`http://192.168.4.1`**, salvo que serial reporte otra IP.
5. No usar `https://` para esta página local ni intentar abrirla desde el dashboard cloud.
6. Mantener una pestaña para el nodo y conservar la página activa durante las capturas.

El AP permite dos clientes. Eso no obliga a conectar Android A; preferimos dejar A disponible para cámara/dashboard/datos móviles. La página hace peticiones normales locales, sin servicio cloud.

### 27.7. Corregir y verificar el reloj

Tu ensayo anterior contiene:

```cpp
rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
```

**Eso establece la hora de compilación, no la hora actual de cada arranque.** Un reinicio posterior puede retroceder el reloj y romper asociaciones. Además, sin batería no se garantiza persistencia tras quitar la energía; no es correcto asumir que todas las desconexiones tienen el mismo comportamiento.

Este sketch **no ajusta automáticamente a la hora de compilación**. Exige verificar explícitamente el RTC en cada arranque, incluso si tiene pila:

1. Antes de salir, asegurar que la hora del teléfono B esté correctamente sincronizada.
2. Abrir la página local y pulsar **«Verificar/ajustar RTC con este teléfono»**.
3. Confirmar que fecha/hora presentada por el teléfono es correcta.
4. El navegador envía epoch UTC al ESP32; se guarda en DS3231 y se anota un evento.
5. Estado debe mostrar UTC verificada y fecha plausible.
6. Comparar una captura con hora Colombia visible. El programa transforma la visualización; no resta cinco horas al valor almacenado.

No se necesita Internet para transferir la hora del teléfono al nodo, pero sí que el teléfono tenga una hora correcta. Si el dispositivo está mal ajustado, no es una referencia válida.

Sin teléfono puede usarse:

```text
TIME <epoch_UTC_de_10_digitos>
```

En PowerShell de un computador con reloj comprobado, obtener el epoch actual con:

```powershell
[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
```

Copiarlo pronto al comando TIME. El tiempo entre obtención y envío añade desfase; registrar esa limitación. No introducir una fecha de ejemplo como si fuera actual.

**Reinicio del nodo → nueva verificación de hora.** Hasta entonces los CSV tienen `time_status=invalid` aunque el RTC muestre algo. El nodo sigue midiendo y guardando uptime/secuencia; no inventa fecha.

### 27.8. Establecer visita e instalación

En página local:

- Visita/prueba: `VIS-001` o código de su visita real.
- Instalación: `DEP-001` o código acordado.
- Pulsar **Guardar contexto**.

Usar letras, números, guion y guion bajo, máximo 48 caracteres. Los códigos se conservan en NVS, y aparecen en cada fila; revisar al iniciar otra visita. Cambiar instalación si se mueve sensor. El manifiesto indica contexto del arranque; los cambios posteriores quedan en eventos y filas.

Si hay reloj o sensor fallidos, no usar los valores para completar campos como si todo estuviera bien. La pantalla debe confirmar: sensor detectado, hora verificada, FS montado, espacio y escritura correcta.

### 27.9. Solicitar muestra y tomar fotografías

**Ensayar este procedimiento completo en casa y luego repetirlo en campo.**

1. A identifica planta/hoja y crea el código `OBS-001` en dashboard o planilla.
2. B escribe ese código en **Observación** de la página local.
3. B pulsa **«Registrar muestra»** una vez. La función adquiere y guarda una lectura nueva, distinta del último registro periódico.
4. B comprueba tres condiciones: `Sensor: ok`, hora válida y **`Guardado: SÍ`**.
5. B dicta T/HR, muestra y hora. A anota esos datos y captura foto dentro del objetivo operativo de 30 segundos.
6. Para planta/hoja/macro del mismo grupo breve, anotar qué imágenes comparten muestra. Si la secuencia tarda más o cambian condiciones, solicitar nueva muestra.
7. A revisa enfoque y vincula nombre de archivo, hora e identificación antes de cambiar de hoja.
8. B conserva el resultado fijo visible hasta la siguiente solicitud; el periódico no cambia esa tarjeta. El estado superior sí se actualiza.

El dato mostrado a dos decimales es comodidad de lectura, no exactitud de centésimas. CSV conserva tres decimales en T/HR; eso tampoco amplía la exactitud física.

Si ambos solicitan muestras, se procesan secuencialmente por el servidor; cada una tiene su ID. Preferimos que B sea quien pulse para evitar confusión.

#### Si una solicitud queda pendiente

- Repetir el botón conserva el mismo `request_id` en esa pestaña.
- Si es la última solicitud atendida, el nodo devuelve la misma muestra sin duplicarla.
- Si otra solicitud fue atendida entre medias, el firmware revisa el CSV del arranque. Si encuentra la solicitud, indica que ya está registrada y requiere recuperar del CSV; no crea otra.
- El control de reintentos se limita al arranque actual; tras reinicio se debe anotar la incidencia y reconciliar archivos anteriores antes de repetir.
- «Abandonar intento» borra la marca pendiente de la pestaña, **no elimina el registro del nodo**.
- Si aparece muestra NO guardada, conservar lo que ocurrió como incidencia. Recuperar almacenamiento y solicitar una nueva lectura identificada; no fingir que la anterior quedó respaldada.

### 27.10. Planilla mínima para la transcripción manual

```csv
session_id,observation_id,image_filename,plant_id,leaf_code,stratum,surface,captured_at,sample_id,sampled_at,temperature_c,relative_humidity_pct,deployment_id,association_method,notes
```

El ID largo de muestra puede anotarse mediante **boot + secuencia**, manteniendo `device_id` en la cabecera de la planilla. No dejar solo «T=27; H=60» sin referencia.

**Antes de cerrar una observación, leer de vuelta los valores** para detectar errores de transcripción. Opcional: foto de la pantalla de B como apoyo, separada de las imágenes biológicas; no sustituye el CSV.

Al cargar posteriormente al dashboard:

- Usar fecha/hora de captura, no fecha/hora de carga.
- Mantener originales de galería.
- Completar T/HR desde anotación y verificar contra CSV.
- Registrar ubicación de referencia del BME280. Si es central, no escribir «temperatura del envés».
- Corregir discrepancias con nota, preservando anotación original.

### 27.11. Operación solo por serial

Si hay computador o terminal serie compatible comprobado:

```text
STATUS
TIME <epoch_UTC>
CONTEXT VIS-001 DEP-001
CAPTURE OBS-001
PAUSE
FILES
DUMP measurements_B...csv
RESUME
```

| Comando | Resultado |
|---|---|
| `STATUS` | Estado completo en JSON |
| `TIME ...` | Ajuste explícito a UTC |
| `CONTEXT ... ...` | Guardar visita/instalación |
| `CAPTURE` / `CAPTURE OBS-001` | Nueva muestra puntual, serial y CSV |
| `PAUSE` | Pausar periódico y registrar evento |
| `RESUME` | Reanudar, sin fabricar filas del tiempo pausado |
| `FILES` | Nombres y tamaños de archivos |
| `DUMP <nombre>` | Mostrar archivo entre marcadores, solo con periódico pausado |
| `FORMAT CONFIRMAR` | Borrar filesystem explícitamente; únicamente banco/respaldado |

Serial muestra `CSV ...`, luego `SAMPLE {...}` con estado de guardado. Monitor serie no guarda automáticamente una copia en el computador. Para respaldo desde DUMP, conservar exactamente contenido entre `---BEGIN FILE---` y `---END FILE---`, sin prefijos, mensajes ni cabeceras ajenas.

USB Android necesita OTG, compatibilidad CP2102, alimentación y app terminal; no está comprobado por esta entrega. **HTTP local es la ruta principal para los teléfonos**. USB del computador sirve de diagnóstico/contingencia.

### 27.12. Descargar antes de desconectar

1. A finaliza las fotografías y anota última observación.
2. B pulsa **Pausar periódico para descargar**.
3. No solicitar nuevas capturas durante descarga. Anotar hora de pausa.
4. Pulsar **Listar CSV y manifiestos**.
5. Descargar `measurements_<boot>.csv`, `events_<boot>.csv` y `manifest_<boot>.json` de **todos los arranques de la visita**.
6. Android los guarda habitualmente en Descargas; comprobar archivos, tamaño y contenido, no solo el mensaje del navegador.
7. Hacer copia adicional en computador/nube cuando haya acceso. Mantener flash hasta comprobar respaldo.
8. Si el nodo se queda, pulsar **Iniciar periódico** antes de irse y verificar nuevas filas.
9. Si se retira, anotar hora y después desconectar alimentación.

Nombres por arranque evitan reemplazar series anteriores. La pausa deja hueco explícito; no se rellenan muestras del tiempo detenido. Al trabajar por varias jornadas, este primer firmware no rota por día: un archivo continúa por arranque. Controlar tamaño y capacidad antes de dejarlo más tiempo.

### 27.13. Verificación física obligatoria del sketch

- [ ] Compila y carga con la placa real.
- [ ] BME280 y DS3231 funcionan simultáneamente.
- [ ] LittleFS montado, con capacidad y espacio observados.
- [ ] La página local abre en ambos Android sin Internet.
- [ ] La hora queda UTC y Colombia se visualiza correctamente.
- [ ] Tras reinicio, hora aparece no verificada hasta nuevo ajuste.
- [ ] Captura manual devuelve valores válidos y `Guardado: SÍ`.
- [ ] Tarjeta de captura no cambia cuando se guarda una periódica.
- [ ] CSV contiene muestra, observación, hora y unidades correctas.
- [ ] Reintento de una solicitud no crea doble fila durante el mismo arranque.
- [ ] Descargar pausado funciona; descarga activa pide pausa.
- [ ] Sensor ausente genera error, no valores antiguos o cero.
- [ ] Reinicio conserva archivos anteriores.
- [ ] Power bank no corta la energía durante el ensayo.
- [ ] Diez fotos de ensayo se pueden vincular con sus muestras.
- [ ] Sin internet, los datos de A siguen recuperables en galería/planilla.

### 27.14. Limitaciones de esta primera implementación

- Hora depende de verificación manual por arranque: adecuada para visita atendida; una instalación desatendida con recuperación automática exige validar pila, convención de hora y política de reinicio en otra versión.
- Última respuesta manual se conserva en RAM; idempotencia se apoya también en CSV del arranque. No promete recuperación automática de respuestas entre arranques.
- LittleFS necesita partición adecuada y tiene capacidad/endurance finitas. Descargar y controlar espacio; no dejar semanas sin cálculo.
- Descargas y búsquedas de solicitudes son síncronas: pueden retrasar el muestreo. Hacer descargas pausadas; retrasos de varios intervalos quedan señalados.
- `flush`/cierre y conteo de bytes mejoran observabilidad, no garantizan integridad ante todo corte de energía. Revisar originales.
- No transmite automáticamente al dashboard, no detecta ácaros y no activa riego.
- No utiliza temperatura del DS3231 ni estima altitud con una presión de referencia arbitraria. Lo registrado es T/HR del BME280 y presión local en Pa.

**Resultado final esperado:** observaciones y fotografías con ambiente asociado manualmente, serie original independiente de internet y respaldo verificable. Ese alcance aporta evidencia útil a WP1 sin añadir integración cloud–sensor a la app durante esta visita.

---

## 28. Depuración del primer montaje integrado — versión 1.0.1

### 28.1. Qué indica el resultado de carga y serial aportado

La compilación y carga reportadas por el equipo terminaron correctamente, incluyendo verificación de hashes y reinicio. La página local abrió en Android: ESP32, programa, AP y servidor funcionan al menos para ese flujo. Esto no acredita todavía adquisición ni almacenamiento.

| Mensaje observado | Interpretación | Próximo paso |
|---|---|---|
| `sensor_status: sensor_not_found` | La inicialización de Adafruit BME280 falló en 0x76 y 0x77. Puede ser bus, conexión, identidad o respuesta del sensor | Escanear I²C y leer identificación antes de decidir |
| `temperature_c: null`, HR/presión `null` | No hubo lectura válida; no son ceros ambientales | No transcribir como datos medidos |
| `filesystem_not_mounted` y `saved: false` | No se montó LittleFS y esas muestras no se guardaron en archivo | Comprobar partición, luego inicializar si procede |
| `time_valid: false` y timestamp vacío | Falta verificación explícita de hora del arranque o se invalidó el reloj | Verificar RTC desde el teléfono una vez detectado |

La línea `CSV ...` impresa por serial **no significa que exista ese archivo**: el campo `saved` informa el resultado de escritura. No comenzar el ensayo biológico mientras adquisición, hora y almacenamiento no estén comprobados.

### 28.2. Cargar la versión de diagnóstico

El sketch incorpora diagnóstico de solo lectura y reintento sin borrado:

- Serial: `DIAG` o `SCAN`.
- Página local: **«Escanear I²C y revisar almacenamiento»**.
- Serial: `RETRY`, o botón **«Reintentar sensores y montaje sin borrar»**.
- HTTP: `GET /diagnostics` y `POST /retry`.

1. Si hubo archivos útiles anteriores, descargarlos antes de reprogramar. En el arranque reportado las filas indican `saved=false`, pero eso no demuestra que no haya archivos de ensayos previos.
2. Cargar el `.ino` actualizado, sin cambiar partición ni activar borrado total de flash.
3. Abrir monitor a 115200 con nueva línea.
4. Ejecutar `PAUSE` para evitar que mensajes periódicos dificulten leer.
5. Ejecutar `DIAG` y conservar la respuesta completa.

El diagnóstico puede tardar si el bus tiene problemas; realizarlo fuera de capturas. No formatea, cambia particiones ni ajusta hora. `RETRY` sí reinicializa módulos y exige volver a verificar hora, pero no borra archivos.

### 28.3. Interpretar diagnóstico I²C

Ejemplo **esperado, no resultado medido**:

```json
{
  "i2c_devices": ["0x57", "0x68", "0x76"],
  "chip_id_0x76": "0x60",
  "chip_id_0x77": null,
  "expected_bme280_id": "0x60",
  "rtc_initialized": true,
  "sensor_initialized": true
}
```

| Resultado | Qué revisar |
|---|---|
| 0x68 y 0x57 aparecen; 0x76/0x77 no | Bus llega al RTC, pero BME no responde: revisar rama del BME, alimentación, SDA/SCL y configuración CS/SDO |
| 0x76 aparece con ID 0x60 | Responde un BME280 compatible; si inicialización sigue falsa, reintentar y revisar comunicación/alimentación/calibración del sensor |
| 0x76 o 0x77 con ID 0x58, 0x56 o 0x57 | Identificación compatible con variantes BMP280; no habilitar HR ni forzar la biblioteca para fingir BME. Contrastar módulo y ensayo previo |
| Dirección aparece, pero ID `null` | Hubo respuesta al escaneo, pero falló lectura del registro; revisar integridad del bus/alimentación |
| No aparece ningún dispositivo | Revisar tierra común, 3V3, pines 21/22, SDA/SCL, pull-ups y posible línea retenida |
| Aparecen muchas direcciones inesperadas | Posible bus en estado incorrecto; no interpretar como decenas de sensores reales |
| Solo falta 0x57 | No afecta directamente al logger: EEPROM no utilizada. Confirmar que RTC 0x68 funciona |

Una dirección por sí sola no identifica inequívocamente un dispositivo. El registro 0xD0 se lee únicamente en 0x76/0x77 como diagnóstico del sensor; el registro del RTC tampoco constituye una prueba completa de integridad del reloj.

#### Secuencia física para aislar el BME280

1. **Desconectar USB/alimentación antes de tocar cables.**
2. Dejar solo BME280: 3V3, GND, SDA→21 y SCL→22, reproduciendo el montaje que funcionó individualmente.
3. Encender y ejecutar `DIAG`.
4. Apagar, añadir RTC en paralelo y repetir.
5. Comparar qué cambia. Si desaparece BME al agregar RTC, revisar rama, alimentación y pull-ups del montaje combinado; ambos dispositivos pueden compartir el bus correctamente.
6. Medir VCC–GND del BME si cuentan con multímetro y revisar cada contacto. No asumir continuidad por apariencia de protoboard.
7. Usar cables cortos y firmes. No alimentar el RTC a 5 V para «probar» mientras siga compartiendo señales de 3,3 V sin verificar el módulo.

El ensayo individual previo que funcionó es una evidencia útil: copiar exactamente esa rama ayuda a localizar el cambio de montaje. No concluir que el sensor es otro modelo solo por el fallo de inicialización.

### 28.4. Resolver LittleFS por separado

El diagnóstico informa `flash_bytes`, `filesystem_partition` y estado de montaje.

- La partición buscada es la habitual de Arduino-ESP32: tipo data, subtipo SPIFFS, etiqueta `spiffs`. **Ese nombre de partición también puede alojar LittleFS**; no implica que el sketch esté usando la biblioteca SPIFFS.
- Si `filesystem_partition` muestra dirección y tamaño, existe la partición esperada, pero el montaje puede fallar por estar vacía, tener otro formato, corrupción u otro problema.
- Si es `null`, revisar la tabla de particiones seleccionada. No formatear a ciegas ni cambiarla sin respaldar datos existentes. Un diseño personalizado con otra etiqueta requiere adaptar el código.
- El «78 %» del compilador corresponde a la partición del programa; **no significa que LittleFS esté 78 % lleno**.

Si existe la partición, es la primera inicialización y no hay archivos que conservar, ejecutar por serial:

```text
FORMAT CONFIRMAR
```

El comando elimina todo el filesystem. Después reiniciar, ejecutar `DIAG`/`STATUS` y comprobar montaje y espacio. No repetir el formato en cada encendido. Si no monta después de un formato explícito, conservar el error y revisar partición/flash; no intentar borrar repetidamente como solución general.

### 28.5. Recuperar hora y producir la primera fila buena

Cuando BME y RTC estén detectados y FS montado:

1. Conectar Android B al AP y abrir página local.
2. Pulsar verificar/ajustar RTC, confirmando hora correcta del teléfono.
3. Guardar contexto de ensayo: por ejemplo `PRUEBA-BANCO` y `DEP-BANCO`.
4. Registrar muestra puntual `OBS-PRUEBA-001`.
5. Comprobar:

```text
sensor_status = ok
time_valid = true
timestamp_utc = fecha/hora correcta
saved = true
T/HR/presión = valores presentes y plausibles
```

6. Pausar periódico, listar archivos, descargar CSV y abrirlo.
7. Comprobar que contiene exactamente esa muestra, código y valores.
8. Reanudar periódico y comprobar aumento de `saved_samples` después del intervalo.

Solo entonces pasar al ensayo de diez fotos, estabilización y autonomía de la sección 27. Un dato plausible mostrado por HTTP no reemplaza la comprobación del archivo recuperado.

### 28.6. Información necesaria si el problema continúa

Compartir, sin necesidad de toda la salida de carga:

- JSON completo de `DIAG`.
- JSON de `STATUS`.
- Estado con BME solo y con ambos módulos, si difieren.
- Fotografía nítida de conexiones y etiquetas.
- Esquema de particiones elegido en Arduino IDE.
- Mensaje completo de LittleFS y formato, si se ejecutó con respaldo.

No enviar valores T/HR de las muestras fallidas como resultados de visita. Se conservan como evidencia de depuración técnica.
