import os

import pygame
import requests
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
    address = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty'][
        'GeocoderMetaData']['Address']['formatted']
    place = [float(place.split(',')[1]), float(place.split(',')[0])]
    start = [None, f"{','.join([str(place[1]), str(place[0])])},pmwtm"]
    return start, address, place


start, address, place = find_place()
now = 0
show_place = True
types = ['map', 'sat', 'sat,skl']


def req(num, place, type, start):
    place = ','.join([str(place[1]), str(place[0])])
    map_request = "https://static-maps.yandex.ru/1.x"
    request = (requests.get(map_request,
                            params={'ll': place, 'z': num, 'pt': start[show_place],
                                    'l': type}))
    with open("1.png", "wb") as file:
        file.write(request.content)


# Запишем полученное изображение в файл.
request = req(11, place, types[now % 3], start)
num = 11

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))

myau = 'https://geocode-maps.yandex.ru/1.x'
mur = requests.get(myau, params={'apikey': '40d1649f-0493-4b70-98ba-98533de7710b',
                                 'geocode': 'Москва Улица Петровка 38 Уголовный Розыск', 'format': 'json'})

# Преобразуем ответ в json-объект
json_response = mur.json()
# Получаем первый топоним из ответа геокодера.
# Согласно описанию ответа, он находится по следующему пути:
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
# Полный адрес топонима:
indx = \
    ['', toponym["metaDataProperty"]["GeocoderMetaData"]['AddressDetails']['Country']['AdministrativeArea']['Locality'][
        'Thoroughfare']['Premise']['PostalCode']['PostalCodeNumber']]

show_indx = True


# Рисуем картинку, загружаемую из только что созданного файла.
# Переключаем экран и ждем закрытия окна.
def draw_text():
    font = pygame.font.Font(pygame.font.match_font('arial'), 20)
    text_surface = font.render(address + indx[show_indx], True, 'red')
    text_rect = text_surface.get_rect()
    screen.blit(text_surface, text_rect)


while 1:
    screen.blit(pygame.image.load("1.png"), (0, 0))
    if show_place:
        draw_text()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove("1.png")
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741899:
                if num < 15:
                    num += 1
            if event.key == pygame.K_n:
                start, address, place = find_place()
            if event.key == pygame.K_DELETE:
                show_place = not show_place
            if event.key == 1073741902:
                if num > 1:
                    num -= 1
            if event.key == pygame.K_BACKSPACE:
                show_indx = not show_indx
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
    pygame.display.flip()
