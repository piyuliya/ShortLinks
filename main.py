import requests
import settings

BITLINKS_URL = 'https://api-ssl.bitly.com/v4/bitlinks'
TOTAL_CLICKS_URL = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'


def get_shorten_link(token, url, user_url):
    payload = {'long_url': user_url}
    headers = {'Authorization': token}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    shorten_link_response = response.json()
    return shorten_link_response['link']


def get_user_link(user_link):
    if 'http' in user_link:
        link = user_link[6:]
    else:
        link = user_link
    return link


def get_count_clicks(token, url, user_link):
    link_for_check = get_user_link(user_link)
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
                TOTAL_CLICKS_URL,
                url
            )
            print('Количество переходов по ссылке за всё время', clicks_count)
        except requests.exceptions.HTTPError:
            print('Введен неверный битлинк')
    else:
        try:
            user_bitlink = get_shorten_link(settings.TOKEN, BITLINKS_URL, url)
            print('Битлинк', user_bitlink)
        except requests.exceptions.HTTPError:
            print('Введен неверный url')


if __name__ == "__main__":
    user_input = input('Введите ссылку: ')
    check_user_input(user_input)
