from datetime import datetime
import piexif

import os
import time
import re

folder = './'

def get_datetime(filename):
    re1 = re.compile(r'IMG-\d{8}-WA\d*')
    re2 = re.compile(r'VID-\d{8}-WA\d*')
    re3 = re.compile(r'WhatsApp Image \d{4}-\d{2}-\d{2} at \d*.\d*.\d* (AM|PM).*')
    re4 = re.compile(r'WhatsApp Video \d{4}-\d{2}-\d{2} at \d*.\d*.\d* (AM|PM).*')

    if re1.match(filename) is not None or re2.match(filename) is not None:
        date_str = filename.split('-')[1]
        return datetime.strptime(date_str, '%Y%m%d').strftime("%Y:%m:%d %H:%M:%S")

    elif re3.match(filename) is not None or re4.match(filename) is not None:
        filename_split = filename.split(' ')
        datetime_str = filename_split[2]+" "+filename_split[4]+" "+filename_split[5].split(".")[0]
        return datetime.strptime(datetime_str, '%Y-%m-%d %I.%M.%S %p').strftime("%Y:%m:%d %H:%M:%S")
    return None
    

def get_date(filename):
    re1 = re.compile(r'IMG-\d{8}-WA\d*')
    re2 = re.compile(r'VID-\d{8}-WA\d*')
    re3 = re.compile(r'WhatsApp Image \d{4}-\d{2}-\d{2} at \d*.\d*.\d* (AM|PM).*')
    re4 = re.compile(r'WhatsApp Video \d{4}-\d{2}-\d{2} at \d*.\d*.\d* (AM|PM).*')

    if re1.match(filename) is not None or re2.match(filename) is not None:
        date_str = filename.split('-')[1]
        return datetime.strptime(date_str, '%Y%m%d')
    elif re3.match(filename) is not None or re4.match(filename) is not None:
        filename_split = filename.split(' ')
        datetime_str = filename_split[2]+" "+filename_split[4]+" "+filename_split[5].split(".")[0]
        return datetime.strptime(datetime_str, '%Y-%m-%d %I.%M.%S %p')
    return None


allowedFileEndings = ['mp4','jpg','3gp','jpeg']

filenames = [fn for fn in os.listdir(folder) if fn.split('.')[-1] in allowedFileEndings]

num_files = len(filenames)
print("Number of files: {}".format(num_files))

for i, filename in enumerate(filenames):
    date = get_datetime(filename)
    if date is None:
        print("Error: Incorrect filename format -{filename} ".format(filename = folder+filename))
    elif filename.endswith('mp4') or filename.endswith('3gp'):
        date = get_date(filename)
        modTime = time.mktime(date.timetuple())
        os.utime(folder + filename, (modTime, modTime))

    elif filename.endswith('jpg') or filename.endswith('jpeg'):
        exif_dict = {'Exif': {piexif.ExifIFD.DateTimeOriginal: get_datetime(filename)}}
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, folder + filename)

    num_digits = len(str(num_files))
    print("{num:{width}}/{max} - {filename}"
            .format(num=i+1, width=num_digits, max=num_files, filename=folder+filename))
print('\nDone!')
