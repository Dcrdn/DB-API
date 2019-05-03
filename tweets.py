# -*- coding: utf-8 -*-
import tweepy
import json
import re
from textblob import TextBlob
from variables import apiKey, apiSecretKey, accessToken, accessTokenSecret
import time
from unicodedata import normalize
import sys
import json
import datetime
import operator
reload(sys)  
sys.setdefaultencoding('utf8')

auth = tweepy.OAuthHandler(apiKey, apiSecretKey)
auth.set_access_token(accessToken, accessTokenSecret)

api = tweepy.API(auth)

#hashtags, --> pie    hashtags(user)
#sentimiento, -->pie  analisis(user)
#fechas , --> grafica de lineas.. getDates(user)
#most common words getCommonWords(user)
#posted by day of the week getDias(user)

#calcular average of tweets per day
#las horas a las que mas twitteo


totalTweets=100

totalPast=100

def toText(palabra):
        s=unicode(palabra)
        trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
        s = normalize('NFKC', normalize('NFKD', s).translate(trans_tab))
        return s

def getLastTweet(user):
        public_tweets=api.user_timeline(screen_name=user)
        for tweet in public_tweets:
                return tweet._json

def getTweet(user):
        public_tweets=api.user_timeline(screen_name=user, count=totalTweets)
        tweets=[]

        for tweet in public_tweets:
                tweets.append(tweet._json)
        return tweets

def getTweetsText(user):
        public_tweets=api.user_timeline(screen_name=user, count=totalTweets)
        tweets=[]

        for tweet in public_tweets:
                tweets.append(tweet.text)
        return tweets

def getCommonWords(user):
        common=("y","tu","los","mas","es","cuando","solo","del","pero","no","si","do","este","una","yo","what","What","you","know","mi","lo","la","un","que","te","el","me","a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", "en", "entre", "hacia","hasta", "mediante", "para", "por", "segun", "sin", "son", "sobre", "tras")
        common2=("I","they","been","be","the","The","was","were","a","RT","are","who","not","and","has","have","had","an","so","have","you","in","the","to","my","our","it","is","but","because","that","on","at","by","for","at","those","these","this","of","with", ":")
        dic={}
        public_tweets=api.user_timeline(screen_name=user, count=totalTweets)

        for tweet in public_tweets:
                text=toText(tweet.text)
                text=(text).split()
                newText=[]
                for word in text:
                        if(word not in common and word not in common2):
                                if(word in dic):
                                        count=dic[word]
                                        count+=1
                                        dic[word]=count
                                else:
                                        dic[word]=1
                                newText.append(word)
                
                text=' '.join(newText)
        helper={}
        if(len(dic)>9):
                size=10
        else:
                size=len(dic)

        sorted_x = sorted(dic.items(), key=operator.itemgetter(1), reverse=True)
        for  num in range(0,size):
                helper[sorted_x[num][0]]=sorted_x[num][1
        ]
        return json.dumps(helper)

#getCommonWords("Diego_crdn")

def getDates(user):
#        dias={"Mon":1, "Tue":2 ,"Wed":3 ,"Thu":4, "Fri":5, "Sat":6, "Sun":7}
        meses={"Jan":1, "Feb":2, "Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7, "Aug":8, "Sep":9, "Oct":10, "Nov":11, "Dec":12}
       
        public_tweets=api.user_timeline(screen_name=user, count=200)
        dates=[]

        for tweet in public_tweets:
                dia=tweet._json["created_at"]
                dia=dia.split()
                day=dia[2]
                mes=meses[dia[1]]
                year=dia[5]
                mesStr=mes
                if(mes<10):
                        mesStr="0"+str(mes)
                fecha=[day, mes, year, str(year)+"-"+str(mesStr)+"-"+str(day), str(year)+"-"+str(mesStr) ]   
                dates.append(fecha)   
       # dates.sort(key=lambda x: x[3], reverse=True)
        dates.sort(key=lambda x: datetime.datetime.strptime(x[3], '%Y-%m-%d'))
        helper=[]
        count=[]
        seen=[]
        dic={}

        for element in dates:
                if(element[4] in dic):
                        count=dic[element[4]]
                        count+=1
                        dic[element[4]]=count
                else:
                        dic[element[4]]=1
        return json.dumps(dic)

def getDias(user):
        dias={"Mon":1, "Tue":2 ,"Wed":3 ,"Thu":4, "Fri":5, "Sat":6, "Sun":7}
        dic={}

        public_tweets=api.user_timeline(screen_name=user, count=totalTweets)

        for tweet in public_tweets:
                dia=tweet._json["created_at"]
                dia=dia.split()
                dia=dias[dia[0]]
                if(dia in dic):
                        count=dic[dia]
                        count+=1
                        dic[dia]=count
                else:
                        dic[dia]=1
        return json.dumps(dic)

def analisis(user):
        public_tweets=api.user_timeline(screen_name=user, count=totalTweets)
        sentimientos=[]
        dic={"positive":0, "negative":0,"neutral":0}
        for tweet in public_tweets:
                analysis=TextBlob(tweet.text)
                if(analysis.sentiment[0]>0):
                        count=dic["positive"]
                        count+=1
                        dic["positive"]=count
                        sentimientos.append("positive")
                elif(analysis.sentiment[0]<0):
                        count=dic["negative"]
                        count+=1
                        dic["negative"]=count
                        sentimientos.append("negative")
                else:
                        count=dic["neutral"]
                        count+=1
                        dic["neutral"]=count
                        sentimientos.append("neutral")
        return json.dumps(dic)

def getHashtag(tweet):
	# return list of hashtags
	hashtag_rx = re.compile(r'#\w+')
	hashtags = hashtag_rx.findall(tweet)
	return hashtags

def getAllHashtags(all_tweets):
	all_hashtags = []
	for tweet in all_tweets:
		hashtags_list = getHashtag(tweet)
		all_hashtags.extend([h for h in hashtags_list])
	return all_hashtags

def countHashtag(hashtags_list):
	# return a dict hashtag/frequency pair
	hashtags_freq =  {}
	for h in hashtags_list:
                if h.lower() in hashtags_freq:
                        count=hashtags_freq[h.lower()]
                        hashtags_freq[h.lower()]=count+1
                else:
                        hashtags_freq[h.lower()]=1
	return hashtags_freq

def printMostFrequentHashtags(nb_most_hashtagged, all_hashtags):
	hTag_freq_dict = countHashtag(all_hashtags)
	most_Htag_values = sorted(list(hTag_freq_dict.values()), reverse=True)[:nb_most_hashtagged]
        dic={}
        for i in most_Htag_values:
            value=list(hTag_freq_dict.keys())[list(hTag_freq_dict.values()).index(i)]
            if(value in dic):
                count=dic[value]
                count+=1
                dic[value]=count
            else:
                dic[value]=1
        return dic

def batmanHashtags(user):
        l=getTweetsText(user)
        all_hashtags = getAllHashtags(l)
        dic=printMostFrequentHashtags(15, all_hashtags)
        return json.dumps(dic)

def imprime(user):
        return user


def convertToJson(colors,data,labels):
        data={
                "labels": labels,
                "datasets":[
                        {
                        "label":'Population',
                        "data":data,
                        "backgroundColor":colors
                        }
                ]
        }
        return json.dumps(data)


#consigo los tweets
#all_hashtags = getAllHashtags(l)
#printMostFrequentHashtags(15, all_hashtags)
#getDates()

#user="Diego_crdn"
#getDias("Diego_crdn")

#print(hashtags("Diego_crdn"))

#res=analisis(user)
#print(type(res))
#print(analisis())

"""
    analysis = TextBlob(tweet.text)
    print(analysis.sentiment)
    if analysis.sentiment[0]>0:
       print 'Positive'
    elif analysis.sentiment[0]<0:
       print 'Negative'
    else:
       print 'Neutral'

"""