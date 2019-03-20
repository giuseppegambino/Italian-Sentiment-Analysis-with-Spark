import pandas as pd
from nltk.corpus import stopwords

df = pd.read_csv("desktop/tesi/tweet/tweetIta.csv", encoding='utf-8')

# Elimino i tweet uguali
df = df.drop_duplicates(subset='tweet')
df['tweetIta']=df['tweet']

# Aggiungo uno spazio prima e dopo ogni stopword in modo tale 
# da non coniderare il caso in cui la stopword è contenuta in una parola
words = set(stopwords.words('italian'))
stopwords = [' ' + x + ' ' for x in words]

emoticons =  ('😇','😊','❤️','😘','💞','💖','🤗','💕','👏','🎉','👍',
              '😂','😡','😠','😭','🤦‍','🤷🏼‍','😞','👎','😱','😓','🔝')

df.tweet = df.tweet.replace("@[\w]*[_-]*[\w]*"," ",regex=True)   # rimuovo i tag
df.tweet = df.tweet.replace("https?://[\w/%-.]*"," ",regex=True) # rimuovo i link url
# Rimuovo tutto tranne le lettere dell'alfabeto e le emoticons
df.tweet = df.tweet.replace('[^ a-zA-Zà-ú'
                            '\😇\😊\❤️\😘\💞\💖\🤗\💕\👏\🎉\👍'
                            '\😂\😡\😠\😭\🤦‍\🤷🏼‍\😞\😱\👎\😓\🔝]', " ",regex=True)    
for word in emoticons:
    df.tweet = df.tweet.replace(word, " "+word+" ",regex=True) 

df.tweet = df.tweet.replace('\s+', ' ',regex=True)               # Rimuovo gli spazi in eccesso 
df.tweet = df.tweet.replace('^ ', '', regex=True)                # Rimuovo lo spazio all'inizio
df.tweet = df.tweet.replace(' $', '', regex=True)                # Rimuovo lo spazio alla fine
df.tweet = df.tweet.apply(lambda x: x.lower())                   # Rendo tutto minuscolo
df.tweet = df.tweet.replace('^', ' ', regex=True) 
df.tweet = df.tweet.replace('$', ' ', regex=True)

for word in stopwords:
    df.tweet = df.tweet.replace(word, ' ',regex=True)

# Rimuovo gli spazi all'inizio e alla fine di ogni tweet
df.tweet = df.tweet.apply(lambda x: x.strip())         
# Rimuovo i tweet rimasti vuoti
df = df[df.tweet != '']                          
df.to_csv("desktop/tesi/tweet/tweetClean.csv", index=False)

