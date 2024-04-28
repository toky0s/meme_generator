import os
import random
import pathlib
import argparse

from QuoteEngine.Ingestors import Ingestor
import models
from MemeEngine import MemeEngine
import models.QuoteModel


def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given an path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        img = random.choice(imgs)
    else:
        img = path

    if body is None:
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

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        quote = models.QuoteModel.QuoteModel(body, author)

    meme = MemeEngine('./.tmp')
    path = meme.make_meme(img, quote.body, quote.author)
    return path


if __name__ == "__main__":
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    parser = argparse.ArgumentParser(
                    prog='Meme Generator Command-Line Interface',
                    description='Create super cute meme',
                    epilog='From Udacity')

    parser.add_argument('--body')           # positional argument
    parser.add_argument('--author')      # option that takes a value
    parser.add_argument('--path')  
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
