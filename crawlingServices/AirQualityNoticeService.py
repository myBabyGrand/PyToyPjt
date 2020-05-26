import requests
from bs4 import BeautifulSoup
from datetime import datetime

import telegram

#날짜 문자열 만들기
NOW = datetime.now()
tYear = str(NOW.year)
tMonth = str(NOW.month)
if len(tMonth) == 1:
    tMonth = '0'+tMonth

tDay= str(NOW.day)
if len(tDay) == 1:
    tDay = '0'+tDay

MSG = tYear+'-'+tMonth+'-'+tDay+' '+'미세먼지'


#Crawling
#대상 URL
URL_PM25 = 'http://www.airkorea.or.kr/web/vicinityStation?item_code=10008&station_code=111273'
URL_PM10 = 'http://www.airkorea.or.kr/web/vicinityStation?item_code=10007&station_code=111273'
URL_OZONE = 'http://www.airkorea.or.kr/web/vicinityStation?item_code=10003&station_code=111273'
URL_NOX = 'http://www.airkorea.or.kr/web/vicinityStation?item_code=10006&station_code=111273'
URL_CO = 'http://www.airkorea.or.kr/web/vicinityStation?item_code=10002&station_code=111273'
URL_SOX = 'http://www.airkorea.or.kr/web/vicinityStation?item_code=10001&station_code=111273'

urlList = [URL_PM25]
urlList.append(URL_PM10)
urlList.append(URL_OZONE)
urlList.append(URL_NOX)
urlList.append(URL_CO)
urlList.append(URL_SOX)

matterList = ['PM2.5']
matterList.append('PM10')
matterList.append('오존')
matterList.append('NOx')
matterList.append('CO')
matterList.append('SOx')

MSG = tYear+'-'+tMonth+'-'+tDay+' '+' 송파구 대기질 측정값'

idx = 0;
for tUrl in urlList:

    #Crawling 시작
    res = requests.get(tUrl)
    soup = BeautifulSoup(res.content, 'html.parser')

    tbody = soup.find('tbody')
    tr_list = soup.findAll('tr', {'class': 'al2'})

    cnt = 0
    content = '';
    for i in tr_list:
        tdCn = i.find('td')
        if cnt==1:
            #데이터 타입을 str으로 해야 str함수를 사용할 수 있다.
            content = str(tdCn)

        # print(tdCn)
        cnt=cnt+1

    # print(content)

    content = content.replace('<td>',' ')
    content = content.replace('</td>',' ')
    content = matterList[idx]+' : '+content
    # print(content)
    MSG = MSG + '\n' + content
    idx = idx+1

print(MSG)

#telegram bot으로 메시지 보내기 https://vmpo.tistory.com/85?category=736951
standardP_Bot_token = '****'  #token from telegram bot faather
standardP_Bot = telegram.Bot(token = standardP_Bot_token)
updates = standardP_Bot.getUpdates()
# print(updates)
# for i in updates:
#     print(i)

standardP_Bot.sendMessage(chat_id = '****', text = MSG) #to get chat id,  start conversation with the bots


