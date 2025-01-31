#! /home/asus/env/bin/python

import sys
import os
from dataclasses import dataclass
from mimetypes import MimeTypes
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.metadata']

FOLDER_MIME_TYPE = "application/vnd.google-apps.folder"
GDRIVE_PREFIX = "gd://"
CREDENTIALS_PATH = os.path.expanduser("~/.gdrive/credentials.json")
TOKEN_PATH = os.path.expanduser("~/.gdrive/token.json")

@dataclass
class DriveItem:
    id: str
    name: str
    is_folder: bool

def print_usage():
    pass

def get_service(scopes):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, scopes)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, scopes
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)

def query_items(service, query: str) -> list[DriveItem]:
    page_token = None
    results = []

    while True:
        response = (
            service.files()
            .list(
                q=query,
                spaces='drive', 
                pageSize=20, 
                fields="nextPageToken, files(id, name, mimeType)",
                supportsAllDrives=True,
                pageToken=page_token
            )
            .execute()
        )
        items = response.get("files", [])

        if not items:
            break

        for item in items:
            results.append(DriveItem(
                id=item['id'],
                name=item['name'],
                is_folder=item['mimeType'] == FOLDER_MIME_TYPE
            ))
        
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    
    return results

def list_items(service, parent_id:str='root') -> list[DriveItem]:
    return query_items(service, f"'{parent_id}' in parents")

def get_drive_item(service, parent_id:str, name: str) -> DriveItem:
    query = f"'{parent_id}' in parents and name='{name}'"
    items = query_items(service, query)
    return items[0] if len(items) > 0 else None

def download_file(service, file_id, output_path):
    request = service.files().get_media(fileId=file_id)

    with open(output_path, 'wb') as fo:
        downloader = MediaIoBaseDownload(fo, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            pctg = int(status.progress() * 100)
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*pctg, pctg))
            sys.stdout.flush()
            #print(f"Download progress: {int(status.progress() * 100)}%")

def download_folder(service, folder_id, output_path, quite=False):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if not quite:
        print("Downloading folder:", output_path)

    items = list_items(service, folder_id)
    file_items = [item for item in items if not item.is_folder]
    folder_items = [item for item in items if item.is_folder]

    for item in folder_items:
        download_folder(service, item.id, os.path.join(output_path, item.name), quite=quite)
    
    for item in file_items:
        if not quite:
            print("Downloading file:", os.path.join(output_path, item.name))

        download_file(service, item.id, os.path.join(output_path, item.name))

def upload_file(service, input_path, parent_id=None, target_name=None):
    mime = MimeTypes()
    mimetype = mime.guess_type(input_path)[0]
    media = MediaFileUpload(input_path, mimetype=mimetype, resumable=True)
    request = service.files().create(
        body={
            'parents': [parent_id] if parent_id else None,
            'name': target_name or os.path.split(input_path)[-1]
        },
        media_body=media,
        fields='id'
    )
    media.stream()
    done = False
    while not done:
        status, done = request.next_chunk()
        if status is not None:
            pctg = int(status.progress() * 100)
            sys.stdout.write('\r')
            sys.stdout.write("[%-100s] %d%%" % ('='*pctg, pctg))
            sys.stdout.flush()
        

def create_folder(service, parent_id, name) -> DriveItem:
    response = service.files().create(body={
        "parents": [parent_id] if parent_id else None,
        "name": name,
        "mimeType": FOLDER_MIME_TYPE,
    }, fields="id,name").execute()

    return DriveItem(
        id=response['id'],
        name=response['name'],
        is_folder=True
    )

def upload_folder(service, input_path, parent_id=None, target_name=None, quite=False):
    folder_name = target_name or os.path.split(input_path)[-1]
    folder_item = get_drive_item(service, parent_id or 'root', folder_name)

    if folder_item is None:
        folder_item = create_folder(service, parent_id, folder_name)

    if not quite:
        print("Uploading folder:", input_path)

    entries = os.listdir(input_path)
    folder_entries = [entry for entry in entries if os.path.isdir(os.path.join(input_path, entry))]
    file_entries = [entry for entry in entries if os.path.isfile(os.path.join(input_path, entry))]
    
    for entry in folder_entries:
        upload_folder(service, os.path.join(input_path, entry), folder_item.id, quite=quite)
    
    for entry in file_entries:
        if not quite:
            print("Uploading file:", os.path.join(input_path, entry))
        upload_file(service, os.path.join(input_path, entry), folder_item.id)

def get_drive_item_by_path(service, path: str) -> DriveItem:
    assert(path.startswith(GDRIVE_PREFIX))
    if path == GDRIVE_PREFIX:
        return DriveItem(id="root", name="root", is_folder=True)

    item : DriveItem = None

    for name_item in path[len(GDRIVE_PREFIX):].split("/"):
        item = get_drive_item(service, item.id if item else 'root', name_item)
    
    return item

def remove_item(service, item_id):
    service.files().update(fileId=item_id, body={'trashed': True}).execute()

def main():
    if len(sys.argv) < 2:
        print_usage()
        exit()

    service = get_service(SCOPES)

    cmd = sys.argv[1]
    if cmd == 'ls':
        path = sys.argv[2]
        if path != GDRIVE_PREFIX and path[-1] == "/":
            path = path[:-1]

        root_item = get_drive_item_by_path(service, path)
        items = list_items(service, root_item.id)
        file_items = [item for item in items if not item.is_folder]
        folder_items = [item for item in items if item.is_folder]

        for item in folder_items:
            print("+", item.name)
        
        for item in file_items:
            print(item.name)
    
    elif cmd == "cp":
        args = [arg for arg in sys.argv[2:] if arg[0] != '-']
        kwargs = [arg for arg in sys.argv[2:] if arg[0] == '-']
        src, dst = args[0:2]

        if src.startswith(GDRIVE_PREFIX):
            item = get_drive_item_by_path(service, src)
            if dst[-1] == "/" or dst == ".":
                dst = os.path.join(dst, item.name)

            if "-r" not in kwargs:
                assert(not item.is_folder)
                download_file(service, item.id, dst)
            else:
                assert(item.is_folder)
                download_folder(service, item.id, dst, quite="-q" in kwargs)
        else:
            assert(dst.startswith(GDRIVE_PREFIX))
            if dst[-1] != '/':
                item = get_drive_item_by_path(service, dst)
                if item is not None:
                    print(f"A folder/file with path '{dst}' already exists")
                    exit()

                dst, dst_name = os.path.split(dst)
                if '//' not in dst:
                    dst += "//"
            else:
                dst = dst[:-1]
                dst_name = None

            item = get_drive_item_by_path(service, dst)

            if "-r" not in kwargs:
                assert(os.path.isfile(src))
                upload_file(service, src, item.id, dst_name)
            else:
                assert(os.path.isdir(src))
                upload_folder(service, src, item.id, dst_name, quite="-q" in kwargs)

    elif cmd == "mkdir":
        path = sys.argv[2]
        assert(path.startswith(GDRIVE_PREFIX))
        root_item = get_drive_item_by_path(service, path)
        if root_item is not None:
            print(f"Error, folder or file '{path}' already exists")

        parent_path, name = os.path.split(path)

        if "/" not in path[len(GDRIVE_PREFIX):]:
            parent_path = parent_path + "//"

        root_item = get_drive_item_by_path(service, parent_path)
        create_folder(service, root_item.id, name)

    elif cmd == "rm":
        path = sys.argv[2]
        item = get_drive_item_by_path(service, path)
        if item:
            remove_item(service, item.id)
        else:
            print(f"No file/folder exists at path: {path}")

if __name__ == '__main__':
    main()