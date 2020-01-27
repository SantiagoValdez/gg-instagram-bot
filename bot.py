from InstagramAPI import InstagramAPI
from time import sleep
from random import randint
import json
import logging
import praw
import urllib
from dotenv import load_dotenv
import os


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

load_dotenv()

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
client_id = os.getenv("R_CLIENT_ID")
client_secret = os.getenv("R_SECRET")
user_agent = os.getenv("R_U_AGENT")

reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)

print(reddit.read_only)
photos = []
desc = []
for post in reddit.subreddit('gamingphotography').top('day'):
    print(post.title)
    if str(post.url).endswith('.jpg'):
            print("Termina en jpg")
            try:
                response = urllib.request.urlopen(post.url)
            except Exception as e:
                print("Error")
                print(e)
                break
            img = response.read()
            name = post.title.replace(" ", "_") + '.jpg'
            with open(name,'wb') as f:
                f.write(img)
                photos.append(name)
                desc.append(post.title)

print(photos)
print(desc)

InstagramAPI.ver = login_challenge
api = InstagramAPI(username,password)
api.login()
print("First Login")
try:
    link = api.LastJson['challenge']['api_path']
    api.ver(link)
    api.login()
    print("Second Login")
    i=0
    for photo in photos:
        photo_path = photo
        #image = 'https://i.ibb.co/nLVqw8q/test.jpg'  # here you can put the image directory
        text = desc[i] + '\r\n'
        text = text + '#gemagang #videojuegos #twitchparaguay #tpy #gamer #gaming #paraguay'
        caption = text
        api.uploadPhoto(photo_path, caption=caption)
        print("Upload")
        os.unlink(photo) #Delete photo on upload
except:
    pass
