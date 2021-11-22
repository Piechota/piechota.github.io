from lxml import html
import validators
from requests import get
from io import BytesIO
from PIL import Image
from videoprops import get_video_properties
import sys

def main():
    index_html = html.parse( "index_raw.html" )
    media_conteiner = index_html.xpath('//div[@class="media"]')
    media_width = 25 * 0.85
    for medium_conteiner in media_conteiner:
        media = medium_conteiner.xpath('img | video/source')
        media_height = 0
        for medium in media:
            src = medium.get('src')
            width, height = 0, 0
            if medium.tag == 'img':
                image = None
                if validators.url(src):
                    image_raw = get(src)
                    image = Image.open(BytesIO(image_raw.content))                
                else:
                    
                    image = Image.open(src)
                width, height = image.size
            else:
                video_props = get_video_properties(src)
                width, height = video_props['width'], video_props['height']
                
            media_height = max(media_height, height * media_width / width)

        if media_height > 0:
            medium_conteiner.set('style', 'height: ' + str(media_height) + 'vw;')

    index_html.write('index.html', method='html', pretty_print=True)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())