################################################
#
# CLI for the HP ArcSight ESM Web Services
# We can make this more generic and customized later
#
################################################

import sys

from web_service import web_service

# ========================================
def print_usage():
  #print "Usage: python main.py (getMatrixData|downloadReport) (QueryViewerID|ReportID)"
  print "\n"
  print "Usage: python main.py getMatrixData QueryViewerID"
  print "Usage: python main.py downloadReport ReportID"
  print "\n"

# ========================================
def main():

  # read arguments, for simplicity sake read directly
  # TODO: use argparse: https://docs.python.org/3.3/library/argparse.html
  if len(sys.argv) != 3:
    print_usage()
    sys.exit()
  # check command
  allowed_cmd_list = ['getMatrixData', 'downloadReport']
  cmd = sys.argv[1]
  if cmd not in allowed_cmd_list:
    print_usage()
    sys.exit()

  # TODO: read this from a config file
  username = 'secret_username'        # username
  passwd = 'secret_passwd'            # password
  host = 'localhost'                  # server hostname
  save_path = '/home/robot/reports/'  # where we save the reports
  report_doc_type = 'csv'

  # our web service obj
  my_ws = web_service(host)

  # login
  auth_token = ""
  try:
    auth_token = my_ws.login(username, passwd)
  except Exception:
    # TODO: email alert, don't silently die...
    print "Login failed"
    sys.exit()

  # OPERATION
  if cmd == "getMatrixData":
    query_viewer_id = sys.argv[2]
    rows = my_ws.get_matrix_data(auth_token, query_viewer_id)
    # print out the rows
    for r in rows:
      name, value = r
      print "%s: %s\n" % (name, value)
  elif cmd == "downloadReport":
    report_id = sys.argv[2]
    my_ws.download_report(auth_token, report_id, save_path, report_doc_type)
  else:
    # raise exception
    sys.exit()

  # cleanup
  # nothing to do...


# ========================================
if __name__ == "__main__":
  main()


