from wnaffect import WNAffect
import csv
import numpy as np
from nltk import pos_tag
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords


wna = WNAffect('wordnet-1.6/', 'wn-domains-3.2/')


tokenizer = RegexpTokenizer(r'\w+')
en_stopwords = stopwords.words('english')
lyrics_emotion = []

with open('lyrics.txt', 'rb') as csvfile:
    lines = csv.reader(csvfile, delimiter='$')
    lines = [line for line in lines]    


with open('lyrics_emotion.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)

    artist = ''
    title = ''
    emotion_sad = 0           # compassion, sadness
                              # joy, love

    emotion_frustrated = 0    # humility, despair, shame, negative-fear
                              # positive-fear, fearlessness,
                              # positive-expectation, enthusiasm,
                              # positive-hope

    emotion_angry = 0         # shame, general-dislike
                              # love, liking

    emotion_anxious = 0       # anxiety, negative-fear
                              # positive-fear, positive-hope, calmness
        
    count = 2
    for line in lines:
        if line == []:
            count += 1
        elif line[0] == \
            '******* This Lyrics is NOT for Commercial use *******':
            count = 0
            # store emotion data of one song
            lyric_emotion = [ \
                artist, \
                title, \
                emotion_sad, \
                emotion_frustrated, \
                emotion_angry, \
                emotion_anxious \
            ]
            writer.writerow(lyric_emotion)

        else:
            count += 1
                
            # artist and title
            if count == 3:
                artist = line[0]
                title = line[1]
                emotion_sad = 0
                emotion_frustrated = 0

                emotion_angry = 0
                emotion_anxious = 0
            else:
                words = pos_tag(tokenizer.tokenize(line[0].lower()))
                for word in words:
                    if word[0] not in en_stopwords:
                        emo = wna.get_emotion(word[0], word[1])
                        if emo == None:
                            # do nothing
                            pass

                        else:
                            emo_r = emo.get_level(5).name
                            print word, emo_r                        

                            if (emo_r == 'compassion' or emo_r == 'sadness' \
                              or emo_r == 'joy' or emo_r == 'love'):
                                emotion_sad += 1

                            elif (emo_r  == 'humility' or emo_r == 'despair' \
                              or emo_r == 'shame' or emo_r == 'negative-fear' \
                              or emo_r == 'positive-fear' or emo_r == 'fearlessness' \
                              or emo_r == 'positive-expectation' or emo_r == 'enthusiasm' \
                              or emo_r == 'positive-hope'):
                                emotion_frustrated += 1

                            elif (emo_r == 'shame' or emo_r == 'general-dislike' \
                              or emo_r == 'love' or emo_r == 'liking'):
                                emotion_angry += 1

                            elif (emo_r  == 'anxiety' or emo_r == 'negative-fear' \
                              or emo_r == 'positive-fear' or emo_r == 'positive-hope' \
                              or emo_r == 'calmness'):
                                emotion_anxious += 1


'''
with open('lyrics_emotion.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    _ = map(writer.writerow, lyrics_emotion)
'''    
