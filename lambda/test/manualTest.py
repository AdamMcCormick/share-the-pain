import os

from ..pain_lambda import handleRequest as handler
payload = json.load(open('yay.json'))

os.environ = {
  'stage': 'dev',
  'apiKey': 'AIzaSyAgJEKrEdc6Gv6Cwp3ANODIzymloPWJM_s',
  'authDomain': 'intense-fire-8265.firebaseapp.com',
  'databaseURL': 'https://intense-fire-8265.firebaseio.com',
  'projectId': 'intense-fire-8265',
  'storageBucket': 'intense-fire-8265.appspot.com',
  'messagingSenderId': '301339768416',
}

print(handler(payload, {}))
