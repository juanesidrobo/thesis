# Invernadero

Ilustración técnica 3D para la tesis, no un plano constructivo ni un diseño
eléctrico validado. Modelo y seis renders generados y verificados con Blender.
Esta carpeta contiene únicamente la versión actual.

## Distribución e instrumentación

Invernadero de **6 x 14.4 m ilustrativos**, con tres surcos longitudinales de
diez plantas cada uno: **30 macetas**. Los identificadores van de `S1-P01` a
`S3-P10`; en cada surco, P01 está junto a la entrada y P10 al fondo.
La tierra es café casi negro, con textura.

| Ubicación | Variables | Sensores |
|---|---|---|
| Soportes ambientales independientes | Humedad relativa (HR) ambiente y temperatura ambiente | 2 |
| Parche de suelo al centro | Humedad del suelo general | 1 |
| S1-P01 | Temperatura de hoja y humedad del sustrato de la maceta | 2 |
| S2-P05 | Temperatura de hoja y humedad del sustrato de la maceta | 2 |
| S3-P10 | Temperatura de hoja y humedad del sustrato de la maceta | 2 |

**Total: nueve sensores**, seis de ellos locales, exclusivamente en las tres
plantas indicadas. Las otras 27 plantas no llevan instrumentación.
La humedad del suelo o sustrato **no es HR del aire**; no se usa el término
«HR suelo» para estas sondas.

Una caja Raspberry Pi ocupa una posición lateral a media longitud del
invernadero. Los **nueve cables continuos** llegan a entradas individuales.
La placa Raspberry Pi y el bloque de interfaces son esquemáticos: no representan
cableado eléctrico validado ni una conexión analógica directa a GPIO.

Las entradas de la caja se identifican así: **1 HA** (HR ambiente), **2 TA**
(temperatura ambiente), **3 HG** (suelo general), **4 A-T**, **5 A-H**,
**6 B-T**, **7 B-H**, **8 C-T**, **9 C-H**. A, B y C corresponden a las tres
plantas instrumentadas; T indica temperatura de hoja y H humedad de la maceta.
La cubierta y la puerta de la caja se mantienen editables, ocultas en los renders
para mostrar el interior. En el detalle de Raspberry Pi solo se muestran los
tramos de cable que llegan a la caja; las vistas generales conservan el recorrido completo.

## Artefactos

Rutas relativas a esta carpeta:

| Archivo | Contenido |
|---|---|
| `modelo/invernadero_mejorado.blend` | Modelo editable con seis escenas persistentes. |
| `modelo/renderizar_invernadero.py` | Generador del modelo y de los seis renders. |
| `modelo/verificar_invernadero.py` | Comprueba el archivo guardado, las conexiones y las dimensiones de los PNG. |
| `renders/render_invernadero_mejorado.png` | Vista general. |
| `renders/distribucion_sensores.png` | Distribución e identificación de sensores. |
| `renders/detalle_sensores_planta.png` | Detalle de S1-P01. |
| `renders/detalle_surco2_planta05.png` | Detalle de S2-P05. |
| `renders/detalle_surco3_planta10.png` | Detalle de S3-P10. |
| `renders/detalle_raspberry_pi.png` | Caja, placa, interfaces y entradas de cables. |

## Generación y uso

Configuración utilizada: **Blender 5.2.1**, **Cycles**, **48 muestras** y reducción
de ruido (denoise). General y distribución: **2400 x 1600 px**; los cuatro
detalles: **1800 x 1500 px**.

Desde la raíz del repositorio, en PowerShell:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python-exit-code 1 --python "invernadero/modelo/renderizar_invernadero.py"
```

Añade `-- --preview` al comando para reducir ambas dimensiones al **50 %** y
usar **16 muestras**. Esta modalidad sobrescribe los mismos seis PNG y el
`.blend`; no conserva las salidas de resolución completa. Las rutas de salida
se resuelven respecto al script, no al directorio de trabajo.

Para repetir los renders desde el `.blend` existente sin reconstruir las 30
plantas, añade `-- --render-only`. La generación completa puede tardar varios
minutos; esta opción evita ese paso. No aplica cambios nuevos de geometría del
script. Los PNG se guardan primero en un archivo temporal junto al destino y
después lo reemplazan para reducir conflictos con la sincronización de OneDrive.

**Precaución:** el script borra la escena actual. Ejecútalo en segundo plano
como en el comando anterior o en un archivo nuevo, nunca sobre trabajo sin guardar.

Abre `modelo/invernadero_mejorado.blend` mediante **File > Open**. Las seis
escenas persistentes tienen cámaras y visibilidad propias: selecciona la escena
en Blender y pulsa **F12** para renderizarla. El archivo se guarda con la vista
general activa.

## Verificación

Se comprobaron las 30 macetas, diez por surco, las tres ubicaciones instrumentadas,
los nueve sensores, los extremos de cada cable en su sensor y su entrada de la
caja, las seis escenas y las dimensiones de los seis PNG finales. Se revisaron
visualmente los renders. Para repetir la comprobación sobre las salidas finales:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python-exit-code 1 --python "invernadero/modelo/verificar_invernadero.py"
```
