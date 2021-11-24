import requests
import csv
import re
from bs4 import BeautifulSoup
import sys

from zipfile import ZipFile

import tensorflow as tf
site_url = 'https://webrobots.io/kickstarter-datasets/'
data_path = './data'


request = requests.get(site_url)

soup = BeautifulSoup(request.content, features='html.parser')

# for some reason bs4 keeps mixing in Nones with the data so we do a final sweep over everything to remove the Nones
urls_to_download = [i for i in [link.get('href') for link in soup.find_all('a')] if i]

# filter out everything that doesn't have .zip extensions
final_urls = []

for i in urls_to_download:
	if ".zip" in i:
		final_urls.append(i)



final_urls = [i for i in final_urls if "2020" in i]

path_to_file = tf.keras.utils.get_file(final_urls[0].split('/')[-1], final_urls[0])
print(path_to_file)

zf = ZipFile(path_to_file)
zf.extractall(path='./data')

