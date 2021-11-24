import psycopg2
import base64
import os
from io import BytesIO

def getDistinctUserIds(cur):
  cur.execute('SELECT DISTINCT "userId" FROM "Captures"')
  return cur.fetchall()

def getUserCapturedUrls(cur, userId):
  cur.execute(f'SELECT "capturedUrl" FROM "Captures" WHERE "userId" = {userId[0]}')
  return cur.fetchall()

def insertTopSites(cur, userId, topSites):
  cur.execute(f'INSERT INTO "TopSites" VALUES({userId[0]}, \'{topSites}\')')

def updateTopSites(cur, userId, topSites):
  cur.execute(f'UPDATE "TopSites" SET "topSites" = \'{topSites}\' WHERE "userId" = {userId[0]}')

def countUserTopSites(cur, userId):
  cur.execute(f'SELECT COUNT("userId") FROM "TopSites" WHERE "userId" = {userId[0]}')
  return cur.fetchone()

def getCapturedTags(cur, userId):
  cur.execute(f'SELECT "capturedTags" FROM "Captures" WHERE "userId"  = {userId[0]} AND "capturedTags" IS NOT NULL')
  return cur.fetchall()

def insertWordCloud(cur, userId, wordCloud):
  buffered = BytesIO()
  wordCloud.save(buffered, format="PNG")
  img_str = base64.b64encode(buffered.getvalue())

  cur.execute("INSERT INTO \"WordClouds\" VALUES (%s, %s)", (userId, img_str))


def updateWordCloud(cur, userId, wordCloud):

  print(wordCloud)
  # img_str = base64.b64encode(wordCloud)


  # cur.execute(f'UPDATE "WordClouds" SET "wordCloud" = \'{img_str}\' WHERE "userId" = {userId[0]}')

