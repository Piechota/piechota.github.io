from lxml import html
import validators
from requests import get
from io import BytesIO
from PIL import Image
from videoprops import get_video_properties
import sys
import copy

def main():
    index_html = html.parse( "index_raw.html" )
    resume_css = open("css/resume.css", 'w')
    resume_raw_css = open("css/resume_raw.css", 'r')
    resume_css.write(resume_raw_css.read())
    resume_raw_css.close()

    prev_element = html.fromstring('<a class="prev" onclick="plusSlides(this.parentNode, -1)">&#10094;</a>' )
    next_element = html.fromstring('<a class="next" onclick="plusSlides(this.parentNode, 1)">&#10095;</a>' )

    resume_sections = index_html.xpath('//div[@class="resume_section_element"]')
    for resume_section in resume_sections:        
        media_conteiner = resume_section.xpath('div[@class="media"]')
        if len(media_conteiner) > 0:
            id_name = resume_section.xpath('h3')[0].text_content()
            id_name = id_name.replace(' ', '_')
            id_name = id_name.replace(':', '')
            id_name = id_name.replace('/', '')
            id_name = id_name.replace("'", '')
            media_width = 25 * 0.85
            media_width_mobile = 100 * 0.85
        
            if len(media_conteiner[0]) > 1:
                media_conteiner[0].append(copy.deepcopy(prev_element))
                media_conteiner[0].append(copy.deepcopy(next_element))

            media = media_conteiner[0].xpath('img | video/source')
            media_height = 0
            media_height_mobile = 0
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
                media_height_mobile = max(media_height_mobile, height * media_width_mobile / width)

            if media_height > 0:
                media_conteiner[0].set('id', id_name)
                resume_css.write(  "\n#" + id_name + """ {
    height:""" + str(media_height) + """vw;
}
@media only screen and (max-width: 768px) {
    #""" + id_name + """ {
        height: """ + str(media_height_mobile) + """vw;
    }
}""" )

    index_html.write('index.html', method='html', pretty_print=False)
    resume_css.close()

    return 0

if __name__ == '__main__':
    sys.exit(main())