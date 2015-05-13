import matplotlib.pyplot as plt
import numpy as np
import sys

def plot_my_data(data, x_values,true_n,name,timestamp):
    k = len(x_values)
    #print >> sys.stderr, k
    fig = plt.figure(num=None, figsize=(k/3, 5), dpi=100, facecolor='w', edgecolor='k')
    ax = fig.add_subplot(111)

    ax.set_aspect(1)

    def avg(a, b):
        return (a + b) / 2.0

    for y, row in enumerate(data):
        for x, col in enumerate(row):
            x1 = [x, x+1]
            y1 = np.array([y, y]) - 0.5
            y2 = y1+1
            # LAMP
            if y == 4 and col != 0 :
                plt.fill_between(x1, y1, y2=y2, color='yellow')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
                                            horizontalalignment='center',
                                            verticalalignment='center')
            # LIGHT
            if y == 3 and col == 1 :
                plt.fill_between(x1, y1, y2=y2, color='red')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "H",
                                            horizontalalignment='center',
                                            verticalalignment='center')
            if y == 3 and col == 2 :
                plt.fill_between(x1, y1, y2=y2, color='grey')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "T",
                                            horizontalalignment='center',
                                            verticalalignment='center')
            if y == 2 and col == 1 :
                plt.fill_between(x1, y1, y2=y2, color='grey')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "F",
                                            horizontalalignment='center',
                                            verticalalignment='center')
            if y == 2 and col == 2 :
                plt.fill_between(x1, y1, y2=y2, color='grey')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "B",
                                            horizontalalignment='center',
                                            verticalalignment='center')
            if y == 1 and col == 1 :
                plt.fill_between(x1, y1, y2=y2, color='grey')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "C",
                                            horizontalalignment='center',
                                            verticalalignment='center')

            if y == 0 and col != 0 and col < 10:
                if col == true_n:
                    plt.fill_between(x1, y1, y2=y2, color='green')
                    plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
                                                horizontalalignment='center',
                                                verticalalignment='center')
                elif col == true_n+1 or col == true_n-1:
                    plt.fill_between(x1, y1, y2=y2, color='orange')
                    plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
                                                horizontalalignment='center',
                                                verticalalignment='center')
                else:
                    plt.fill_between(x1, y1, y2=y2, color='red')
                    plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), int(col),
                                                horizontalalignment='center',
                                                verticalalignment='center')

            if y == 0 and col == 10:
                plt.fill_between(x1, y1, y2=y2, color='grey')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "T",
                                            horizontalalignment='center',
                                            verticalalignment='center')

            #if col == 2:
            #    plt.fill_between(x1, y1, y2=y2, color='orange')
            #    plt.text(avg(x1[0], x1[0]+1), avg(y1[0], y2[0]), "B",
            #                                horizontalalignment='center',
            #                                verticalalignment='center')
            #if col == 3:
            #    plt.fill_between(x1, y1, y2=y2, color='yellow')
            #    plt.text(avg(x1[0], x1[0]+1), avg(y1[0], y2[0]), "9",
            #                                horizontalalignment='center',
            #                                verticalalignment='center')

    #plt.ylim(4, 0)
    plt.yticks(np.arange(5), ["Hole","Tray","Beam","Light","Lamp"])
    plt.xticks(np.arange(len(x_values)), x_values,rotation='vertical')
    ax.set_ylim(-0.5,4.5)
    ax.set_xlim(-0.5,len(x_values)+0.5)
    plt.title(name + str(timestamp))
    #fig = plt.figure(figsize=(4, 5))
    plt.savefig(name + ".png")
    plt.close('all')

def plot_bar_graph(my_hash):
    x = []
    y = []
    for key, value in my_hash.items():
        x.append(key)
        if value[2] == None:
            y.append(0)
        else:
            y.append(value[2])
    plt.bar(x,y, align='center')
    ind = range(1,10)
    plt.xticks(ind, x)
    plt.title("Average response time")
    plt.savefig("bar" + ".png")

def plot_bar_graph2(my_hash):
    x = []
    y = []
    for key, value in my_hash.items():
        x.append(key)
        if value[0] == None:
            y.append(0)
        else:
            y.append(value[0])
    plt.bar(x,y, align='center')
    ind = range(1,10)
    plt.xticks(ind, x)
    plt.title("Times visited")
    plt.savefig("bar_visited" + ".png")

def main():
    data = [[1, 1, 0, 1, 0,1, 1, 0, 0, 0, 0, 1, 0, 1, 0],
            [0, 0, 2, 0, 0,0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 2, 0, 0,0, 0, 2, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0,0, 0, 0, 0, 3, 3, 0, 3, 1, 3]]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    #ax.axes.get_yaxis().set_visible(False)
    ax.axes.get_xaxis().set_visible(False)

    ax.set_aspect(1)

    def avg(a, b):
        return (a + b) / 2.0

    for y, row in enumerate(data):
        for x, col in enumerate(row):
            x1 = [x, x+1]
            y1 = np.array([y, y]) - 0.5
            y2 = y1+1
            if col == 1:
                plt.fill_between(x1, y1, y2=y2, color='red')
                plt.text(avg(x1[0], x1[1]), avg(y1[0], y2[0]), "A",
                                            horizontalalignment='center',
                                            verticalalignment='center')
            if col == 2:
                plt.fill_between(x1, y1, y2=y2, color='orange')
                plt.text(avg(x1[0], x1[0]+1), avg(y1[0], y2[0]), "B",
                                            horizontalalignment='center',
                                            verticalalignment='center')
            if col == 3:
                plt.fill_between(x1, y1, y2=y2, color='yellow')
                plt.text(avg(x1[0], x1[0]+1), avg(y1[0], y2[0]), "9",
                                            horizontalalignment='center',
                                            verticalalignment='center')

    #plt.ylim(4, 0)
    plt.yticks(np.arange(4), ["Hole","Tray","Beam","Light"])
    ax.set_ylim(-0.5,3.5)
    plt.title("Trial 1")
    #fig = plt.figure(figsize=(4, 5))
    plt.savefig("testo.png")

if __name__ == '__main__':
    sys.exit(main())