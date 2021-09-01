#!/usr/bin/env python
# coding: utf-8

# In[25]:


from flickrapi import FlickrAPI
import pandas as pd
import sys
import webbrowser
from xml.etree import ElementTree as ET
import matplotlib.pyplot as plt


# In[26]:


from IPython.display import Image
Image(filename='C:/Users/sonny/OneDrive/Desktop/uni/terzo anno/social-media-management-master/img progetto/read-permission.png')


# In[27]:


key='8044708142907ea81eaa37a7f09fe438' #chiave API
secret='41e5fc7070d84667' # segreto API
    
    
def get_valid_permission(type_permission,flickr):
     if not flickr.token_valid(perms=type_permission):
        flickr.get_request_token(oauth_callback="oob")
        authorize_url=flickr.auth_url(perms=type_permission)
        webbrowser.open_new_tab(authorize_url)
        verifier=str(input("Verifier code: "))
        flickr.get_access_token(verifier)
def get_permission_flick(key,secret):
    flickr=FlickrAPI(key,secret)
    get_valid_permission("read",flickr)
    get_valid_permission("write",flickr)
    
    return flickr


print("Otteniamo l'oggetto flickr")
flickr=get_permission_flick(key,secret)## inizializza oggetto flickr


# In[28]:


## dato il codice di una gallery in input salva le foto in una cartella
import json
import urllib.request as uRequest
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uRequest
from urllib.request import urlretrieve as retrieve


# In[29]:


Image(filename='C:/Users/sonny/OneDrive/Desktop/uni/terzo anno/social-media-management-master/img progetto/json-response.png')


# In[41]:


Image(filename='C:/Users/sonny/OneDrive/Desktop/uni/terzo anno/social-media-management-master/img progetto/rest response.png')


# In[31]:


Image(filename='C:/Users/sonny/OneDrive/Desktop/uni/terzo anno/social-media-management-master/img progetto/api-explorer.png')


# In[32]:


def download_single_image(photo_id,index,path_middle):
    response_photo=flickr.photos.getInfo(photo_id=photo_id,format="json")
    response_json=response_photo.decode()
    url_prova=json.loads(response_json)
    
    photo_url=url_prova['photo']['urls']['url'][0]['_content']
    photo_url_retrieve=photo_url

    if index==-1: ## -1 RITORNA SOLO L'URL
        return photo_url
    
    download_image_from_url(photo_url_retrieve,index,path_middle)


# In[33]:


def download_image_from_url(photo_url,index,path_middle):
    new_url=photo_url
    page_html=uRequest(new_url)
    
    page_soup=soup(page_html)
    container_img=page_soup.findAll("img")[0]
    #SALVA LE FOTO SU /flickrAPI/{id_photo}.jpg
    retrieve("https:"+container_img['src'],"C:/Users/sonny/OneDrive/Desktop/uni/terzo anno/social-media-management-master/FlickrAPI/"+str(item)+".jpg")


# In[34]:


print("Cerchiamo di prendere l'url delle foto della galleria Community Favorites from Explore ,→Flickr") # id ->72157716843071466

input_id_gallery=72157716843071466
response=flickr.galleries.getPhotos(gallery_id=input_id_gallery,format="json")
response=json.loads(response)
list_photo_id=[]

for i in range(len(response['photos']['photo'])):# ciclo per ogni id restituito
    list_photo_id.append(int(response['photos']['photo'][i]["id"]))#accedo␣ ,→all'id

print("Ora downloadiamo ogni foto trovata")
index=0
for item in list_photo_id:

    download_single_image(item,index,str(input_id_gallery))
    index=index+1
    print(f" Foto{index} scaricata ")


# In[35]:


class statElement:
    def __init__(self,likes,views,comments,title,rid):
        self.likes=likes
        self.views=views
        self.comments=comments
        self.title=title
        self.id=rid
    def getId(self):
        return self.id
    def getLikes(self):
        return self.likes
    def getViews(self):
        return self.views
    def getComments(self):
        return self.comments
    def getLenComments(self):
        return len(self.comments)
    def getTitle(self):
        return self.title
    def __str__(self):
        string= "Id "+ str(self.id) + " title " + self.title+ " likes"+str(self.likes)+" views "+str(self.views)
        comment=""
        if self.getLenComments()>0:
            comment+=self.comments[0]
        return string+" comments(primo) "+comment


# In[36]:


lista_elementi_stat=[] ## elementi con dati statistici
list_di_prova=list_photo_id ## debug
for item in list_di_prova:
    
    #COMMENTI
    response_analysis=flickr.photos.comments.getList(photo_id=item,format="json")
    analysis_json=json.loads(response_analysis.decode())

    
    ## VIEWS, TITOLO
    response_views=flickr.photos.getInfo(photo_id=item,format="json")
    total=json.loads(response_views.decode())['photo']
    total_views=total['views']
    title=total['title']['_content']

    #LIKES
    likes=(flickr.photos.getFavorites(photo_id=item,format="json"))
    total_likes=(json.loads(likes.decode()))['photo']['total']
    
    
    # eccezione foto con 0 commenti
    try:
        x=analysis_json['comments']['comment'] ## causa un eccezione se non sono presenti commenti
        list_comment=[ comment['_content'] for comment in x]
    except:
        print("Eccezione ",item)
        list_comment=[] # lista commenti vuota

    prova=statElement(total_likes,total_views,list_comment,title,item)
    lista_elementi_stat.append(prova)

print(lista_elementi_stat[1])#stampa 2 elemento


# In[37]:


import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib.image as mpimg
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sid = SentimentIntensityAnalyzer()


# In[38]:


def get_scores(comments):
    pos=0
    neg=0
    for i in comments:
        if sid.polarity_scores(i)['compound']>=0.5: pos+=1## positive
        elif sid.polarity_scores(i)['compound']<=-0.5: neg+=1
    return pos,neg




data_views=[]
data_likes=[]
data_comment=[]
data_title=[]
positives=[]
negatives=[]
totals=[]
SCALA_VIEWS=1000
for i in range(len(lista_elementi_stat)):
    
    
    item=lista_elementi_stat[i]
    data_views.append(int(item.getViews())/SCALA_VIEWS) ## scaliamo di un fattore 1000 per vedere meglio nel grafico
    data_likes.append(int(item.getLikes()))
    data_comment.append(int(item.getLenComments()))
    data_title.append(item.getTitle()[:10])
    positive,negative=get_scores(item.getComments())
    positives.append(positive)
    negatives.append(negative)
    totals.append(data_comment)
    
    
    img = np.uint8(mpimg.imread("C:/Users/sonny/OneDrive/Desktop/uni/terzo anno/social-media-management-master/FlickrAPI/"+ str(item.getId()) +".jpg"))
    
    
    fig = plt.figure()
   

    # show original image
    fig.add_subplot(221)
    plt.title(item.getTitle()[:20])
    plt.imshow(img)
    #print(item)
    fig.add_subplot(222)
    plt.title(' Statistica')
    plt.bar( 0.02, int(item.getLikes()), width=0.02, label="likes") #graph likes+ blue
    plt.bar( 0.04, int(item.getViews())/SCALA_VIEWS, width=0.02,label="views") #graph views green
    plt.bar( 0.06, item.getLenComments(), width=0.02, label="commenti")#graph comment orange
    plt.bar( 0.08, positive, width=0.02, label="commenti pos") #graph comment
    plt.legend(loc=1, fontsize = 'x-small')
    plt.xticks([0.02,0.04,0.06,0.08],["L","V","C","Pos"])
    plt.xlim([0,0.20])
    plt.legend()
    plt.tight_layout()


# In[39]:


print("Grafico totale")
get_ipython().run_line_magic('matplotlib', 'qt')
x=np.arange(len(lista_elementi_stat))
plt.bar(x+ 0.10, data_likes, width=0.15, label="likes") #graph likes+ blue
plt.bar(x+ 0.40, data_views, width=0.15, label="views") #graph views green
plt.bar(x+ 0.25, data_comment, width=0.15, label="commenti") #graph comment orange
plt.bar(x+ 0.55, positives, width=0.15, label="commenti pos") #graph comment orange
plt.bar(x+1 ,negatives ,width=0.25,label="commenti neg")
plt.tight_layout()
plt.xticks(x, data_title, rotation=90)

low = 0
high =4500
plt.ylim([low,high])
plt.legend()
plt.show()


# In[40]:


Image(filename='C:/Users/sonny/OneDrive/Desktop/uni/terzo anno/social-media-management-master/img progetto/grafico totale.png')

