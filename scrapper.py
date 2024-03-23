# Pillow selenium requests

from selenium import webdriver
import chromedriver_autoinstaller
import io
from PIL import Image
import requests

chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

def download_image(url, path, file_name):
    img_content = requests.get(url).content
    img_file = io.BytesIO(img_content)
    img = Image.open(img_file)
    save_to = path + file_name

    with open(save_to, 'wb') as f:
        img.save(f, format='JPEG')

    print('done')
    
url = 'https://i.natgeofe.com/n/548467d8-c5f1-4551-9f58-6817a8d2c45e/NationalGeographic_2572187_square.jpg'
download_image(url=url, path='/img', file_name='cat.jpg')
# driver.get("http://www.python.org")
# assert "Python" in driver.title