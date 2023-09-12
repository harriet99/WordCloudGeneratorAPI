from wordcloud import WordCloud
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure nltk data is downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Flask web server object
app = Flask(__name__)

# Font path setting
font_path = 'Roboto-Bold.ttf'

def get_tags(text, max_count):
    # Tokenize and filter out stopwords and non-alphabetic tokens
    tokens = [word for word in word_tokenize(text) if word.isalpha() and word not in stopwords.words('english')]
    count = Counter(tokens)
    return dict(count.most_common(max_count))

def make_cloud_image(tags, file_name):
    word_cloud = WordCloud(
        font_path=font_path,
        width=800,
        height=800,
        background_color="white",
    )
    word_cloud = word_cloud.generate_from_frequencies(tags)
    fig = plt.figure(figsize=(10, 10))
    plt.imshow(word_cloud)
    plt.axis("off")
    fig.savefig("outputs/{0}.png".format(file_name))

def process_from_text(text, max_count, words):
    tags = get_tags(text, max_count)
    for n, c in words.items():
        if n in tags:
            tags[n] = tags[n] * int(words[n])
    make_cloud_image(tags, "output")

@app.route("/process", methods=['GET', 'POST'])
def process():
    content = request.json
    words = {}
    if content['words'] is not None:
        for data in content['words'].values():
            words[data['word']] = data['weight']
    process_from_text(content['text'], content['maxCount'], words)
    result = {'result': True}
    return jsonify(result)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)