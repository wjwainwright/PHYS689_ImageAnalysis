# -*- coding: utf-8 -*-

def splitAVI(dates,src='data/avi/',dest='data/img/',status=False):
    import cv2
    import os
    
    
    for date in dates:
        if not os.path.exists(f"{src}{date}"):
            print(f"{src}{date} directory does not exist")
            return
        
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
    




def loadImg(date,src='data/img/'):
    import os
    import cv2
    
    
    images = dict()
    folder = f"{src}{date}/"
    iList = []
    
    for file in os.listdir(folder):
        for fn in os.listdir(f'{folder}{file}/'):
            iList.append(cv2.imread(f"{folder}{file}/{fn}"))
    
    images[date] = iList
    
    return images
        






#Example use, please run file and then use console to call methods
"""

#Splitting
dateList = getList('20200316','20200326')
splitAVI(dateList,status=True)


#Reading in images
images = loadImg('20200316')

"""