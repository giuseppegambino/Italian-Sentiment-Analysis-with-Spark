# -*- coding: UTF-8 -*-

from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml import Pipeline
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import col
from pyspark.sql.functions import count
import pyspark.sql.functions as f

dataFrame = spark.read.format("csv")\
    .option("header", "true")\
    .option("inferSchema", "true")\
    .option("encoding", "utf-8")\
    .load("desktop/tesi/tweet/tweetSentiment.csv")

# Genero il trainingSet e il dataSet selezionando
# solamente le colonne che servono per l'algoritmo di ML
(trainingD, testD) = dataFrame.randomSplit([0.9, 0.1])
trainingData = trainingD.select("id","tweet","label")
testData = testD.select("id","tweet","label")

# Configurazione del dataframe per la libreria di ML
tokenizer = Tokenizer(inputCol="tweet", outputCol="words")
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="rawFeatures")
idf = IDF(minDocFreq=3, inputCol="rawFeatures", outputCol="features")

# Invocazione dell'algoritmo Naive Bayes
nb = NaiveBayes()

# Dichiarazione della pipeline
pipeline = Pipeline(stages=[tokenizer, hashingTF, idf, nb])

# Training del modello con trainingData
model = pipeline.fit(trainingData)

# Valutazione del modello con trainingData
predictions = model.transform(trainingData)
evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
evaluator.evaluate(predictions)

# Valutazione del modello con testData
predictions = model.transform(testData)
evaluator = MulticlassClassificationEvaluator(predictionCol="prediction")
evaluator.evaluate(predictions)

# Mostra in output il dataframe della pipeline
predictions.show(10)

# Mostra il totale di tweet positivi, negativi e neutri
tweetPosNegNeu = predictions.groupBy("prediction").count()
tweetPosNegNeu.show()

# Parole più frequenti nei tweet positivi
tweetPosWord = predictions.select("label","prediction","tweet")\
    .withColumn('word', f.explode(f.split(f.col('tweet'), ' ')))\
    .where(col('label') == 2)\
    .groupBy('word')\
    .count()\
    .sort('count', ascending=False)
tweetPosWord.show(40)

# Parole più frequenti nei tweet negativi
tweetNegWord = predictions.select("label","prediction","tweet")\
    .withColumn('word', f.explode(f.split(f.col('tweet'), ' ')))\
    .where(col('label') == 0)\
    .groupBy('word')\
    .count()\
    .sort('count', ascending=False)
tweetNegWord.show(40)

# Salvataggio su file csv con tweet non filtrati affiancati dalla previsione
testIta = testD.select("id","tweetIta")
outputTemp = predictions.join(testIta,"id")
output = outputTemp.select("prediction","tweetIta")
output.coalesce(1).write.csv("desktop/risultati.csv")








