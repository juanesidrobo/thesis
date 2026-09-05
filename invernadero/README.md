# invernadero/

## Versión Mejorada Para Blender

La versión actual es **`modelo/invernadero_mejorado.blend`**. Se abre directamente
con **File > Open**; no requiere importar el GLB anterior.

| Archivo nuevo | Contenido |
|---|---|
| [`renders/render_invernadero_mejorado.png`](renders/render_invernadero_mejorado.png) | Vista general con nueve plantas P01–P09 y cuatro sensores identificados. |
| [`renders/detalle_sensores_planta.png`](renders/detalle_sensores_planta.png) | Acercamiento de P02, con los sensores de hoja y de humedad relativa del aire. |
| [`modelo/invernadero_mejorado.blend`](modelo/invernadero_mejorado.blend) | Geometría editable, materiales, luces, rótulos y dos cámaras. |
| [`modelo/renderizar_invernadero.py`](modelo/renderizar_invernadero.py) | Generador nativo de Blender; no necesita numpy, trimesh ni recursos externos. |

### Instrumentación Actual

| ID / color | Variable | Ubicación |
|---|---|---|
| 01 / azul | Humedad relativa ambiente | Soporte independiente con abrigo de radiación blanco. |
| 02 / naranja | Temperatura ambiente | Segundo soporte con abrigo de radiación blanco. |
| 03 / rojo | Temperatura de una hoja | Pinza de contacto sobre una hoja de P02. |
| 04 / turquesa | Humedad relativa del aire junto al follaje | Carcasa ventilada sostenida en la misma planta P02. |

**Humedad relativa no significa humedad del suelo.** Esta versión no incorpora
sondas de humedad de sustrato. La caja situada junto al tronco representa un
registrador de datos, no un quinto sensor. Las otras ocho plantas no llevan sensores.

La composición es una **ilustración técnica 3D**, no una fotografía ni un plano
constructivo. Las dimensiones, carcasas y colores son ilustrativos, no modelos
comerciales validados. Se ocultan el cerramiento frontal, el lateral derecho y
una mitad de la cubierta para ver el interior; las piezas permanecen en el `.blend`.
El detalle oculta temporalmente las otras plantas y la estructura, sin cambiar P02.

### Regenerar Los Renders

Probado con Blender **5.2.1**, motor **Cycles**, 48 muestras, reducción de ruido y
salida de **1800 × 1500 píxeles**. Desde la raíz del repositorio, en PowerShell:

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" --background --python-exit-code 1 --python "invernadero/modelo/renderizar_invernadero.py"
```

Si Blender está en `PATH`:

```bash
blender --background --python-exit-code 1 --python invernadero/modelo/renderizar_invernadero.py
```

Añade `-- --preview` para una prueba a 990 × 825 y 16 muestras. Ambas modalidades
sobrescriben los **dos PNG nuevos y el `.blend` mejorado**; la prueba no conserva
la resolución final. Las rutas de salida se resuelven desde el script.

**Precaución:** el script reemplaza la escena activa. Ejecútalo en segundo plano
o en un archivo nuevo, no sobre una escena con trabajo sin guardar.
El `.blend` queda preparado para renderizar la vista general con F12. Para repetir
el acercamiento con el aislamiento y los rótulos correctos, ejecuta el script;
cambiar únicamente de cámara no aplica ese aislamiento.

## Versión Anterior Conservada

Los archivos y la documentación siguientes corresponden al **modelo base anterior**,
no al `.blend` mejorado. Se conservan como referencia; sus sensores de suelo y su
instrumentación en tres plantas **no describen la versión actual**.

Carpeta para el **render / modelo 3D del invernadero** donde se ejecutará y
desplegará el proyecto de la tesis.

> ✅ **Estado: AVANZADO.** Ya se generó el modelo 3D editable y el render
> fotorrealista según la imagen de referencia aportada.

## 📂 Estructura

```
invernadero/
├── README.md                  ← este archivo
├── modelo/                    ← modelo 3D y scripts generadores
│   ├── generar_invernadero.py ← genera el modelo 3D (GLB) proceduralmente
│   ├── vista_previa.py        → render de vista previa (matplotlib) del GLB
│   └── invernadero.glb        ← MODELO 3D editable (ábrelo en Blender)
└── renders/                   ← imágenes de render finales
    ├── render_invernadero.png        ← render fotorrealista (para la tesis)
    └── vista_previa_invernadero.png  ← vista previa técnica del modelo
```

## 🖼️ Renders generados

| Archivo | Descripción |
|---|---|
| `renders/render_invernadero.png` | **Render fotorrealista** listo para insertar en la tesis/ontología. |
| `renders/vista_previa_invernadero.png` | Vista previa técnica (3D) del modelo. |

## 🧊 Modelo 3D — `modelo/invernadero.glb`

El modelo es un **archivo GLB** (glTF Binary) **editable**: puedes abrirlo,
modificarlo y re-renderizarlo en **Blender**, o visualizarlo en visores web.

### Contenido del modelo
- **Estructura de aluminio**: postes, vigas de alero, cabios y cumbrera (techo a dos aguas).
- **Paredes y techo en** **policarbonato blanco translúcido** (material PBR con
  transparencia `alphaMode=BLEND`).
- **Suelo de grava** (lecho de piedrecillas + base).
- **9 plantas madre de cítricos** en macetas de barro (tronco, ramas y copa de hojas),
  distribuidas en una cuadrícula 3×3.
- **Sensores**:
  - Sensor de **temperatura/humedad ambiente**: carcasa blanca de láminas sobre poste.
  - Sensor de **humedad en el suelo**: sonda clavada en la grava.
  - **Solo en 3 plantas** (esquinas y centro): sensor de **humedad en la maceta**
    (sonda + conector verde) y sensor de **temperatura en las hojas** (pinza + cable).
  - Las **demás plantas no llevan sensores**, tal como pediste.

### Materiales PBR aplicados
`aluminio`, `policarbonato` (translúcido), `terracota`, `suelo`, `tronco`, `hoja`,
`grava`, `sensor_wh`, `sensor_dk`, `metal`, `conn_green`.

## 📖 Cómo abrir el modelo en Blender

> ⚠️ **Importante:** en Blender un archivo `.glb` **NO se abre con `File > Open`**
> (eso solo abre archivos `.blend`). Debes **importarlo**:
> `File > Import > glTF 2.0 (.glb/.gltf)` → selecciona `invernadero.glb`.

La forma más cómoda es usar el script incluido **`modelo/abrir_en_blender.py`**:

**Opción A — desde la interfaz de Blender (recomendada):**
1. Abre Blender.
2. Cambia a la pestaña **Scripting** (arriba, junto a Layout/Modeling).
3. `Text > Open...` → selecciona `modelo/abrir_en_blender.py`.
4. Pulsa **▶ Run Script** (o `Alt+P`).
   → El invernadero se importará solo y quedará en la colección *Invernadero*.

**Opción B — terminal:**
```bash
blender --background --python abrir_en_blender.py
```

**Opción C — manual:** `File > Import > glTF 2.0` y elige `invernadero.glb`.

> 💡 Para ver los colores del modelo, pon el *Viewport Shading* en **Material Preview
> o Rendered**.

### ¿Por qué no abría antes?
El `.glb` anterior era **glTF 2.0 válido** pero las mallas se exportaron **sin el
atributo `NORMAL`**, lo que hace que en Blender se vean con sombreado plano/facetado
y, sobre todo, puede confundir a algunos importadores/configuraciones. Eso se ha
**corregido**: el archivo actual incluye **normales por vértice** (sombreado suave).
Además, el paso más habitual de error era intentar `File > Open` en vez de
`File > Import > glTF 2.0`.

## 🛠️ Herramientas

- **Blender** para abrir y renderizar `invernadero.glb`.
- **Blender / 3.js** si se quiere un visor interactivo web.
- Los scripts regeneran el modelo y la vista previa con **Python** (`numpy`, `trimesh`, `matplotlib`).

### Scripts de `modelo/`
| Archivo | Para qué sirve |
|---|---|
| `generar_invernadero.py` | Regenera `invernadero.glb` (con normales) desde cero. |
| `abrir_en_blender.py` | Abre el GLB automáticamente dentro de Blender. |
| `vista_previa.py` | Genera la vista previa técnica 3D (matplotlib). |

### Regenerar el modelo (opcional)
```bash
# Desde la carpeta modelo/ (requiere un entorno con numpy, trimesh, scipy)
python3 generar_invernadero.py     # escribe invernadero.glb
python3 vista_previa.py            # escribe ../renders/vista_previa_invernadero.png
```

## 📎 Notas sobre el control de versiones

- El **render final** (`render_invernadero.png`) es ligero y puede versionarse en Git.
- El **modelo `.glb`** y el **script** se pueden versionar; si el `glb` llegara a
  crecer demasiado, usa **Git LFS** (`git lfs track "*.glb"`) o guárdalo fuera del repo.
- El render fotorrealista es de carácter **referencial / ilustrativo**.

> ⏳ Próximo paso opcional: integrar este invernadero como caso de estudio en la
> ontología (`../ontologia/`) y en el capítulo de desarrollo de la tesis.
