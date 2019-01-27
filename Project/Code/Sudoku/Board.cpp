//This is the source file that contains the board constructors and functions

#include <cmath>
#include "Board.h"

using namespace std;

board::board(int sqSize)
// Board constructor
   : value(BoardSize,BoardSize), rows(BoardSize, BoardSize, false), columns(BoardSize, BoardSize, false), squares(BoardSize, BoardSize, false)

{
   clear();
}

void board::clear()
// Mark all possible values as legal for each board entry
{
	for (int i = 0; i < BoardSize; i++)
	
		for (int j = 0; j < BoardSize; j++)
		
		{
			value[i][j] = Blank;
			rows[i][j] = false;
			columns[i][j] = false;
			squares[i][j] = false;
			counter = 0;
		}
}

void board::initialize(ifstream &fin)
// Read a Sudoku board from the input file.
{
   char ch;

   clear();

   for (int i = 0; i < BoardSize; i++)
   
   {
      for (int j = 0; j < BoardSize; j++)
      
	    {
	       fin >> ch;

          // If the read char is not Blank
	      if (ch != '.')
             fillCell(i, j, ch-'0');   // Convert char to int
        }
   }
}

int squareNumber(int i, int j)
// Return the square number of cell i,j (counting from left to right,
// top to bottom. 
{

   return (int) (SquareSize * (floor((i) / SquareSize)) + floor((j) / SquareSize));
}

ostream &operator<<(ostream &ostr, vector<int> &v)
// Overloaded output operator for vector class.
{
   for (int i = 0; i < (int)v.size(); i++)
   
	  ostr << v[i] << " ";
   cout << endl;

   return ostr;
}

ValueType board::getCell(int i, int j)
// Returns the value stored in a cell.  Throws an exception
// if bad values are passed.
{
	
   if (i >= 0 && i < BoardSize && j >= 0 && j < BoardSize)
      return value[i][j];
      
   else
      throw rangeError("bad value in getCell");
}

bool board::isBlank(int i, int j)
// Returns true if cell i,j is blank, and false otherwise.
{
   if (i < 0 || i > BoardSize-1 || j < 0 || j > BoardSize-1)
      throw rangeError("bad value in setCell");

   return (getCell(i,j) == Blank);
}

void board::print()
// Prints the current board.
{
   for (int i = 0; i < BoardSize; i++)
   {
      if ((i) % SquareSize == 0)
      
      {
         cout << " -";
	
	 for (int j = 0; j < BoardSize; j++)
	 
	    cout << "---";
         cout << "-";
	 cout << endl;
      }
    
	  for (int j = 0; j < BoardSize; j++)  
      {
	
	 if ((j) % SquareSize == 0)
	 
	    cout << "|";
	 if (!isBlank(i,j))
	 
	    cout << " " << getCell(i,j) << " ";
	 else
	 
	    cout << "   ";
      }
      cout << "|";
      cout << endl;
   }

   cout << " -";
   
   for (int j = 0; j < BoardSize; j++)
      cout << "---";
   cout << "-";
   cout << endl;
}


ostream &operator<<(ostream &ostr, matrix<bool> &m)
// Overloaded output operator for vector class.
{
   for (int i = 0; i < 9; i++)
   {
	   for (int j = 0; j < 9; j++)
	   {
		   ostr << m[i][j] << " ";
	   }
	   cout << endl;
   }
   return ostr;
}

void board::printConflicts()
//prints the found conflicts
{
	cout << "Rows\n" << rows << "Columns\n" << columns << "Squares\n" << squares;
}

void board::fillCell(int i, int j, int ch)
// this fills a cell when prompted to play the game
{
	value[i][j] = ch;
	rows[i][ch-1] = true;
	columns[j][ch-1] = true;
	squares[squareNumber(i, j)][ch-1] = true;
}

void board::clearCell(int i, int j)
//this clears a cell if prompted because of inaccuracy
{
	int tmp = getCell(i, j);
	value[i][j] = Blank;
	rows[i][tmp-1] = false;
	columns[j][tmp-1] = false;
	squares[squareNumber(i, j)][tmp-1] = false;
}

bool board::isSolved()
//sees if the board is completely right 
{
	for (int i = 0; i < BoardSize; i++)
	{
		for (int j = 0; j < BoardSize; j++)
		{
			if (value[i][j] == Blank)
				return false;
		}
	}
	return true;
}

pair<int, int> board::findEmptyCell()
//find cell with most conflicts that has not been filled yet
{
	pair<int, int> p;
	int max = 0;
	
	for (int i = 0; i < BoardSize; i++)
	{
		for (int j = 0; j < BoardSize; j++)
		{
			if (value[i][j] == Blank)
			{
				int count = 0;
				
				for (int k = 0; k < 9; k++)
				{
					if (rows[i][k] == true || columns[j][k] == true || squares[squareNumber(i, j)][k] == true)
						count++;
				}
				
				if (count > max)
				{
					max = count;
					p = make_pair(i, j);
				}
			}
		}
	}
	return p;
}

void board::solve()
// recursive function to fill and solve board
{
	if (isSolved() == true)
	{
		cout << "Board is solved\n";
		print();
		return;
	}
	
	else
	{
		pair<int, int> p = findEmptyCell();

		int r = checkSameRow(p.first, p.second);
		int c = checkSameColumn(p.first, p.second);
		int s = checkSameSquare(p.first, p.second);
//
		if(r >= 0 && isValid(p.first, p.second, r) == true)
		{
			fillCell(p.first, p.second, r + 1);
			//print();
			counter++;
			solve();
			if (isSolved() == true)
				return;
			clearCell(p.first, p.second);
			//print();
		}

		if(c >= 0 && isValid(p.first, p.second, c) == true && c != r)
		{
			fillCell(p.first, p.second, c + 1);
			//print();
			counter++;
			solve();
			if (isSolved() == true)
				return;
			clearCell(p.first, p.second);
			//print();
		}
//
		if(s >= 0 && isValid(p.first, p.second, s) == true && s != r && s != c)
		{
			fillCell(p.first, p.second, s + 1);
			counter++;
			solve();
			if (isSolved() == true)
				return;
			clearCell(p.first, p.second);
		}

		for (int ch = 0; ch < BoardSize; ch++)
		{
			if(isValid(p.first, p.second, ch) == true && ch != r && ch != c && ch != s)
			{
				fillCell(p.first, p.second, ch + 1);
				//print();
				counter++;
				solve();
				if (isSolved() == true)
					return;
				else
					clearCell(p.first, p.second);
				//print();
			}
		}
		return;
	}
}

void board::printCounter()
//prints number times the recursive count function is called
{
	cout << "Number of recursive calls: " << counter << endl;
	calls.push_back(counter);
}

void board::printAverageAndTotalCalls()
// averages the total recursive count and prints it
{
	unsigned int numerator = 0;
	unsigned int denominator = (unsigned int) calls.size();
	
	for (int i = 0; i < (int)calls.size(); i++)
	{
		numerator += calls[i];
	}
	cout << "Average number of recursive calls: " << numerator/denominator << endl;
	cout << "Total number of recursive calls: " << numerator << endl;
}

bool board::isValid(int i, int j, int ch)
{
	return rows[i][ch] == false && columns[j][ch] == false && squares[squareNumber(i, j)][ch] == false;
}

int board::checkSameRow(int i, int j)
{
	int blank_cells = BoardSize - 1;
	vector<int> options(BoardSize, 0);
	for (int k = 0; k < BoardSize; k++)
	{
		if (k != j)
		{
			for (int ch = 0; ch < BoardSize; ch++)
			{
				if (isValid(i, j, ch))
				{
					if (!isBlank(i, k) || (isBlank(i, k) && !isValid(i, k, ch)))
						options[ch]++;
				}
			}
		}
	}
	for (int n = 0; n < BoardSize; n++)
	{
		if (options[n] == blank_cells)
			return n;
	}
	return -1;
}

int board::checkSameColumn(int i, int j)
{
	int blank_cells = BoardSize - 1;
	vector<int> options(BoardSize, 0);
	for (int k = 0; k < BoardSize; k++)
	{
		if (k != i)
		{
			for (int ch = 0; ch < BoardSize; ch++)
			{
				if (isValid(i, j, ch))
				{
					if (!isBlank(k, j) || (isBlank(k, j) && !isValid(k, j, ch)))
						options[ch]++;
				}
			}
		}
	}
	for (int n = 0; n < BoardSize; n++)
	{
		if (options[n] == blank_cells)
			return n;
	}
	return -1;
}

int board::checkSameSquare(int i, int j)
{
	vector<int> options(BoardSize, 0);
	int blank_cells = BoardSize - 1;
	switch(squareNumber(i, j))
	{
	case 0:
		for (int k = 0; k < 3; k++)
		{
			for (int m = 0; m < 3; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch) == true)
						{
							if ((isBlank(k, m) == false) || (isBlank(k, m) == true && isValid(k, m, ch) == false))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	case 1:
		for (int k = 0; k < 3; k++)
		{
			for (int m = 3; m < 6; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch) == true)
						{
							if ((isBlank(k, m) == false) || (isBlank(k, m) == true && isValid(k, m, ch) == false))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	case 2:
		for (int k = 0; k < 3; k++)
		{
			for (int m = 6; m < 9; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch) == true)
						{
							if ((isBlank(k, m) == false) || (isBlank(k, m) == true && isValid(k, m, ch) == false))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	case 3:
		for (int k = 3; k < 6; k++)
		{
			for (int m = 0; m < 3; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch) == true)
						{
							if ((isBlank(k, m) == false) || (isBlank(k, m) == true && isValid(k, m, ch) == false))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	case 4:
		for (int k = 3; k < 6; k++)
		{
			for (int m = 3; m < 6; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch) == true)
						{
							if ((isBlank(k, m) == false) || (isBlank(k, m) == true && isValid(k, m, ch) == false))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	case 5:
		for (int k = 3; k < 6; k++)
		{
			for (int m = 6; m < 9; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch) == true)
						{
							if ((isBlank(k, m) == false) || (isBlank(k, m) == true && isValid(k, m, ch) == false))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	case 6:
		for (int k = 6; k < 9; k++)
		{
			for (int m = 0; m < 3; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch))
						{
							if (!isBlank(k, m) || (isBlank(k, m) && !isValid(k, m, ch)))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	case 7:
		for (int k = 6; k < 9; k++)
		{
			for (int m = 3; m < 6; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch))
						{
							if (!isBlank(k, m) || (isBlank(k, m) == true && !isValid(k, m, ch)))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	case 8:
		for (int k = 6; k < 9; k++)
		{
			for (int m = 6; m < 9; m++)
			{
				if (k != i || m != j)
				{
					for (int ch = 0; ch < BoardSize; ch++)
					{
						if (isValid(i, j, ch))
						{
							if (!isBlank(k, m) || (isBlank(k, m) && !isValid(k, m, ch)))
								options[ch]++;
						}
					}
				}
			}
		}
		break;
	}
	for (int n = 0; n < BoardSize; n++)
	{
		if (options[n] == blank_cells)
			return n;
	}
	return -1;
}
