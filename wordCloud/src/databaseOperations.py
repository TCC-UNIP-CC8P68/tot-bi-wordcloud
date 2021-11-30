import psycopg2
import base64
import os
from io import BytesIO

def getUserEmail(cur, userId):
  cur.execute(f'SELECT DISTINCT "email" FROM "Users" WHERE "id" = {userId[0]}')
  return cur.fetchone()

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

def insertWordCloud(cur, userId, email, wordCloud):
  buffered = BytesIO()
  wordCloud.save(buffered, format="PNG")
  imgStr = base64.b64encode(buffered.getvalue())
  decodedStr = imgStr.decode('utf-8')

  cur.execute("INSERT INTO \"WordClouds\" VALUES (%s, %s, %s)", (userId[0], decodedStr, email))


def updateWordCloud(cur, userId, wordCloud):
  buffered = BytesIO()
  wordCloud.save(buffered, format="PNG")
  imgStr = base64.b64encode(buffered.getvalue())
  decodedStr = imgStr.decode('utf-8')

  cur.execute(f'UPDATE "WordClouds" SET "wordCloud" = \'{decodedStr}\' WHERE "userId" = {userId[0]}')

def saveWordCloud(cur, userId, wordCloud):
  cur.execute(f'SELECT COUNT("wordCloud") FROM "WordClouds" WHERE "userId" = {userId[0]}')
  userHasWordCloud = cur.fetchone()[0]
  userEmail = getUserEmail(cur, userId)

  if userHasWordCloud == 0:
    insertWordCloud(cur, userId, userEmail, wordCloud)
  else:
    updateWordCloud(cur, userId, wordCloud)
