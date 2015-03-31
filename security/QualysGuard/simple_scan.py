################################################
#
# Just a simple scan
# We can make this more generic and customized later
#
################################################

import requests
import sys
import time

from qualysapi import qualysapi

# ========================================
def main():

  # IP list to scan
  # TODO: read this in from stdin
  ip_list = ['192.168.1.100', '192.168.1.121']

  # TODO: validate the IPs, take out duplicates

  # TODO: read this from a config file
  username = 'secret_username'        # Qualys API username
  passwd = 'secret_passwd'            # Qualys API password
  save_path = '/home/robot/reports/'  # where we save the reports
  report_doc_type = 'pdf'

  # init session
  session = requests.Session()
  session.headers.update({'X-Requested-With':'Facklers PyQual python primer'})

  # our Qualys obj
  my_q = qualysapi()

  # login
  try:
    my_q.login(session, username, passwd)
  except Exception:
    # TODO: email alert, don't silently die...
    print "Login failed"
    sys.exit()

  # OPERATION: scan
  ip_list_scanRef = {}
  for ip in ip_list:
    ip_list_scanRef[ip] = my_q.scan(session, ip)
  time.sleep(500)   # API calls cost $$$, wait a little bit here

  # OPERATION: gen report
  remaining_ips = set(ip_list)
  ip_list_reportID = {}
  while len(remaining_ips) > 0:
    for ip in remaining_ips:
      scanRef = ip_list_scanRef[ip]
      if my_q.get_scan_status(session, scanRef) == 'Finished':
        # remove from our list
        remaining_ips.remove(scanRef)
        # get the report ID
        ip_list_reportID[ip] = my_q.gen_report(session, scanRef, report_doc_type, ip)
    # end for
    # wait a little, then go through the remaining items again
    time.sleep(500)
  time.sleep(500)   # API calls cost $$$, wait a little bit here

  # OPERATION: download report
  remaining_ips = set(ip_list)
  while len(remaining_ips) > 0:
    for ip in remaining_ips:
      reportID = ip_list_reportID[ip]
      if my_q.get_report_status(session, reportID) == 'Finished':
        # remove from our list
        remaining_ips.remove(reportID)
        # download report, save it to our specified path
        my_q.report_download(session, reportID, ip, save_path, report_doc_type)
    # end for
    # wait a little, then go through the remaining items again
    time.sleep(500)

  # cleanup
  my_q.logout(session)
  session.close()


# ========================================
if __name__ == "__main__":
  main()


