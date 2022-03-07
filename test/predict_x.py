import function as f
import numpy as np
import cp
import sys

train_x = np.loadtxt(sys.argv[1])
train = []
for i in range(100000):
    row = []
    for k in range(140):
        day = []
        for j in range(3):
            day.append(train_x[i][(k*3)+j])
        row.append(day)
    train.append(row)

temp = []
for i in range(100000):
    row_x = []
    for r in range(20):
        week = []
        for k in range(7):
            week.append(train[i][(r * 7) + k])
        row_x.append(week)
    temp.append(row_x)

# const value
num_shifts = 3
num_days = 7
option = 1
# default value
guard = 20
num_shift = [2, 2, 2, 3, 3, 3, 4, 4, 4, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 2]
temp = np.array(temp)
train = temp.astype(int)

#predict
y = open("train_y", "w")
for prob in range(100000):
    ret = cp.main(guard, train[prob], num_days, num_shifts, num_shift)
    for i in range(420):
        y.write(str(ret[i]))
        if i != 419:
            y.write(" ")
    y.write("\n")
y.close()


