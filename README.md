University of Dundee
Programming Languages for Data Engineering

Student: Dhanashree Nangre(2544403)
Python assignment: 
	For this assignment, we were supposed to read a file with names of phrases and generate three-letter abbreviations for each while satisfying certain rules. I have used different things in code, created multiple functions and used pandas to simplify the code for me, Here I’ll explain the flow of code.
 
The first code asks the user to provide details of the input file through the command prompt.
After that, a data frame will store details for abbreviations like name, abbreviation and score of that abbreviation.
The code will open the input file and read a line of line 
In the for loop, at first, the code will collect possible abbreviations for the phrase, making sure 
	not to include non-alphanumeric values.
	The first letter of the abbreviation is the first letter of the phrase
	Make sure the same abbreviation is not repeated.
After that code will check the score for each abbreviation. For the score, we are already collecting details like the starting index of the word, and the index of letters.
After calculating the score for each letter by
	Checking if the letter is at the beginning of the word, then 0
	If it is the end of the word then 5 and if it’s E at the end then 20
	Else-based addition of index in word and value from the file and then that abbreviation. 
We are storing everything in a data frame.
Then deleting duplicate abbreviations which are available in other words as well.
Getting rows with a minimum score for abbreviations and merging those
Storing results in CSV and text files.

Sample input file:
Trees.py

Alder
Crab Apple
Common Ash
Silver Birch
Downy Birch
European Beech
Box


Sample Output file:
Nangre_trees_abbrevs.txt

Alder
Crab Apple CBP
Common Ash CAS
Silver Birch SVB
Downy Birch DYB
European Beech EBH
Box BOX



