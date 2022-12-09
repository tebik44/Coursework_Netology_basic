from Settings import TOKEN_VK, TOKEN_YANDEX
import VK
import Yandex

if __name__ == '__main__':
    # token = input('Укажите свой api token yandex для закрузки: ')
    yandex = Yandex.Yandex_disk(TOKEN_YANDEX)
    vk = VK.Vk(TOKEN_VK)
    vk.transform_dict_vk()
    # yandex.upload_from_internet(vk.transform_dict_vk())

