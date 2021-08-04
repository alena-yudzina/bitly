import requests
import argparse
import os
from urllib.parse import urlparse
from dotenv import load_dotenv


class WrongUrlException(Exception):
    pass


def parse_cli_args():
    ''' parse arguments from cli

    '''
    parser = argparse.ArgumentParser(description='make bitlink or count bitlink clicks')
    parser.add_argument('link', help='set link')
    args = parser.parse_args()
    return args.link


def is_bitlink(token, url):

    parsed_url = urlparse(url)
    no_schema_url = '{}{}'.format(parsed_url.netloc, parsed_url.path)
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(no_schema_url)
    headers = {
        'Authorization': 'Bearer {}'.format(token),
    }
    response = requests.get(api_url, headers=headers)
    return response.ok


def shorten_link(token, url):

    api_url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {
        'Authorization': 'Bearer {}'.format(token),
    }
    payload = {
        'long_url': url,
    }
    response = requests.post(api_url, headers=headers, json=payload)

    if not response.ok:
        raise WrongUrlException
    return response.json()['link']


def count_clicks(token, link):

    parsed_url = urlparse(link)
    no_schema_url = '{}{}'.format(parsed_url.netloc, parsed_url.path)
    api_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(no_schema_url)
    headers = {
        'Authorization': 'Bearer {}'.format(token),
    }
    payload = {
        'units': -1,
    }
    response = requests.get(api_url, headers=headers, params=payload)

    if not response.ok:
        raise WrongUrlException
    return response.json()['total_clicks']


def main():

    load_dotenv()

    token = os.environ['BITLY_TOKEN']
    link = parse_cli_args()
    try:
        if is_bitlink(token, link):
            clicks = count_clicks(token, link)
            print(clicks)
        else:
            bitlink = shorten_link(token, link)
            print(bitlink)
    except WrongUrlException:
        print('Wrong URL')


if __name__ == '__main__':
    main()
