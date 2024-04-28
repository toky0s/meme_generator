import pathlib
import random
import os
import requests
from flask import Flask, render_template, abort, request

from MemeEngine import MemeEngine
from QuoteEngine.Ingestors import Ingestor

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = []
    for f in quote_files:
        suffix = pathlib.Path(f).suffix
        ingestor = Ingestor.create(suffix)
        if (ingestor.can_ingest(f)):
            quotes.extend(ingestor.parse(f))
        else:
            raise Exception('Quote file path should be txt, docx, pdf or csv')

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs.extend([os.path.join(root, name) for name in files])

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)
    
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.
    form_data = request.form
    image_url = form_data['image_url']
    body = form_data['body']
    author = form_data['author']

    response = requests.get(image_url, stream=True) 
    image_path = f"./.tmp/downloaded_image.jpg"
    with open(image_path, 'wb') as fout:
        for chunk in response:
            fout.write(chunk)
    meme_path = meme.make_meme(image_path, body, author)
    return render_template('meme.html', path=meme_path)


if __name__ == "__main__":
    app.run()
