from tkinter import *
from requests import get
from time import time
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from PIL import ImageTk,Image, ImageFont, ImageDraw


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

master = Tk()
canvas = Canvas(master, width=1280, height=720)
image = ImageTk.PhotoImage(Image.open("C:\\Users\\NicholasHinds\\Desktop\\RasPi_Display_Project_Python\\hothBG.png"))                           
canvas.create_image(0, 0, anchor = NW, image = image)
canvas.pack()
y = 205
delta = 100
delay = 0
raw_html = simple_get('https://www.npr.org/')
html = BeautifulSoup(raw_html, 'html.parser')
for i, h3 in enumerate(html.select('h3')):
    if y == 400:
        y = 205
    canvas.create_text(800, y, text=h3.text)
    y += 10 
mainloop()