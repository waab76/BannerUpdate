#!/usr/local/bin/python3
# coding: utf-8

'''
Created on Mar 29, 2020

@author: rcurtis
'''
import logging

logging.basicConfig(filename='BannerBot.log', level=logging.DEBUG, 
                    format='%(asctime)s :: %(levelname)s :: %(threadName)s :: %(module)s:%(funcName)s :: %(message)s ', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')
import os
import praw

from datetime import datetime
from utils.imgur_helper import download_as
from utils.reddit_helper import css_sheet, reddit, subreddit
from PIL import Image

banner_image_name = "banner.jpg"
sidebar_image_name = "sidebar-img.jpg"

def exec_update():
    logging.info('Connected to Reddit instance as [%s]', reddit.user.me())
    
    workingDir = './winners'
    if not os.path.isdir(workingDir):
        logging.info('Creating working directory [%s]', workingDir)
        os.makedirs(workingDir)
    files = os.listdir(workingDir)
    
    logging.info('Clean up old banner and sidebar files if they exist')
    if os.path.isfile(os.path.join(workingDir, banner_image_name)):
        logging.info('Removing old banner image')
        os.remove(os.path.join(workingDir, banner_image_name))
    if os.path.isfile(os.path.join(workingDir, sidebar_image_name)):
        logging.info('Removing old sidebar image')
        os.remove(os.path.join(workingDir, sidebar_image_name))
    
    logging.info('Fetch winning images')
    winners = subreddit.search(query="weekly contest results", sort="new", time_filter="month")
    for winner in winners:
        titleDate = winner.title[40:]
        winnerDate = datetime.strptime(titleDate, "%B %d, %Y")
        winnerFilename = winnerDate.strftime("%Y-%m-%d") + '.jpg'
        if not winnerFilename in files:
            logging.info('Downloading [%s]', winnerFilename)
            firstIndex = winner.selftext.find('1st')
            lastIndex = winner.selftext.find('votes')
            imgurLink = winner.selftext[firstIndex:lastIndex].split(" ")[4]
            download_as(imgurLink, os.path.join(workingDir, winnerFilename))
        else:
            logging.info('[%s] already exists, not downloading', winnerFilename)
    
    logging.info('Generate new sidebar image')
    inputFileList = os.listdir(workingDir)
    srcFileList = []
    for filename in inputFileList:
        filename = filename.lower()
        if filename.count('.jpg') > 0:
            srcFileList.append(filename)
    srcFileList = reversed(sorted(srcFileList))
    for srcFile in srcFileList:
        logging.info('Creating sidebar image from [%s]', srcFile)
        srcFileName = os.path.join(workingDir, srcFile)
        sidebarSourceImage = Image.open(srcFileName)
        size = 512,512
        sidebarSourceImage.thumbnail(size)
        sidebarSourceImage.save(os.path.join(workingDir, sidebar_image_name), "JPEG")
        break
    
    logging.info('Generate new banner image')
    bannerSize = 1920, 256
    bannerImage = Image.new('RGB', bannerSize)
    startPixel = 0
    skippedLatest = 0
    inputFileList = os.listdir(workingDir)
    
    srcFileList = []
    for filename in inputFileList:
        filename = filename.lower()
        if filename.count('.jpg') > 0:
            srcFileList.append(filename)
    srcFileList = reversed(sorted(srcFileList))
    
    for srcFile in srcFileList:
        if skippedLatest < 2:
            print('Skipping ', srcFile)
            skippedLatest += 1
            continue
        
        if startPixel < bannerSize[0]:
            srcImage = Image.open(os.path.join(workingDir, srcFile))
            srcImage.thumbnail(bannerSize)
        
            cropBox = (0, 0, srcImage.size[0], srcImage.size[1])
            region = srcImage.crop(cropBox)
        
            pasteBox = (startPixel, 0, startPixel + srcImage.size[0], 256)
            bannerImage.paste(region, pasteBox)
        
            startPixel += srcImage.size[0]
        else:
            logging.info('Probably need to delete [%s]', srcFile)
        
    bannerImage.save(os.path.join(workingDir, banner_image_name))
    
    bannerImage.save(os.path.join(workingDir, banner_image_name))
    
    logging.info('Update the subreddit')
    stylesheet = subreddit.stylesheet

    # Update the sidebar image
    stylesheet.delete_image("sidebar-img")
    stylesheet.upload("sidebar-img", os.path.join(workingDir, sidebar_image_name))

    # Update the banner image
    stylesheet.delete_image("banner")
    stylesheet.upload("banner", os.path.join(workingDir, banner_image_name))

    # Trigger the update
    stylesheet.update(css_sheet, "Auto-updating sidebar/banner")

    # Update the sidebar widget (New Reddit)
    widgets = subreddit.widgets
    image_widget = None

    for widget in widgets.sidebar:
        if isinstance(widget, praw.models.ImageWidget):
            image_widget = widget
            break

    imageData = [{'width': 1000, 'height': 1000, 'linkUrl': '',
             'url': widgets.mod.upload_image(os.path.join(workingDir, sidebar_image_name))}]
    image_widget.mod.update(data=imageData)

    # Update the banner (New Reddit)
    stylesheet.upload_banner(os.path.join(workingDir, banner_image_name))

    
if __name__ == '__main__':
    exec_update()