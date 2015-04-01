""" 
# Simple script for gdrive operations
"""

import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
from oauth2client.tools import run
from apiclient.discovery import build
from httplib2 import HttpLib2Error
from apiclient.http import MediaIoBaseUpload

import io
import mimetypes
import os
import sys

# ===========================================================
# Define
API_VERSION = 'v1beta2'
GS_SCOPE = 'https://www.googleapis.com/auth/devstorage.full_control'
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secrets.json')
OAUTH2_STORAGE = 'oauth2.dat'

BUCKET = 'my_bucket'      # default

# ===========================================================
def print_usage():
  print "\n"
  print "Usage: python fileutil.py cp local_file [bucket_name]"
  print "Usage: python fileutil.py rm gdrive_file [bucket_name]"
  print "Usage: python fileutil.py wget gdrive_file [bucket_name]"
  print "\n"

# ===========================================================
def main(argv):

  # read arguments, for simplicity sake read directly
  # TODO: use argparse: https://docs.python.org/3.3/library/argparse.html
  if len(sys.argv) < 3:
    print_usage()
    sys.exit()
  cmd = sys.argv[1]
  filename = sys.argv[2]
  mimeType = mimetypes.guess_type(filename)[0]
  # check command
  allowed_cmd_list = ['cp', 'rm', 'wget']
  if cmd not in allowed_cmd_list:
    print_usage()
    sys.exit()
  # get the bucket name
  bucket_name = BUCKET
  try:
    bucket_name = sys.argv[3]
  except:
    pass

  # get credentials
  flow = flow_from_clientsecrets(CLIENT_SECRETS, scope=GS_SCOPE)
  storage = Storage(OAUTH2_STORAGE)
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = run(flow, storage)

  # http w/ credentials
  http = httplib2.Http()
  auth_http = credentials.authorize(http)

  # Construct the service obj
  gs_service = build('storage', API_VERSION, http=auth_http)

  # operations
  # TODO: create a class to group these operations
  resp = ""
  if cmd == "cp":
    # upload this file to gdrive
    fp = open(filename, 'r')
    fh = io.BytesIO(fp.read())
    media = MediaIoBaseUpload(fh, mimeType)
    req = gs_service.objects().insert(bucket=bucket_name, name=filename, media_body=media)
    resp = req.execute()
  elif cmd == "rm":
    # remove the file from gdrive
    req = gs_service.objects().delete(bucket=bucket_name, object=filename)
    resp = req.execute()
  elif cmd == "wget":
    # download the file from gdrive
    req = gs_service.objects().get_media(bucket=bucket_name, object=filename)
    # The BytesIO object may be replaced with any io.Base instance.
    fh = io.BytesIO()
    downloader = auth_http.MediaIoBaseDownload(fh, req, chunksize=1024*1024)
    done = False
    while not done:
      status, done = downloader.next_chunk()
      if status:
        pass
        #print 'Download %d%%.' % int(status.progress() * 100)
    resp = 'Download Complete!'
    # save file
    with open(filename, 'w') as file_:
      file_.write(fh.getvalue())
  else:
    # raise exception
    sys.exit()

  # output
  print json.dumps(resp, indent=2)

# ===========================================================
# ===========================================================
# ===========================================================
if __name__ == '__main__':
  main(sys.argv)


