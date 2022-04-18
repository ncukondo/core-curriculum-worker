pwd:=$(shell pwd)
uid:=$(shell id -u)
gid:=$(shell id -g)
repo=ghcr.io/ncukondo/
d_run:=docker run --rm --volume "${pwd}:/data" --user ${uid}:${gid} ${repo}

.PHONY: pdf statistics deploy markdowns

deploy:
	python ./python/deploy_to_google_drive.py

statistics:
	python ./python/output_statistics.py

markdowns:
	python ./python/output_tables.py
	python ./python/output_md_for_tex.py
	python ./python/output_md_for_docx.py


# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --filter=pandoc-crossref --pdf-engine=lualatex ./output/outcomes_for_tex.md -o ./output/outcomes.pdf
pdf: 
	${d_run}pandoc-latex-ja \
		-V documentclass=ltjsarticle \
		--pdf-engine=lualatex \
		--filter=pandoc-crossref \
		--toc \
		--toc-depth=2 \
		./output/outcomes_for_tex.md \
		-o ./output/outcomes.pdf

# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --filter=pandoc-crossref --pdf-engine=lualatex ./output/outcomes_for_tex.md -o ./output/outcomes.pdf
docx: 
	${d_run}pandoc-latex-ja \
		--filter=pandoc-crossref \
		--toc \
		--reference-doc=src/template.docx \
		./output/outcomes_for_docx.md \
		-o ./output/outcomes.docx


python_files:
	jupyter nbconvert --to python ./src/*.ipynb
	rm -rf python
	mkdir python
	cp ./src/*.py python
	cp -r ./src/lib python
	rm ./src/*.py
