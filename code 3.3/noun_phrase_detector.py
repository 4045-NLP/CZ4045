import nltk
from nltk.corpus import stopwords

lemmatizer = nltk.WordNetLemmatizer()
stopwords = stopwords.words('english')

def leaves(tree,grammar):
    """Finds NP (nounp_listhrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()==grammar):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and lemmatizes it."""
    word = word.lower()
    word = lemmatizer.lemmatize(word)
    return word

def get_terms(tree,grammar):
    for leaf in leaves(tree,grammar):
        term = [ normalise(w) for w,t in leaf ]	
        yield term		
		
def get_np(text):
	re = r'(?:\w+[nN]\'[tT])|(?:\w+(?:-\w+)*)|(?:[-+*()$]*(?:\d.?)*\d+\%?)|(?:\'[sS])|(?:[.,;:"?!])'
	grammar = r"""
	MOD:{<JJ.*|VBG|CD>}	#Modifier
	NNB:{<MOD|NN.*>*<NN.*>}	#Noun + noun
	JJN:{<DT><MOD>}	#Adjectives as Nouns
	NP:{<RB.*>?<DT|PRP\$>?(<NN.*><IN|POS>?)*<NN.*>}
	{<PRP>}
	{<NNB>}
	{<JJN>}
	"""
	tokens = nltk.regexp_tokenize(text, re)
	cp = nltk.RegexpParser(grammar)	
	t = cp.parse(nltk.tag.pos_tag(tokens))
	#print t
	global tree
	tree = cp.parse(t)

	terms = get_terms(tree,'NP')	
	np_list = []
	for term in terms:		
		np_list.append(str(' '.join(term)))
	while '' in np_list:
		np_list.remove('')
		
	return np_list
