import requests
from pprint import pprint
from tqdm import tqdm
from time import sleep
from datetime import datetime

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
        user_id = respoun['response'][0]['id']
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

        for count in tqdm(range(0, len(new_dict['response']['items']))):
            sleep(0.2)
            date = datetime.utcfromtimestamp(new_dict['response']['items'][count]['date']).strftime('%Y-%m-%d %H.%M.%S')
            reforge_dict.append((new_dict['response']['items'][count]['sizes'][-1]['url'],
                                 new_dict['response']['items'][count]['likes']['count'], date, new_dict['response']['items'][count]['sizes'][-1]['type']))


        print("Загрузка из вк успешна!")
        return reforge_dict


    # def transform_dict_vk(self):
    #     new_dict = Vk.photos_get(self)
    #
    #     reforge_dict = {}
    #     for count in tqdm(range(len(new_dict['response']['items']))):
    #         if str(new_dict['response']['items'][count]['likes']['count']) not in reforge_dict:
    #             reforge_dict[new_dict['response']['items'][count]['likes']['count']] = \
    #                 new_dict['response']['items'][count]['sizes'][-1]['url']
    #
    #         else:
    #             date = datetime.utcfromtimestamp(new_dict['response']['items'][count]['date'])\
    #                 .strftime('%Y-%m-%d %H:%M:%S')
    #             reforge_dict[new_dict['response']['items'][count]['likes']['count'] + " | " + date] = \
    #                 new_dict['response']['items'][count]['sizes'][-1]['url']

        #
        #
        # print("Загрузка из вк успешна!")
        # pprint(reforge_dict)
        # return reforge_dict






