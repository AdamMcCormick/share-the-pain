from datetime import datetime
import json
import re
import os
import pyrebase

firebase = pyrebase.initialize_app(os.environ)

auth = firebase.auth()

def resource(path, base = None) :
  base = base if base else firebase.database();
  segment, subPath = re.sub(r'/+', '/', re.sub(r'^/', '', path)).partition('/')[::2]
  #print('"' + base.path + '"', '"' + segment + '"', '"' + subPath + '"')
  return base if not segment else resource(subPath, base.child(segment))

def getUserData(user) :
  return resource('users/' + user['localId'] + '/metadata');

def getCurrentReason(user) :
  userData = getUserData(user)
  if not userData :
    return None;
  metadata = userData.get().val()
  return metadata['currentReason'] if metadata and 'currentReason' in metadata else None;

def failure(typeVal, event) :
  return lambda user, reason, note, isLearning: {
    'isBase64Encoded': False,
    'statusCode': 404,
    'headers': {
      'Content-Type': 'text/plain'
    },
    'body': 'Call failed, resource ' + typeVal + ' not found'
  }

def pushMessage(user, type, reason = False, note = None, isLearning = False, date = None) :
  if type :
    message = {
      'reason': reason if reason else 'unknown',
      'note': note,
      'isLearning': isLearning,
      'type': type,
      'date': (date if date else datetime.now()).isoformat()
    }
    userMessages = resource('users/' + user['localId'] + '/pain')
    userMessages.push(message)
    allMessage = message.copy()
    allMessage['user'] = user['localId']
    allMessages = resource('pain')
    allMessages.push(allMessage)
  return {
    "isBase64Encoded": False,
    "statusCode": 200,
    "headers": {},
    "body": None
  }

def setReason(user, reason, note, isLearning = False) :
  current = getCurrentReason(user)
  if current :
    pushMessage(user, 'DUN', current, note, isLearning)
  getUserData(user).child('currentReason').set(reason)
  return pushMessage(user, 'MUX', reason, note, isLearning)

def wtf(user, reason, note, isLearning) :
  return pushMessage(user, 'WTF', reason if reason else getCurrentReason(user), note)

def yay(user, reason, note, isLearning) :
  return pushMessage(user, 'YAY', reason if reason else getCurrentReason(user), note)

def handleRequest(event, context) :
  body = json.loads(event['body'])
  user = auth.sign_in_with_email_and_password(body['email'], body['password'])
  typeVal = body.get('type', event['path'])
  return {
    'yay': yay,
    '/yay': yay,
    'wtf': wtf,
    '/wtf': wtf,
    'mux': setReason,
    '/mux': setReason
  }.get(typeVal.lower(), failure(typeVal, event))(
    user,
    body.get('reason', None),
    body.get('note', None),
    body.get('isLearning', None)
  )
