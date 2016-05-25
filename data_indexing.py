from whoosh.fields import SchemaClass,Schema, TEXT, KEYWORD, ID, STORED
import os,os.path
from whoosh import index
from collections import deque
import urllib.request
from bs4 import BeautifulSoup,Comment
import re
import docx
import docx2txt
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
def remove_non_ascii(text):
	return ''.join([i if ord(i) < 128 else ' ' for i in text])
def from_doc_func(url):
	download_url = url
	new_f = urllib.request.urlopen(download_url)
	length_downloadfile = new_f.headers['Content-length']
	y = int(length_downloadfile)
	if y > 30000:
		return "sravan"
	ran_file = urllib.request.URLopener()
	ran_file.retrieve(download_url,"rand.doc")
	text = docx2txt.process("rand.doc")
	value = remove_non_ascii(text)
	value = value.replace('\n',' ')
	value = re.sub('_+',' ',value)
	value = value.replace('\t',' ')
	#value = value.replace('/',' ')
	value = value.replace('\n',' ')
	value = re.sub(' +',' ',value)
	#print(doc)
	#print(value)
	return value
def from_docx_func(url):
	download_url = url
	new_f = urllib.request.urlopen(download_url)
	length_downloadfile = new_f.headers['Content-length']
	y = int(length_downloadfile)
	if y > 50000:
		return "sravan"
	ran_file = urllib.request.URLopener()
	ran_file.retrieve(download_url,"rand.docx")
	text = docx2txt.process("rand.docx")
	value = remove_non_ascii(text)
	value = value.replace('\n',' ')
	value = re.sub('_+',' ',value)
	value = value.replace('\t',' ')
	#value = value.replace('/',' ')
	value = value.replace('\n',' ')
	value = re.sub(' +',' ',value)
	#print("docs--------------------------------")
	#print(value)
	return value
def pdf_func(url):
	f = open('temp.txt','w')
	download_url = "http://shilloi.iitg.ernet.in/~establishment/Forms/pdf/book-SenateHall.pdf"
	new_f = urllib.request.urlopen(download_url)
	length_downloadfile = new_f.headers['Content-length']
	y = int(length_downloadfile)
	if y > 30000:
		return "sravan"
	ran_file = urllib.request.URLopener()
	ran_file.retrieve(download_url,"rand.pdf")
	fp = open('rand.pdf', 'rb')
	parser = PDFParser(fp)
	doc = PDFDocument()
	parser.set_document(doc)
	doc.set_parser(parser)
	doc.initialize('')
	rsrcmgr = PDFResourceManager()
	laparams = LAParams()
	device = PDFPageAggregator(rsrcmgr, laparams=laparams)
	interpreter = PDFPageInterpreter(rsrcmgr, device)
	for page in doc.get_pages():
	    interpreter.process_page(page)
	    layout = device.get_result()
	    for lt_obj in layout:
	        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
	        	text = lt_obj.get_text()
	        	f.write(text)
	fp.close()
	os.remove('rand.pdf')
	f.close()
	f = open('temp.txt','r')
	data = f.read()
	f.close()
	value = remove_non_ascii(data)
	value = value.replace('\n',' ')
	value = re.sub('_+',' ',value)
	value = value.replace('\t',' ')
	#value = value.replace('/',' ')
	value = value.replace('\n',' ')
	value = re.sub(' +',' ',value)
	#print("docs--------------------------------")
	#print(value)
	return value
def func(url):
	#print("sravan")
	html = urllib.request.urlopen(url)
	soup = BeautifulSoup(html)
	#print("sravan")
	#doc_typer = soup.contents[0]
	#doc_typer.extract()
	comments = soup.findAll(text=lambda text:isinstance(text,Comment))
	for comment in comments:
		comment.extract()
	scripts = soup.findAll('script')
	for scri in scripts:
		scri.extract()
	doc_type = soup.findAll('!DOCTYPE')
	for scri in doc_type:
		scri.extract()
	linked = soup.findAll('link')
	for lin in linked:
		lin.extract()
	meta = soup.findAll('meta')
	for lin in meta:
		lin.extract()
	texts = soup.find_all(text=True)
	for t in texts:
		newtext = t.replace("&nbsp;","")
		t.replace_with(newtext)
	value = soup.get_text()	
	value = value.replace('\n',' ')
	space = soup.findAll(text="&nbsp;")
	for lin in space:
		lin.extract()
	value = value.replace('\t',' ')
	value = re.sub(' +',' ',value)
	#sravan = remove(value)
	#value = value.replace('|','')

	#print(value)
	return value
	#value = value.replace(unichr(160),"")
	#value = value.replace('&nbsp;','')
#schema = Schema(title=TEXT(stored=True),url=TEXT,content=TEXT)
class schema(SchemaClass):
	title = TEXT(stored=True)
	url = TEXT(stored=True)
	toke_no = ID(stored=True)
	content = TEXT(stored=True)
	last_modify = TEXT(stored=True)

if not os.path.exists("new_indexdir"):
	os.mkdir("new_indexdir")
ix = index.create_in("new_indexdir",schema)
ix = index.open_dir("new_indexdir")
new_exceptions = open("exception.txt","w")
exception=0
writer = ix.writer()
#q.append(url)
q = deque([])
fn = open("crawled.txt","r")
data = fn.read()
for line in data.split('\n'):
	q.append(line)
#q.append("http://shilloi.iitg.ernet.in/~er/")
length = len(q)
for i in range(length):
	flag=0
	try:
		print( i)
		if len(q) > 0:
			url = q.popleft()
		print("sravan")
		r = urllib.request.urlopen(url)
		extension = url[-4:]
		extension_x = url[-5:]
		if extension == ".pdf":
			content_co = pdf_func(url)
			if content_co == "sravan":
				flag = 1
		elif extension_x == ".docx":
			content_co = from_docx_func(url)
			if content_co == "sravan":
				flag = 1
		elif extension == ".doc":
			content_co = from_doc_func(url)
			if content_co == "sravan":
				flag = 1
		elif extension == ".zip" or extension == ".iso" or extension ==".exe" or extension == ".txt" or extension ==".jpg" or extension == ".gif":
			p = url.split('/')
			s = p[-1]
			t = s.split('.')
			w = t[0]
			title_co = w
			content_co = w
			ziper = 1
		else:
			content_co = func(url)
			#soup = BeautifulSoup(r)
			r = urllib.request.urlopen(url)
			if r.headers['last-modified'] is not None:
				last_modified = r.headers['last-modified'].lower()
			else:
				last_modified = "sravan"
		#print("Last Called")
		#content_co = func(url)
		r = urllib.request.urlopen(url)
		length_downloadfile = r.headers['Content-Length']
		#print("sravan")
		if length_downloadfile is not None:
			y = int(length_downloadfile)
		else:
			y = 20000
		#print("sravan")
		if y < 30000:
			#print("sravan")
			soup = BeautifulSoup(r)
			#print("sravan")
			title_co = soup.find("title")
			if title_co is not None:
				if title_co.string is not None:
					title_co = title_co.string
					title_co = title_co.lower()
				elif ziper == 1:
					title_co=content_co
				else:
					title_co = "sravan"
			title_co = str(title_co)
			token_no = 0
			if flag == 0:
				print(url)
				writer.add_document(title=title_co,url = url,content=content_co.lower(),last_modify=last_modified)
		else:
			print("large Size")
	except:
		fghj="sravan"
		print("India lost the Semifinal against Westindies")
			#value = re.sub(' +',' ',value)
		exception += 1
		#new_exceptions.write(exception)

		new_exceptions.write("---------------------|------------------------")
		'''new_exceptions("----------------------|------------------------")
		new_exceptions("----------------------|------------------------")
		new_exceptions("----------------------|------------------------")
		new_exceptions("----------------------|------------------------")
		new_exceptions("----------------------|------------------------")	'''
writer.commit()









