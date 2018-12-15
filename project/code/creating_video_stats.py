# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 19:54:35 2018

@author: Lance
"""
import csv
import channel_videos
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import seaborn as sns

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#% matplotlib inline

df = pd.read_csv('channelStats.csv')
df.columns

print ('colletcing stats for', len(df['Channel Id']), 'channels' )

print ('loaded .csv file')

invalid_channel_ids = 0
unicode_errors = 0
i = 0

with open('newfile.csv', mode = 'w') as new_file:
    feature_names = []
    video_stat_names = ['viewCount','likeCount','dislikeCount','favoriteCount','commentCount', 'title','description','publishedAt', 'video Id','channel Id','title similarity']
    feature_names += [name for name in video_stat_names]
    newfile_writer = csv.DictWriter(new_file, fieldnames=feature_names,lineterminator = '\n')
    newfile_writer.writeheader()
    
    for x in df['Channel Id']:
            try:
                row = channel_videos.most_recent_video_stats(x, 25)
            except:
                invalid_channel_ids += 1
                continue
            i += 1
            # feature vector is the last ten videos [viewcount from 1st video, lilecount from first
            # from first video, dislike count, favoritecount, commentCount  .... viewcount from 1st video 
            # likecount, viewcount ]
            first_video_title = ''
            first  = 0
            for video in row.keys():
                if first == 0:
                    first += 1
                    first_video_title = video
                
                row[video]['title similarity'] = str(similar(first_video_title, video))
                row[video]['video Id'] = video
                row[video]['channel Id'] = x
                try:
                    newfile_writer.writerow(row[video])
                except:
                    unicode_errors += 1
            if (i%200 == 0):  
                print ('added video stats for ', i, 'channels')
                

print ('invalid_channel_ids = ',invalid_channel_ids)
print ('unicode_errors = ',unicode_errors )
print ('done')
