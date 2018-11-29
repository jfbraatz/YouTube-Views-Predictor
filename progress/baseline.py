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

def baseline(channel_id):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  number_to_avg_over = 5

  search_response = youtube.search().list(
      channelId=channel_id,
      type='video',
      order='date',
      part='id',
      fields='items(id/videoId)',
      maxResults=number_to_avg_over
  ).execute()
  ids = [result['id']['videoId']
         for result in search_response.get('items',[])]

  most_recent_videos = youtube.videos().list(
      id=','.join(ids),
      part='statistics',
      fields='items/statistics/viewCount',
  ).execute()

  most_recent_view_counts = [int(result['statistics']['viewCount'])
                             for result in most_recent_videos['items']]
  prediction = sum(most_recent_view_counts) / len(most_recent_view_counts)

  # print "Prediction: %d" % prediction
  return prediction

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--title', help='Candidate Title', default='Google')
  parser.add_argument('--channel-id', help='Channel ID')
  args = parser.parse_args()

  try:
    baseline(args.channel_id)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
