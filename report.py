import csv
import re

def nina(a):
  return a*a

class Report:

  def __init__(self, report_file):
    self.report_file = report_file
    self.events = {}
    self.group = {}
    self.events_by_time = {}


  def read_csv(self):
    p = re.compile('^\d')
    r = csv.reader(open(self.report_file))
    h = []
    for row in r:
      if not p.match(row[0]):
        h = row
      else:
        if not row[h.index("Evnt_Name")] in self.events:
          self.events[row[h.index("Evnt_Name")]] = {}
        if not row[h.index("Item_Name")] in self.events[row[h.index("Evnt_Name")]]:
          self.events[row[h.index("Evnt_Name")]][row[h.index("Item_Name")]] = []
        self.events[row[h.index("Evnt_Name")]][row[h.index("Item_Name")]].append(float(row[h.index("Evnt_Time")]))
        self.group[float(row[h.index("Evnt_Time")])] = (int(row[h.index("Group_ID")]))
        if not float(row[h.index("Evnt_Time")]) in self.events_by_time:
          self.events_by_time[float(row[h.index("Evnt_Time")])] = []
        self.events_by_time[float(row[h.index("Evnt_Time")])].append([row[h.index("Evnt_Name")],row[h.index("Item_Name")]])
    return

  def write(self):
    print(self.report_file)
    return





