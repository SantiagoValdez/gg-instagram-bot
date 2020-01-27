from instapy_cli import client


import subprocess
subprocess.call("firefox  'https://google.com'", shell=True)

username = 'sadfasdfasdf'  # your username
password = 'sdfasfdasdfasdf'  # your password
image = 'https://i.ibb.co/nLVqw8q/test.jpg'  # here you can put the image directory
text = '¡Finalmente lo logramos!' + '\r\n'
text = text + 'Ya somos afiliados de #Twitch . No dudes en seguirnos para no perderte ningun directo'
text = text + '\r\n'
text = text + '#gemagang #videojuegos #twitchparaguay #tpy'
with client(username, password) as cli:
    cookies = cli.get_cookie()
    try:
        cli.upload(image, text)
    except Exception as e:
        print("EXCEPTION:")
        print(e)
        
        
