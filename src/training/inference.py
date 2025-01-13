import torch
import io
import os
import models
from PIL import Image
from tqdm import tqdm
from transformers import AutoProcessor
import glob
import base64


def encode_png_to_base64(file_path) -> str:
    """
    Encodes a PNG file to a Base64 string.

    Args:
        file_path (str): Path to the PNG file.

    Returns:
        str: Base64 encoded string.
    """
    try:
        with open(file_path, "rb") as png_file:
            # Read the binary content of the file
            binary_data = png_file.read()
            # Encode the binary data to Base64
            base64_encoded_str = base64.b64encode(binary_data).decode("utf-8")
            return base64_encoded_str
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error: {str(e)}"


def inference(model, processor, b64str):

    with Image.open(io.BytesIO(base64.b64decode(b64str))) as img, torch.no_grad():

        img = img.convert('RGB')
        inputs = processor(images=[img, ], return_tensors="pt")
        outputs = model(inputs)
    char_arr = [chr(ord('a') + idx)for idx in torch.argmax(outputs[0, :, :], axis=1)]
    ret_str = ''.join(char_arr)
    return ret_str


if __name__ == '__main__':
    model = models.CLIPClassifier(26, 4)
    model.load_state_dict(torch.load('/tmp/dev.model', map_location=torch.device('cpu')))
    model.eval()
    processor = AutoProcessor.from_pretrained("openai/clip-vit-base-patch32")
    file_list = glob.glob('/volume/payo-ws/git/captcha/src/test/*.png')

    hit = 0
    for filename in tqdm(file_list):
        # encode image as b64str
        b64str = encode_png_to_base64(filename)
        pred = inference(model, processor, b64str)
        label = os.path.basename(filename).replace('.png', '')

        if pred == label:
            hit += 1

    print(f'Accuracy: {hit / len(file_list) * 100:.2f}%')
