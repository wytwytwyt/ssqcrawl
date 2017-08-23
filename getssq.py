import requests
from bs4 import BeautifulSoup


def get_html(url):
	try:
		h = requests.get(url)
		h.raise_for_status()
		h.encoding = h.apparent_encoding
		print('downloading:'+ url)
		return h.text
	except :
		print("url error")

def get_content(url):
	datas = []
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')

	trtags = soup.find_all('tr', align = 'center')
	for tr in trtags:
		data = {}
		if tr.find('td', height='35') != None:
			data['number'] = tr.find('td', height='35').text.strip()
			balls = tr.find_all('span')
			red_balls = []
			for i in balls:
				red_balls.append(i.text.strip())
			data['blue_ball'] = red_balls[-1]
			red_balls.pop()
			red_balls.sort()
			data['red_ball'] = red_balls
			datas.append(data)
	return datas


def outtofile(datas):
	with open('ssqlishi.txt', 'a+') as f:
		for data in datas:
			f.write('number: {}  red balls: {}  blue ball: {} \n'.format(data['number'], data['red_ball'], data['blue_ball']))
		print ("To file success")
		

def main(url):
	content = get_content(url)
	outtofile(content)
	print('success')


if __name__ == '__main__':
	urls = []
	pagenums = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]

	for x in pagenums:
		if x == 0:
			urls.append('http://www.cwl.gov.cn/kjxx/ssq/hmhz/index.shtml')
		else:
			a = str(x)
			urls.append('http://www.cwl.gov.cn/kjxx/ssq/hmhz/index_' + a + '.shtml')
	for j in urls:
		main(j)
		