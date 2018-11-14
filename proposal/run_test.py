#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python search.py --q=surfing --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse
from math import log10

from secrets import DEVELOPER_KEY
from baseline import *
from oracle import *
import csv

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                developerKey=DEVELOPER_KEY)

def get_data(filename):
  results = []
  with open(filename, mode='r') as infile:
      reader = csv.reader(infile)
      next(reader, None) # skip header
      for rows in reader:
        yield (rows[1], rows[8], rows[3])
        # results.append((rows[1], rows[5], rows[9]))
  # return results

test_data = get_data('video_characteristics_upload.csv')
counter = 1
baseline_loss_avg = 0.0
oracle_loss_avg = 0.0
for video_id, title, channel_id in test_data:
  try:
    baseline_prediction = baseline(channel_id)
    oracle_prediction = oracle(title, channel_id)
    view_count = int(youtube.videos().list(
      id = video_id,
      part='statistics',
      fields='items/statistics/viewCount',
    ).execute()['items'][0]['statistics']['viewCount'])
    baseline_loss = log10(float(baseline_prediction)/view_count) ** 2
    oracle_loss = log10(float(oracle_prediction)/view_count) ** 2
    baseline_loss_avg = ((counter-1)*baseline_loss_avg + baseline_loss)/counter
    oracle_loss_avg = ((counter-1)*oracle_loss_avg + oracle_loss)/counter
    print counter
    print "Baseline: %d (Loss %f), Oracle: %d (Loss %f), True Value: %d" % (
      baseline_prediction,
      baseline_loss,
      oracle_prediction,
      oracle_loss,
      view_count)
    print "Baseline Avg Loss: %f, Oracle Avg Loss %f" % (baseline_loss_avg, oracle_loss_avg)
    counter += 1

  except Exception:
    continue
