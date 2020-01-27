from InstagramAPI import InstagramAPI
from time import sleep
from random import randint
import json
import logging


def login_challenge(self, checkpoint_url):
    BASE_URL = 'https://www.instagram.com/'
    self.s.headers.update({'Referer': BASE_URL})
    req = self.s.get(BASE_URL[:-1] + checkpoint_url)
    self.s.headers.update({'X-CSRFToken': req.cookies['csrftoken'], 'X-Instagram-AJAX': '1'})
    self.s.headers.update({'Referer': BASE_URL[:-1] + checkpoint_url})
    mode = int(input('Choose a challenge mode (0 - SMS, 1 - Email): '))
    challenge_data = {'choice': mode}
    challenge = self.s.post(BASE_URL[:-1] + checkpoint_url, data=challenge_data, allow_redirects=True)
    self.s.headers.update({'X-CSRFToken': challenge.cookies['csrftoken'], 'X-Instagram-AJAX': '1'})

    code = input('Enter code received: ').strip()
    code_data = {'security_code': code}
    code = self.s.post(BASE_URL[:-1] + checkpoint_url, data=code_data, allow_redirects=True)
    self.s.headers.update({'X-CSRFToken': code.cookies['csrftoken']})
    self.cookies = code.cookies
    code_text = json.loads(code.text)
    if code_text.get('status') == 'ok':
        self.authenticated = True
        self.logged_in = True
    elif 'errors' in code.text:
        for count, error in enumerate(code_text['challenge']['errors']):
            count += 1
            logging.error('Session error %(count)s: "%(error)s"' % locals())
    else:
        logging.error(json.dumps(code_text))


username = 'sadfasfdasdf'  # your username
password = 'sdfasdfasdfasdf'  # your password
InstagramAPI.ver = login_challenge
api = InstagramAPI(username,password)
api.login()
print("First Login")
try:
    link = api.LastJson['challenge']['api_path']
    api.ver(link)
    api.login()
    print("Second Login")
    photo_path = 'test.jpg'
    #image = 'https://i.ibb.co/nLVqw8q/test.jpg'  # here you can put the image directory
    text = '¡Finalmente lo logramos!' + '\r\n'
    text = text + 'Ya somos afiliados de #Twitch . No dudes en seguirnos para no perderte ningun directo'
    text = text + '\r\n'
    text = text + '#gemagang #videojuegos #twitchparaguay #tpy'
    caption = text
    api.uploadPhoto(photo_path, caption=caption)
    print("Upload")
except:
    pass
