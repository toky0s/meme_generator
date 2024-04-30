# Overview
Project to generate random memes at the press of a button or from your input.

1. Install library
python
```
pip install -r requirements.txt
```
2. Install xpdf and setup enviroment variable
3. Run Flask app
python
```
flask --app app run   
```

4. Check python code style
 pycodestyle ./ --exclude python_env

## Modules
QuoteEngine contains Ingestor classes that allow creating QuoteModels based on given input file formats.
The meme.py file is a simple CLI that allows you to create meme images using the command line.
MemeEngine, receives input as image paths, meme body and meme author to create meme image.