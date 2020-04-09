# -*- coding: utf-8 -*-

def splitAVI(dates,src='data/avi/',dest='data/img/',status=False):
    import cv2
    import os
    
    
    for date in dates:
        if not os.path.exists(f"{src}{date}"):
            print(f"{src}{date} directory does not exist")
            continue
        
        if not os.path.exists(f'{dest}{date}'):
            os.makedirs(f'{dest}{date}')
        
        for vid in os.listdir(f'{src}{date}/'):
            vidcap = cv2.VideoCapture(f'{src}{date}/{vid}')
            success,image = vidcap.read()
            count = 0
            
            fname = vid.split('.avi')[0]
            
            if not os.path.exists(f'{dest}{date}/{fname}'):
                os.makedirs(f'{dest}{date}/{fname}')
            
            while success:
              cv2.imwrite(f'{dest}{date}/{fname}/{count}.png', image)   
              success,image = vidcap.read()
              #print ('Read a new frame: ', success)
              count += 1
              
            
            cv2.VideoCapture.release(vidcap)
            
        if status:
            print(f"Processed {date}")


def getList(start,end):
    """
    Strictly Ymd format no spaces or slashes
    """
    
    import datetime
    
    start = datetime.datetime.strptime(str(start),'%Y%m%d')
    end = datetime.datetime.strptime(str(end),'%Y%m%d')
    
    dateList = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days + 1)]
    
    sList = [datetime.datetime.strftime(x,'%Y%m%d') for x in dateList]
    
    return sList
    


def processDates(dates,src='data/img/',dest='data/subtracted/'):
    import cv2
    import os
    import numpy as np
    
    for date in dates:
        images = loadImg(date,src)
        
        if not os.path.exists(f'{dest}{date}/'):
            os.mkdir(f'{dest}{date}')
        
        #Images is an array of observations, each observation is an array of actual images from that observation
        for obs in images:
            
            if not os.path.exists(f'{dest}{date}/{obs[0]}'):
                os.mkdir(f'{dest}{date}/{obs[0]}')
            
            #Make the numbr of images correct for stacking purposes
            #Usually the first few frames contains no information anyway
            #The first index in the list is actually a string with the file name,
            #So len(obs)%5 should be 1 if there are the correct number of images
            while not len(obs)%5 == 1:
                obs.pop(1)
            
            #Subtract the images in intervals of 5
            subList = []
            for i in range(1,len(obs),5):
                sub = cv2.subtract(obs[i+4],obs[i])
                subList.append(sub)
                cv2.imwrite(f'{dest}{date}/{obs[0]}/{i}_{i+4}.png',sub)
            
            #Stack the subtracted images
            stacked = subList[0]
            for i in range(1,len(subList)):
                stacked = cv2.add(stacked,subList[i])
            cv2.imwrite(f'{dest}{date}/{obs[0]}/_stacked.png',stacked)




def loadImg(date,src='data/img/'):
    import os
    import cv2
    
    folder = f"{src}{date}/"
    images = []
    
    for file in os.listdir(folder):
        iList = [file]
        for fn in os.listdir(f'{folder}{file}/'):
            iList.append(cv2.imread(f"{folder}{file}/{fn}"))
        images.append(iList)
    
    
    return images
        






#Example use, please run file and then use console to call methods
"""

#Splitting
dateList = getList('20200316','20200326')
splitAVI(dateList,status=True)


#Reading in images
images = loadImg('20200316')

"""