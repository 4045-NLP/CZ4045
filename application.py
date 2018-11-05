#import
import json
import nltk
import string
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#lists to hold the result
result=[]
judge=[]
error=[]
content=[]
good_id=[]
#set up sentiment analyser
sid = SentimentIntensityAnalyzer()

#make the judge score mapped to a range of (1,5)
def score_translate(old_value,old_min,old_max,new_min,new_max):
	OldRange=(old_max-old_min)  
	NewRange=(new_max-new_min)  
	NewValue = (((old_value-old_min)*NewRange)/OldRange)+new_min
	return NewValue

#data process
with open('CellPhoneReview.json') as datafile:
	#for each review text do:
	for line in datafile:
		data = json.loads(line)
		text=data["reviewText"]
		summary=data["summary"]
		overall_score=data["overall"]
		comment_id=data["reviewerID"]
		goodid=data["asin"]
		#tokenize the review text
		sens=nltk.sent_tokenize(text)
		#inite the judge score to be 0
		score=0
		for sentence in sens:
			ss=sid.polarity_scores(sentence)
			score=score+ss["compound"]
		sss=sid.polarity_scores(summary)
		#allocate different weights to review text and summmary
		score=0.2*score+0.8*sss["compound"]
		if ((score>1 and overall_score<2.5) or (score<-1 and overall_score>2.5)):
			score=score_translate(score,-3,3,1,5)
			error.append(comment_id)
			result.append(score)
			judge.append(overall_score)
			content.append(text)
			good_id.append(goodid)
			
print("done")
#show result
print("There are " ,len(error), "comflix reviews")
print()
print()
for x in range(len(error)):
	print("reviewer id:",error[x])
	print("product id",good_id[x])
	print("judge result:",result[x])
	print("overall score given by reviewer:",judge[x])
	print("review text:",content[x])





