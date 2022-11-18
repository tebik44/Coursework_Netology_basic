import requests
from Settings import TOKEN_VK, TOKEN_YANDEX
from pprint import pprint

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
        pprint(respoun)
        return respoun

    def transform_dict_vk(self):
        new_dict = VK.photos_get(self)
        reforge_dict = []
        new = len(new_dict['response']['items'])
        for count in range(0, len(new_dict['response']['items'])):
            reforge_dict.append((VK.photos_get(self)['response']['items'][int(count)]['sizes'][-1]['url'], VK.photos_get(self)['response']['items'][int(count)]['likes']['count']))

        pprint(reforge_dict)
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


    def upload_from_internet(self, dict_url):
        uri = 'v1/disk/resources/upload/new_vk'
        request_url = self.base_host + uri
        for item in dict_url:
            params = {'url': item[0], 'path': f'/{item[1]}.jpg'}
            response = requests.post(request_url, params=params, headers=self.get_headers_authorization())
            print(response.status_code)
            print(response.json())


if __name__ == '__main__':
    yandex = Yandex_disk(TOKEN_YANDEX)
    vk = VK(TOKEN_VK)
    vk.photos_get()
    yandex.upload_from_internet(vk.transform_dict_vk())
