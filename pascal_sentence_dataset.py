#!/usr/bin/python
#-*- coding: utf-8 -*-

from urllib.parse import urljoin
from pyquery import PyQuery
import os
import requests
import csv

__author__ = 'rupy'
__modified = 'infinitusposs'

class PascalSentenceDataSet():

    DATASET_DIR = 'dataset/'
    SENTENCE_DIR = 'sentence/'
    PASCAL_SENTENCE_DATASET_URL = 'http://vision.cs.uiuc.edu/pascal-sentences/'

    def __init__(self):
        self.url = PascalSentenceDataSet.PASCAL_SENTENCE_DATASET_URL

    def download_images(self):
        dom = PyQuery(self.url)
        for img in dom('img').items():
            img_src = img.attr['src']
            category, img_file_name = os.path.split(img_src)

            # make category directories
            output_dir = PascalSentenceDataSet.DATASET_DIR + category
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)

            # download image
            output = os.path.join(output_dir, img_file_name)
            print (output)
            if img_src.startswith('http'):
                img_url = img_src
            else:
                img_url = urljoin(self.url, img_src)
            if os.path.isfile(output):
                print ("Already downloaded, Skipping: %s" % output)
                continue
            print ("Downloading: %s" % output)
            with open(output,'wb') as f:

                while True:
                    result = requests.get(img_url)
                    raw = result.content
                    if result.status_code == 200:
                        f.write(raw)
                        break
                    print ("error occurred while fetching img")
                    print ("retry...")


    def download_sentences(self):
        dom = PyQuery(self.url)
        # tbody disappears in pyquery DOM
        for tr in dom('body>table>tr').items():
            img_src = tr('img').attr['src']
            category, img_file_name = os.path.split(img_src)

            # make category directories
            output_dir = PascalSentenceDataSet.SENTENCE_DIR + category
            if not os.path.isdir(output_dir):
                os.mkdir(output_dir)

            # dowonload sentences
            head, tail = os.path.splitext(img_file_name)
            sentence_file_name = head + ".txt"
            output = os.path.join(output_dir, sentence_file_name)
            if os.path.isfile(output):
                print ("Already downloaded, Skipping: %s" % output)
                continue
            print ("Downloading: %s" % output)
            with open(output,'w') as f:
                for td in tr('table tr td').items():
                    f.write(td.text() + "\n")

    def create_correspondence_data(self):
        dom = PyQuery(self.url)
        writer = csv.writer(open('correspondence.csv', 'w'))
        for i, img in enumerate(dom('img').items()):
            img_src = img.attr['src']
            print ("%d => %s" % (i + 1, img_src))
            writer.writerow([i + 1, img_src])

if __name__=="__main__":

    # create instance
    dataset = PascalSentenceDataSet()
    # download images
    dataset.download_images()
    # download sentences
    dataset.download_sentences()
    # create correspondence data by dataset
    dataset.create_correspondence_data()
