# Compilar la tesis en Windows 11 con VS Code

Esta guía describe cómo editar y compilar la tesis de forma nativa en Windows 11. El documento principal es `documentacion/main.tex`, la configuración de compilación está en `documentacion/latexmkrc` y el PDF generado se guarda en `documentacion/build/main.pdf`.

La tesis usa la clase LaTeX `book`, **XeLaTeX**, `fontspec`, `unicode-math` y las fuentes **TeX Gyre Termes, Heros, Cursor y Termes Math**. La bibliografía utiliza `biblatex-ieee` con **Biber**, no BibTeX. No hacen falta Blender, Python, Node.js ni Make para compilarla.

## 1. Herramientas necesarias

En este equipo ya están instalados **MiKTeX 26.2**, **VS Code** y **LaTeX Workshop**. Están disponibles los comandos `xelatex`, `biber` y `latexmk`. La compilación se verificó exponiendo temporalmente el Perl de Git: Perl todavía no está en el `PATH` habitual de VS Code.

Enlaces oficiales:

- MiKTeX: <https://miktex.org/download>
- Strawberry Perl de 64 bits: <https://strawberryperl.com>
- Visual Studio Code: <https://code.visualstudio.com>
- Extensión LaTeX Workshop, de James Yu: <https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop>

Para una configuración habitual, se recomienda **MiKTeX + Strawberry Perl de 64 bits**, con Perl disponible en `PATH`. Instalar Strawberry Perl o cambiar permanentemente `PATH` es una decisión del usuario; esta guía no ejecuta esos cambios. Después de una instalación o un cambio de entorno, cierre todas las ventanas de VS Code y vuelva a abrirlo para que sus terminales y extensiones reciban el nuevo `PATH`.

Como alternativa a MiKTeX puede utilizar **TeX Live completo**, desde <https://www.tug.org/texlive/>. Elija una distribución: no mezcle ejecutables ni paquetes de MiKTeX y TeX Live en el mismo flujo de compilación.

### Preparar MiKTeX

1. Abra **MiKTeX Console** y revise las actualizaciones en **Updates**. Aplique las actualizaciones autorizadas antes de compilar.
2. Revise la opción de instalación de paquetes faltantes. Manténgala en modo de confirmación cuando esté disponible; seleccione **Yes** para instalación automática únicamente si autoriza las descargas e instalaciones.
3. Si prefiere controlar las instalaciones, use la sección **Packages** para instalar los paquetes que solicite el registro de compilación.

Se necesitan los paquetes de `preamble/paquetes.tex`: `babel` con español, `csquotes`, `fontspec`, `amsmath`, `amssymb`, `mathtools`, `unicode-math`, `graphicx`, `float`, `longtable`, `booktabs`, `multirow`, `array`, `caption`, `subcaption`, `geometry`, `setspace`, `fancyhdr`, `enumitem`, `etoolbox`, `biblatex`, `biblatex-ieee` e `hyperref`, además de TeX Gyre, TeX Gyre Math, Biber y `latexmk`.

Durante la comprobación inicial faltaban paquetes como `csquotes` y `mathtools`; MiKTeX resolvió paquetes faltantes mediante su instalación automática. No se cambiaron sus ajustes ni se instaló otra distribución. No cambie el motor a pdfLaTeX para resolver un paquete o una fuente faltante.

## 2. Comprobar el entorno

Abra PowerShell y ejecute:

```powershell
Get-Command xelatex,latexmk,biber,perl
xelatex --version
biber --version
perl --version
latexmk -v
```

`Get-Command` muestra qué ejecutable se encuentra y su ubicación. Que `latexmk` aparezca no garantiza que pueda ejecutarse: también debe poder encontrar Perl. Si alguna comprobación falla, resuelva esa dependencia antes de usar la receta automática.

### Perl de Git: solución temporal para una terminal

En este equipo se ha localizado Perl en `C:\Program Files\Git\usr\bin\perl.exe`. Puede exponerlo **solo durante la sesión actual de PowerShell**, sin instalar nada ni modificar permanentemente `PATH`:

```powershell
Test-Path -LiteralPath 'C:\Program Files\Git\usr\bin\perl.exe'
$env:PATH = 'C:\Program Files\Git\usr\bin;' + $env:PATH
Get-Command perl
perl --version
latexmk -v
```

Continúe solo si `Test-Path` devuelve `True`. Esta alternativa sirve para intentar la compilación desde esa terminal; no sustituye la recomendación de Strawberry Perl para un entorno habitual. El cambio desaparece al cerrar la terminal y no actualiza el entorno de una extensión de VS Code que ya estaba en ejecución.

## 3. Abrir y editar la tesis

1. En VS Code, use **Archivo > Abrir carpeta** y seleccione `documentacion`, no la raíz del repositorio. Así se simplifican las rutas y el directorio de trabajo.
2. Instale la extensión **LaTeX Workshop** con identificador `James-Yu.latex-workshop`, si todavía no la tiene.
3. Edite `main.tex` y los archivos de contenido que este incorpora. Guarde los cambios antes de compilar.
4. Abra una terminal integrada de PowerShell y compruebe con `Get-Location` que está en `documentacion`.

La plantilla organiza la tesis en siete capítulos y contempla destacados, referencias y anexos. La numeración de capítulos y páginas es automática: las páginas no tienen posiciones fijas. Los marcadores de posición deben sustituirse por contenido real; la plantilla no garantiza una extensión de más de 70 páginas.

## 4. Configurar LaTeX Workshop

Abra la paleta de comandos y seleccione **Preferences: Open User Settings (JSON)**. Integre las siguientes propiedades en sus ajustes de **usuario**, conservando los ajustes existentes y evitando claves duplicadas. No es necesario crear ni editar `.vscode`.

```json
{
  "latex-workshop.latex.tools": [
    {
      "name": "latexmk-xelatex",
      "command": "latexmk",
      "args": [
        "-xelatex",
        "-synctex=1",
        "-interaction=nonstopmode",
        "-file-line-error",
        "-halt-on-error",
        "-outdir=%OUTDIR%",
        "%DOC%"
      ]
    }
  ],
  "latex-workshop.latex.recipes": [
    {
      "name": "latexmk (XeLaTeX)",
      "tools": ["latexmk-xelatex"]
    }
  ],
  "latex-workshop.latex.recipe.default": "first",
  "latex-workshop.latex.outDir": "%DIR%/build",
  "latex-workshop.latex.search.rootFiles.include": ["main.tex"],
  "latex-workshop.view.pdf.viewer": "tab"
}
```

Estos ajustes de usuario también afectan a otros proyectos LaTeX. La búsqueda de raíz limitada a `main.tex` está pensada para abrir `documentacion` como carpeta. `%DOC%`, `%DIR%` y `%OUTDIR%` son variables de LaTeX Workshop, no de PowerShell.

Con `main.tex` activo:

- **Ctrl+Alt+B** compila mediante la primera receta.
- **Ctrl+Alt+V** abre el PDF en una pestaña de VS Code.
- El panel **Salida > LaTeX Workshop** permite consultar los mensajes de compilación.

La receta requiere que el proceso de VS Code pueda encontrar Perl. Si únicamente añadió el Perl de Git al `PATH` de una terminal integrada, compile desde esa terminal; la extensión no hereda ese cambio.

## 5. Compilar desde PowerShell

Todos los comandos de esta sección se ejecutan **desde `documentacion`**. Si su terminal está en la raíz del repositorio, entre primero en esa carpeta:

```powershell
Set-Location -LiteralPath .\documentacion
```

No repita este paso si ya está dentro. Ejecutar allí `latexmk` permite que encuentre el archivo local `latexmkrc`, que configura la salida en `build`.

### Compilación normal

```powershell
latexmk -xelatex -synctex=1 -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

`latexmk` coordina las pasadas de XeLaTeX y ejecuta Biber cuando la bibliografía lo requiere. No añada `-pdf` a esta orden: el motor elegido es XeLaTeX.

Resultado esperado: `build/main.pdf`, equivalente a `documentacion/build/main.pdf` desde la raíz del repositorio.

### Limpiar auxiliares sin borrar el PDF

```powershell
latexmk -c main.tex
```

La opción `-c` limpia auxiliares y conserva el PDF. No la confunda con `-C`, que también elimina los resultados finales.

### Recompilación continua opcional

```powershell
latexmk -pvc -xelatex main.tex
```

Este modo vigila los cambios y recompila. Deténgalo con **Ctrl+C** en la terminal. Evite ejecutar simultáneamente este modo y otra compilación sobre el mismo documento.

## 6. Alternativa directa sin Perl

Si `latexmk` no arranca por falta de Perl, puede invocar XeLaTeX y Biber directamente. Desde **`documentacion`**, ejecute cada paso por separado y continúe solo si el anterior termina correctamente:

```powershell
New-Item -ItemType Directory -Force build
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 -output-directory=build main.tex
biber --input-directory=build --output-directory=build main
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 -output-directory=build main.tex
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -synctex=1 -output-directory=build main.tex
```

La primera pasada genera los datos que necesita Biber, incluido `build/main.bcf`. Biber escribe sus resultados en `build`, y las dos pasadas posteriores actualizan citas, referencias cruzadas e índices. Si la primera pasada falla, no ejecute Biber con archivos incompletos o antiguos.

Mantenga `documentacion` como directorio de trabajo: las rutas relativas del archivo `.bib` deben seguir siendo accesibles desde la raíz del documento. No entre en `build` para ejecutar esta secuencia. El backend es **Biber**, no `bibtex`.

## 7. Bibliografía y contenido pendiente

- Sustituya los textos de ejemplo y marcadores de posición por el contenido definitivo.
- El archivo `bibliografia/referencias.bib` contiene entradas de ejemplo, algunas ficticias y con DOI de muestra: verifique y reemplace esas entradas antes de entregar la tesis.
- Añada las fuentes reales al archivo `.bib` utilizado por el documento y cítelas donde corresponda, por ejemplo mediante `\cite{clave-real}` con una clave existente.
- Es esperable que la sección **REFERENCIAS** esté vacía mientras no haya citas reales. No añada `\nocite{*}` para llenarla artificialmente.
- Tras cambiar citas o bibliografía, use la compilación completa con `latexmk` o repita la secuencia manual con Biber.

## 8. Diagnóstico y comprobación final

| Síntoma | Qué revisar |
| --- | --- |
| `latexmk` indica que no encuentra Perl | Compruebe `Get-Command perl` y el `PATH` del proceso que compila. Use la alternativa temporal o la secuencia directa. |
| La terminal compila pero LaTeX Workshop no | El `PATH` de la extensión puede ser distinto. Un cambio temporal en PowerShell no modifica el entorno de VS Code. |
| Error de `fontspec` o `unicode-math` por el motor | Compruebe que se usa XeLaTeX y no pdfLaTeX. |
| Falta un paquete o una fuente TeX Gyre | Revise MiKTeX Console, sus actualizaciones y los paquetes requeridos. Autorice las instalaciones de forma controlada. |
| Citas indefinidas o petición de ejecutar Biber | Compruebe las claves y la ruta del `.bib`; ejecute Biber y después dos pasadas de XeLaTeX. |
| REFERENCIAS vacía | Compruebe si hay citas reales. Sin ellas, la sección vacía puede ser normal. |
| No aparece el PDF o parece antiguo | Revise el primer error y la fecha de `build/main.pdf`; un PDF previo puede permanecer después de una compilación fallida. |

Lista de comprobación para una compilación local:

- `xelatex`, `biber` y `latexmk` responden; Perl también, si usa `latexmk`.
- El directorio de trabajo es `documentacion`.
- La compilación termina sin errores; revise también las advertencias y `build/main.log` y, cuando se haya ejecutado Biber, `build/main.blg`.
- `build/main.pdf` se ha actualizado y se abre correctamente.
- Las referencias cruzadas, citas, índices y anexos se ven como corresponde al contenido actual.
- Los archivos generados se mantienen en `build`, excluidos de Git; no deben añadirse al control de versiones.

## 9. Estado del documento

Se compiló el proyecto con **XeLaTeX + Biber mediante latexmk** y se generó `build/main.pdf`. La estructura contiene los siete capítulos de la guía, las subsecciones solicitadas en los capítulos 1 y 2 y los apartados finales DESTACADOS, REFERENCIAS y ANEXOS. Los capítulos 3 a 7 quedan sin subsecciones por ahora. El anexo usa numeración alfabética automática.

La plantilla está preparada para escribir, **no para entregar como tesis terminada**: siguen pendientes el título definitivo, autoría, institución, objetivos, desarrollo, resultados y bibliografía real. Los números de página del índice se calculan según el contenido, no se fuerzan a los de la guía.

Las páginas de separación son consecuencia de `twoside,openright`: los capítulos comienzan en página impar. No son un error ni contenido adicional escrito. Los índices de figuras y tablas permanecen vacíos hasta incorporar esos elementos.

Advertencias no bloqueantes observadas: bibliografía vacía y Biber sin citas, avisos de compatibilidad de símbolos entre `unicode-math` y `mathtools`, y una página con espacio vertical insuficientemente distribuido (`Underfull \vbox`) debido al escaso texto de la plantilla. No se añadieron citas ficticias ni se ocultaron estas advertencias para aparentar un documento terminado.

También se comprobó la sintaxis y el modelo de datos del `.bib` con `biber --tool --validate-datamodel`; no se detectaron errores de formato. Esta prueba no verifica la autenticidad de las fuentes ni sus DOI.
