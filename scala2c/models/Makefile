SOURCES := $(wildcard *.c)
SOURCES := $(filter-out sym_input.c, $(SOURCES))
OBJECTS := $(patsubst %.c, %.o, $(SOURCES))

libmodels.a: $(OBJECTS)
	ar rcs libmodels.a $(OBJECTS)

.c.o:
	gcc -c -g $< -o $@

clean:
	rm -fr *.o *.a
