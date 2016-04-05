import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

def plot1(winrecord, path, k):
    win = []
    lose= []
    draw =[]
    for i in range(len(winrecord)/10000):
        win.append(winrecord[i * 10000:i * 10000 + 10000].count(1))
        lose.append(winrecord[i * 10000:i * 10000 + 10000].count(-1))
        draw.append(winrecord[i * 10000:i * 10000 + 10000].count(0))
    plt.figure(k, figsize = (15,5))
    plt.title('The outcome of game', size=14)
    plt.ylabel('Number in every 10000 rounds', size=14)
    p1, = plt.plot([x for x in np.arange(len(win))], win, color='r')
    p2, = plt.plot([x for x in np.arange(len(lose))], lose, color='g')
    p3, = plt.plot([x for x in np.arange(len(draw))], draw, color='b')
    plt.legend((p1, p2, p3), ('win', 'lose', 'draw'), loc=5)
    plt.savefig(path)

def plot2(winrecord1, winrecord2, num, name):
    win = []
    lose= []
    draw =[]
    win.append(winrecord1.count(1))
    lose.append(winrecord1.count(-1))
    draw.append(winrecord1.count(0))
    win.append(winrecord2.count(1))
    lose.append(winrecord2.count(-1))
    draw.append(winrecord2.count(0))
    data = [win, lose, draw]
    color_index = ['r', 'g', 'b']
    xaxis = ['epsilon greedy', 'best policy']
    fig = plt.figure(num, figsize = (5,12))
    plt.ylabel('Number of games', size=15)
    plt.xticks([0.05, 0.2], (xaxis))
    p= [0, 0, 0]
    for i in range(3):
      p[i] = plt.bar([0, 0.15], data[i], width = .1, color = color_index[i], bottom = np.sum(data[:i], axis = 0), alpha = .7)
    fig.legend((p[0], p[1], p[2]), ('win', 'lose', 'draw'))
    plt.savefig('D:/Project/' +name + '.pdf')

def plot3(name):
    v = np.zeros((18, 18))
    q = []
    csvfile = file('D:/Project/' +name + '.csv', 'rb')
    reader = csv.reader(csvfile)
    for line in reader:
        q.append(line)
    csvfile.close()
    q.remove(['player', 'dealer', 'action', 'value'])
    qdict = {}
    for i in q:
        i[0] = int(i[0])
        i[1] = int(i[1])
        i[2] = int(i[2])
        i[3] = float(i[3])
        qdict[i[0], i[1], i[2]] = i[3]

    for player in range(4, 22):
        for dealer in range(4, 22):
            value_HIT = qdict[(player, dealer, 0)]
            value_STICK = qdict[(player, dealer, 1)]

            if value_HIT > value_STICK:
                v[player-4][dealer-4] = value_HIT
                del qdict[(player, dealer, 1)]
            else:
                v[player-4][dealer-4] = value_STICK
                del qdict[(player, dealer, 0)]

    x = []
    y = []
    z = qdict.values()
    for i in range(324):
        x.append(list(qdict)[i][0])
        y.append(list(qdict)[i][1])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(y, x, z, cmap=cm.coolwarm, linewidth=0)
    plt.show()

print(Name + 'Wins2: %.4f%%' % ((float(wins2) / (iterations * 0.2)) * 100))
plot1(winrecord1, 'D:/Project/' +Name + '.pdf', k)
valuelist = value_function.items()
with open(Name + 'value.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, dialect='excel')
    csvwriter.writerow(['player', 'dealer', 'action', 'value'])
    for i in range(len(valuelist)):
        csvwriter.writerow([valuelist[i][0][0], valuelist[i][0][1], valuelist[i][0][2], valuelist[i][1]])
plot2(winrecord_MC_epsilon, winrecord_MC_best, 7, 'MC')
plot2(winrecord_QL_epsilon, winrecord_QL_best, 8, 'QL')
plot2(winrecord_TD_epsilon, winrecord_TD_best, 9, 'TD')
