# importar os pacotes necessários
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from . import databaseOperations as dbOperations
import wordcloud

def wordCloud(cur, conn):
  userIds = dbOperations.getDistinctUserIds(cur)
  for userId in userIds:
    tags = dbOperations.getCapturedTags(cur, userId)

    all_summary = " ".join(s[0][0] for s in tags)

    # lista de stopword
    stopwords = set(STOPWORDS)
    stopwords.update(["da", "meu", "em", "você", "de", "ao", "os", "br", "o", "a", "para", "e", "quot"])

    # gerar uma wordcloud
    wordcloud = WordCloud(stopwords=stopwords,
                          background_color="black",
                          width=1600, height=800).generate(all_summary)

    # mostrar a imagem final
    fig, ax = plt.subplots(figsize=(10,6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()

    plt.imshow(wordcloud)
    wordcloud.to_file(f"{userId[0]}-wordcloud.png")
