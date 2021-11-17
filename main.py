import ya_user
import vk_user


if __name__ == '__main__':
    def choose_photo_sourse():
        while True:
            user_input = input(
                'Выберите откуда хотите скопировать фотографии\n'
                '1 - VKontakte\n'
                '2 - coming soon\n'
                'q - завершение работы\n'
            )

            if user_input == '1':
                vktoken = ''  # Вставить токен ВК
                vk_cl = vk_user.Vkuser(vktoken, 5.131)
                vk_user_id = input('Введите id пользователя ВК: ')
                # id примера 552934290

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
                ya_cl = ya_user.Yauser(yatoken)
                ya_cl.upload_reserve_photos(photos)
                print('Фотографии успешно скопированы.')
                break

            elif user_input == 'q':
                print('Завершение работы.')
                exit()

            else:
                print('Недоступно')

    print('Вас приветствует программа'
          ' резервного копирования фото из соц. сетей.')

    photo = choose_photo_sourse()

    if photo is None:
        photo = choose_photo_sourse()
    else:
        choose_upload_sourse(photo)
