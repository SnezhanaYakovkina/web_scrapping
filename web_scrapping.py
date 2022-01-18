import bs4
import requests, re

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'hl=ru; fl=ru; _ga=GA1.2.1645936541.1639904313; _ym_uid=1639904314126969645; _ym_d=1639904314; __gads=ID=5b51f6146381b757:T=1639904317:S=ALNI_MZEtpctyamq1OWN0_hdRuQMLLAsIg; visited_articles=488720:335298:167015:598939:598957:99923:215117:547290:540380; cto_bundle=dg4iuV9SRmt0amRBMEZHUnNxTXJDdVdaaGJWeWF4ejhLWnZWYTJ5anNNenNBa05yREhBaGR6T044Sk94cXptUCUyRmolMkZTRXUyRyUyQnhGNEZrUEhCeWpPUHNuSFBQUmNxZUxhVW5kbFdZWjVCTkhGMUJqM2pQMHV5ZU51WjF2R0pUeXJ5JTJCdWNa; connect_sid=s%3AI_5UMIfzvMNu8wAGogxS3_PeHqgrp_yW.I8TWWNnCVVYnXTnuJuxDBFqJoW7%2F73cUv2%2BSgeu6F6Q; habrsession_id=habrsession_id_85cf20ff38248253f131b9d7fc4eb00b; PHPSESSID=al3b0eremvfkq8gb4e1q7mp385; hsec_id=7c11167c08ede8c1dc6e0836290f8922; habr_web_ga_uid=f5462d3ef625413494e973a86e1671c7; habr_web_hide_ads=true; habr_web_user_id=2865003; _fbp=fb.1.1641280060036.1819726131; habr_web_home=ARTICLES_LIST_ALL; _gid=GA1.2.1567658556.1642311745',
    'Host': 'habr.com',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'
}

KEYWORDS = {'дизайн', 'фото', 'web', 'python'}
URL = 'https://habr.com/ru/all/'



def get_articles(keywords, url):
    response = requests.get(url, headers=HEADERS)
    text = response.text
    soup = bs4.BeautifulSoup(text, features='html.parser')

    articles = soup.find_all('article', class_='tm-articles-list__item')
    for article in articles:
        title = article.find('a', class_='tm-article-snippet__title-link').text  # получили все заголовки
        preview_texts = article.find_all('div', class_='article-formatted-body article-formatted-body_version-2')
        preview_texts = [preview_text.find('p').text for preview_text in preview_texts]
        href = article.find('a', class_='tm-article-snippet__title-link').get('href')
        post_link = 'https://habr.com' + href
        date_of_public = article.find('span', class_='tm-article-snippet__datetime-published').text
        # print(title)
        # print(preview_texts)
        # print(post_link)
        # print(date_of_public)
        # print('------')

        words = [word.group() for word in re.finditer(r"[a-zа-я]{2,}", preview_texts.lower())]
        for word in words:
            if any([keyword in word for keyword in keywords]):
                print(f'Дата: {date_of_public} - Заголовок: {title} - Ссылка: {post_link}')
                print('-----')
                break


if __name__ == '__main__':
    get_articles(KEYWORDS, URL)
