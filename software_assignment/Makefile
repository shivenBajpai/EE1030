SHELL := /bin/bash

.PHONY: build

build: main.out test.out
	@echo "Finshed"

clean:
	@echo "Removing binaries"
	-@rm main.out
	-@rm test.out

run: main.out
	@time ./main.out

test: test.out
	@./test.out

main.out: main.c matlib.c sapack.c
	@gcc main.c matlib.c sapack.c -g -lm -fopenmp -mavx2 -march=native -Ofast -o main.out

test.out: test.c matlib.c sapack.c
	@gcc test.c matlib.c sapack.c -g -lm -fopenmp -mavx2 -march=native -Ofast -o test.out