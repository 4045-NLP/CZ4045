from collections import Counter
import json
import noun_phrase_detector as npd
import operator
from nltk.corpus import stopwords

stopwords = stopwords.words('english')

def read_data(file_name):
	data = []
	with open(file_name, 'r') as f:
		for line in f:
			data.append(json.loads(line))
	return data

def sortByValue(dict):	#Sort dictionary by value
    sortedlist = sorted(dict.items(), key=operator.itemgetter(1))
    sortedlist.reverse()
    return sortedlist	
	
def extract_np(data):
	c = Counter()
	for i in range(len(data)):
		c.update(Counter(npd.get_np(data[i]["reviewText"])))
		c.update(Counter(npd.get_np(data[i]["summary"])))
		print "extracting np...", i
	all_np = dict(c)
	if '' in all_np:
		all_np.pop('')
	for w in stopwords:	#Remove single stopword
		if w in all_np:
			all_np.pop(w)
	
	return all_np	

#def extract_asin(data): 
#	c = Counter()
#	for i in range(len(data)):
#		c.update(Counter(data[i]["asin"]))
#	asin = dict(c)
#	return asin

def get_data_p(data, product_asin):
	data_p = []	#part of the dataset
	for i in range(len(data)):
		if data[i]["asin"]==product_asin:
			data_p.append(data[i])
	return data_p
	
def top_fq_np(n, all_np):
	total_no_np = sum(all_np.values())
	sorted_np = sortByValue(all_np)[:n]	#a list of tuples
	np_fq = [None]*n
	for i in range(n):
		np_fq[i] = list(sorted_np[i])
		np_fq[i][1] = np_fq[i][1] * 1.0 / total_no_np	#frequency
	return np_fq	#a list of lists

def get_fq(np, all_np):
	total_no_np = sum(all_np.values())
	f = all_np[np] * 1.0 / total_no_np
	return f
	
def get_rp_list(p_np, all_np): #Representative noun phrase
	rp_dict = {}
	for np in p_np.keys():
		fq_all = get_fq(np, all_np)	#The frequency of the noun phrase amoung all reviews
		fq_p = get_fq(np, p_np)	#The frequency of the noun phrase in this product’s reviews
		rp = fq_p * (fq_p -fq_all) #Representativity
		rp_dict[np] = rp
	rp_list = sortByValue(rp_dict)[:10]	
	return rp_list	#a list of tuples
	
'''
Q1: List the top-20 most frequent noun phrases
'''
#data = read_data("SampleReview.json")
data = read_data("CellPhoneReview.json")
all_np = extract_np(data)
top_20_np = top_fq_np(20, all_np)

with open('all_np.txt', 'w') as file:
	file.write(json.dumps(all_np))

with open("top-20 most frequent noun phrases.txt", 'w') as file:
	for i in top_20_np:
		value = ', '.join(map(str, i))
		file.write(value + '\n')

'''
Q2: Choose any 3 popular products which has the largest number of reviews, and summarize the reviews of each product by using 10 representative noun phrases.
'''

#asin = ["120401325X","3998899561","6073894996"]	#"SampleReview.json"
asin = ["B005SUHPO6","B0042FV2SI","B008OHNZI0"]	#"CellPhoneReview.json"

rp_list1 = get_rp_list(extract_np(get_data_p(data, asin[0])), all_np)
rp_list2 = get_rp_list(extract_np(get_data_p(data, asin[1])), all_np)
rp_list3 = get_rp_list(extract_np(get_data_p(data, asin[2])), all_np)

with open("3 popular products.txt","w") as file:
	file.write("Product " + asin[0] + ': \n')
	for i in rp_list1:
		value = ', '.join(map(str, i))
		file.write(value + '\n')
	file.write("\nProduct " + asin[1] + ': \n')
	for i in rp_list2:
		value = ', '.join(map(str, i))
		file.write(value + '\n')
	file.write("\nProduct " + asin[2] + ': \n')
	for i in rp_list3:
		value = ', '.join(map(str, i))
		file.write(value + '\n')
