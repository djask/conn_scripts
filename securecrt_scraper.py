import os, glob
import uuid
from time import sleep
import csv
import sys


class scrt_scrape():
  session_path = ''

  #folder, filename, protocl, hostname, port
  sessions = []

  def __init__(self, path):
    self.session_path = path

  def export_csv(self, csv_file='./sessions.csv'):
    print('session size:', len(self.sessions))
    with open(os.path.join(sys.path[0], csv_file), 'w', newline='') as csvfile:
      csv_writer = csv.writer(csvfile, delimiter=',')
      for s in self.sessions:
        csv_writer.writerow(s)

  def scrape_sessions(self, folder=session_path):
    os.chdir(folder)
    for file in glob.glob("*.ini", recursive=True):
      print('found:', file)
      if "__FolderData__" in file:
        continue

      ini = open(file, "r")
      flag = 0
      valid = 1
      host = ""

      #default port 22
      port = 22
      prot = "Unknown"
      for line in ini:
        # check if it's a telnet session
        if 'S:"Protocol Name"' in line:
          prot = line.split('=')[1].strip('\n')
        if 'S:"Hostname"' in line:
          host = line.split('=')[1].strip('\n')
          flag += 1
        elif 'D:"Port"' in line:
          port = int("0x" + line.split('=')[1].strip('\n'), 0)
          flag += 1
        if flag == 2:
          break

      self.sessions.append(
        [file.strip('.ini'), prot, host,
          str(port)])

  #returns a list of tuples (IP, PORT) for all telnet sessions
  def scrape_sessions_recursive(self):
    orig = len(self.session_path.split('/'))
    print(self.session_path)
    print('orig', orig)
    depth = -1
    for direc in os.walk(self.session_path):
      sess_count = 0
      cur_depth = len(direc[0].split('/')) - orig
      self.scrape_sessions(direc[0])


if __name__ == '__main__':
  if len(sys.argv) < 3:
    print ("Usage: securecrt_scrapyer.py [base scrt file] [export file name]")
    sys.exit()
  print ("exporting " + sys.argv[1])
  crt = scrt_scrape(sys.argv[1])
  crt.scrape_sessions_recursive()
crt.export_csv(sys.argv[2])
