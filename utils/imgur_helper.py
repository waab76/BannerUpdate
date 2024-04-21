'''
Created on Mar 29, 2020

@author: rcurtis
'''

import json
import logging
import re
import requests

def download_as(imgurUrl, localFileName):
    logging.info('Downloading image from {} to {}'.format(imgurUrl, localFileName))
    album_url = 'https://api.imgur.com/3/album/{}/images'
    image_url = 'https://api.imgur.com/3/image/{}'
    payload={}
    files={}
    headers = {
         'Authorization': 'Client-ID b8a49806af1c02a',
         'user-agent': 'curl/7.84.0',
         'accept': '*/*'
    }

    match = re.search('https?\:\/\/.*imgur\.com\/a?\/?(\w*)', imgurUrl)
    album_id = match.group(1)

    response = requests.request("GET", album_url.format(album_id), headers=headers, data=payload, files=files)
    if response.status_code >= 300:
         logging.error('Status code {} attempting to get album'.format(response.status_code))
         response = requests.request("GET", image_url.format(album_id), headers=headers, data=payload, files=files)
         if response.status_code < 300:
              logging.error('Status code {} attempting to get image'.format(response.status_code))
              image_data = json.loads(response.text)
              download_url = image_data['data']['link'].replace('jpg', 'jpeg')
    else:
        album_data = json.loads(response.text)
        download_url = album_data['data'][0]['link'].replace('jpg', 'jpeg')
    response = requests.request("GET", download_url, headers=headers, data=payload, files=files)

    if response.status_code == 200:
        with open(localFileName, 'wb') as fo:
                for chunk in response.iter_content(4096):
                    fo.write(chunk)