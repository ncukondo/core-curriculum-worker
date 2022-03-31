.PHONY: sheets python_files csv markdown

markdown:
	python ./python/output_markdown.py

csv:
	python ./python/output_csv.py

sheets:
	python -m python.download_sheets

# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --pdf-engine=lualatex --filter=pandoc-crossref ./output/outcomes_tex.md -o ./output/outcomes.pdf
pdf: markdown
	${d_run}pandoc-latex-ja \
		-V documentclass=ltjsarticle \
		--pdf-engine=lualatex \
		--filter=pandoc-crossref \
		-N \
		--toc \
		./dist/r4.md \
		-o ./dist/r4.pdf


python_files:
	jupyter nbconvert --to python ./ipynb/*.ipynb
	rm -rf python
	mkdir python
	cp ./ipynb/*.py python
	cp -r ./ipynb/lib python
	rm ./ipynb/*.py
