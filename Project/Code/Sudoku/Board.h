//This is the header file that contains the class baord for Project 4b

#include <iostream>
#include <limits>
#include "d_matrix.h"
#include "d_except.h"
#include <list>
#include <fstream>

using namespace std;

typedef int ValueType; // The type of the value in a cell
const int Blank = -1;  // Indicates that a cell is blank

const int SquareSize = 3;  //  The number of cells in a small square
                           //  (usually 3).  The board has
                           //  SquareSize^2 rows and SquareSize^2
                           //  columns.

const int BoardSize = SquareSize * SquareSize;

const int MinValue = 1;
const int MaxValue = 9;

//int numSolutions = 0;

#ifndef BOARD_H
#define BOARD_H

class board
// Stores the entire Sudoku board
{
   public:
      board(int);
      void clear();
      void initialize(ifstream &fin);
      void print();
      bool isBlank(int, int);
      void printConflicts();
      void fillCell(int, int, int);
      void clearCell(int, int);
      bool isSolved();
      pair<int, int> findEmptyCell();
      ValueType getCell(int, int);
      void solve();
      void printCounter();
      void printAverageAndTotalCalls();
      int checkSameRow(int, int);
      int checkSameColumn(int, int);
      int checkSameSquare(int, int);
      bool isValid(int, int, int);

   private:
// defines how the Sudoku Board is going to be compared 
      matrix<ValueType> value;
      matrix<bool> rows;
      matrix<bool> columns;
      matrix<bool> squares;
      unsigned int counter;
      vector<unsigned int> calls;
};

#endif
