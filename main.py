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
        new_dict = VK.photos_get(self)['response']['items'][1]['likes']['count']
        new_dict = VK.photos_get(self)['response']['items'][1]['sizes'][-1]['url']
        pprint(new_dict)



class Yandex_disk():
    def __init__(self, TOKEN_YANDEX):
        self.TOKEN_YANDEX = TOKEN_YANDEX


    def get_headers_authorization(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.TOKEN_YANDEX}'
        }


    def Uploud_to_disk_vk_photo(self):
        url = ''


if __name__ == '__main__':
    yandex = Yandex_disk(TOKEN_YANDEX)
    vk = VK(TOKEN_VK)
    vk.photos_get()
    vk.transform_dict_vk()
