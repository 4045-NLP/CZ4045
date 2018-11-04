import nltk

stopwords = ['don','doesn','wounldn','shouldn','\'t','shall',
             'what','when','where','why','which','how']  #np can not start with these words 
			
def get_terms(tree,grammar):
    subtrees = []
    for s in tree:
        if type(s) == nltk.tree.Tree and s.label() == grammar:
            subtrees.append(s)
    terms = []
    for s in subtrees:
        if s.leaves()[0][0].lower() in stopwords:
            continue
        term = [w.lower() for w,t in s.leaves()]
        terms.append(term)
    return terms
		
def get_np(text):
	re = r'(?:\w+(?:-\w+)*)|(?:[-+*()$]*(?:\d.?)*\d+\%?)|(?:\'\w)|(?:[.,;:"?!\\])'
	grammar = r"""
        IF:{<TO><VB>}   #Infinitive
        VP:{<MD>?<VB|VBD|VBP|VBZ><VBG|VBN|RB.*>*<IN|RP>?}
	MOD:{<JJ.*|VBG|CD>}	#Modifier
	NNB:{(<MOD|NN.*>+<IN|POS>?)*<NN.*>}	#Noun + noun
	JJN:{<DT><MOD>}	#Adjectives as Nouns
	PP:{<IN><N.*>}  #Prepositional phrase
	NP:{<RB.*>?<DT|PRP\$>?<N.*><PP|IF>*}
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
		
	return np_list
