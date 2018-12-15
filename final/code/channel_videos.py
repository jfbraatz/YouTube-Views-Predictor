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


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyB6VBJRsj7OmbabT_pQHXzrkcuDPmmCdnU'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

def most_recent_video_stats(channel_id, max_results):

  # Call the search.list method to retrieve results matching the specified
  # query term.
  # Pets & Animals, Entertainment, Howto & Style, People & Blogs,
  # Film & Animation, Science & Technology, Gaming, Videoblogging,
  # News & Politics
  search_response = youtube.search().list(
    channelId=channel_id,
    order='date',
    type='video',
    part='id',
    fields='items(id/videoId)',
    maxResults=max_results
  ).execute()

  video_ids = [result['id']['videoId'] for result in search_response['items']]
  search_response = youtube.videos().list(
          id=','.join(video_ids),
          part='snippet,id,statistics',
          #fields='items(snippet/title,id)',
          ).execute()

  channel_stats = {}
  for item in search_response['items']:
      channel_stats[item['id']] = item['statistics']
      channel_stats[item['id']].update({
          'title': item['snippet']['title'],
          'description': item['snippet']['description'],
          'publishedAt': item['snippet']['publishedAt']
          })

  return channel_stats


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--channel-id', help='Search term', default='Google')
  parser.add_argument('--max-results', help='Max results', default=10)
  args = parser.parse_args()

  try:
    print most_recent_video_stats(args.channel_id, args.max_results)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
