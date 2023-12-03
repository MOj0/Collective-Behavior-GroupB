# How to build?

**1. Run pdflatex:** This generates the `.aux` file which contains information about citations.
```bash
pdflatex --output-directory=out report.tex
```
**2. Run BibTeX:** This processes the `.aux` file and generates the bibliography data.
```bash
bibtex out/report.aux
```
**3. Run pdflatex again:** Running it twice ensures that all cross-references and citations are resolved correctly.
```bash
pdflatex --output-directory=out report.tex
```
