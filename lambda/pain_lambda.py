from datetime import datetime
import json
import re
import pyrebase

config = {
  'apiKey': 'AIzaSyAgJEKrEdc6Gv6Cwp3ANODIzymloPWJM_s',
  'authDomain': 'intense-fire-8265.firebaseapp.com',
  'databaseURL': 'https://intense-fire-8265.firebaseio.com',
  'projectId': 'intense-fire-8265',
  'storageBucket': 'intense-fire-8265.appspot.com',
  'messagingSenderId': '301339768416',
}

firebase = pyrebase.initialize_app(config)

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

def pushMessage(user, type, reason = False, note = None, isLearning = False, date = None) :
  if type :
    message = {
      'reason': reason if reason else 'unknown',
      'note': note,
      'isLearning': isLearning,
      'type': type,
      'date': (date if date else datetime.now()).isoformat()
    }
    userMessages = resource('users/' + user['localId'] + '/pain');
    allMessages = resource('pain');
    for i in [userMessages, allMessages] :
      i.push(message);

def setReason(user, reason, note, isLearning = False) :
  current = getCurrentReason(user)
  if current :
    pushMessage(user, 'DUN', current, note, isLearning)
  getUserData(user).child('currentReason').set(reason)
  pushMessage(user, 'MUX', reason, note, isLearning)

def wtf(user, reason, note, isLearning) :
  pushMessage(user, 'WTF', reason if reason else getCurrentReason(user), note)

def yay(user, reason, note, isLearning) :
  pushMessage(user, 'YAY', reason if reason else getCurrentReason(user), note)

def handleRequest(event, context) :
  body = json.loads(event['body'])
  user = auth.sign_in_with_email_and_password(body['email'], body['password'])
  typeVal = body.get('type', event['pathParameters']['proxy'])
  return {
    'yay': yay,
    'wtf': wtf,
    'mux': setReason
  }.get(typeVal.lower(), lambda x, y, z: x)(
    user,
    body.get('reason', None),
    body.get('note', None),
    body.get('isLearning', None)
  )
