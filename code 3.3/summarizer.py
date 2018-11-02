import json
import os
import numpy
import noun_phrase_detector as npd

def read_data(file_name):
	data = []
	n = 0 #line counter
	with open(file_name, 'r') as f:
		for line in f:
			data.append(json.loads(line))
			n += 1
			print "reading line...", n
	return data

def get_asin_list(data): 
	asin = []
	uniq_asin = []
	for i in range(len(data)):
		asin.append(data[i]["asin"])
	for item in asin:
		if item not in uniq_asin:
			uniq_asin.append(item)
	sorted_asin = []
	for item in uniq_asin:
		sorted_asin.append([asin.count(item),item])
	sorted_asin = sorted(uniq_asin, reverse=True)
	return sorted_asin
	
def extract_np(data):
	np = []
	for i in range(len(data)):
		np.append(npd.get_np(data[i]["reviewText"]))
		np.append(npd.get_np(data[i]["summary"]))
		print "appending...", i
	np_flat_list = [item for sublist in np for item in sublist] #all np
	total_no_np = len(np_flat_list)
	np_list = [] #without duplicates
	for term in np_flat_list:
		if term not in np_list:
			np_list.append(term)
	result_list = []
	for term in np_list:
			f = np_flat_list.count(term) * 1.0 / total_no_np	#frequency
			result_list.append([f,term])
	result_list = sorted(result_list, reverse=True)
	return np_flat_list, result_list

def np_fq_among_all(np,all_np):
	f = all_np.count(np) * 1.0 / len(all_np)
	return f
	
def top_10_np(data, product_asin):
	data_p = []	#part of the dataset
	for i in range(len(data)):
		if data[i]["asin"]==product_asin:
			data_p.append(data[i])
	all_np, result_list = extract_np(data_p)
	return result_list[:10]
	
def get_rp_list(top_10,all_np):	#representative noun phrase
	rp_list = [None]*10 #[np, frequency in this product, frequency amoung all]
	for i in range(10):
		f = np_fq_among_all(top_10[i][1],all_np)
		rp_list[i] = [top_10[i][1],top_10[i][0],f]
	return rp_list
	
'''
Q1: List the top-20 most frequent noun phrases
'''
data = read_data("CellPhoneReview.json")
all_np, result_list = extract_np(data)

with open("top-20 most frequent noun phrases.txt", 'w') as file:
	for i in range(20):
		file.write(result_list[i][1] + '\n')
		
print numpy.array(result_list[:20])
'''
Q2: Choose 3 popular products
'''
asin = ["B005SUHPO6","B0042FV2SI","B008OHNZI0"]
p1 = get_rp_list(top_10_np(data, asin[0]),all_np)
p2 = get_rp_list(top_10_np(data, asin[1]),all_np)
p3 = get_rp_list(top_10_np(data, asin[2]),all_np)
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

