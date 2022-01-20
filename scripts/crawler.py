from bs4 import BeautifulSoup
import requests
import telegram
from hotdeal.models import Deal
from datetime import datetime, timedelta

response = requests.get(
    "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
)
soup = BeautifulSoup(response.text, 'html.parser')
BOT_TOKEN = '5006961994:AAF20WWgovP5EqkZgzLm-omVEcXMp1baOiI'
bot = telegram.Bot(token=BOT_TOKEN)

def run(): 
    # 현재 시간에서 3일을 뺀 시간보다 작은 created_at 필드를 가진 게시물은 삭제한다.
    # 즉, 3일이 지난 게시물은 삭제된다.
    row, _ = Deal.objects.filter(created_at__lte=datetime.now() - timedelta(days=3)).delete()
    print(row, "deals deleted")

    for item in soup.find_all('tr', {'class': ['list1', 'list0']}):
        try: 
            image = item.find('img', class_='thumb_border').get('src')[2:]
            image = 'http://' + image
            title = item.find('font', class_='list_title').text
            title = title.strip()
            link = item.find('font', class_='list_title').parent.get('href')
            link = 'https://www.ppomppu.co.kr/zboard/' + link
            reply_count = item.find('span', class_='list_comment2').text
            reply_count = int(reply_count)
            up_count = item.find_all('td')[-2].text
            up_count = up_count.split("-")[0]
            up_count = int(up_count)

            if up_count >= 5:
                # iexact : 대소문자를 구분하지않고 정확히 일치하는 데이터를 찾는다.
                # DB내의 링크와 크롤링한 링크가 같은 것이 없으면 
                # 크롤링 데이터를 DB에 집어넣는다. (즉, 등록되어 있지 않은 글만 집어넣음.)
                if (Deal.objects.filter(link__iexact=link).count() == 0):
                    Deal(image_url=image, title=title, link=link, reply_count=reply_count, up_count=up_count).save()
                    bot.send_message(-1001760796628, '{} {}'.format(title, link))

        except Exception as e:
            continue
