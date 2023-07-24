PAN = pan

all: loop-prob.pml
	spin -a loop-prob.pml; \
	gcc -g -o $(PAN) pan.c 

run: all
	./pan

clean:
	rm pan*