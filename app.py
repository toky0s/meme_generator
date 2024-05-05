import pathlib
import random
import os
from PIL import UnidentifiedImageError
import requests
from flask import Flask, render_template, abort, request

from MemeEngine import MemeEngine
from QuoteEngine.Ingestors import Ingestor
from meme import generate_meme

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']
    quotes = []
    for f in quote_files:
        suffix = pathlib.Path(f).suffix
        ingestor = Ingestor.create(suffix)
        if (ingestor.can_ingest(f)):
            quotes.extend(ingestor.parse(f))
        else:
            raise Exception('Quote file path should be txt, docx, pdf or csv')

    images_path = "./_data/photos/dog/"

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
    try:
        form_data = request.form
        image_url =None if str.strip(form_data['image_url']) == "" else form_data['image_url']
        body = None if str.strip(form_data['body']) == "" else form_data['body']
        author = None if str.strip(form_data['author']) == "" else form_data['author']

        image_path = None
        meme_path = None
        if (image_url is not None):
            response = requests.get(image_url, stream=True)
            image_path = "./.tmp/downloaded_image.jpg"
            with open(image_path, 'wb') as fout:
                for chunk in response:
                    fout.write(chunk)
            meme_path = generate_meme(image_path, body, author)
            os.remove(image_path)
        else:
            meme_path = generate_meme(image_path, body, author)
        return render_template('meme.html', path=meme_path)
    except UnidentifiedImageError as ex:
        error = f"Url should be a image, {ex}"
        return render_template('error.html', error=error)
    except Exception as ex:
        return render_template('error.html', error=ex)


if __name__ == "__main__":
    app.run()
