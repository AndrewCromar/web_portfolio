# Thumbnails

Generated using Python with Pillow:

- Resized to 200px wide (maintaining aspect ratio)
- Saved as JPEG with quality 30

```python
from PIL import Image

img = Image.open("source.png")
img.thumbnail((200, 200))
img.save("thumbnail.jpg", quality=30)
```
### OR

Use the (main.py)[main.py] by placing it in the folder with the images to make copies of and running it.