# ontologia/

Carpeta destinada a la **ontología del invernadero inteligente** que se construye en la tesis.

## 📂 Estructura propuesta

```
ontologia/
├── README.md                       ← este archivo
├── ontologia_invernadero.owl       ← documento inicial (esqueleto, editable en Protégé)
└── datos/                          ← (opcional) datos de prueba, ejemplos de individuos
```

## 🛠️ Herramientas

- **Protégé Desktop** — editor de ontologías. Descárgalo en https://protege.stanford.edu
- **Razonadores** (opcional): HermiT, Pellet (vienen integrados en Protégé).
- **Consultas SPARQL** en Protégé o `Apache Jena Fuseki` para consultar la ontología.

## 📖 Cómo usar el esqueleto `ontologia_invernadero.owl`

1. Abre Protégé → *File* → *Open…* → selecciona `ontologia_invernadero.owl`.
2. Revisa las clases y propiedades de ejemplo (Invernadero, Sensor, Cultivo, Medición, etc.).
3. Añade/renombra clases e individuos según tu dominio.
4. Guarda; Protégé regenera el `.owl` automáticamente.

> ⚠️ Es un **punto de partida**. Amplíalo para cubrir todos los conceptos del sistema
> (actuadores, zonas, hortalizas, sensores, lecturas, alarmas, usuarios, etc.).

## ⚙️ Dónde referenciarlo en la tesis

En `documentacion/contenido/capitulos/04_metodologia.tex` y `05_desarrollo.tex`
se menciona el desarrollo de la ontología. Puedes citar este archivo desde el
documento con un `\includegraphics` si generas un diagrama, o referenciarlo como anexo.
