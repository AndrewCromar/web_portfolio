from PIL import Image
import os

thumb_dir = "thumbnails"
os.makedirs(thumb_dir, exist_ok=True)

for filename in os.listdir("."):
    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        try:
            img = Image.open(filename)

            # Convert to RGB so it can save as JPG
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.thumbnail((200, 200))

            base, _ = os.path.splitext(filename)
            outpath = os.path.join(thumb_dir, f"{base}.jpg")

            img.save(outpath, "JPEG", quality=60)

            print(f"Created {outpath}")

        except Exception as e:
            print(f"Skipping {filename}: {e}")