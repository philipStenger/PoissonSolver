all: poisson

# -g outputs debugging information
# -Wall enables all warnings
# -pthread configures threading
CFLAGS = -g -Wall -pthread -fopenmp -Ofast

poisson: poisson.c
	gcc $(CFLAGS) -o poisson poisson.c

poisson_profile: poisson.c
	gcc -pg -O3 -o poisson_profile poisson.c -pthread

.PHONY: disassembly
disassembly: poisson.s

poisson.s: poisson
	objdump -S --disassemble $< > $@

.PHONY: test
test: poisson
	./test.sh

.PHONY: clean
clean:
	rm -f poisson *.o *.s *.out poisson_profile

.PHONY: profile
profile: gmon.out
	gprof -b poisson_profile gmon.out

gmon.out: poisson_profile
	./$<