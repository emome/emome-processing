# emome-processing
A recommender system that uses crowdsourced data and public Spotify playlists to make recommendations to users

#### What we've done
* After pulling lyrics from the public Spotify playlists using Spotify API as well as Musixmatch API, NLPK tools and WNAffect are used to process and analyze the lyrics to extract the emotions of a song, where we currently used sadness, frustration, angryness, and anxiousness as the primary emotions. Representitive emotions are to be explored.
* Given the four emotions of a song, we then use K-Means to classify different types of songs to make recommendations to the corresponding users.
