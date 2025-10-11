import requests
from bs4 import BeautifulSoup

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
content = requests.get(URL).content

soup = BeautifulSoup(content, 'html.parser')
movie_list = soup.find_all(name='h3', class_='title')
movie_list.reverse()

for i in range(len(movie_list)):
    movie_list[i] = movie_list[i].getText() # type: ignore

# print(movie_list)
with open('./day-45-web-scraping/3-top-100-movies/movies.txt', 'w', encoding='utf-8') as file:
    for movie in movie_list:
        file.write(f'{movie}\n')