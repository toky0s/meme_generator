from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os
import textwrap


class MemeEngine:
    """A meme engine."""

    def __init__(self, path) -> None:
        self.path = path

    def make_meme(self, img_path: str, text: str, author: str, width: int = 500) -> str:
        """Generate a meme and return meme path"""
        if os.path.exists(img_path):
            # Use text wrapper
            wrapper = textwrap.TextWrapper(width=25, max_lines=12) 
            text_and_author = f"{text} - {author}"
            string = wrapper.fill(text=text_and_author) 

            image = Image.open(img_path)
            imgWidth, imgHeight = image.size
            aspect_ratio = imgWidth / imgHeight

            new_width = min(width, imgWidth)
            new_height = int(new_width / aspect_ratio)

            resized_image = image.resize((new_width, new_height))

            draw = ImageDraw.Draw(resized_image)
            fontSize = 35
            font = ImageFont.truetype('Arial.ttf', size=fontSize)

            # Draw the text on the image
            textPos = (1, 1)
            draw.text(textPos, string, font=font, fill="white", stroke_width=2, stroke_fill='black')

            # Create a safe system path
            path = Path(self.path)
            # Create the directory if it doesn't exist
            path.mkdir(parents=True, exist_ok=True)

            # Join path components
            file_path = path / "output_image.jpg"
            resized_image.save(file_path)
            return file_path
        else:
            raise Exception(f"Image path {img_path} doesn't exist")
