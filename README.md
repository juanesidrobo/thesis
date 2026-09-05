# Tesis — Anteproyecto, Documentación, Ontología e Invernadero

Este repositorio aloja **todo** lo relacionado con el proyecto de tesis:

- 📄 **`documentacion/`** → plantilla del documento de tesis en LaTeX, con **XeLaTeX + biber** y citas estilo **IEEE**. El contenido y las referencias definitivas están pendientes.
- 🧩 **`ontologia/`** → el documento inicial de la **ontología** (formato `.owl`, abrible en Protégé).
- 🌱 **`invernadero/`** → render/modelo 3D del invernadero donde se ejecutará el proyecto *(pendiente — lo retomamos más adelante)*.
- 📊 **`datos/`** → conjuntos de datos, registros y logs asociados al proyecto.
- 🔧 **`scripts/`** → utilidades (compilación, etc.).

---

## 📁 Estructura de carpetas

```
thesis/
├── README.md                    ← este archivo (índice general)
├── .gitignore                   ← ignora artefactos de compilación y archivos temporales
├── Makefile                     ← orquestador de compilación (delega en documentacion/)
│
├── documentacion/               ← 📄 LA TESIS — proyecto LaTeX
│   ├── main.tex                 ← documento principal (punto de entrada)
│   ├── Makefile                 ← compilación local de la tesis
│   ├── latexmkrc                ← configuración de latexmk (XeLaTeX + biber)
│   ├── preamble/                ← paquetes, configuración y macros
│   ├── contenido/
│   │   ├── datos_tesis.tex      ← metadatos de la tesis (título, autor, tutor…)
│   │   ├── portada.tex          ← carátula
│   │   ├── dedicatoria.tex
│   │   ├── agradecimientos.tex
│   │   ├── resumen.tex          ← resumen en español
│   │   ├── abstract.tex         ← resumen en inglés
│   │   ├── lista_abreviaturas.tex
│   │   ├── capitulos/           ← capítulos del cuerpo (01…07)
│   │   ├── anexos/              ← anexos
│   │   └── figuras/             ← figuras/imágenes (PNG, PDF, etc.)
│   ├── bibliografia/
│   │   └── referencias.bib      ← bibliografía (BibTeX, estilo IEEE vía biber)
│   └── build/                   ← salida generada (PDF/aux) — NO se sube a Git
│
├── ontologia/                   ← 🧩 ONTOLOGÍA (Protégé)
│   ├── README.md
│   └── ontologia_invernadero.owl
│
├── invernadero/                 ← 🌱 RENDER / MODELO 3D del invernadero (pendiente)
│   └── README.md
│
├── datos/                       ← 📊 DATOS del proyecto
│   └── README.md
│
└── scripts/                     ← 🔧 UTILIDADES
    ├── README.md
    └── compilar.sh              ← compila la tesis con un comando
```

---

## ✅ Requisitos para compilar TEX en local

**Windows 11 y VS Code:** consulta la [guía de instalación, escritura y compilación](documentacion/README.md).
Incluye LaTeX Workshop, Perl para `latexmk` y una alternativa nativa sin Make ni Bash.

Necesitas una distribución de **TeX Live** completa (o MiKTeX en Windows) con:

- `xelatex` (compilador XeLaTeX)
- `latexmk` (automatiza compilación, biber, etc.)
- `biber` (procesa la bibliografía con `biblatex`)
- Paquetes: `babel` (+ español), `fontspec`, `biblatex`, `csquotes`, `geometry`, `unicode-math`, `amsmath`, `graphicx`, `booktabs`, `caption`, `fancyhdr`, `hyperref`, etc.
- Fuentes **TeX Gyre** (`TeX Gyre Termes`, `Heros`, `Cursor`, `Termes Math`). Incluidas en TeX Live y MiKTeX.

> 💡 La tesis usa **XeLaTeX** para un manejo limpio de acentos/Unicode en español y fuentes del sistema.
> Si prefieres la fuente *Times New Roman*, en `preamble/paquetes.tex` cambia `\setmainfont{TeX Gyre Termes}` por `\setmainfont{Times New Roman}`.

### Instalación por sistema operativo

| Sistema | Cómo instalar |
|---|---|
| **Windows** | Instala [MiKTeX](https://miktex.org) (asegura *"Install missing packages on the fly"* activado) y luego `latexmk`/`biber` desde el MiKTeX Console, o instala TeX Live. |
| **macOS** | `brew install --cask mactex` (trae TeX Live completo). |
| **Linux (Debian/Ubuntu)** | `sudo apt install texlive-full biber latexmk` |

---

## ⚙️ Cómo compilar (local)

Desde la **raíz** del repositorio:

```bash
make            # compila la tesis (equivalente a: make -C documentacion)
make watch      # compilación continua (recarga con cada cambio)
make clean      # limpia los temporales
```

O directamente desde `documentacion/`:

```bash
cd documentacion
make            # genera documentacion/build/main.pdf
```

También hay un script de conveniencia:

```bash
bash scripts/compilar.sh
```

El PDF final queda en **`documentacion/build/main.pdf`**.

---

## ✍️ Cómo escribir la tesis

1. **Metadatos** → edita `documentacion/contenido/datos_tesis.tex` (título, autor, tutor, universidad…).
2. **Capítulos** → añade/edita archivos en `documentacion/contenido/capitulos/`. Para añadir uno:
   - crea `documentacion/contenido/capitulos/NN_nombre.tex`,
   - e inclúyelo en `documentacion/main.tex` (ordenado) con `\input{contenido/capitulos/NN_nombre}`.
3. **Bibliografía** → añade entradas en `documentacion/bibliografia/referencias.bib`. Las citas van con `\cite{clave}` (estilo IEEE, numeración por orden de cita).
4. **Figuras** → coloca los archivos en `documentacion/contenido/figuras/` e inserta con `\includegraphics`.
5. **Anexos** → edita `documentacion/contenido/anexos/`.

---

## 🔐 Archivos grandes / binarios (render 3D, datasets)

El modelo 3D del invernadero (`.blend`, texturas, renders) y los datasets pueden ser **muy pesados** para Git. Recomendado:

- Mantener los **archivos fuente del render** con [Git LFS](https://git-lfs.com) (`git lfs track "*.blend" "*.fbx" "*.obj"`), o
- Almacenarlos fuera del repositorio y registrar **solo** los renders finales en formato ligero (PNG/JPG/GLB comprimidos) + un enlace a la fuente.

> ⚠️ Los artefactos de compilación (`documentacion/build/`) están ignorados en Git (`.gitignore`).

---

## 🧭 Estado actual

- ✅ Estructura de carpetas lista.
- ✅ Sistema de compilación LaTeX funcionando (XeLaTeX + biber, citas IEEE).
- ✅ Esqueleto de la tesis (portada, dedicatoria, agradecimientos, resumen/abstract, abreviaturas, 7 capítulos, anexos, bibliografía).
- ✅ Ontología inicial para Protégé (`.owl`).
- ⏳ Render del invernadero — **pendiente** (se retoma más adelante).
