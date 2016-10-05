import requests, io, re, urllib
import cPickle as pickle
from os import listdir
from os.path import isfile, join

philosophers_dir = './philosophers'
content_dir = 'content'

def file_dir():
	return philosophers_dir + '/' + content_dir

def lists():
	# create a set which contains words we want to remove (including philosphers with missing links)
	remove_words = set([])
	f = io.open(philosophers_dir + '/remove_words.txt','r',encoding='utf-8')
	for line in f:
		remove_words.add(line.replace('\n',''))

	pattern = r'\[\[([^|\[\]]*)\|?[^|\[\]]*\]\]';

	# open file
	aest_file = io.open(philosophers_dir + '/aestheticians.txt','r',encoding='utf-8')
	# match the regex to find all links
	aestheticians = re.findall(pattern, aest_file.read())
	# use remove_words set to remove all non-philosphers out of the set
	aestheticians = list(set(aestheticians).difference(remove_words))

	# the following the same but compressed into two lines
	epistemologists = re.findall(pattern, io.open(philosophers_dir + '/epistemologists.txt','r',encoding='utf-8').read())
	epistemologists = list(set(epistemologists).difference(remove_words))

	ethicists = re.findall(pattern, io.open(philosophers_dir + '/ethicists.txt','r',encoding='utf-8').read())
	ethicists = list(set(ethicists).difference(remove_words))

	logicians = re.findall(pattern, io.open(philosophers_dir + '/logicians.txt','r',encoding='utf-8').read())
	logicians = list(set(logicians).difference(remove_words))

	metaphysicians = re.findall(pattern, io.open(philosophers_dir + '/metaphysicians.txt','r',encoding='utf-8').read())
	metaphysicians = list(set(metaphysicians).difference(remove_words))

	social_politicals = re.findall(pattern, io.open(philosophers_dir + '/social_politicals.txt','r',encoding='utf-8').read())
	social_politicals = list(set(social_politicals).difference(remove_words))

	# create list of lists as this may be useful later
	return (aestheticians, epistemologists, ethicists, logicians, metaphysicians, social_politicals)

def combined():
	phils_matrix = lists()
	# create a list which contains all the philosphers (including repeats)
	combined_philosphers = []
	for lst in phils_matrix:
		combined_philosphers += lst

	# Convert to a set to remove duplicate values
	unique_philosphers = list(set(combined_philosphers))

	return unique_philosphers

def get_wikicontent(philosopher):
	wikipedia_root_api_url = "http://en.wikipedia.org/w/api.php"

	payload = {
		'action': 'query',
		'format': 'json',
		'prop': 'revisions',
		'rvprop': 'content',
		'titles': philosopher
	}

	response = requests.get(wikipedia_root_api_url, params=payload)
	wikijson = response.json()

	if 'pages' not in wikijson['query']:
		return None

	# grab the id of the wiki page  
	page_id = wikijson['query']['pages'].keys()[0]
	# check to see if some content is contained in the json
	content = wikijson['query']['pages'][page_id]

	# if the data is missing the id is -1
	if page_id == '-1':
		print 'ERROR: missing %s' % wikijson['query']['pages']['-1']['title']
		return None
	# if the content exists then return
	if 'revisions' in content:
		return content['revisions'][0]['*']
	else:
		print 'UNHANDLED CASE: id = %s ' % page_id

def save_to_file(file_name, content):
	with io.open(file_dir() + '/' + file_name + '.pickle', 'wb') as f:
		pickle.dump(content, f)
		f.close()

def file_dump():
	for philosopher in combined():
		if 'Categor' in philosopher:
			continue
		wikicontent = get_wikicontent(philosopher)
		if wikicontent:
			save_to_file(philosopher, (philosopher, wikicontent))

def file_load():
	directory = file_dir()
	content = []
	for file in [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]:
		if './philosophers/content/.DS_Store' in file:
			continue
		with open(file, 'rb') as f:
			try:
				(phil, wikicontent) = pickle.load(f)
				content.append((phil,wikicontent))
				f.close()
			except Exception as e:
				print e, file
	return content
