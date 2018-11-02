import nltk
from nltk.corpus import stopwords

lemmatizer = nltk.WordNetLemmatizer()
stopwords = stopwords.words('english')

def leaves(tree,grammar):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter = lambda t: t.label()==grammar):
        yield subtree.leaves()

def normalise(word):
    """Normalises words to lowercase and lemmatizes it."""
    word = word.lower()
    word = lemmatizer.lemmatize(word)
    return word

def get_terms(tree,grammar):
    for leaf in leaves(tree,grammar):
        term = [ normalise(w) for w,t in leaf if bool(2 <= len(w) <= 40) ]	
        yield term		
		
def get_np(text):
	re = r'(?:\w+(?:-\w+)*)|(?:[-+*()$]*(?:\d.?)*\d+\%?)|(?:[.,;:"\'?])'
	grammar = r"""
	NNB:{<JJ.*|VBG|NN.*>*<NN.*>}
	JJN:{<DT><JJ>}
	NP:{<DT>?(<NN.*><IN>?)*<NN.*>}
	{<NNB>}
	"""
	tokens = nltk.regexp_tokenize(text, re)
	cp = nltk.RegexpParser(grammar)	
	t = cp.parse(nltk.tag.pos_tag(tokens))
	#print t
	global tree
	tree = cp.parse(t)

	terms = get_terms(tree,'NP')	
	np = []
	for term in terms:
		#print term
		if term != [] and term[0] in stopwords:	#remove the first stopword
			term.pop(0)
		np.append(str(' '.join(term)))
		
	terms = get_terms(tree,'JJN')
	for term in terms:
		np.append(str(' '.join(term)))		
	while '' in np:
		np.remove('')
	return np
