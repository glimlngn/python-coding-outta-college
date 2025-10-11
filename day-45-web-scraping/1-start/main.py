from bs4 import BeautifulSoup

with open('day-45-web-scraping/1-start/website.html', mode="r") as file:
    content = file.read()

soup = BeautifulSoup(content, "html.parser")
tag_list = soup.find_all(name='a')
for tag in tag_list:
    print(tag.get('href'))

heading = soup.find(name='h1', id='name')
print(heading)

heading = soup.select(selector='.heading')
print(heading)