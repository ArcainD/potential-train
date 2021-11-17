import datetime
import json
import requests


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
            print('Папка с таким именем уже существует. '
                  'Запись будет произведена в неё.')
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
            upload_time_unix = datetime.datetime.fromtimestamp(
                i['max_size_date']
            )
            upload_time = upload_time_unix.strftime('%Y.%m.%d %H-%M-%S')
            photo_url = i['max_size_url']
            self._info_file(biggest_photo_list)
            params = {
                'path': f'reserve vk photos/{upload_time},\n {likes} лайков',
                'url': f'{photo_url}'
            }
            requests.post(url, headers=self.headers, params=params)
            counter += 1
            print(f'{counter} из {len_list}')
