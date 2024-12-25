import os
import requests
import io
from PIL import Image
import numpy as np
import torch
import shutil
import time

class SetuNode:
    """
    A node to fetch setu images from the Lolisuki API.

    Attributes
    ----------
    RETURN_TYPES (`tuple`):
        The type of each element in the output tuple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tuple.
    FUNCTION (`str`):
        The name of the entry-point method.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    """
    def __init__(self):
        self.image_counter = 0  # Initialize image counter

    @classmethod
    def INPUT_TYPES(s):
        """
        Return a dictionary which contains config for all input fields.
        """
        return {
            "required": {
                "r18": (["0", "1", "2"], {"default": "0"}),
                "tag": ("STRING", {"default": "萝莉|少女", "multiline": True}), 
                "num": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
                "ai": (["0", "1", "2"], {"default": "0"}),
                "gif": (["0", "1"], {"default": "0"}),
                "proxy": ("STRING", {"default": "i.pixiv.re"}),
                "level": ("STRING", {"default": "0-3"}),
                "taste": ("STRING", {"default": "0"}),
                "full": (["0", "1"], {"default": "0"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("image_dir",)
    FUNCTION = "fetch_setu"
    CATEGORY = "Setu"

    def fetch_setu(self, r18, tag, num, ai, gif, proxy, level, taste, full):
        """
        Fetch setu images from the Lolisuki API.

        Args:
            r18 (str): R18 flag.
            tag (str): Tags to filter images.
            num (int): Number of images to fetch.
            ai (str): AI flag.
            gif (str): GIF flag.
            proxy (str): Image proxy service.
            level (str): Image level.
            taste (str): Image taste.
            full (str): Full match flag.

        Returns:
            tuple: A tuple containing the image directory path.
        """
        # Reset image counter for each new fetch
        self.image_counter = 0

        # Define the directories
        save_dir = os.path.join(os.getcwd(), "custom_nodes", "comfyui-setu", "image-save")
        backup_dir = os.path.join(save_dir, "save")

        # Ensure the backup directory exists
        os.makedirs(backup_dir, exist_ok=True)

        # Check if there are any images in the save directory
        if os.path.exists(save_dir):
            for filename in os.listdir(save_dir):
                if filename.endswith(".png"):
                    # Move the image to the backup directory with a timestamped name
                    timestamp = time.strftime("%Y%m%d%H%M%S")
                    new_filename = f"{timestamp}_{filename}"
                    shutil.move(os.path.join(save_dir, filename), os.path.join(backup_dir, new_filename))

        url = "https://lolisuki.cn/api/setu/v1"
        params = {
            "r18": r18,
            "tag": tag,
            "num": num,
            "ai": ai,
            "gif": gif,
            "proxy": proxy,
            "level": level,
            "taste": taste,
            "full": full,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch setu: {response.status_code}")

        data = response.json()
        if data["code"] != 0:
            raise Exception(f"API error: {data['error']}")

        # Assuming we only need the first image in the response
        setu = data["data"][0]
        image_url = setu["urls"]["original"]

        image_response = requests.get(image_url)
        if image_response.status_code != 200:
            raise Exception(f"Failed to fetch image: {image_response.status_code}")

        image = Image.open(io.BytesIO(image_response.content))

        # Save the image to the custom directory with a numbered filename
        self.image_counter += 1
        image_filename = f"setu_image_{self.image_counter}.png"
        image_path = os.path.join(save_dir, image_filename)
        image.save(image_path)

        # Return the directory path without the filename
        return (save_dir,)

    @classmethod
    def IS_CHANGED(s, r18, tag, num, ai, gif, proxy, level, taste, full):
        """
        Force the node to re-execute on each workflow run.
        """
        return time.time()

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "SetuNode": SetuNode
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "SetuNode": "Setu Image Fetcher"
}
