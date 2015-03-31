################################################
#
# This contains all the qualys API calls
# See more: https://community.qualys.com/docs/DOC-4551
# 
################################################

import xml.etree.ElementTree as ET


class qualysapi():

  def __init__(self):
    self.url_session = 'https://qualysapi.qualys.com/api/2.0/fo/session/'
    self.url_scan    = 'https://qualysapi.qualys.com/api/2.0/fo/scan/'
    self.url_report  = 'https://qualysapi.qualys.com/api/2.0/fo/report/'

  # ----------------------------------------------
  def login(self, session, username, passwd):
    data = {
      'action': 'login',
      'username': username,
      'password': passwd,
    }
    r = session.post(self.url_session, data)

    # TODO: find success message, or some token. Raise exception otherwise
    xmlreturn = ET.fromstring(r.text)
    for elem in xmlreturn.findall('.//TEXT'):
      print elem.text     # prints the "Logged in" message

  # ----------------------------------------------
  def logout(self, session):
    data = {
      'action': 'logout',
    }
    r = session.post(self.url_session, data)

    # parse the response text here if needed...

  # ----------------------------------------------
  def scan(self, session, ip):
    data = {
      'action': 'launch',
      'ip': ip,
      'iscanner_name': 'your_scanner_name',
      'option_id': '123456',
      'scan_title': ip,
    }

    r = session.post(self.url_scan, data=data)

    # parse the scanRef
    scanRef = ""
    xmlreturn = ET.fromstring(r.text)
    for elem in xmlreturn.findall('.//ITEM'):
      if (elem[0].text == 'REFERENCE'):
        scanRef = elem[1].text
        break

    # TODO: raise exception if scanRef is empty
    return scanRef

  # ----------------------------------------------
  def get_scan_status(self, session, scanRef):
    data = {
      'action': 'list',
      'scan_ref': scanRef,
    }

    r = session.post(self.url_scan, data=data)
 
    # parse the status
    status = self.parse_status_text(r.text)

    return status

  # ----------------------------------------------
  def gen_report(self, session, scanRef, doc_type, ip):
    data = {
      'action': 'launch',
      'report_type': 'Scan',
      'template_id': '234567',
      'output_format': doc_type,
      'report_refs': scanRef,
      'report_title': ip,
    }

    r = session.post(self.url_report, data=data)
 
    # parse the report ID
    reportID = ""
    xmlreturn = ET.fromstring(r.text)
    for elem in xmlreturn.findall('.//ITEM'):
      if (elem[0].text == 'ID'):
        reportID = elem[1].text
        break

    return reportID

  # ----------------------------------------------
  def get_report_status(self, session, reportID):
    data = {
      'action': 'list',
      'id': reportID,
    }

    r = session.post(self.url_report, data=data)
 
    # parse the status
    status = self.parse_status_text(r.text)

    return status

  # ----------------------------------------------
  def report_download(self, session, reportID, ip, save_path, doc_type):
    data = {
      'action': 'fetch',
      'id': reportID,
    }

    r = session.post(self.url_report, data=data)
 
    # Now that all the hard work was done, lets get that report.
    # No chunking needed due to small size of a single IP scan report.
    filename = save_path + ip + "." + doc_type
    with open(filename, "wb") as report:
      report.write(r.content)

  # ----------------------------------------------
  # ----------------------------------------------
  # ----------------------------------------------
  def parse_status_text(self, text):

    status = ""

    xmlreturn = ET.fromstring(text)
    for elem in xmlreturn.findall('.//STATUS'):
      status = elem[0].text
      break

    return status





