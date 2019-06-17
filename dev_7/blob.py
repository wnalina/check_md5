import os
import string
import uuid
from termcolor import colored, cprint
import azure.storage.blob
from azure.storage.blob import (
    BlockBlobService,
    ContainerPermissions,
)

account_name = 'storagecognitive'
account_key = 'M8J257aCkZ09oVTdG5KCjPUIewhtQCUeTQz2Gj3QR/PdwsdlzlBwwdyTd0Ha9z3BEXr/LNPxpKXAolBpzQAe0w=='
block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)

container_name = 'quickstartblobs'

functions = [{'describe': 'Create Container', 'function_name': 'create_container'},
             {'describe': 'Upload', 'function_name': 'upload'},
             {'describe': 'Download', 'function_name': 'download'},
             {'describe': 'List Group', 'function_name': 'list_blob'}]

def listFunction():
    global functions

    cprint('List Function', 'blue')
    for i in range(len(functions)):
        cprint("\t" + str(i + 1) + ". ", 'red', end='')
        cprint(str(functions[i]['describe']), 'red')


def create_container():
    # Create a container called 'quickstartblobs'.
    block_blob_service.create_container(container_name)

    # Set the permission so the blobs are public.
    block_blob_service.set_container_acl(container_name, public_access=azure.storage.blob.PublicAccess.Container)


def upload():
    global container_name
    # Create a file in Documents to test the upload and download.
    local_path = 'D:/image/myteams'
    # for i in os.listdir(local_path):
    #     print(i)
    local_file_name = "QuickStart_" + str(uuid.uuid4()) + ".txt"
    full_path_to_file = os.path.join(local_path, local_file_name)

    # Write text to the file.
    # file = open(full_path_to_file, 'w')
    # file.write("Hello, World!")
    # file.close()

    print("Temp file = " + full_path_to_file)
    print("\nUploading to Blob storage as blob" + local_file_name)

    # Upload the created file, use local_file_name for the blob name
    # block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)
    # block_blob_service.create_blob_from_path(container_name, 'oil.jpg', local_path)

def download():
    local_path = os.path.expanduser("~\Documents")
    local_file_name = "QuickStart_" + str(uuid.uuid4()) + ".txt"
    # Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in Documents.
    full_path_to_file2 = os.path.join(local_path, string.replace(local_file_name, '.txt', '_DOWNLOADED.txt'))
    print("\nDownloading blob to " + full_path_to_file2)
    block_blob_service.get_blob_to_path(container_name, local_file_name, full_path_to_file2)


def list_blob():
    # List the blobs in the container
    print("\nList blobs in the container")
    generator = block_blob_service.list_blobs(container_name)
    for blob in generator:
        print("\t Blob name: " + blob.name)


listFunction()
while (True):
    select = input('Select function: ')


    if str(select).isdigit() and int(select) >= 0 and int(select) <= len(functions):
        locals()[functions[int(select) - 1]['function_name']]()
    else:
        print("Please input number in range only")