################################################
#
# This contains all the web service API calls
# 
################################################

import requests
from lxml import etree


class web_service():

  def __init__(self, host):
    self.host = host
    self.url_login           = 'https://%s:8443/www/core-service/rest/LoginService/login' % (host)
    self.url_get_matrix_data = 'https://%s:8443/www/manager-service/rest/QueryViewerService/getMatrixData' % (host)
    self.url_download_report = 'https://%s:8443/www/manager-service/rest/ArchiveReportService/initDefaultArchiveReportDownloadById' % (host)

  # ----------------------------------------------
  def login(self, username, passwd):

    url = self.url_login + '?login=%s&password=%s' % (username, passwd)
    r = requests.get(url)

    # get the auth_token
    doc = etree.fromstring(r.text)  # xml
    items = doc.xpath('//ns3:loginResponse/ns3:return')
    auth_token = ""
    for item in items:
      auth_token = item.text
      break

    # return
    return auth_token

  # ----------------------------------------------
  def get_matrix_data(self, auth_token, query_viewer_id):

    url = self.url_get_matrix_data + '?authToken=%s&id=%s' % (auth_token, query_viewer_id)
    r = requests.get(url)

    # get the rows   
    # http://lxml.de/tutorial.html
    root = etree.XML(r.text)  # xml
    data_rows = []
    for wrapper in root.findall(".//rows"):
      row1 = wrapper[0]
      row2 = wrapper[1]
      name = row1.text
      value = row2.text
      data_rows.append([name, value])

    # return
    return data_rows

  # ----------------------------------------------
  def download_report(self, auth_token, report_id, save_path, report_doc_type):

    url = self.url_download_report + '?authToken=%s&reportId=%s&reportType=Manual' % (auth_token, report_id)
    r = requests.get(url)

    # save the file
    filename = save_path + report_id + "." + report_doc_type
    with open(filename, "wb") as report:
      report.write(r.text)

  # ----------------------------------------------
  # ----------------------------------------------
  # ----------------------------------------------



