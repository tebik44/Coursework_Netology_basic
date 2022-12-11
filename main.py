from Settings import TOKEN_VK, TOKEN_YANDEX
import VK
import Yandex

import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read("Settings.ini")
    #ЕСЛИ Я ПРОБУЮ ВСТАВИТЬ ПРИ ПОМОЩИ INI, ТО ВЫХОДИТ ОШИБКА, Я ВСТАВЛЯЮ В НИХ ЭТО - config['VK']['TOKEN_VK'] | config['Yandex']['TOKEN_YANDEX'], ПРЯМО В ПАРАМЕТРЫ МЕТОДА
    # Я ПРОВЕРИЛ ПРИ ПОМОЩИ PRINT, ВСЕ РАБОТАЕТ, ТО ЕСТЬ ЭТО ВСЕ ЖЕ ПРОБЛЕМА ПАРАМЕТРОВ МЕТОДА
    # token = input('Укажите свой api token yandex для закрузки: ')
    yandex = Yandex.Yandex_disk(TOKEN_YANDEX)
    vk = VK.Vk(TOKEN_VK)
    vk.transform_dict_vk()
    yandex.upload_from_internet(vk.transform_dict_vk())

