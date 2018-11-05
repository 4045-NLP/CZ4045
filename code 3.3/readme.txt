The code for assignment part 3.3 Development of a Noun Phrase Summarizer is written under Python 2.7.
Following is the third-party library used:
1. NLTK: https://www.nltk.org/install.html

Besides, nltk data may need downloading by:
>>> import nltk
>>> nltk.download('stopwords')
 
Installation guide:
1. Put files "noun_phrase_detector.py" and "summarizer.py" together with the dataset(e.g., "CellPhoneReview.json").

How to use it:
1. If you are running it for "CellPhoneReview.json", nothing needs to change, just run "summarizer.py"
2. If you want edit it:
	in line 77: data = read_data("CellPhoneReview.json") #Put the dataset file name here
	in line 92: asin = ["B005SUHPO6","B0042FV2SI","B008OHNZI0"]	#The items in the list can be changed to any 3 of asin in the dataset.	
3. Two txt files "top-20 most frequent noun phrases.txt" and "3 popular products.txt" will be generated after running the code.
4. To make use "noun_phrase_detector.py", just run it:
	>>> get_np("Input your sentence here.")
	It will detect the noun phrases in the sentence and return a list of string. However, some stopwords like pronouns have been removed. 
	key in 
	>>> tree
	then you can see all the noun phrases in the sentence.

Output:
1. "top-20 most frequent noun phrases.txt" stores the top-20 most frequent noun phrases in the dataset "CellPhoneReview.json", together with their frequency in descending order.
2. "3 popular products.txt" stores the product's asin, followed by its 10 representative noun phrase, together with their representivity in descending order.
