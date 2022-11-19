import requests
from Settings import TOKEN_VK, TOKEN_YANDEX
from pprint import pprint
from progress.bar import IncrementalBar
# from tqdm import tqdm
import time


class VK:
    base_host = 'https://api.vk.com/method'

    def __init__(self, TOKEN_VK):
        self.TOKEN_VK = TOKEN_VK
        self.Users_id = input('Введите id пользователя без пробелов и тому подобного (пример: 329407357) - ')
        self.count_photo = input('Введите, сколько фото вы хотите перенести - ')


    def Get_params(self):
         return {
            'access_token': {self.TOKEN_VK},
            'v': '5.131',
            'owner_id': {self.Users_id},
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': {self.count_photo}
        }

    def photos_get(self):
        url = '/photos.get'

        respoun = requests.get(self.base_host + url, params=self.Get_params()).json()
        # pprint(respoun)
        return respoun

    def transform_dict_vk(self):
        new_dict = VK.photos_get(self)
        reforge_dict = []

        bar = IncrementalBar('---', max=len(new_dict['response']['items']))
        for count in range(0, len(new_dict['response']['items'])):
            bar.next()
            reforge_dict.append((new_dict['response']['items'][count]['sizes'][-1]['url'],
                                 new_dict['response']['items'][count]['likes']['count']))

        bar.finish()

        # pprint(reforge_dict)
        return reforge_dict



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

        check_folder = requests.get(self.base_host + uri_folder, params=path)
        if check_folder.status_code == 401:
            folder = requests.put(self.base_host + uri_folder, params=path, headers=self.get_headers_authorization())
            # print(folder.status_code)
            # print(folder.json())
        for item in reforge_dict:
            params = {'url': item[0], 'path': f'/{folder_name}/{item[1]}.jpg'}
            response = requests.post(self.base_host + uri_uploud, params=params, headers=self.get_headers_authorization())
            # print(response.status_code)
            # print(response.json())
        print('Все готово!')


if __name__ == '__main__':
    yandex = Yandex_disk(TOKEN_YANDEX)
    vk = VK(TOKEN_VK)
    yandex.upload_from_internet(vk.transform_dict_vk())
