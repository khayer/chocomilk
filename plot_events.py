import report
import sys
import numpy as np
import re
import plotter

def summarize_results(data,x_values,true_n,summary):
	#print >> sys.stderr, "NOW HERE!!!"
	#print >> sys.stderr, data
	start = 0.0
	end = 10.0
	mid = 5.0
	time_correct = 0.0
	lamp = False
	k = 1
	for y, row in enumerate(data):
			for x, col in enumerate(row):
					if True: #x_values[x] < end:
						#print >> sys.stderr, ("Y: %i, row: %i" % (y,x))
						#print >> sys.stderr, row
						#print >> sys.stderr, col
						#exit(1)
						#print >> sys.stderr, y
						#x1 = [x, x+1]
						#y1 = np.array([y, y]) - 0.5
						#y2 = y1+1
						# LAMP
						if y == 4 and col != 0 :
							k = 0
							lamp = True
							mid = x_values[x]
							end = x_values[x] + 5.0
							#plt.fill_between(x1, y1, y2=y2, color='yellow')
							#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
							#                            horizontalalignment='center',
								#                            verticalalignment='center')
						# LIGHT
						if y == 3 and col == 1 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='red')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "H",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 3 and col == 2 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "T",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 2 and col == 1 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "F",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 2 and col == 2 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "B",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 1 and col == 1 :
							if not lamp:
								start = x_values[x]
								end = x_values[x]+ 10.0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "C",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 0 and col != 0 and col < 10:
								if col == true_n:
										time_correct = x_values[x]
										#plt.fill_between(x1, y1, y2=y2, color='green')
										#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
										#                            horizontalalignment='center',
										#                            verticalalignment='center')
								elif col == true_n+1 or col == true_n-1:
										k = 0
										#plt.fill_between(x1, y1, y2=y2, color='orange')
										#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
										#                            horizontalalignment='center',
										#                            verticalalignment='center')
								else:
										k = 0
										#plt.fill_between(x1, y1, y2=y2, color='red')
										#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
										#                            horizontalalignment='center',
										#                            verticalalignment='center')
						if y == 0 and col == 10:
								k=0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "T",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
					else:
						break
	#print >> sys.stderr, int((start - start) * 5)
	#print >> sys.stderr, int((end - start) * 5)
	#print >> sys.stderr, int((time_correct - mid + 5.0) * 5)
	#print >> sys.stderr, x_values
	#exit(1)
	if not int((time_correct - mid + 5.0) * 5) in summary:
		summary[int((time_correct - mid + 5.0) * 5)] = 0
	summary[int((time_correct - mid + 5.0)*5)] = summary[int((time_correct - mid + 5.0) * 5)]+1
	#print >> sys.stderr, summary
	#exit(1)
	return summary

def pre_mature_summarize_results(data,x_values,summary):
	#print >> sys.stderr, "NOW HERE!!!"
	#print >> sys.stderr, data
	#start = 0.0
	start = []
	end = 1000.0
	mid = 5.0
	time_correct = 0.0
	time_premature = 0.0
	true_n = 100
	poke = False
	k = 1
	for y, row in enumerate(data):
			for x, col in enumerate(row):
					if True: #x_values[x] < end:
						#print >> sys.stderr, ("Y: %i, row: %i" % (y,x))
						#print >> sys.stderr, row
						#print >> sys.stderr, col
						#exit(1)
						#print >> sys.stderr, y
						#x1 = [x, x+1]
						#y1 = np.array([y, y]) - 0.5
						#y2 = y1+1
						# LAMP
						if y == 4 and col != 0 :
							k = 0
							lamp = True
							#mid = x_values[x]
							#plt.fill_between(x1, y1, y2=y2, color='yellow')
							#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
							#                            horizontalalignment='center',
							#                            verticalalignment='center')
						# LIGHT
						if y == 3 and col == 1 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='red')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "H",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 3 and col == 2 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "T",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 2 and col == 1 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "F",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 2 and col == 2 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "B",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 1 and col == 1 :
								start.append(x_values[x])
								end = x_values[x] + 10.0
										#end = x_values[x]+ 10.0
										#mid = x_values[x]+ 5.0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "C",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 0 and col != 0 and col < 10:
								if col == true_n:
										k = 0
										#time_correct = x_values[x]
										#plt.fill_between(x1, y1, y2=y2, color='green')
										#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
										#                            horizontalalignment='center',
										#                            verticalalignment='center')
								elif col == true_n+1 or col == true_n-1:
										k = 0
										#plt.fill_between(x1, y1, y2=y2, color='orange')
										#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
										#                            horizontalalignment='center',
										#                            verticalalignment='center')
								else:
									if not poke:
										#print >> sys.stderr, "EINMAL"
										time_premature = x_values[x]
										poke = True
										k = 0
										#plt.fill_between(x1, y1, y2=y2, color='red')
										#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
										#                            horizontalalignment='center',
										#                            verticalalignment='center')
						if y == 0 and col == 10:
								k=0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "T",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
					else:
						break
	new_start = 100
	for l in start:
		if l < time_premature:
			new_start = l
		else:
			break
	start = new_start
	end = start+ 10.0
	mid = start+ 5.0
	#print >> sys.stderr, int((start - start) * 5)
	#print >> sys.stderr, int(start * 5)
	#print >> sys.stderr, int((end - start) * 5)
	#print >> sys.stderr, int(end * 5)
	#print >> sys.stderr, int((time_premature - mid + 5.0) * 5)
	#print >> sys.stderr, x_values
	#exit(1)
	if not int((time_premature - mid + 5.0) * 5) in summary:
		summary[int((time_premature - mid + 5.0) * 5)] = 0
	summary[int((time_premature - mid + 5.0)*5)] = summary[int((time_premature - mid + 5.0) * 5)]+1
	#print >> sys.stderr, summary
	#exit(1)
	return summary

def incorrect_summarize_results(data,x_values,true_n,summary):
	print >> sys.stderr, "NOW HERE!!!"
	#print >> sys.stderr, data
	#start = 0.0
	start = []
	end = 10.0
	mid = 5.0
	time_correct = 0.0
	time_incorrect = 0.0
	#true_n = 100
	lamp = False
	poke = False
	k = 1
	for y, row in enumerate(data):
			for x, col in enumerate(row):
					if True: #x_values[x] < end:
						#print >> sys.stderr, ("Y: %i, row: %i" % (y,x))
						#print >> sys.stderr, row
						#print >> sys.stderr, col
						#exit(1)
						#print >> sys.stderr, y
						#x1 = [x, x+1]
						#y1 = np.array([y, y]) - 0.5
						#y2 = y1+1
						# LAMP
						if y == 4 and col != 0 :
							k = 0
							lamp = True
							mid = x_values[x]
							end = x_values[x] + 5.0
							#mid = x_values[x]
							#plt.fill_between(x1, y1, y2=y2, color='yellow')
							#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
							#                            horizontalalignment='center',
							#                            verticalalignment='center')
						# LIGHT
						if y == 3 and col == 1 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='red')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "H",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 3 and col == 2 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "T",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 2 and col == 1 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "F",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 2 and col == 2 :
								k = 0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "B",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 1 and col == 1 :
								start.append(x_values[x])

										#end = x_values[x]+ 10.0
										#mid = x_values[x]+ 5.0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "C",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
						if y == 0 and col != 0 and col < 10 and (col % 2 == 1):
								if col == true_n:
										k = 0
										#time_correct = x_values[x]
										#plt.fill_between(x1, y1, y2=y2, color='green')
										#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
										#                            horizontalalignment='center',
										#                            verticalalignment='center')
								elif col == true_n+1 or col == true_n-1:
										k = 0
										#plt.fill_between(x1, y1, y2=y2, color='orange')
										#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
										#                            horizontalalignment='center',
										#                            verticalalignment='center')
								else:
									if not poke:
										#print >> sys.stderr, "EINMAL"
										time_incorrect = x_values[x]
										poke = True
										k = 0
									#plt.fill_between(x1, y1, y2=y2, color='red')
									#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
									#                            horizontalalignment='center',
									#                            verticalalignment='center')
						if y == 0 and col == 10:
								k=0
								#plt.fill_between(x1, y1, y2=y2, color='grey')
								#plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "T",
								#                            horizontalalignment='center',
								#                            verticalalignment='center')
					else:
						break
	#new_start = 100
	#for l in start:
	#	if l < time_premature:
	#		new_start = l
	#	else:
	#		break
	#start = new_start
	#end = start+ 10.0
	#mid = start+ 5.0
	print >> sys.stderr, int(mid * 5)
	print >> sys.stderr, int((time_incorrect - mid + 5.0) * 5)

	#print >> sys.stderr, x_values
	#exit(1)
	if not int((time_incorrect - mid + 5.0) * 5) in summary:
		summary[int((time_incorrect - mid + 5.0) * 5)] = 0
	summary[int((time_incorrect - mid + 5.0)*5)] = summary[int((time_incorrect - mid + 5.0) * 5)]+1
	print >> sys.stderr, summary
	#x = sys.stdin.read()
	#exit(1)
	return summary

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
	summary = {}
	summary_pre_mature = {}
	summary_incorrect = {}
	l = 0
	#print >> sys.stderr, r.events_by_time[1455.159]
	num_trial = 0
	while num_trial < len(r.events["Input Transition On Event"]["TrayClose #1"])-1 :
		#print >> sys.stderr, l
		first_trial = r.events["Input Transition On Event"]["TrayClose #1"][num_trial]
		while (not len(r.events["Input Transition On Event"]["TrayClose #1"])-1 == num_trial) and (r.group[r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]] == 5 or r.group[r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]] == 4 or r.group[r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]] == 7):
				num_trial += 1
		if len(r.events["Input Transition On Event"]["TrayClose #1"])-1 == num_trial:
			end_first_trial = sorted(r.events_by_time.keys())
			#print >> sys.stderr, "THIS"
		else:
			#print >> sys.stderr, "THAT"
			#print >> sys.stderr, r.group[r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]]
			end_first_trial = r.events["Input Transition On Event"]["TrayClose #1"][num_trial+1]
		subset = []
		for time in r.events_by_time.keys():
			if time >= first_trial and time < end_first_trial:
				if time not in subset:
					subset.append(time)
		#print >> sys.stderr, sorted(subset)
		data = np.zeros(shape=(5,len(subset)))
		#print >> sys.stderr, data
		i = 0
		x = []
		correct_n = 20
		adj = sorted(subset)[0]
		cor = "Omitted_"
		lamp = 0
		start_time_lamp = 0
		counted = 0
		for k in sorted(subset):
			#print >> sys.stderr, ("K: %f" % k)
			x.append(k-adj)
			#print >> sys.stderr, ("K: %f" % (k-adj))
			ev = r.events_by_time[k]
			for e in ev:
				if e[1] == "Incorrect Response":
					cor = "Incorrect_Response_"
				if e[1] == "Correct Response":
					cor = "Correct_Response_"
				#print >> sys.stderr, e
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
					#print >> sys.stderr, lamp
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
		#print >> sys.stderr, x
		#print >> sys.stderr, data
		if cor == "Correct_Response_":
			summary = summarize_results(data,x,correct_n,summary)
		if cor == "Premature_Response_":
			summary_pre_mature = pre_mature_summarize_results(data,x,summary_pre_mature)
		if cor == "Incorrect_Response_":
			summary_incorrect = incorrect_summarize_results(data,x,correct_n,summary_incorrect)
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
	print >> sys.stdout, ("time\tcorrect")
	print >> sys.stderr, summary
	print >> sys.stderr, ("summary_pre_mature:")
	print >> sys.stderr, summary_pre_mature
	print >> sys.stderr, ("summary_incorrect:")
	print >> sys.stderr, summary_incorrect
	for key in summary:
			print >> sys.stdout, ("%f\t%i" % (key/5.0, summary[key]))
	plotter.plot_correct_reponses(summary)
	plotter.plot_pre_mature(summary_pre_mature)
	plotter.plot_incorrect(summary_incorrect)
	plotter.plot_all_responses(summary, summary_pre_mature, summary_incorrect)
	pass

if __name__ == '__main__':
	sys.exit(main())