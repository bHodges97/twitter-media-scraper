import tweepy as tw
import os
import urllib.request
import code



class timeline_dl():
    def __init__(self, key, secret):
        auth = tw.OAuthHandler(key, secret)
        self.api = tw.API(auth)
        
    def start(self, name):
        if not os.path.exists(name):
            os.mkdir(name)        
        self.name = name
    
        out = self.api.user_timeline(name,count=200, tweet_mode="extended")
        #code.interact(local=locals())
        #exit()               
        
        maxid = float('Inf')
        if not out:
            print(maxid, "No tweets found.")        
        
        tid = 0
        while tid != maxid:
            tid = maxid
            if not out:
                print(maxid, "No new tweets found.")
                break
            
            for tweet in out:
                id = int(tweet.id_str)
                self.addtweet(tweet)            
                if maxid > id:
                    maxid = id
            out = self.api.user_timeline(name,count=200,max_id=maxid, tweet_mode="extended")
        

    def addtweet(self, tweet):
        #Download regular tweets
        self.parse_json(tweet._json)
        
        #get the retweets
        if 'quoted_status' in tweet._json:
            self.parse_json(tweet._json['quoted_status'])
        if 'retweeted_status' in tweet._json:
            self.parse_json(tweet._json['retweeted_status'])
    
    def parse_json(self, json):
        if "extended_entities" in json:        
            entities = json["extended_entities"]
        else:
            entities = json["entities"]
        
        if not "media" in entities:
            return
        
        for i in entities["media"]:
            #Download videos and gifs
            if "video_info" in i:
                url = None
                bitrate = 0                 
                for video in i['video_info']['variants']:
                    if 'bitrate' in video and video['bitrate'] >= bitrate:
                        url = video['url']
                        bitrate = video['bitrate']                    
                if url:
                    self.download_media(url)
            #Download images
            elif "media_url_https" in i:
                url = i["media_url_https"]
                self.download_media(url)
    
    def download_media(self, url):
        fname = url.split("/")[-1].split("?")[0]
        urllib.request.urlretrieve(url, os.path.join(self.name, fname))
        print(fname,"added")

if __name__ == "__main__":        
    key = 'api key here'
    secret = 'api secret key here' 
    name = "twitter handle name here"
    dl = timeline_dl(key,secret)
    dl.start(name)

    

