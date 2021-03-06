import pygame
import os
import time
from pygame.locals import *
from requests import get
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


pygame.init()
pygame.font.init()
clock = pygame.time.Clock()

# raspiDisplay = pygame.display.set_mode((800, 600))
raspiDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('ATAT')

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

bg = pygame.image.load(os.path.join(image_path, 'hothBG.png')).convert()

cockPit = pygame.image.load(os.path.join(image_path, 'ATATCockpit.png')).convert_alpha()

threshold_red = 21
threshold_green = 255
threshold_blue = 8

for x in range(cockPit.get_width()):
    for y in range(100, 405):
        color = cockPit.get_at((x, y))
        if color.r >= 0 and color.r <= 150 and color.g >= 140 and color.g <= 255 and color.b >= 0 and color.b <= 150:
            for x2 in range(x-1, x+1):
                for y2 in range(y-1, y+1):
                    cockPit.set_at((x2, y2), (0, 0, 0, 0))
for x in range(cockPit.get_width()):
    for y in range(100, 400):
        color = cockPit.get_at((x, y))
        if color.r >= 0 and color.r <= 150 and color.g >= 80 and color.g <= 255 and color.b >= 0 and color.b <= 150:
            if color.r < 40 and color.b < 60:
                for x2 in range(x-1, x+1):
                    for y2 in range(y-1, y+1):
                        cockPit.set_at((x2, y2), (color.r, color.g-30, color.b, color.a))


pygame.display.update()

gameExit = False
    
y = 300
black = (0,0,0)
bg_y = -720
countTitles = 0
countWalkX = 0
countWalkY = 0
walkX = -760
walk = walkX
titleA = 0
titleB = 1
titleC = 2
titleD = 3
titleE = 4
titleF = 5
titleG = 6

# raspiDisplay.blit(bg, (walkX ,bg_y))

while not gameExit:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
    raspiDisplay.fill((0,0,0))
    
    if countWalkX < 40:
        walk += 2
    elif countWalkX > 40 and countWalkX < 70:
        walk -= 2
    elif countWalkX == 70:
        countWalkX = 0

    if countWalkY < 10:
        bg_y += 2
    elif countWalkY > 10 and countWalkY < 20:
        bg_y -= 2
    elif countWalkY == 20:
        countWalkY = 0

    raspiDisplay.blit(bg, (walk, bg_y))

    countWalkX += 1
    countWalkY += 1
    
    nprTitles = []
    raw_html = simple_get('https://www.npr.org/')
    html = BeautifulSoup(raw_html, 'html.parser')
    for i, h3 in enumerate(html.select('h3')):
        temp = str(h3.text)
        if len(temp) > 40:
           tempA = temp[:40] + "-"
           tempB = temp[40:]
           nprTitles.append(tempA)
           nprTitles.append(tempB)
        else:
           nprTitles.append(temp)

    localtime = time.localtime()

    h = localtime.tm_hour
    m = str(localtime.tm_min)
    s = str(localtime.tm_sec)
    
    if localtime.tm_hour > 12:
        h = h - 12

    h = str(h)

    if localtime.tm_hour < 10:
        h = "0"+h

    if localtime.tm_min < 10:
        m = "0"+m

    if y <= -60:
        y = 300
    font = pygame.font.SysFont('comicsansms', 24, bold=True)
    fontTime = pygame.font.SysFont('comicsansms', 36, bold=True)

    t0 = nprTitles[titleA]
    t1 = nprTitles[titleB]
    t2 = nprTitles[titleC]
    t3 = nprTitles[titleD]
    t4 = nprTitles[titleE]
    t5 = nprTitles[titleF]
    t6 = nprTitles[titleG]

    text0 = font.render(t0, True,
            pygame.Color(0,0,0))
    text1 = font.render(t1, True,
            pygame.Color(0,0,0))
    text2 = font.render(t2, True,
            pygame.Color(0,0,0))
    text3 = font.render(t3, True,
            pygame.Color(0,0,0))
    text4 = font.render(t4, True,
            pygame.Color(0,0,0))
    text5 = font.render(t5, True,
            pygame.Color(0,0,0))
    text6 = font.render(t6, True,
            pygame.Color(0,0,0))

    hourText = fontTime.render(h, True,
            pygame.Color(0,0,0))
    minuteText = fontTime.render(m, True,
            pygame.Color(0,0,0))
    secondsText = fontTime.render(s, True,
            pygame.Color(0,0,0))

    raspiDisplay.blit(text0, (186,y))
    raspiDisplay.blit(text1, (186,y+60))
    raspiDisplay.blit(text2, (186,y+120))
    raspiDisplay.blit(text3, (186,y+180))
    raspiDisplay.blit(text4, (186,y+240))
    raspiDisplay.blit(text5, (186,y+300))
    raspiDisplay.blit(text6, (186,y+360))
    raspiDisplay.blit(hourText, (10, 173))
    raspiDisplay.blit(minuteText, (10, 232))
    raspiDisplay.blit(secondsText, (10, 292))
    raspiDisplay.blit(cockPit, (0,0))
    pygame.display.flip()

    countTitles += 1
    

    if countTitles == 90:
        titleA += 7
        titleB += 7
        titleC += 7
        titleD += 7
        titleE += 7
        titleF += 7
        titleG += 7

        if titleA > len(nprTitles) - 1 or titleB > len(nprTitles) - 1 or titleC > len(nprTitles) - 1 or titleD > len(nprTitles) - 1 or titleE > len(nprTitles) - 1 or titleF > len(nprTitles) - 1 or titleG > len(nprTitles) - 1:
            titleA = 0
            titleB = 1
            titleC = 2
            titleD = 3
            titleE = 4
            titleF = 5
            titleG = 6

        countTitles = 0
        
    

    clock.tick(60)
    y -= 4

    if bg_y == 0:
        bg_y += 1
    if bg_y == 10:
        bg_y = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()	

pygame.quit()
quit()
