import os
import pygame
import requests
import sys
import time

class MapParams(object):
    def __init__(self):
        self.lat = 61.665279  # Координаты центра карты на старте [1](https://www.CyberForum.ru/python-pygame/thread2783841.html)
        self.lon = 50.813492
        self.zoom = 16  # Масштаб карты на старте (изменяется от 1 до 19)
        self.type = "map"  # Другие значения: "sat", "sat,skl" [1](https://www.CyberForum.ru/python-pygame/thread2783841.html)

    def ll(self):
        return str(self.lon) + "," + str(self.lat)

    def set_zoom(self, new_zoom):
        self.zoom += new_zoom

def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
    # Запись полученного изображения в файл
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file

def main():
    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    mp = MapParams()
    map_file = load_map(mp)
    pygame.display.set_caption('Задача 2')
    run = 1
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Выход из программы
                run = 0
            if event.type == pygame.K_PAGEDOWN:
                print(mp.zoom)
                if mp.zoom != 1:
                    mp.set_zoom(-1)
            else:
                print("Min zoom")
            if event.type == pygame.K_PAGEUP:
                print(mp.zoom)
                if mp.zoom != 19:
                    mp.set_zoom(1)
    # Создаём файл
        map_file = load_map(mp)
        # Рисуем картинку, загружаемую из только что созданного файла
        screen.blit(pygame.image.load(map_file), (0, 0))
        clock.tick(50)
        pygame.display.flip()
    pygame.quit()
    # Удаляем файл с изображением
    os.remove(map_file)
if __name__ == "__main__":
    main()