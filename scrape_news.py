import asyncio
import csv
import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


async def get_news(date_news, url_news, session):
    try:
        with session.get(url_news, allow_redirects=False, timeout=10) as response:
            page_content = BeautifulSoup(response.content, 'html.parser')
            div_news = page_content.find('article', itemprop="articleBody")
            temp = " ".join([str(rows.text) for rows in div_news.findAll('p')])
            temp = temp.split("-", 1)
            return [date_news, temp[1]]
    except:
        return None


async def scrape_news(start_date, end_date, file):
    delta = datetime.timedelta(days=1)

    headers = {
        'User-Agent': UserAgent().random,
    }

    with requests.Session() as session:
        with file:
            file_writer = csv.writer(file, lineterminator='\n')
            file_writer.writerow(['date_news', 'news'])

            while start_date <= end_date:
                date = start_date.strftime('%Y/%m/%d')
                date_news = start_date.strftime('%d.%m.%Y')
                url = f'https://www.interfax.ru/russia/news/{date}'
                print(url)

                with session.get(url, headers=headers, allow_redirects=False, timeout=10) as response:
                    page_content = BeautifulSoup(
                        response.content, "html.parser")
                    div_news = page_content.find(class_="an")
                    data_id = [tag['data-id']
                               for tag in div_news.select('div[data-id]')]

                    tasks = [get_news(
                        date_news, f'https://www.interfax.ru/russia/{id}', session) for id in data_id]
                    news = [n for n in await asyncio.gather(*tasks) if n is not None]

                    file_writer.writerows(news)

                start_date += delta


if __name__ == "__main__":
    start_date = datetime.date(2022, 1, 1)
    end_date = datetime.date(2022, 12, 31)

    asyncio.run(scrape_news(start_date, end_date, open(
        "data.csv", mode="w", encoding='utf-8', newline='')))
