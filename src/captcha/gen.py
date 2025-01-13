from PIL import Image, ImageDraw, ImageFont
import random
import string
import os
from tqdm import tqdm
from glob import glob


def generate_captcha_image(text, font, output_path,
                           width=120, height=100,
                           bg_color=(2, 102, 222),  # approximate bright-blue
                           text_color=(255, 255, 255)):  # white
    """
    Generate a single CAPTCHA-like image with given text and font,
    adding random rotation, offset, and smoother edges.
    """
    # 1. Create a background image
    img = Image.new('RGB', (width, height), color=bg_color)

    # 2. Create a temporary transparent image for the text
    text_layer = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_layer)

    # 3. Measure text size
    text_width, text_height = text_draw.textsize(text, font=font)

    # 4. Random offset
    max_offset_x = 5
    max_offset_y = 5
    offset_x = random.randint(-max_offset_x, max_offset_x)
    offset_y = random.randint(-max_offset_y, max_offset_y)

    # 5. Center + offset
    x = (width - text_width) // 2 + offset_x
    y = (height - text_height) // 2 + offset_y

    # 6. Draw text onto the transparent layer
    text_draw.text((x, y), text, fill=text_color, font=font)

    # 7. Apply random rotation with a better resampling filter for smooth edges
    angle = random.randint(-15, 15)
    # Use BICUBIC (good for smoothed edges).
    # If using Pillow >= 9, you can do Image.Resampling.LANCZOS for even better results.
    rotated_text_layer = text_layer.rotate(
        angle,
        expand=True,
        resample=Image.BICUBIC  # or Image.Resampling.LANCZOS
    )

    # 8. Re-calculate position after rotation
    new_w, new_h = rotated_text_layer.size
    paste_x = (width - new_w) // 2
    paste_y = (height - new_h) // 2

    # 9. Paste the rotated text onto the background
    img.paste(rotated_text_layer, (paste_x, paste_y), rotated_text_layer)

    # 10. Save the result
    img.save(output_path)
    print(f"Saved: {output_path}")


def random_string(length=4):
    characters = string.ascii_lowercase
    return ''.join(random.choice(characters) for _ in range(length))


if __name__ == "__main__":
    # Find all TTF fonts in "../fonts/"
    fl = glob("../fonts/*.ttf", recursive=False)
    font_size = 50
    fonts = [ImageFont.truetype(font_path, font_size) for font_path in fl]

    # Directory for output samples
    output_dir = "captcha_samples"
    os.makedirs(output_dir, exist_ok=True)

    for i in tqdm(range(1)):
        random_txt = random_string()
        fname = f"{random_txt}.png"
        output_path = os.path.join(output_dir, fname)

        generate_captcha_image(
            text=random_txt,
            font=random.choice(fonts),
            output_path=output_path
        )
