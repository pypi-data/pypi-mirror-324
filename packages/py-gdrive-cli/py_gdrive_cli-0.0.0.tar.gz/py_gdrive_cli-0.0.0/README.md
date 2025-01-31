## Google Drive Client CLI

### Install:  
    pip install gdrive-cli

### Download credentials:  
  
Download file "credentials.json" from [GCP Console](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application) and put it at folder "~/.gdrive"  


### Usage:  

```
    gdrive ls gd://
    gdrive ls gd://<remote_dir>
    gdrive cp gd://<remote_dir>/<remote_file> <local_path>
    gdrive cp -r gd://<remote_dir> <local_path>
    gdrive cp <local_path> gd://<remote_dir>/
    gdrive cp -r <local_path> gd://<remote_dir>/
    gdrive rm <remote_file>
```

### Github:  
https://github.com/dttvn0010/gdrive-cli
