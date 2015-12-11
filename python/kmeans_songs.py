import numpy as np
import csv
from sklearn.cluster import KMeans
from sklearn import preprocessing
from sklearn.externals import joblib
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient


# build the suggestion-emotion matrix

client = MongoClient('localhost', 27017)
db = client.primer

cursor = db.suggestions.find()

emotion_mat = []
suggestion_ids = []
for data in cursor:
    suggestion_ids.append(data['_id'])
    sad = data['emotion']['sad']
    frustrated = data['emotion']['frustrated']
    angry = data['emotion']['angry']
    anxious = data['emotion']['anxious']
    emotion_mat.append([sad, frustrated, angry, anxious])
    
emotion_mat = np.array(emotion_mat)
# normalization
emotion_mat = preprocessing.normalize(emotion_mat)



# extract K-Means

n_clusters = 6
clf = KMeans(n_clusters=n_clusters)
predictions = clf.fit_predict(emotion_mat)
means = clf.cluster_centers_

suggestion_clusters = []
for c in range(n_clusters):
    print sum(predictions==c)
    suggestion_clusters.append([suggestion_ids[x] for x in range(len(predictions)) if predictions[x]==c])

with open('../data/suggestion_clusters.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile)
    for suggestion_cluster in suggestion_clusters:
        writer.writerow(suggestion_cluster)

#print suggestion_clusters
joblib.dump(clf, '../data/suggestion_kmeans.pkl')
