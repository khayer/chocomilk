import csv
import re

def nina(a):
  return a*a

class Report:

  def __init__(self, report_file):
    self.report_file = report_file
    self.events = {}


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
    return





