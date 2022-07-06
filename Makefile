pwd:=$(shell pwd)
uid:=$(shell id -u)
gid:=$(shell id -g)
repo=ghcr.io/ncukondo/
get_dir:=$${LOCAL_WORKSPACE_FOLDER:-$$(pwd)}
local_dir:=$(get_dir)
d_run:=docker run --rm --volume "${local_dir}:/data" --user ${uid}:${gid} ${repo}

.PHONY: pdf statistics deploy markdowns html output prepare_for_pandoc all

all:
	make documents
	make deploy

documents: 
	make prepare_for_pandoc 
	make pdf 
	make outcome_pdf 
	make docx 
	make outcome_docx 
	make statistics

prepare_for_pandoc: 
	make python_files 
	make markdowns

deploy:
	python ./python/deploy_to_google_drive.py

statistics:
	python ./python/output_statistics.py

markdowns:
	python ./python/output_outcomes_md.py
	python ./python/output_tables.py
	python ./python/output_documents_md.py
	python ./python/output_md_for_tex.py
	python ./python/output_md_for_docx.py


# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --filter=pandoc-crossref --pdf-engine=lualatex ./output/outcomes_for_tex.md -o ./output/outcomes.pdf
pdf: 
	${d_run}pandoc-lualatex-ja pandoc\
		-V documentclass=ltjsarticle \
		--pdf-engine=lualatex \
		--filter=pandoc-crossref \
		--toc \
		--toc-depth=3 \
		--bibliography=./data_in_github/citations.bib \
		--citeproc \
		--csl=apa \
		./output/core_curriculum_for_tex.md \
		-o ./output/core_curriculum.pdf

outcome_pdf: 
	${d_run}pandoc-lualatex-ja pandoc\
		-V documentclass=ltjsarticle \
		--pdf-engine=lualatex \
		--filter=pandoc-crossref \
		--toc \
		--toc-depth=3 \
		./output/outcomes_for_tex.md \
		-o ./output/outcomes.pdf


pdf_from_tex: 
	${d_run}pandoc-lualatex-ja lualatex\
		-output-directory=output \
		./output/outcomes.tex \


# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --filter=pandoc-crossref --pdf-engine=lualatex ./output/outcomes_for_tex.md -o ./output/outcomes.pdf
tex: 
	${d_run}pandoc-lualatex-ja pandoc\
		-V documentclass=ltjsarticle \
		--pdf-engine=lualatex \
		--filter=pandoc-crossref \
		--toc \
		--toc-depth=3 \
		--self-contained \
		./output/outcomes_for_tex.md \
		-o ./output/outcomes.tex


# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --filter=pandoc-crossref --pdf-engine=lualatex ./output/outcomes_for_tex.md -o ./output/outcomes.pdf
docx_direct: 
	${d_run}pandoc-lualatex-ja pandoc\
		--filter=pandoc-crossref \
		--toc \
		--reference-doc=src/template.docx \
		./output/outcomes_for_docx.md \
		-o ./output/outcomes.docx

docx: 
	${d_run}pandoc-lualatex-ja pandoc\
		--filter=pandoc-crossref \
		--citeproc \
		--bibliography=./data_in_github/citations.bib \
		--csl=ama \
		--self-contained \
		./output/core_curriculum_for_docx.md \
		-o ./output/core_curriculum.html
	${d_run}pandoc-latex-ja \
		--toc \
		--reference-doc=src/template.docx \
		./output/core_curriculum.html \
		-o ./output/core_curriculum.docx

outcome_docx: 
	${d_run}pandoc-lualatex-ja pandoc\
		--filter=pandoc-crossref \
		--self-contained \
		./output/outcomes_for_docx.md \
		-o ./output/outcomes.html
	${d_run}pandoc-lualatex-ja pandoc\
		--toc \
		--reference-doc=src/template.docx \
		./output/outcomes.html \
		-o ./output/outcomes.docx


python_files:
	jupyter nbconvert --to python ./src/*.ipynb
	rm -rf python
	mkdir python
	cp ./src/*.py python
	cp -r ./src/lib python
	rm ./src/*.py
