import requests
import time
from lxml import etree
from bs4 import BeautifulSoup


def get_html(url):
    try:
        print('downloading:'+ url)
        h = requests.get(url)
        h.raise_for_status()
        h.encoding = h.apparent_encoding
        print('download success')
        
        return h.text
    except :
        print("url error")

def get_content(url):
    datas = []
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    print('souping')

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
    print(url + '  success')


if __name__ == '__main__':
    urls = ['http://www.cwl.gov.cn/kjxx/ssq/hmhz/index.shtml']
    pagenums = []
    print('getting pagecounts')
    selector = etree.HTML(requests.get(urls[0]).text)
    pagecount = selector.xpath('//div[@class="pagebar"]//td//text()')[-2]
    pagecounts = int(pagecount[2]+pagecount[3])
    print('pagecounts:'+str(pagecounts))
    for i in range(1, pagecounts):
        pagenums.append(i)
    for x in pagenums:
        a = str(x)
        urls.append('http://www.cwl.gov.cn/kjxx/ssq/hmhz/index_' + a + '.shtml')
    for j in urls:
        main(j)
        time.sleep(1)

        
