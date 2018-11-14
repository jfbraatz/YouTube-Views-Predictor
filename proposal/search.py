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

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  # Pets & Animals, Entertainment, Howto & Style, People & Blogs,
  # Film & Animation, Science & Technology, Gaming, Videoblogging,
  # News & Politics
  search_response = youtube.videos().list(
    # q=options.q,
    part='snippet,id',
    chart='mostPopular',
    regionCode='us',
    fields='nextPageToken,items(snippet/title,id)',
    videoCategoryId=24,
    maxResults=options.max_results
  ).execute()
  # search_response = youtube.search().list(
  #   q=options.q,
  #   order='viewCount',
  #   type='video',
  #   part='id,snippet',
  #   fields='items(snippet/title,id/videoId)',
  #   maxResults=options.max_results
  # ).execute()

  for search_result in search_response.get('items', []):
    print '%s (%s)' % (search_result['snippet']['title'],
                       search_result['id'])


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--q', help='Search term', default='Google')
  parser.add_argument('--max-results', help='Max results', default=5)
  args = parser.parse_args()

  try:
    youtube_search(args)
  except HttpError, e:
    print 'An HTTP error %d occurred:\n%s' % (e.resp.status, e.content)
