import sys
import numpy as np

input_file = np.loadtxt(sys.argv[1])
len = len(input_file)
indices = np.arange(input_file.shape[0])
np.random.shuffle(indices)
input_file = input_file[indices]
out = open("train_xs", "w")
for line in input_file:
    out.write(line)
out.close()
