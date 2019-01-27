//This is the source file that contains the main functions and definitions

#include "Board.h"

using namespace std;

int main()
{
	ifstream fin;

	// Read the sample puzzle from the file
    string fileName;
    cout << "Enter filename of puzzle: " << endl;
	cin >> fileName;
	fin.open(fileName.c_str());
	if (!fin)
	{
		cerr << "Cannot open " << fileName << endl;
		exit(1);
	}

	try
	{
		board b1(SquareSize); //initializes board

		while (fin && fin.peek() != 'Z')
		
		{
			b1.initialize(fin);
			b1.print();
			b1.printConflicts();
			b1.solve();
			b1.printCounter();
		}
		b1.printAverageAndTotalCalls();
	}

	catch  (indexRangeError &ex)
   // range error
	{
		cout << ex.what() << endl;
		exit(1);
	}
}
