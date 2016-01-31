CC=g++
CFLAGS=-std=c++11 -Wall -pedantic
BIN=psearch

SRC=$(wildcard *.cpp)
OBJ=$(SRC:%.cpp=%.o)

all: $(OBJ)
	$(CC) -o $(BIN) $^

%.o: %.c
	$(CC) $@ -c $<

clean:
	rm -f *.o
	rm $(BIN) 
