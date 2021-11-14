import datetime
import json
import requests


class Vkuser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def _get_photos(self, id):
        get_photos_url = self.url + 'photos.get'
        photos_get_params = {
            'owner_id': id,
            'album_id': 'profile',
            'extended': '1'
        }
        response = requests.get(get_photos_url, params={**self.params, **photos_get_params})

        if response.status_code == 200:
            response = response.json()

            if 'error' in response:
                print(response['error']['error_msg'])
                return None
            elif response['response']['count'] == 0:
                print('\nФотографий в профиле нет\n')
                return None
            elif response['response']['count'] >= 1:
                print('\nФотографии найдены\n')
                return response['response']['items']

        else:
            print(f'Ошибка {response.status_code}')
            return None

    def get_biggest_photo_list(self, id):
        biggest_photo_list = []
        res = self._get_photos(id=id)

        if res is None:
            return None
        else:
            for item in res:
                sizes = item['sizes']
                max_size_url = max(sizes, key=self._get_biggest_photo)['url']
                max_size_type = max(sizes, key=self._get_biggest_photo)['type']
                max_size_date = item['date']
                max_size_likes = item['likes']['count']
                biggest_photo_list.append(
                    {
                        'max_size_url': max_size_url,
                        'max_size_type': max_size_type,
                        'max_size_date': max_size_date,
                        'max_size_like': max_size_likes
                    }
                )
            return biggest_photo_list

    def _get_biggest_photo(self, sizes_dict):
        if sizes_dict['width'] >= sizes_dict['height']:
            return sizes_dict['width']
        else:
            return sizes_dict['height']


class Yauser:
    url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, ya_token):
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'OAuth ' + ya_token
        }

    def _create_folder(self):
        print('Создаю папку...')
        url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        params = {'path': 'reserve vk photos'}
        response = requests.put(url, headers=self.headers, params=params)

        if response.status_code == 201:
            print('Успешно')
        elif response.status_code == 409:
            print('Папка с таким именем уже существует. Запись будет произведена в неё.')
        else:
            print(response.json()['message'])

    def _info_file(self, url):
        with open('copied photos.json', 'w') as f:
            json.dump(url, f, indent=4)

    def upload_reserve_photos(self, biggest_photo_list):
        self._create_folder()
        url = self.url + 'upload'
        counter = 0
        len_list = len(biggest_photo_list)

        for i in biggest_photo_list:
            likes = i['max_size_like']
            upload_time_unix = datetime.datetime.fromtimestamp(i['max_size_date'])
            upload_time = upload_time_unix.strftime('%Y.%m.%d %H-%M-%S')
            photo_url = i['max_size_url']
            self._info_file(biggest_photo_list)
            params = {'path': f'reserve vk photos/{upload_time},\n {likes} лайков', 'url': f'{photo_url}'}
            requests.post(url, headers=self.headers, params=params)
            counter += 1
            print(f'{counter} из {len_list}')



def choose_photo_sourse():
    while True:
        user_input = input(
            'Выберите откуда хотите скопировать фотографии\n'
            '1 - VKontakte\n'
            '2 - coming soon\n'
            'q - завершение работы\n'
        )

        if user_input == '1':
            with open('vktoken.txt', 'r') as f:
                vktoken = f.read()
            vk_cl = Vkuser(vktoken, 5.131)
            vk_user_id = input('Введите id пользователя ВК: ')  # id примера 552934290

            if vk_user_id.isdigit():
                photos = vk_cl.get_biggest_photo_list(vk_user_id)
                return photos
            else:
                print('Неверный ввод\n')

        elif user_input == 'q':
            print('Завершение работы.')
            exit()

        else:
            print('Недоступно')


def choose_upload_sourse(photos):
    while True:

        user_input = input(
            'Выберете куда хотите скопировать их\n'
            '1 - YandexDisk\n'
            '2 - Coming soon\n'
            'q - прервать работу\n'
        )

        if user_input == '1':
            yatoken = input('Вставте токен Яндекс диска:\n')
            ya_cl = Yauser(yatoken)
            ya_cl.upload_reserve_photos(photos)
            print('Фотографии успешно скопированы.')
            break

        elif user_input == 'q':
            print('Завершение работы.')
            exit()

        else:
            print('Недоступно')


if __name__ == '__main__':
    print('Вас приветствует программа резервного копирования фото из соц. сетей.')
    photo = choose_photo_sourse()

    if photo is None:
        photo = choose_photo_sourse()
    else:
        choose_upload_sourse(photo)
