import requests
from os import environ
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from .get import *
from ruqqus.__main__ import db

def thumbnail_thread(pid):

    post=get_post(pid)

    #step 1: see if post is image

    print("thumbnail thread")

    domain_obj=post.domain_obj

    if domain_obj and domain_obj.show_thumbnail:
        print("image post")
        x=requests.head(post.url)

        if x.headers.get("Content-Type","/").split("/")[0]=="image":
            post.is_image=True
            db.add(post)
            db.commit()

            return

##    url=f"https://api.apiflash.com/v1/urltoimage"
##    params={'access_key':environ.get("APIFLASH_KEY"),
##            'format':'png',
##            'height':720,
##            'width':1280,
##            'response_type':'image',
##            'thumbnail_width':600,
##            'url': post.embed_url if post.embed_url else post.url,
##            'css':"iframe {display:none;}"
##            }


    x=requests.get(post.url)
    
    if x.status_code != 200 or not x.headers["Content-Type"].startswith("text/html"):
        print('not html post')
        return

    soup=BeautifulSoup(x.content, 'html.parser')
    img=soup.find('img')
    if not img:
        print('no image in doc')
        return

    src=img['src']
    if not src.startswith("https://"):
        parsed_url=urlparse(post.url)
        src=f"https://{parsed_url.netloc}/{src.lstrip('/')}"

    
    x=requests.get(src, params=params)
    print("have first image")

    if x.status_code!=200:
        print('no image')
        return

    name=f"posts/{post.base36id}/thumb.png"
    tempname=name.replace("/","_")

    with open(tempname, "wb") as file:
        for chunk in x.iter_content(1024):
            file.write(chunk)

    print("thumb saved")

    aws.upload_from_file(name, tempname)
    post.has_thumb=True
    db.add(post)
    db.commit()

    print("thumb all success")
