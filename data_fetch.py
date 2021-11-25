import requests
import csv
from bs4 import BeautifulSoup
import sys
import os
import pandas as pd

from zipfile import ZipFile

import tensorflow as tf
site_url = 'https://webrobots.io/kickstarter-datasets/'
data_path = './data/'


request = requests.get(site_url)

soup = BeautifulSoup(request.content, features='html.parser')

# for some reason bs4 keeps mixing in Nones with the data so we do a final sweep over everything to remove the Nones
urls_to_download = [i for i in [link.get('href') for link in soup.find_all('a')] if i]

# filter out everything that doesn't have .zip extensions
final_urls = []

for i in urls_to_download:
	if ".zip" in i:
		final_urls.append(i)

'''
Please note: This is currently only set up to grab the last entry of data for 2020. You could technically set it up to grab every month's data for each year, but it appears successive sets of data are cumulative so there's not really a point to grabbing sets from earlier in the year. 2020 alone provides over 200000 kickstarter names and blurbs, more than enough for our RNN text generator to learn from
'''

final_urls = [i for i in final_urls if "2020" in i]

path_to_file = tf.keras.utils.get_file(final_urls[0].split('/')[-1], final_urls[0])
print(path_to_file)

zf = ZipFile(path_to_file)
zf.extractall(path='./data')


files_to_process = os.listdir(data_path)
output_df = pd.DataFrame()
cols_to_take = ['blurb', 'name']




for f in files_to_process:
	df = pd.read_csv(data_path + f)
	output_df = output_df.append(df[cols_to_take])
	os.remove(data_path + f)


print(output_df.shape)
output_df.to_csv('kickstarter_data.csv', encoding='utf-8', index=False)
