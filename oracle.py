#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from secrets import DEVELOPER_KEY

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def oracle(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=options.title,
    type='video',
    part='id,snippet',
      fields='items(snippet/title,snippet/channelId,id/videoId)',
    maxResults=50
  ).execute()

  real_channel_view_count = int(youtube.channels().list(
      id=options.channel_id,
      part='statistics',
      fields='items/statistics/viewCount',
  ).execute()['items'][0]['statistics']['viewCount'])

  ids = [result['snippet']['channelId']
                   for result in search_response.get('items',[])]
  channel_response = youtube.channels().list(
      id=','.join(ids),
      part='statistics',
      fields='items(id,statistics/viewCount)',
      maxResults=50
  ).execute()

  search_results = search_response.get('items', [])
  channel_results = channel_response.get('items', [])
  min_difference = 1000000000
  channel_view_counts = {item['id']: int(item['statistics']['viewCount'])
                         for item in channel_results}
  for i in range(len(search_results)):

      title = search_results[i]['snippet']['title']
      videoId = search_results[i]['id']['videoId']
      if ids[i] == options.channel_id and title == options.title:
        continue # for testing against existing videos
      channelViewCount = channel_view_counts[ids[i]]
      if abs(channelViewCount - real_channel_view_count)  < min_difference:
          min_difference = abs(channelViewCount - real_channel_view_count)
          min_index = i
      print '%s (Id %s, ChannelViews %s)' % (
          title, videoId, channelViewCount)
  prediction = int(youtube.videos().list(
      id=search_results[min_index]['id']['videoId'],
      part='statistics',
      fields='items(statistics/viewCount)',
  ).execute()['items'][0]['statistics']['viewCount'])
  print "Prediction: %d (from %s)" % (
    prediction, search_results[min_index]['snippet']['title'])



if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--title', help='Candidate Title', default='Google')
  parser.add_argument('--channel-id', help='Channel ID')
  args = parser.parse_args()

  try:
    oracle(args)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
