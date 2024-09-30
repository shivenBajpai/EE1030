#!/bin/bash

pdflatex main.tex
if [[ $? == 0 && $(hostname) == "localhost" ]]; then
	termux-open main.pdf
else
	open main.pdf
fi
