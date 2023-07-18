import cv2 as cv
import numpy as np
from time import sleep
import win32gui, win32con, win32ui
from win32api import SetCursorPos
import pydirectinput as pd
import urllib3
import requests
import json

pd.PAUSE = 0
urllib3.disable_warnings()
pd.FAILSAFE = False

#Accounname
sName = ''

def getDeaths(name):
    request = requests.get("https://127.0.0.1:2999/liveclientdata/playerscores?summonerName="+name, verify=False).text #get matchdata
    data = json.loads(request) #convert to json / dictionary
    return data['deaths'] #return death value


#Screenshots for pixelbot
#Roles to enter the queue
queue = 'queue.jpg'

#Accepting the game when in queue
accept = 'accept.jpg'

#Ingame
#Novision redside
blueside = 'blueside.jpg'
#Novision blueside
redside =  'redside.jpg'
#Surrendervote
surr = 'surrender.jpg'

#Post-game
#Scoreboard
scoreboard = 'scoreboard.jpg'
#team1
team1 = 'team1.jpg'
#Handle events such as levelling up
ok = 'ok.jpg'


#FUNCTIONS FOR PIXELBOT
#Compare
def coords(src):
    coordinates = []

    #import images
    farm_img = windowCapture()
    
    #farm_img = cv.imread(windowCapture(),cv.IMREAD_UNCHANGED)
    wheat_img = cv.imread(src, cv.IMREAD_UNCHANGED)
    
    #do template matching
    #result = cv.matchTemplate(farm_img, wheat_img, cv.TM_CCOEFF_NORMED)
    result = cv.matchTemplate(farm_img, wheat_img, cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    #filter
    threshold = 0.95
    yloc, xloc = np.where(result >= threshold)

    #fill in coordinates
    for x,y in zip(xloc,yloc):
        coordinates.append([x,y])

    #return
    try:
        return coordinates
    except:
        return None

#get screenshot
def windowCapture():
    w = 1920
    h = 1080
    
    hwnd = win32gui.FindWindow(None, 'kekw')

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')
    img.shape = (h,w,4)


    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    img = img[...,:3]
    img = np.array(img)
    #plt.show()
    return img


####################
#FUNCTIONS FOR GAME#
####################

#LEVEL ABILITIES
def levelup():
    pd.keyDown('ctrl')
    sleep(0.1)
    pd.keyDown('r')
    sleep(0.1)
    pd.keyUp('r')
    pd.mouseDown(button='right')
    sleep(0.1)
    pd.mouseUp(button='right')
    pd.keyDown('q')
    sleep(0.1)
    pd.keyUp('q')
    pd.keyDown('w')
    sleep(0.1)
    pd.keyUp('w')
    pd.keyDown('e')
    sleep(0.1)
    pd.keyUp('ek')
    pd.keyUp('ctrl')
    sleep(0.1)


#Check if ingame
def checkIngame():
    try:
        request = requests.get("https://127.0.0.1:2999/liveclientdata/activeplayer", verify=False).text
        return True
    except:
        return False


#Buying items
def item():
    #X,Y coordinates of item, purchase button in the shop
    itemcoords = [500,400]
    itemcoords1 = [650,400]
    itemcoords2 = [800,400]
    purchasecoords = [1068,888]

    #Open the shop
    pd.keyDown('p')
    sleep(0.1)
    pd.keyUp('p')
    
    #Aim at item
    SetCursorPos((itemcoords[0],itemcoords[1]))
    
    #Select
    pd.mouseDown(button='left')
    sleep(0.1)
    pd.mouseUp(button='left')
    sleep(0.2)
    
    #Aim at purchase
    SetCursorPos((purchasecoords[0],purchasecoords[1]))

    #Select
    pd.mouseDown(button='left')
    sleep(0.1)
    pd.mouseUp(button='left')
    sleep(0.5)

    #Aim at item
    SetCursorPos((itemcoords1[0],itemcoords1[1]))
    
    #Select
    pd.mouseDown(button='left')
    sleep(0.1)
    pd.mouseUp(button='left')
    sleep(0.2)
    
    #Aim at purchase
    SetCursorPos((purchasecoords[0],purchasecoords[1]))

    #Select
    pd.mouseDown(button='left')
    sleep(0.1)
    pd.mouseUp(button='left')
    sleep(0.5)

    #Aim at item
    SetCursorPos((itemcoords2[0],itemcoords2[1]))
    
    #Select
    pd.mouseDown(button='left')
    sleep(0.1)
    pd.mouseUp(button='left')
    sleep(0.2)
    
    #Aim at purchase
    SetCursorPos((purchasecoords[0],purchasecoords[1]))
    
    #Do purchase
    pd.mouseDown(button='left')
    sleep(0.1)
    pd.mouseUp(button='left')
    sleep(0.5)
    
    #Close shop
    pd.keyDown('p')
    sleep(0.1)
    pd.keyUp('p')


#Vote yes if currently a surrender vote is active
def surrender():
    xy = coords(surr)
    if xy != []:
        SetCursorPos((xy[0][0],xy[0][1]+74))
        pd.mouseDown(button='left')
        sleep(0.1)
        pd.mouseUp(button='left')


#Figure out whether blueside or redside
def blueredSide():
    if coords(blueside) != []:
        return True
    elif coords(redside) != []:
        return False
    else:
        return None

#Annoying npc behaviour aka walking after your adc doing nothing
def behaviour(side):
    allies = ['u','j','k','l'] #keys to wach allies
    deaths = int(getDeaths(sName)) #get deaths
    ingame = checkIngame() #check if ingame
    while ingame:
        deaths = int(getDeaths(sName)) #update deathcount
        #Coords where to position
        pos = []

        #If blueside
        if side == True:
            pos = [760,530]  #blueside position
        
        #If redside
        else:
            pos = [1098,440] #redside position
        try:
            while int(getDeaths(sName)) == deaths: #while not dead
                levelup() #handle levelup
                surrender() #handle surrender
                sleep(0.5)
                for ally in allies: #go through allies
                    SetCursorPos((pos[0],pos[1])) #set mouse to original position
                    pd.keyDown(ally) #focus cam on ally
                    for k in range(5): #loop through behaviour 5 times
                        if int(getDeaths(sName)) == deaths:
                            sleep(0.1)

                            pd.mouseDown(button='right') #walk
                            sleep(0.1)
                            pd.mouseUp(button='right')
                            sleep(0.1)

                            pd.keyDown('s') #attack
                            sleep(0.1)
                            pd.keyUp('s')
                            sleep(0.5)

                            pd.mouseDown(button='right') #walk
                            sleep(0.1)
                            pd.mouseUp(button='right')

                    pd.keyUp(ally)
        except:
            pass

        item()
        ingame = checkIngame()
        




while True:
    xy = [] 
    draft = str
    ingame = checkIngame()
    hasShopped = False
    side = 2

    #Execute when in Lobby, Queue, Draft
    while ingame != True:

        #Handle post-game events such as levelling up that come with "ok" button
        xy = []
        xy = coords(ok)
        if xy!= []:
            SetCursorPos((xy[0][0],xy[0][1]))
            pd.click()
            print('OK')
            sleep(0.2)
            SetCursorPos((960,540))

        #Handle post-game 1/2
        xy = []
        xy = coords(scoreboard)
        if xy != []:
            print()
            SetCursorPos((xy[0][0]+370,xy[0][1]+570))
            pd.click()
            print('Handling post-game 1/2')
            sleep(0.2)
            SetCursorPos((960,540))

        #Handle post-game 2/2
        xy = []
        xy = coords(team1)
        if xy != []:
            print()
            SetCursorPos((xy[0][0]+430,xy[0][1]+540))
            pd.click()
            print('Handling post-game 2/2')
            sleep(0.2)
            SetCursorPos((960,540))

        #Enter Queue
        xy = []
        xy = coords(queue)
        if xy != []:
            print()
            SetCursorPos((xy[0][0],xy[0][1]))
            pd.click()
            print('Entered queue')
            sleep(0.2)
            SetCursorPos((960,540))

        #Accept Game
        xy = []
        xy = coords(accept)
        if xy != []:
            SetCursorPos((xy[0][0],xy[0][1]))
            pd.click()
            print('Accepted game')
            sleep(0.2)
            SetCursorPos((960,540))

        #Check if ingame
        if checkIngame() == True:
            ingame =  True
            print('Now ingame')
            sleep(0.2)
            SetCursorPos((960,540))
        else:
            ingame = False


    #When queueing, drafting, etc is done and it is ingame
    while ingame:
        SetCursorPos((960,540))
        sleep(0.2)
        pd.mouseDown(button='left')
        sleep(0.1)
        pd.mouseUp(button='left')

        #Variables to use one single time when the game has started
        side = int
        hasShopped = bool

        #Wait until player is actually ingame, not just in loading screen
        while side != 0 and side != 1:
            if blueredSide() == True:
                side = 0
                print('Blueside')
            elif blueredSide() == False:
                side = 1
                print('Redside')
            else:
                pass
            sleep(5)
        sleep(5)

        #Buying starter items
        if hasShopped != True:

            print('buying initial item')
            #X,Y coordinates of item, purchase button in the shop
            itemcoords = [640,450]
            purchasecoords = [1068,888]

            #Open the shop
            pd.keyDown('p')
            sleep(0.1)
            pd.keyUp('p')
            
            #Aim at item
            SetCursorPos((itemcoords[0],itemcoords[1]))
            
            #Select
            pd.mouseDown(button='left')
            sleep(0.1)
            pd.mouseUp(button='left')
            sleep(0.2)
            
            #Aim at purchase
            SetCursorPos((purchasecoords[0],purchasecoords[1]))
            
            #Do purchase
            pd.mouseDown(button='left')
            sleep(0.1)
            pd.mouseUp(button='left')
            
            #Close shop
            pd.keyDown('p')
            sleep(0.1)
            pd.keyUp('p')

        #Entire ingame behaviour -> Walking, using abilities, leveling, buying items
        print('Behaviour')
        behaviour(blueredSide())
        ingame = checkIngame()
        SetCursorPos((960,540))