import praw
import urllib

reddit = praw.Reddit(client_id='asdfasdfasdf',
                     client_secret='asdfasdfasdf',
                     user_agent='asdfasdfasdf')

print(reddit.read_only)

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
            name = post.title.replace(" ", "_")
            with open(str(name)+'.jpg','wb') as f:
                f.write(img)
