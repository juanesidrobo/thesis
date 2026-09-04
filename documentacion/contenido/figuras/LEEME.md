# Carpeta de figuras

Coloca aquí las **imágenes, diagramas y gráficos** de la tesis.

### Formatos admitidos
- `.png` (recomendado para capturas y gráficas)
- `.pdf` (recomendado para diagramas vectoriales)
- `.jpg` / `.jpeg` (fotografías)
- `.eps` (solo si compilas con `pdflatex`; con XeLaTeX mejor `pdf`)

### Cómo insertar una figura
En cualquier capítulo, por ejemplo `contenido/capitulos/05_desarrollo.tex`:

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\textwidth]{contenido/figuras/nombre_archivo}
    \caption{Descripción de la figura.}
    \label{fig:etiqueta}
\end{figure}
```

> 💡 Recuerda que las rutas son **relativas a `main.tex`**. Si la figura está en
> `contenido/figuras/`, la ruta en `\includegraphics` es `contenido/figuras/archivo`.
> Habla de la figura en el texto con `\ref{fig:etiqueta}` (o el atajo `\figura{fig:etiqueta}`).
