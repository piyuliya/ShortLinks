import requests
import settings

bitlinks_url = 'https://api-ssl.bitly.com/v4/bitlinks'
total_clicks_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'


def get_shorten_link(token, url, user_url):
    payload = {'long_url': user_url}
    headers = {'Authorization': token}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    user_response = response.json()
    return user_response['link']


def check_user_link(user_link):
    if 'http' in user_link:
        link = user_link[6:]
    else:
        link = user_link
    return link


def get_count_clicks(token, url, user_link):
    link_for_check = check_user_link(user_link)
    headers = {'Authorization': token}
    params = {'unit_reference': ''}
    response = requests.get(
        url.format(link_for_check),
        params=params,
        headers=headers
    )
    response.raise_for_status()
    count_clicks = response.json()
    return count_clicks['total_clicks']


def check_user_input(url):
    if 'bit.ly' in url:
        try:
            clicks_count = get_count_clicks(
                settings.TOKEN,
                total_clicks_url,
                url
            )
            print('Количество переходов по ссылке за всё время', clicks_count)
        except requests.exceptions.HTTPError:
            print('Введен неверный битлинк')
    else:
        try:
            user_bitlink = get_shorten_link(settings.TOKEN, bitlinks_url, url)
            print('Битлинк', user_bitlink)
        except requests.exceptions.HTTPError:
            print('Введен неверный url')


if __name__ == "__main__":
    user_input = input('Введите ссылку: ')
    check_user_input(user_input)
