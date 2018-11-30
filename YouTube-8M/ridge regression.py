# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 20:37:12 2018

@author: Lance
"""

from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge

df = pd.read_csv('video_stats.csv', encoding = "ISO-8859-1")
df['PublishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
df = df.dropna()
df['logViews'] = np.log(df['viewCount']+1)

channels = {}
for _, video in df.iterrows():
    channel_id = video['channel Id']
    if not channel_id in channels:
        channels[channel_id] = [video]
    else:
        channels[channel_id].append(video)
for channel_id in channels:
    channels[channel_id] = sorted(channels[channel_id], key=lambda v: v['PublishedAt'])
    
def prediction_answer_and_feature_extractor(channel, n):
    """
    I'm assuming the thing that's passed in is a list of videos,
    in other words a channel is a value in the channels dict.
    This also assumes that 
    
    This takes one of those entries and returns a tuple, one value of which
    is the correct view count that we want to predict for the most recent video
    posted to the channel, and the second is a dictionary containing feature names
    and feature values of the previous 10 videos before the most recent one.
    """
    if len(channel) < n+1:
        raise Exception("Not enough videos in channel to create a feature vector.")
        
    video_stat_names = ['likeCount', 'dislikeCount', 'viewCount', 
                        'favoriteCount', 'commentCount']
    correct_prediction = channel[-1]['logViews']
    feature_values = []
    feature_names = []
    for i in range(-2,-n-2,-1):
        feature_values += list(channel[i][video_stat_names])
        feature_names += [name + "%d"%(i+1) for name in video_stat_names]
    return (correct_prediction, dict(zip(feature_names, feature_values)))

prolific_channels = {k:v for k, v in channels.items() if 11 < len(v)}

data = []
for channel_id, vids in prolific_channels.items():
    
    answer, vid_features = prediction_answer_and_feature_extractor(vids, 10)
    vid_features['trueViewCount'] = answer
    data.append(vid_features)
    
from xgboost import XGBRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

features = ['likeCount', 'dislikeCount', 'viewCount', 
                        'favoriteCount', 'commentCount']
real_features = [name+'-%d'%i for i in range(1,11) for name in features]
df = pd.DataFrame(data)
df = df.dropna()
X = df[real_features]
y = df['trueViewCount']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)


n_samples, n_features = 10, 5
np.random.seed(0)
y = np.random.randn(n_samples)
X = np.random.randn(n_samples, n_features)

clf = Ridge(alpha=1.0)
clf.fit(X_train, y_train)

print (clf.get_params())

ridge_pred = clf.predict(X_test)

plot_df = pd.DataFrame(ridge_pred, columns=['Predictions'])
plot_df['True'] = np.array(y_test)
sns.regplot(x='Predictions', y='True', data=plot_df)
    
 
print (mean_squared_error(y_test,ridge_pred))













