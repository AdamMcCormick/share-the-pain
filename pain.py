from datetime import datetime
import re
import pyrebase

email = 'alanbly@gmail.com';
password = 'u7NV*(Djpcn%7aCgtcAqMdxGS)Y^SX'

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

user = auth.sign_in_with_email_and_password(email, password)

def getUserData() :
  return resource('users/' + user['localId'] + '/metadata');

def getCurrentReason() :
  userData = getUserData()
  if not userData :
    return None;
  metadata = userData.get().val()
  return metadata['currentReason'] if metadata and 'currentReason' in metadata else None;

def pushMessage(type, reason = False, isLearning = False, date = datetime.now()) :
  if type :
    message = {
      'reason': reason if bool(reason) else 'unknown',
      'isLearning': isLearning,
      'type': type,
      'date': date.isoformat(),
    }
    userMessages = resource('users/' + user['localId'] + '/pain');
    allMessages = resource('pain');
    for i in [userMessages, allMessages] :
      i.push(message);

def setReason(reason, isLearning = False) :
  current = getCurrentReason()
  if current :
    pushMessage('DUN', current)
  getUserData().child('currentReason').set(reason)
  pushMessage('MUX', reason, isLearning)

def wtf(reason = getCurrentReason()) :
  pushMessage('WTF', reason)

def yay(reason = getCurrentReason()) :
  pushMessage('YAY', reason)
