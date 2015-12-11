import numpy as np
from bson.objectid import ObjectId
import random
from pymongo import MongoClient
import csv 
from datetime import datetime


EMOTION_SAD = 'sad'
EMOTION_FRUSTRATED = 'frustrated'
EMOTION_ANGRY = 'angry'
EMOTION_ANXIOUS = 'anxious'


client = MongoClient('localhost', 27017)
db = client.test
#db = client.primer

print db.suggestions.find().count()

song_info = []
with open('../data/song_info.csv', 'rb') as csvfile:
    lines = csv.reader(csvfile)
    song_info = [line for line in lines]
song_info = np.array(song_info)
print len(song_info)

lyrics_emotion_ching = []
with open('../data/lyrics_emotion_01.csv', 'rb') as csvfile:
    lines = csv.reader(csvfile)
    lyrics_emotion_ching = [line for line in lines]
lyrics_emotion_ching = np.array(lyrics_emotion_ching)

lyrics_emotion_huai = []
with open('../data/lyrics_emotion_02.csv', 'rb') as csvfile:
    lines = csv.reader(csvfile)
    lyrics_emotion_huai = [line for line in lines]
lyrics_emotion_huai = np.array(lyrics_emotion_huai)

lyrics_emotion = np.concatenate((lyrics_emotion_ching,lyrics_emotion_huai),axis=0)
print lyrics_emotion.shape


messages = [
    "try this song now. I think you'll like it!",
    "you're not alone. I can play this for you :)",
    "how about trying some music? I found this one really great!",
    "hey although I'm a robot, I really think you'll like this!"
]


idx_song_info = 0
c = 0
for lyric_emo in lyrics_emotion:
    artist = lyric_emo[0]
    title = lyric_emo[1]
    sad = int(lyric_emo[2])
    frustrated = int(lyric_emo[3])
    angry = int(lyric_emo[4])
    anxious = int(lyric_emo[5])
    if sad + frustrated + angry + anxious > 0:
        print c
        c += 1
        print artist, title
        while song_info[idx_song_info][0] != artist:
            idx_song_info += 1
            print idx_song_info

        object_id = str(ObjectId())


        results = {
            '_id': object_id,
            'user_id': 'robot',
            'emotion': {
                EMOTION_SAD: sad,
                EMOTION_FRUSTRATED: frustrated,
                EMOTION_ANGRY: angry,
                EMOTION_ANXIOUS: anxious
            },  
            'scenario_id': '0',
            'time': datetime.now(),
            'content': {
                'type': "Spotify",
                'data': {
                    'artist': artist,
                    'track_name': title,
                    'url': song_info[idx_song_info][2],
                    'cover_img_url': song_info[idx_song_info][3]
                }
            },
            'message': messages[random.sample(range(len(messages)),1)[0]],
            'impact': None
        }
        print results

        db.suggestions.insert_one({
            '_id': object_id,
            'user_id': 'robot',
            'emotion': {
                EMOTION_SAD: int(sad),
                EMOTION_FRUSTRATED: int(frustrated),
                EMOTION_ANGRY: int(angry),
                EMOTION_ANXIOUS: int(anxious)
            },  
            'scenario_id': '0',
            'time': datetime.now(),
            'content': {
                'type': "Spotify",
                'data': {
                    'artist': artist,
                    'track_name': title,
                    'url': song_info[idx_song_info][2],
                    'cover_img_url': song_info[idx_song_info][3]
                }
            },
            'message': messages[random.sample(range(len(messages)),1)[0]],
            'impact': None
        })
