from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
import re
from whoosh import qparser
from whoosh.spelling import ListCorrector,MultiCorrector
def Search_text(val):
	ix = index.open_dir("new_indexdir")
	s = ix.searcher()
	name = []
	'''qp = QueryParser("content", schema=ix.schema)
	q = qp.parse(val)'''
	og = qparser.OrGroup.factory(0.9)
	mparser = MultifieldParser(["title","content"],schema=ix.schema,group=og)
	q = mparser.parse(val)
	results = s.search(q,limit=None)
	#print(len(results))
	elements = []
	if len(results) < 10:
		listi = re.sub("[^\w]"," ",val).split()
		y = len(listi)
		if y == 1:
			val = listi[0]
			mparsere = MultifieldParser(["title","content"],schema=ix.schema)
			q_new = mparsere.parse(val)
			resul = s.search(q_new,limit=10)
			corrector = s.corrector("content")
			correct = corrector.suggest(val,limit=3,maxdist=2,prefix=0)
			len_corrected = len(correct)
			search_no = 0
			for g in range(len_corrected):
				mparsere = MultifieldParser(["title","content"],schema=ix.schema)
				q_new = mparsere.parse(correct[g])
				resul = s.search(q_new,limit=10)
				string = listi[0]
				if(len(resul)>search_no):
					string = correct[g]
					search_no = len(resul)
		else:
			for i in range(y):
				elements.append([])
				#print(listi[i])
				val = listi[i]
				mparsere = MultifieldParser(["title","content"],schema=ix.schema)
				q_new = mparsere.parse(listi[i])
				resul = s.search(q_new,limit=10)
				if len(resul) > -1:
					corrector = s.corrector("content")
					correct = corrector.suggest(val,limit=3,maxdist=2,prefix=0)
					len_corrected = len(correct)
					for g in range(len_corrected):
						elements[i].append(correct[g])
			new_list = []
			links_url = []
			for i in range(y):
				one_more = len(elements[i])
				links_url.append([])
				for j in range(one_more):
					new_parser = MultifieldParser(["title","content"],schema=ix.schema)
					new_q = new_parser.parse(elements[i][j])
					resuls = s.search(new_q,limit=None)
					len_resuls = len(resuls)
					links_url[i].append([])
					for k in range(len_resuls):
						links_url[i][j].append(resuls[k]['url'])
					#links_url[i].append(resuls[]['title'])
			#for i in range(y):
			for i in range(y):
				length = len(links_url[i])
				for j in range(length):
					for k in range(i+1,y):
						one_more_length = len(links_url[k])
						for e in range(one_more_length):
							p = set(links_url[i][j])&set(links_url[k][e])
							if len(p) > 0:
								listi[i] = elements[i][j]
								listi[k] = elements[k][e]

			#print(links_url[0][0][0])		
			string = ' '.join(listi)
		print("Did You Mean:"+" "+string)
	for i in range(len(results)):
		print(results[i]['title'])
		print(results[i]['url'])
		value = results[i].highlights("content")
		value = re.sub(r'\W+',' ',value)
		value = re.sub('class',' ',value)
		value = re.sub('match',' ',value)
		value = re.sub('term0',' ',value)
		value = re.sub(' +',' ',value)
		print(value)
	s.close()

var = input("Enter the text to be searched:")
var = var.lower()
Search_text(var)
