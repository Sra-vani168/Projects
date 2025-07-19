from pymongo import MongoClient
from datetime import datetime
from textblob import TextBlob
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

client = MongoClient("mongodb://localhost:27017/")
db = client["social_analytics"]
collection = db["posts"]

sample_posts = [
    {"user": "kiran", "text": "AI is revolutionizing the world! #AI #Future",
        "timestamp": datetime.now()},
    {"user": "meena", "text": "Climate change is real. We need action now! #ClimateCrisis",
        "timestamp": datetime.now()},
    {"user": "ravi", "text": "Feeling happy and blessed! #Grateful",
        "timestamp": datetime.now()},
    {"user": "sita", "text": "Python makes data engineering so easy. #Python #Data",
        "timestamp": datetime.now()},
]

collection.insert_many(sample_posts)
print("Sample posts inserted!\n")

posts = collection.find()
word_count = 0
hashtags = []
sentiments = {"positive": 0, "neutral": 0, "negative": 0}

print("Analyzing Posts...\n")

for post in posts:
    text = post["text"]
    word_count += len(text.split())
    hashtags.extend(re.findall(r"#\w+", text))

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0:
        sentiments["positive"] += 1
    elif polarity == 0:
        sentiments["neutral"] += 1
    else:
        sentiments["negative"] += 1

print(f" Total Words: {word_count}")
print(f" Sentiment Summary: {sentiments}")
print(f" Top Hashtags: {Counter(hashtags).most_common(5)}\n")

all_texts = " ".join([doc["text"] for doc in collection.find()])
wordcloud = WordCloud(width=800, height=400,
                      background_color='white').generate(all_texts)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("WordCloud of Social Media Posts")
plt.show()