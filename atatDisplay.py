import pygame
import os
from pygame.locals import *
from requests import get
from time import time
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

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

# def text_objects(text, font):
#     textSurface = font.render(text, True, black)
#     return textSurface, textSurface.get_rect()

# def message_display(text):
#     largeText = pygame.font.Font('freesansbold.ttf',115)
#     TextSurf, TextRect = text_objects(text, largeText)
#     TextRect.center = (800, y)
#     raspiDisplay.blit(TextSurf, TextRect)

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

raspiDisplay = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('ATAT')

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

bg = pygame.image.load(os.path.join(image_path, 'hothBG.png')).convert()

cockPit = pygame.image.load(os.path.join(image_path, 'ATATCockpit.png')).convert_alpha()

threshold_red = 21
threshold_green = 255
threshold_blue = 8

for x in range(cockPit.get_width()):
    for y in range(187, 405):
        color = cockPit.get_at((x, y))
        if color.r >= 0 and color.r <= 150 and color.g >= 140 and color.g <= 255 and color.b >= 0 and color.b <= 150:
            for x2 in range(x-1, x+1):
                for y2 in range(y-1, y+1):
                    cockPit.set_at((x2, y2), (0, 0, 0, 0))
for x in range(cockPit.get_width()):
    for y in range(187, 400):
        color = cockPit.get_at((x, y))
        if color.r >= 0 and color.r <= 150 and color.g >= 80 and color.g <= 255 and color.b >= 0 and color.b <= 150:
            if color.r < 40 and color.b < 60:
                for x2 in range(x-1, x+1):
                    for y2 in range(y-1, y+1):
                        cockPit.set_at((x2, y2), (color.r, color.g-30, color.b, color.a))


pygame.display.update()

gameExit = False
    
y = 480
black = (0,0,0)
bg_y = 0

while not gameExit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    raspiDisplay.fill((0,0,0))
    raspiDisplay.blit(bg, (0,bg_y))

    nprTitles = []
    raw_html = simple_get('https://www.npr.org/')
    html = BeautifulSoup(raw_html, 'html.parser')
    for i, h3 in enumerate(html.select('h3')):
        nprTitles.append(h3.text)

    if y == 200:
        y = 480
    font = pygame.font.SysFont('comicsansms', 16, bold=True)
    text0 = font.render(nprTitles[0], True,
            pygame.Color(0,0,0))
    text1 = font.render(nprTitles[1], True,
            pygame.Color(0,0,0))
    text2 = font.render(nprTitles[2], True,
            pygame.Color(0,0,0))
    text3 = font.render(nprTitles[3], True,
            pygame.Color(0,0,0))
    text4 = font.render(nprTitles[4], True,
            pygame.Color(0,0,0))
    raspiDisplay.blit(text0, (306,y))
    raspiDisplay.blit(text1, (306,y+40))
    raspiDisplay.blit(text2, (306,y+80))
    raspiDisplay.blit(text3, (306,y+120))
    raspiDisplay.blit(text4, (306,y+160))
    raspiDisplay.blit(cockPit, (0,0))
    pygame.display.flip()

    clock.tick(60)
    y -= 1

    if bg_y == 0:
        bg_y += 1
    if bg_y == 10:
        bg_y = 0
	

pygame.quit()
quit()