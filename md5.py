from hashlib import md5
from base64 import b64encode
import os

def getmd5(fname):
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return b64encode(hash_md5.digest()).decode('utf-8')
    # return (hash_md5.hexdigest())

while  True:

    full_path_to_file = input("Enter full path to file: ")
    md5_check = input("Enter md5: ")
    # t = full_path_to_file
    # local_path = 'C:/Users/NALINA/Desktop/'
    # local_file_name = 'md5-1.txt'
    # full_path_to_file = os.path.join(local_path, local_file_name)

    # vhd = 'C:/Users/NALINA/Documents/image file/myvhdfilename_2.vhd'
    print('working...')
    result = getmd5(full_path_to_file)
    print("md5 of " + str(full_path_to_file) + " => " + str(result)),
    if result == md5_check:
        print('md5 is match')
    else:
        print('md5 not match')
    print('------------------------------')

