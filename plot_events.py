import report
import sys
import numpy as np
import re
import plotter

def main():
    """Main entry point for the script."""
    print >> sys.stderr, sys.argv
    r = report.Report(sys.argv[1])
    r.read_csv()
    r.write()
    print >> sys.stderr, r.events["Output On Event"]["HouseLight #1"][0]
    print >> sys.stderr, ("Num of trials: %s" % len(r.events["Condition Event"]["Start Trial"]))
    print >> sys.stderr, ("Num of trials2: %s" % len(r.events["Output On Event"]["TrayLight #1"]))
    print >> sys.stderr, sorted(r.events_by_time.keys())

    #print >> sys.stderr, r.events_by_time[1455.159]
    for num_trial in range(0,len(r.events["Condition Event"]["Start Trial"])-1):
      print >> sys.stderr, num_trial
      first_trial = r.events["Condition Event"]["Start Trial"][num_trial]
      if len(r.events["Condition Event"]["Start Trial"])-1 == num_trial:
        end_first_trial = sorted(r.events_by_time.keys())
      else:
        end_first_trial = r.events["Condition Event"]["Start Trial"][num_trial+1]
      subset = []
      for time in r.events_by_time.keys():
        if time >= first_trial and time < end_first_trial:
          subset.append(time)
      print >> sys.stderr, sorted(subset)
      data = np.zeros(shape=(5,len(subset)))
      print >> sys.stderr, data
      i = 0
      x = []
      correct_n = 20
      adj = sorted(subset)[0]
      cor = "NA_"
      for k in sorted(subset):

        x.append(k-adj)
        ev = r.events_by_time[k]
        for e in ev:
          if e[1] == "Incorrect Response":
            cor = "Incorrect_Response_"
          if e[1] == "Correct Response":
            cor = "Correct_Response_"
          print >> sys.stderr, e
          n = re.findall('\d+', e[1])
          if n:
            n = int(n[0])
          # LAMP
          p = re.compile('^Lamp')
          if p.match(e[1]) and e[0] =="Output On Event":
            data[4,i] = n
            correct_n = n

          # LIGHTS
          if e[1] == "HouseLight #1" and e[0] =="Output On Event":
            data[3,i] = 1
          if e[1] == "TrayLight #1" and e[0] =="Output On Event":
            data[3,i] = 2

          # BEAM
          if e[1] == "FIRBeam #1" and e[0] == "Input Transition On Event":
            data[2,i] = 1
          if e[1] == "BIRBeam #1" and e[0] == "Input Transition On Event":
            data[2,i] = 2

          # TRAY
          if e[1] == "TrayClose #1" and e[0] == "Input Transition On Event":
            data[1,i] = 1

          # HOLE  1-9 TrayHole
          p = re.compile('^Hole')
          if p.match(e[1]) and e[0] == "Input Transition On Event":
            data[0,i] = n
          if e[1] == "Tray #1" and e[0] == "Input Transition On Event":
            data[0,i] = 10

        i = i +1
      #t.run()
      x =np.around(x,2)
      plotter.plot_my_data(data,x,correct_n,"{0}trial_{1}".format(cor, num_trial))
      print >> sys.stderr, x
      print >> sys.stderr, data
      if cor == "NA_":
        exit()
    pass

if __name__ == '__main__':
    sys.exit(main())