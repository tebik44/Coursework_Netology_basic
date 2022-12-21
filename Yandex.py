import requests
from pprint import pprint
from tqdm import tqdm
import time
from datetime import datetime
class Yandex_disk():

    base_host = 'https://cloud-api.yandex.net/'

    def __init__(self, TOKEN_YANDEX):
        self.TOKEN_YANDEX = TOKEN_YANDEX

    def get_headers_authorization(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.TOKEN_YANDEX}'
        }

    def upload_from_internet(self, reforge_dict):
        folder_name = input("Дайте название папки, в которой хотите хранить фото БЕЗ ПРОБЕЛОВ: ")
        uri_uploud = 'v1/disk/resources/upload'
        uri_folder = 'v1/disk/resources'
        path = {'path': folder_name}
        info_about_photo = []
        for item in reforge_dict:
            info_about_photo.append({'file_name': f"{item[1]} | {item[2]}.jpg",
                                     'size': item[3]})

        check_folder = requests.get(self.base_host + uri_folder, params=path)

        if check_folder.status_code == 401:
            folder = requests.put(self.base_host + uri_folder, params=path, headers=self.get_headers_authorization())
            # print(folder.status_code)
            # print(folder.json())
        for item in tqdm(reforge_dict):
            time.sleep(0.15)
            params = {'url': item[0], 'path': f'/{folder_name}/{item[1]} | {item[2]}.jpg'}
            response = requests.post(self.base_host + uri_uploud, params=params, headers=self.get_headers_authorization())
            # print(response.status_code)
            # print(response.json())

        print('Все перенеслось в диск! \nВсе готово!\n')
        print('Данные об загруженных фото:')
        return info_about_photo
