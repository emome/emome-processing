import numpy as np
import csv
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.externals import joblib


# build the song-emotion matrix

song_mat = []
emotion_mat = []
with open('old_lyrics_emotion.csv', 'rb') as csvfile:
    lines = csv.reader(csvfile)
    lines = [line for line in lines]

    for line in lines:
        # [artist, title, sad, frustrated, angry, anxious]
        artist = line[0]
        title = line[1]
        sad = float(line[2])
        frustrated = float(line[3])
        angry = float(line[4])
        anxious = float(line[5])

        if sad + frustrated + angry + anxious > 0:
            song_mat.append([artist, title])
            emotion_mat.append([sad, frustrated, angry, anxious])
    
    emotion_mat = np.array(emotion_mat)
    # normalization
    emotion_mat = preprocessing.normalize(emotion_mat)
    print emotion_mat.shape
    print len(song_mat)


# extract K-Means

n_clusters = 5
clf = KMeans(n_clusters=n_clusters)
predictions = clf.fit_predict(emotion_mat)
means = clf.cluster_centers_
print predictions.shape, means.shape

song_clusters = []
for c in range(n_clusters):
    print sum(predictions==c)
    song_clusters.append([song_mat[x] for x in range(len(predictions)) if predictions[x]==c])

with open('song_clusters.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for song_cluster in song_clusters:
        writer.writerow(song_cluster)


joblib.dump(clf, 'song_kmeans.pkl')
 
