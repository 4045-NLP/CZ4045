from collections import Counter
import json
import noun_phrase_detector as npd
import operator

def read_data(file_name):
	print "reading line..."
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
		print "extract np...", i
	all_np = dict(c)
	return all_np	

#def extract_asin(data): 
#	c = Counter()
#	for i in range(len(data)):
#		c.update(Counter(data[i]["asin"]))
#	asin = dict(c)
#	return asin

def get_data_p(data, product_asin):
	print "reading data..."
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

def np_fq_among_all(np, all_np):
	total_no_np = sum(all_np.values())
	f = all_np[np] * 1.0 / total_no_np
	return f
	
def get_rp_list(top_10_np, all_np):	#representative noun phrase
	rp_list = [None]*10 #[np, frequency in this product, frequency amoung all]
	for i in range(10):
		f = np_fq_among_all(top_10_np[i][0],all_np)
		rp_list[i] = [top_10_np[i][0], top_10_np[i][1],f]
	return rp_list
	
'''
Q1: List the top-20 most frequent noun phrases
'''
#data = read_data("SampleReview.json")
data = read_data("CellPhoneReview.json")
all_np = extract_np(data)
top_20_np = top_fq_np(20, all_np)

with open("top-20 most frequent noun phrases.txt", 'w') as file:
	for i in top_20_np:
		value = ', '.join(map(str, i))
		file.write(value + '\n')

'''
Q2: Choose 3 popular products
'''

#asin = ["120401325X","3998899561","6073894996"]
asin = ["B005SUHPO6","B0042FV2SI","B008OHNZI0"]
p1 = get_rp_list(top_fq_np(10, extract_np(get_data_p(data, asin[0]))),all_np)
p2 = get_rp_list(top_fq_np(10, extract_np(get_data_p(data, asin[1]))),all_np)
p3 = get_rp_list(top_fq_np(10, extract_np(get_data_p(data, asin[2]))),all_np)

with open("3 popular products.txt","w") as file:
	file.write("Product " + asin[0] + ': \n')
	for i in p1:
		file.write(str(i) + '\n')
	file.write("Product " + asin[1] + ': \n')
	for i in p2:
		file.write(str(i) + '\n')
	file.write("Product " + asin[2] + ': \n')
	for i in p3:
		file.write(str(i) + '\n')
