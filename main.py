import requests
from Settings import TOKEN_VK, TOKEN_YANDEX
from pprint import pprint
from progress.bar import IncrementalBar
# from tqdm import tqdm
import time


class Vk:
    base_host = 'https://api.vk.com/method'

    def __init__(self, TOKEN_VK):
        self.TOKEN_VK = TOKEN_VK
        self.users_id = input('Введите id пользователя без пробелов и тому подобного (пример: 329407357) - ')
        if self.users_id.isdigit() == False:
            Vk.user_id_get(self)
        self.count_photo = input('Введите, сколько фото вы хотите перенести - ')


    def get_params_from_user_id(self):
        return {
            'access_token': {self.TOKEN_VK},
            'v': '5.131',
            'user_ids': {self.users_id}
        }

    def get_params_from_photo(self):
         return {
            'access_token': {self.TOKEN_VK},
            'v': '5.131',
            'owner_id': {self.users_id},
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'count': {self.count_photo}
        }


    def user_id_get(self):
        respoun = requests.get(self.base_host + '/users.get', params=self.get_params_from_user_id()).json()
        pprint(respoun)
        user_id = respoun['response'][0]['id']
        print(user_id)
        self.users_id = user_id

    def photos_get(self):
        if self.users_id is not int:
            Vk.user_id_get(self)
        url = '/photos.get'

        respoun = requests.get(self.base_host + url, params=self.get_params_from_photo()).json()
        pprint(respoun)

        return respoun

    def transform_dict_vk(self):
        new_dict = Vk.photos_get(self)
        reforge_dict = []

        bar = IncrementalBar('---', max=len(new_dict['response']['items']))
        for count in range(0, len(new_dict['response']['items'])):
            time.sleep(0.15)
            bar.next()
            reforge_dict.append((new_dict['response']['items'][count]['sizes'][-1]['url'],
                                 new_dict['response']['items'][count]['likes']['count']))

        bar.finish()
        print("Загрузка из вк успешна!")
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
            print(folder.status_code)
            # print(folder.json())
        bar = IncrementalBar('---', max=len(reforge_dict))
        for item in reforge_dict:
            params = {'url': item[0], 'path': f'/{folder_name}/{item[1]}.jpg'}
            response = requests.post(self.base_host + uri_uploud, params=params, headers=self.get_headers_authorization())
            bar.next()
            # print(response.status_code)
            # print(response.json())
        bar.finish()
        print('Все перенеслось в диск! \nВсе готово!')


if __name__ == '__main__':
    # token = input('Укажите свой api token yandex для закрузки: ')
    yandex = Yandex_disk(TOKEN_YANDEX)
    vk = Vk(TOKEN_VK)
    vk.photos_get()
    # yandex.upload_from_internet(vk.transform_dict_vk())
