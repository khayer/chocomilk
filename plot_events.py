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
    print >> sys.stderr, ("Num of trials3: %s" % len(r.events["Input Transition On Event"]["TrayClose #1"]))
    print >> sys.stderr, ("Num of trials4: %s" % len(r.events["Condition Event"]["Start ITI"]))
    print >> sys.stderr, sorted(r.events_by_time.keys())
    print >> sys.stderr, sorted(r.group)
    #exit(0)

    interactions_response_time = {
      1 : [0,0.0,0,None],
      2 : [0,0.0,0,None],
      3 : [0,0.0,0,None],
      4 : [0,0.0,0,None],
      5 : [0,0.0,0,None],
      6 : [0,0.0,0,None],
      7 : [0,0.0,0,None],
      8 : [0,0.0,0,None],
      9 : [0,0.0,0,None]
    }

    l = 0
    #print >> sys.stderr, r.events_by_time[1455.159]
    num_trial = 0

    while num_trial < len(r.events["Input Transition On Event"]["TrayClose #1"])-1 :
      print >> sys.stderr, l
      first_trial = r.events["Input Transition On Event"]["TrayClose #1"][num_trial]
      while (not len(r.events["Input Transition On Event"]["TrayClose #1"])-1 == num_trial) and (r.group[r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]] == 5 or r.group[r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]] == 4 or r.group[r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]] == 7):
          num_trial += 1
      if len(r.events["Input Transition On Event"]["TrayClose #1"])-1 == num_trial:
        end_first_trial = sorted(r.events_by_time.keys())
        print >> sys.stderr, "THIS"
      else:
        #print >> sys.stderr, "THAT"
        #print >> sys.stderr, r.group[r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]]
        end_first_trial = r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]
      subset = []
      for time in r.events_by_time.keys():
        if time >= first_trial and time < end_first_trial:
          if time not in subset:
            subset.append(time)
      print >> sys.stderr, sorted(subset)
      data = np.zeros(shape=(5,len(subset)))
      print >> sys.stderr, data


      i = 0
      x = []
      correct_n = 20
      adj = sorted(subset)[0]
      cor = "Omitted_"
      lamp = 0
      start_time_lamp = 0
      counted = 0
      for k in sorted(subset):
        print >> sys.stderr, ("K: %f" % k)
        x.append(k-adj)
        print >> sys.stderr, ("K: %f" % (k-adj))
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
            lamp = 1
            start_time_lamp = k

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
            interactions_response_time[n][2] += 1
            print >> sys.stderr, lamp
            if lamp == 0:
              cor = "Premature_Response_"
            elif counted == 0:
              interactions_response_time[n][0] += 1
              interactions_response_time[n][1] += k - start_time_lamp
              counted = 1
          if e[1] == "Tray #1" and e[0] == "Input Transition On Event":
            data[0,i] = 10

        i = i +1
      #t.run()
      x =np.around(x,5)

      if l < 10 :
        plotter.plot_my_data(data,x,correct_n,"00{0}_{1}trial".format(l, cor),sorted(subset)[0])
      elif l< 100:
        plotter.plot_my_data(data,x,correct_n,"0{0}_{1}trial".format(l, cor),sorted(subset)[0])
      else:
        plotter.plot_my_data(data,x,correct_n,"{0}_{1}trial".format(l, cor),sorted(subset)[0])
      l += 1
      num_trial += 1
      print >> sys.stderr, x
      print >> sys.stderr, data
      #if l == 44:
      #  exit()
      #exit(1)
    print >> sys.stdout, ("hole\tnum\ttotal\taverage")
    for key, value in interactions_response_time.items():
      if not value[0] == 0:
        interactions_response_time[key][3] = value[1]/value[0]
      if not value[3] == None:
        print >> sys.stdout, ("%i\t%i\t%f\t%i\t%f" % (key, value[0], value[1], value[2], interactions_response_time[key][3] ))
      else:
        print >> sys.stdout, ("%i\t%i\t%f\t%i\tNaN" % (key, value[0], value[1] ,value[2]))
    print >> sys.stderr, interactions_response_time
    plotter.plot_bar_graph(interactions_response_time)
    plotter.plot_bar_graph2(interactions_response_time)
    plotter.plot_bar_graph3(interactions_response_time)
    pass

if __name__ == '__main__':
    sys.exit(main())