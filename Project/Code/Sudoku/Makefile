main: main.o Board.o d_matrix.o d_except.o
	g++ main.o Board.o d_matrix.o d_except.o -o main
main.o: main.cpp Board.h
	g++ -c main.cpp
Board.o: Board.cpp Board.h d_matrix.h d_except.h
	g++ -c Board.cpp
d_matrix.o: d_matrix.h d_except.h
	g++ -c d_matrix.cpp
d_except.o: d_except.h
	g++ -c d_except.cpp
clean:
	rm main main.o Board.o d_except.o d_matrix.o
