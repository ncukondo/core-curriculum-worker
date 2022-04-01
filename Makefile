pwd:=$(shell pwd)
uid:=$(shell id -u)
gid:=$(shell id -g)
repo=ghcr.io/ncukondo/
d_run:=docker run --rm --volume "${pwd}:/data" --user ${uid}:${gid} ${repo}

.PHONY: pdf statistics deploy

deploy:
	python ./python/deploy_to_google_drive.py

statistics:
	python ./python/output_statistics.py

markdown_for_tex:
	python ./python/output_tables.py
	python ./python/output_md_for_tex.py


# docker run --rm --volume "$(pwd):/data" --user $(id -u):$(id -g) ghcr.io/ncukondo/pandoc-latex-ja -V documentclass=ltjsarticle --filter=pandoc-crossref --pdf-engine=lualatex ./output/outcomes_for_tex.md -o ./output/outcomes.pdf
pdf: 
	${d_run}pandoc-latex-ja \
		-V documentclass=ltjsarticle \
		--pdf-engine=lualatex \
		--filter=pandoc-crossref \
		--toc \
		./output/outcomes_for_tex.md \
		-o ./output/outcomes.pdf

python_files:
	jupyter nbconvert --to python ./ipynb/*.ipynb
	rm -rf python
	mkdir python
	cp ./ipynb/*.py python
	cp -r ./ipynb/lib python
	rm ./ipynb/*.py
