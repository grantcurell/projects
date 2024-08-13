from PIL import Image, ImageDraw, ImageFont
import os
import multiprocessing


def generate_image(char, font, img_size, output_folder):
    img = Image.new('L', img_size, color=255)  # Create a white image
    draw = ImageDraw.Draw(img)
    bbox = draw.textbbox((0, 0), char, font=font)
    text_x = (img_size[0] - (bbox[2] - bbox[0])) // 2 - bbox[0]
    text_y = (img_size[1] - (bbox[3] - bbox[1])) // 2 - bbox[1]
    draw.text((text_x, text_y), char, font=font, fill=0)  # Draw character in black

    img_path = os.path.join(output_folder, f"{ord(char):04X}.png")
    img.save(img_path)


def generate_images_from_utf8(output_folder, font_path=None, img_size=(64, 64)):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Set font (default to a system font if not provided)
    try:
        if font_path is None or not os.path.exists(font_path):
            font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"  # Fallback to Noto Sans CJK Traditional
        font = ImageFont.truetype(font_path, size=48)
    except OSError:
        print("Error: Cannot open font resource. Please check the font path.")
        return

    # Generate images for a range of Unicode characters
    unicode_start = 0x4E00  # Start of CJK Unified Ideographs
    unicode_end = 0x9FFF  # End of CJK Unified Ideographs

    with multiprocessing.Pool() as pool:
        pool.starmap(generate_image, [(chr(codepoint), font, img_size, output_folder) for codepoint in
                                      range(unicode_start, unicode_end + 1)])

    print(f"Generated images for Unicode characters U+{unicode_start:04X} to U+{unicode_end:04X}")


if __name__ == "__main__":
    output_folder = "output_images"
    generate_images_from_utf8(output_folder)
