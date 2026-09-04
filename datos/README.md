# datos/

Carpeta para los **conjuntos de datos, registros y logs** utilizados y generados
durante el proyecto de tesis (lecturas de sensores, resultados de experimentos, etc.).

## 📂 Estructura propuesta

```
datos/
├── README.md                  ← este archivo
├── crudos/                    ← datos tal cual se obtienen de los sensores (CSV, JSON)
├── procesados/                ← datos depurados y listos para análisis/modelado
├── ontologia/                 ← ejemplos de individuos (instancias) de la ontología
└── resultados/                ← salidas de experimentos y métricas (CSV, gráficas)
```

## 🗂️ Formatos recomendados

- **CSV** para series temporales de sensores (fecha/hora + variables).
- **JSON** para intercambio con servicios (MQTT/API).
- **Parquet** cuando los datos sean grandes y quieras consultas eficientes (Python/Pandas).

## 💡 Buenas prácticas

- Docuementa el **origen, formato y unidad** de cada variable en un archivo `LEEME.md`
  dentro de `datos/` (o en la tesis).
- Usa nombres descriptivos: `temperatura_C.csv`, `humedad_porcentaje.csv`, etc.
- Mantén una **convención de fechas** clara (UTC u hora local, indica la zona).

> ⚠️ Si los datasets son muy pesados, guárdalos fuera de Git o usa Git LFS.
> Los formatos de datos ligeros (CSV pequeños) sí pueden versionarse.
