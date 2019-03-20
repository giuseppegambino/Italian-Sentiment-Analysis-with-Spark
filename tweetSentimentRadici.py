import pandas as pd

dfTweet = pd.read_csv("desktop/tesi/tweet/tweetClean.csv")

emoticonsPositive = ('😇','😊','❤️','😘','💞','💖','🤗','💕','👏','🎉','👍','🔝')
emoticonsNegative = ('😂','😡','😠','😭','🤦‍','🤷🏼‍','😞','😱','😓','👎')

radiciPositive = ("ama","amo","affett","allegr","amabil","apprezz","armon","affet",
                  "applaus","abbracc","ador",
                  "bell","ben","beat","brav","buon","benef","brill",
                  "cuor","coeren","celebr",
                  "dolc","divert",
                  "evviva","emoz","elog",
                  "felic","fest","facil",
                  "gentil","god","grazi","generos","gioi", 
                  "innamor", "interes","insieme",
                  "libert",
                  "maestos","miglior",
                  "pace","passion","perfe","piac","pura","purezz","prezios","promuov",
                  "rilass","riabbracc",
                  "solida","spero","speran","success","sì","sacr","stupend","spettacol", 
                  "viv","vin","valor","vale","vera","vittor")
radiciNegative = ("accus","amaro","amarez","arm","ammazz", 
                  "brut","boicott","boh","bho",
                  "condann","cazz","crisi","critic","coglion", 
                  "decent","depress","detest","disgr","delir","damn","drog",
                  "fumo","fuma",
                  "esorcis",
                  "fascis",
                  "guai", 
                  "immat","insult", "inuman","impone",
                  "lent",  
                  "mor","merd","male","maial",
                  "no", "nega","ncazz","negr", 
                  "od","oscur",
                  "perde","preoccup","pusillanim","porc",
                  "rovina",
                  "schif","satan","sprof","soffri","soffer","scandal","scars","sporc", "spar","stalk",
                  "trist","trash","tarocc",
                  "vergogn",
                  "zitt")
radiciDaEscludere = ("now", "nom", "not","noz", "amp", "nor","veramente","imponent")

def textSentiment(string):
    val = 0
    list = string.split()
    for word in list:

        if word in emoticonsPositive:
            return 2    # Tweet considerato positivo

        elif word in emoticonsNegative:
            return 0    # Tweet considerato negativo

        else:
            if not word.startswith(radiciDaEscludere):

                if (word.startswith(radiciPositive)):
                    val = val + 1

                if (word.startswith(radiciNegative)):
                    if word not in ("non", "nonostante"):
                        val = val - 1

                # Il 'non' cambia dinamicamente la polarita' del tweet
                if word == "non":
                    val = val * -1

                # Tutte le parole prima di 'ma' e 'però' non vengono considerate
                if word in ("ma", "però"):
                    val = 0

    if (val > 0):
        label = 2
    elif(val < 0):
        label = 0
    else:
        label = 1
    return label

dfTweet[['label']] = dfTweet['tweet'].apply(lambda tweet: pd.Series(textSentiment(tweet)))

# Ordino il dataframe per la successiva parte di Machine Learning
dfTweet = dfTweet[['id', 'tweet', 'label', 'tweetIta']]



# from nltk.stem.snowball import SnowballStemmer
# stemmer = SnowballStemmer("italian")

# def stemming(string):
#     list = string.split()
#     wordStem = ""
#     text = ""
#     for word in list:
#         wordStem = stemmer.stem(word)    
#         text = text + wordStem + " "
    
#     text = text.rstrip()
#     return text

# dfTweet['tweet'] = dfTweet["tweet"].apply(lambda tweet: pd.Series(stemming(tweet)))

# print(dfTweet)

dfTweet.to_csv("desktop/tesi/tweet/tweetSentiment.csv", index=False)



