import sys
import os
from PIL import Image
from resizeimage import resizeimage
import moviepy.editor as mp

def main():
    media_path = "./media/"
    save_dir = "small/"
    directory = os.fsencode(media_path)
    
    for file in os.listdir(directory):
        filename_full = os.fsdecode(file)
        if os.path.isfile(media_path + filename_full):
            print( filename_full )
            filename, file_extension =  os.path.splitext( filename_full )
            src_filename = media_path + filename_full
            dst_filename = media_path + save_dir + filename_full
            if file_extension == '.mp4':
                clip = mp.VideoFileClip(src_filename)
                width, heigth = clip.size
                if width > 700:
                    clip = clip.resize(width=700) 
                clip.write_videofile( dst_filename )
            else:
                image = Image.open(src_filename)
                width, heigth = image.size                
                if width > 700:
                    image = resizeimage.resize_width(image, 700)
                image.save( dst_filename, image.format)

    return 0

if __name__ == '__main__':
    sys.exit(main())