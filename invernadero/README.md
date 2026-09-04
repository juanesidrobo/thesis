# invernadero/

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

## 🛠️ Herramientas

- **Blender** para abrir y renderizar `invernadero.glb` (importar → *File > Import > glTF 2.0*).
- **Blender / 3.js** si se quiere un visor interactivo web.
- Los scripts `generar_invernadero.py` y `vista_previa.py` regeneran el modelo y la
  vista previa con **Python** (`numpy`, `trimesh`, `matplotlib`).

### Regenerar el modelo (opcional)
```bash
# Desde la carpeta modelo/ (requiere un entorno con numpy, trimesh)
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
