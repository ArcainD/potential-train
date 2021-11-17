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

        try:
            response = requests.get(
                get_photos_url, params={**self.params, **photos_get_params}
            )

            # ======================================
            if response.status_code == 200:
                response = response.json()

                if 'error' in response:
                    print(response['error']['error_msg'])
                    return None
                elif response['response']['count'] == 0:
                    print('\nФотографий в профиле нет\n')
                    return None
                elif response['response']['count'] >= 1:
                    res = response['response']['count']
                    print(f'\nФотографий найдено: {res}\n')
                    return response['response']['items']

            else:
                print(f'Ошибка {response.status_code}')
                return None

        except Exception as e:
            print(e)

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
