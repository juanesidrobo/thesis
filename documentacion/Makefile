# ============================================================
#  Makefile — Compilación local de la tesis
#  Motor: XeLaTeX + biber (citas IEEE)
#
#  Uso:
#    make          → compila (genera build/main.pdf)
#    make watch    → compilación continua (con cada guardado)
#    make clean    → elimina la carpeta build/ (temporales y PDF)
#    make clean-full→ alias de clean (por compatibilidad)
# ============================================================

.PHONY: all pdf watch clean clean-full

LATEXMK      ?= latexmk
OUTDIR       := build
JOB          := main

# Opciones de latexmk (motores y salida en build/)
LATEXMK_OPTS  = -xelatex -pdf -interaction=nonstopmode -halt-on-error \
                -outdir=$(OUTDIR) -auxdir=$(OUTDIR)

all: pdf

pdf:
	@echo "▶ Compilando la tesis con XeLaTeX + biber..."
	$(LATEXMK) $(LATEXMK_OPTS) $(JOB).tex
	@echo
	@echo "════════════════════════════════════════════════════"
	@echo "  ✔ PDF generado:  $(OUTDIR)/$(JOB).pdf"
	@echo "════════════════════════════════════════════════════"
	@echo "  Ábrelo con:  xdg-open $(OUTDIR)/$(JOB).pdf  (Linux)"
	@echo "               open $(OUTDIR)/$(JOB).pdf       (macOS)"

watch:
	$(LATEXMK) -xelatex -pdf -pvc -interaction=nonstopmode \
		-outdir=$(OUTDIR) -auxdir=$(OUTDIR) $(JOB).tex

clean:
	rm -rf $(OUTDIR)
	@echo "✔ Carpeta $(OUTDIR)/ eliminada."

clean-full: clean
