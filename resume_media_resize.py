import sys
import os
from PIL import Image
from resizeimage import resizeimage
import moviepy.editor as mp
from shutil import copyfile
from termcolor import colored

def main():
    args = sys.argv[1:]
    formats_array = None
    if '-f' in args:
        formats_index = args.index('-f') + 1
        formats_str = args[formats_index].replace(" ", "")
        formats = formats_str.split(',')
        for index, f in enumerate(formats):
            if f[0] != '.':
                formats[index] = '.' + f
        
        formats_array = set(formats)

    media_path = "./media/"
    save_dir = "small/"
    directory = os.fsencode(media_path)
    
    for file in os.listdir(directory):
        filename_full = os.fsdecode(file)
        if os.path.isfile(media_path + filename_full):            
            filename, file_extension =  os.path.splitext( filename_full )
            src_filename = media_path + filename_full
            dst_filename = media_path + save_dir + filename_full

            if len(formats_array) == 0 or file_extension in formats_array:
                print( filename_full )
                if file_extension == '.mp4':
                    clip = mp.VideoFileClip(src_filename)
                    width, heigth = clip.size
                    if width < 700:                    
                        copyfile(src_filename, dst_filename)
                        continue

                    print( colored("some MP4s have problems, check: " + filename_full, 'yellow') )
                    clip2 = clip.resize(width=700) 
                    clip2.write_videofile( dst_filename )
                else:
                    image = Image.open(src_filename)
                    width, heigth = image.size         
                    if width < 700:                    
                        copyfile(src_filename, dst_filename)
                        continue
                    
                    if file_extension == '.gif':
                        print( colored("Gif resize isn't supported: " + filename_full, 'red') )
                        continue

                    image = resizeimage.resize_width(image, 700)
                    image.save( dst_filename, image.format)

    return 0

if __name__ == '__main__':
    sys.exit(main())