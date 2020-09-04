
# Sfybook
---
# Introduction
---
Sfybook is a library for interaction with mbasic.facebook, using scraping and parsing methods with the goal of packing all mbasic.facebook in a simple library


## New methods on the way!
---
The library is in development and I have a lot of new methods cooking, which will be used to

- Interact with the chat, groups..
- Search for friends, pages, etc
- Download videos, images

and many other things!

## Installation
---
For the moment there are no plans to upload it to PyPi  until the library has advanced but you can clone the repository with a simple command.
```sh
$ git clone https://github.com/Scr44gr/sfybook.git
```
... remember to install the requirements!
```sh
$ pip install -r requirements.txt
```
## Usage
---
### Authentication
---
```python
from sfybook.client import Client
client = Client()
client.auth.login(email, password)
```
### Submit a post on the current user profile
---
```python
...
client.post("Hello world")
# An if we want to submit a post with an image, we can use the param image.
client.post("Hello world", image=r"./root/image.png")
# Or we can also submit a post with a list of images with the param images.
images = [r"./root/image.png", r"./root/image_2.png"]
client.post("Hello world", images=images)
```
### Submit a post on a facebook page
---
```python
...
from sfybook.mbasic_home_header import Pages
pages_header = Pages(client)
pages = pages_header.my_pages()
for page in pages:
    if page.name == 'My Page Name':
        page.post("Hello World")
```
## Avoiding Re-login
---
To avoid having to log in again every time we run our script, we can save the cookies containing our session and load them whenever we want.

The saved auth cookie can be reused for up to 90 days.
## Saving the auth_cookies
```python
from sfybook.client import Client

client = Client()
client.auth.login(email, password)
filename = "./root/filename.json"
client.save_session(filename=filename)
```
---
## Loading the auth_cookies
```python
from sfybook.client import Client

client = Client()
filename = "./root/filename.json"
client.load_session(filename=filename)
```
---
## Donate
---
If you like it you can buy me a coffee! [https://www.buymeacoff.ee/scr44gr](https://www.buymeacoff.ee/scr44gr)

[![Build](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoff.ee/scr44gr)

## Legal
---
Disclaimer: This is not affliated, endorsed or certified by Facebook. This is an independent Library. **Strictly not for spam**. Use at your own risk.
