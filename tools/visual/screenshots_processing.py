import base64
import logging
import time
from io import BytesIO

from PIL import ImageDraw, Image
from selene.api import *

logger = logging.getLogger(__name__)


class ImageComparer:
    ACCURACY = 0.0001

    def __init__(self):
        self.result_image = None
        self.screenshot_production = None
        self.screenshot_staging = None

    def compare_pages(self, screenshots_cache, production_url, staging_url):

        browser.open(staging_url).driver.execute_script("document.activeElement.blur();")
        screen_staging = self.take_screenshot()

        browser.open(production_url).driver.execute_script("document.activeElement.blur();")
        screen_production = self.take_screenshot()

        errors = self.compare_pictures(screen_staging=screen_staging, screen_production=screen_production)
        self.save_images_for_report(screenshots_cache)
        assert errors == 0, "Some visual mistakes! Found {} mistaken blocks".format(errors)

    def compare_pictures(self, screen_staging, screen_production):
        self.screenshot_staging = Image.open(BytesIO(screen_staging))
        self.screenshot_production = Image.open(BytesIO(screen_production))
        self.result_image = Image.open(BytesIO(screen_staging))
        columns = 60
        rows = 80
        screen_width, screen_height = self.screenshot_staging.size

        block_width = ((screen_width - 1) // columns) + 1
        block_height = ((screen_height - 1) // rows) + 1
        mistaken_blocks = 0
        for y in range(0, screen_height, block_height + 1):
            for x in range(0, screen_width, block_width + 1):
                region_staging = self.process_region(self.screenshot_staging, x, y, block_width, block_height)
                region_production = self.process_region(self.screenshot_production, x, y, block_width, block_height)

                if region_staging is None or region_production is None:
                    continue
                diff = region_production / region_staging
                if abs(1 - diff) > self.ACCURACY:
                    draw = ImageDraw.Draw(self.result_image)
                    draw.rectangle((x, y, x + block_width, y + block_height), outline="red")
                    mistaken_blocks += 1
        return mistaken_blocks

    def image_to_b64(self, img):
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str

    def process_region(self, image, x, y, width, height):
        region_total = 0

        for coordinateY in range(y, y + height):
            for coordinateX in range(x, x + width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel)
                except:
                    return

        return region_total

    def save_images_for_report(self, screenshots_cache):
        screenshots_cache['diff'] = self.image_to_b64(self.result_image)
        screenshots_cache['production'] = self.image_to_b64(self.screenshot_production)
        screenshots_cache['staging'] = self.image_to_b64(self.screenshot_staging)

    def take_screenshot(self):
        browser.driver.execute_script("scrollTo(0,0);")
        time.sleep(1)
        screenshot = browser.driver.get_screenshot_as_png()
        return screenshot

    def divide_to_cells(self, image):
        image = Image.open(BytesIO(image))
        columns = 30
        rows = 40
        screen_width, screen_height = image.size

        block_width = ((screen_width - 1) // columns) + 1
        block_height = ((screen_height - 1) // rows) + 1

        for i in range(0, screen_height, block_height + 1):
            for j in range(0, screen_width, block_width + 1):
                draw = ImageDraw.Draw(image)
                draw.rectangle((j, i, j + block_width, i + block_height), outline="blue")

        image.save("cells.png")


image_comparer = ImageComparer()
