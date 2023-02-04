import os

import pygame
import requests

import input as ip


def find_place():
    name = ip.main()
    geocoder_api_server = 'http://geocode-maps.yandex.ru/1.x/'
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json",
        'envelope': ''}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    place = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].replace(
        ' ',
        ',')
    place = [float(place.split(',')[1]), float(place.split(',')[0])]
    start = ','.join([str(place[1]), str(place[0])])
    return start, place

now = 0


types = ['map', 'sat', 'sat,skl']

start, place = find_place()


def req(num, place, type, start):
    place = ','.join([str(place[1]), str(place[0])])
    map_request = "https://static-maps.yandex.ru/1.x"
    request = (requests.get(map_request,
                            params={'ll': place, 'z': num, 'pt': f'{start},pmwtm',
                                    'l': type}))
    with open("1.png", "wb") as file:
        file.write(request.content)


# Запишем полученное изображение в файл.
request = req(11, place, types[now % 3], start)
num = 11

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
# Переключаем экран и ждем закрытия окна.
while 1:
    screen.blit(pygame.image.load("1.png"), (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove("1.png")
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741899:
                if num < 15:
                    num += 1
            if event.key == 1073741902:
                if num > 1:
                    num -= 1
            if event.key == pygame.K_n:
                find_place()
            if event.key == pygame.K_LEFT:
                if place[1] - 1 / num > -180:
                    place[1] -= 1 / num
                else:
                    place[1] = 180
            if event.key == pygame.K_RIGHT:
                if place[1] + 1 / num < 180:
                    place[1] += 1 / num
                else:
                    place[1] = -180
            if event.key == pygame.K_UP:
                if place[0] + 1 / num < 90:
                    place[0] += 1 / num
            if event.key == pygame.K_DOWN:
                if place[0] - 1 / num > -90:
                    place[0] -= 1 / num
            if event.key == pygame.K_5:
                now += 1
            req(num, place, types[now % 3], start)
