import urllib.request
import json
import time

last_search=-1
def control_pressure():
	global last_search
	interval=10
	t = time.time()
	if t - last_search < interval:
		# print(f"sleeping {interval+last_search-t}")
		time.sleep(interval + last_search - t)
	last_search = time.time()

def search_repos(stars, size = None, page = None):
	control_pressure()
	url = f"https://api.github.com/search/repositories?per_page=100&q=language:scala+stars:{stars}"
	if size:
		url = url + f"+size:{size}"
	if page:
		url = url + f"&page={page}"
	j = urllib.request.urlopen(url).read()
	with open(f"json/{stars}_{size}_{page}", "w") as f:
		f.write(j.decode("utf-8"))
	return json.loads(j)

def print_repos(j):
	for item in j["items"]:
		print(f"{item['stargazers_count']} {item['size']} {item['html_url']}")


params = [
	('60..132', None),
	('40..59', None),
	('30..39', None),
	('22..29', None),
	('17..21', None),
	('14..16', None),
	('12..13', None),
	('10..11', None),
	('9', None),
	('8', None),
	('7', None),
	('6', '<100'),
	('6', '>=100'),
	('5', '<100'),
	('5', '>=100'),
	('4', '<100'),
	('4', '100..1000'),
	('4', '>1000'),
	('3', '<80'),
	('3', '80..169'),
	('3', '170..999'),
	('3', '>1000'),
	('2', '<20'),
	('2', '20..79'),
	('2', '80..129'),
	('2', '130..229'),
	('2', '230..999'),
	('2', '1000..2999'),
	('2', '>3000'),
	('1', '<5'),
	('1', '5..8'),
	('1', '9..13'),
	('1', '14..19'),
	('1', '20..29'),
	('1', '30..47'),
	('1', '48..75'),
	('1', '76..95'),
	('1', '96..103'),
	('1', '104..115'),
	('1', '116..132'),
	('1', '133..155'),
	('1', '156..195'),
	('1', '196..270'),
	('1', '271..450'),
	('1', '451..900'),
	('1', '901..1300'),
	('1', '1301..3000'),
	('1', '3001..10000'),
	('1', '10001..60000'),
	('1', '>60000'),
]

#for p in params:
#	j = search_repos(p[0], p[1], 1)
#	assert j['total_count'] < 995

for p in params:
	j = search_repos(p[0], p[1], 1)
	print_repos(j)

	total_count = j['total_count']
	page = 1
	while total_count > 100:
		page += 1
		print_repos(search_repos(p[0], p[1], page))
		total_count -= 100

