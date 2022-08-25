from PIL import Image,ImageChops,ImageOps,UnidentifiedImageError
from io import BytesIO
import io
import requests
import ftplib
import pandas as pd
import os.path

CRED = '\033[43m'
def read_csv():
    urls = []
    data = pd.read_csv("vers.csv",sep=';',encoding='ANSI')
    df = pd.DataFrame(data)
    for url in df['Img']:
        urls.append(url)

    return urls


def trim(urls):

    for url in urls:
        # name = url.replace('https://slava.su/image/catalog/foto/', '')
        name_patch = os.path.split(url)
        name = name_patch[1]
        path = name_patch[0].replace('https://slava.su/image/','')
        r = requests.get(url)
        im = Image.open(BytesIO(r.content))
        bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
        diff = ImageChops.difference(im, bg)
        diff = ImageChops.add(diff, diff, 0.1, -100)
        bbox = diff.getbbox()
        if bbox:
            im = im.crop(bbox)
            im = ImageOps.expand(im, border=10, fill='white')
            print('Cохраняю картинку: '+ name)
            width, height = im.size
            if width < 320:
                im = ImageOps.contain(im, (1000,1000))
            if height < 1000:
                im = ImageOps.contain(im, (1000, 1000))
            session = ftplib.FTP('***', '***', '***') # FTP Данные
            im.seek(0)
            toftp = io.BytesIO()
            im.save(toftp,format='PNG')
            toftp.seek(0)
            session.cwd(path)            # file to send
            print('Отправляю фото на сервер по пути:'+ path)
            session.storbinary(f'STOR {os.path.split(url)[1]}', toftp)     # send the file
            print('Завершено!')
            toftp.close()  # close file and FTP


def main():
    urls = read_csv()
    trim(urls)


if __name__ == '__main__':
    main()