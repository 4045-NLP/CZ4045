import nltk

stopwords = ['i','don','doesn','didn','wounldn','shouldn','\'t','shall']  #np can not start with these words 

def change_tag(tokens, tagged_t):
	for w in tokens:
		if w == 'i':
			tagged_t[tokens.index(w)] = (w, 'PRP')
		if w in ['don', 'doesn','didn']:
			tagged_t[tokens.index(w)] = (w, 'VB')
		if w in ['wouldn', 'shouldn','couldn']:
			tagged_t[tokens.index(w)] = (w, 'MD')
		if w == '\'t':
			tagged_t[tokens.index(w)] = (w, 'POS')
	return tagged_t
	
def get_terms(tree,grammar):
    subtrees = []
    for s in tree:
        if type(s) == nltk.tree.Tree and s.label() == grammar:
            subtrees.append(s)
    terms = []
    for s in subtrees:
        if s.leaves()[0][0] in stopwords:
            continue
        term = [w for w,t in s.leaves()]
        terms.append(term)
    return terms
		
def get_np(text):
        text = text.lower()
        re = r'(?:\w+(?:-\w+)*)|(?:[-+*()$]*(?:\d.?)*\d+\%?)|(?:\'\w)|(?:[.,;:"?!\\])'
        grammar = r"""        
        IF:{<TO><VB>}   #Infinitive
        VP:{<MD>?<VB|VBD|VBP|VBZ><VBG|VBN|RB.*>*<IN|RP>?}
	MOD:{<JJ.*|VBG|CD>}	#Modifier
	NNB:{(<MOD|N.*>+<IN|POS|CC>?)*<N.*>}	#Noun + noun
	JJN:{<DT><MOD>}	#Adjectives as Nouns
	PP:{<IN><N.*>}  #Prepositional phrase
	NP:{<RB.*>?<DT|PRP\$>?<N.*><PP|IF|AC>*}
	{<NNB>}
	{<JJN>}
	{<PRP>}
	AC:{<W.*><N.*>*<VP><MOD|RB|N.*>*}	#Adjective clauses
	"""
        cp = nltk.RegexpParser(grammar)
        global tokens
        tokens = nltk.regexp_tokenize(text, re)	#a list of words
        tagged_t = nltk.tag.pos_tag(tokens) #a list of tuples(word, tag)
        for w in tokens:	#check and change tags
                if w in stopwords:
                        tagged_t = change_tag(tokens, tagged_t)
                        break
        t = cp.parse(tagged_t)
        #print t
        global tree
        tree = cp.parse(t)

        terms = get_terms(tree,'NP')
        np_list = []
        for term in terms:
                np_list.append(str(' '.join(term)))

        return np_list
