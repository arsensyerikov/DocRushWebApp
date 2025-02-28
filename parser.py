import requests
from bs4 import BeautifulSoup


response = requests.get('https://www.pravda.com.ua/news/')
html = response.content
soup = BeautifulSoup(html, "html5lib")

links_data = soup.select('.article_header > a')

links = []
headers = []
for i in links_data[:4]:
    links.append(i.get('href'))
    headers.append(i.text)

new_links = []
for el in links:
    if el[:5] != 'https':
        el = 'https://www.pravda.com.ua' + el
    new_links.append(el)


articles = []

for i in new_links:
    article = requests.get(i).content
    new_soup = BeautifulSoup(article, "html5lib")

    post_text = new_soup.select('.post__text > p, .article > p, .post_text > p')
    article_body = []
    for article in post_text:
        article_body.append(article.text + '\n')
    article_text = ''.join(article_body)
    articles.append(article_text)

print(headers)