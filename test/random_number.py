# Python program to print all permutations with
# duplicates allowed
import random

out = open("train_x", "w")
for i in range(100000):
    for i in range(420):
        out.write(str(random.randint(0,1)))
        if i != 419:
            out.write(" ")
    out.write("\n")
out.close()
print("end")

"""
def toString(List,count):
    count +=1
    if count == 100000:
        out.close()
        exit(0)
    return ''.join(List)

def permute(a, l, r, count):
    if l == r:
        print(toString(a, count))
        out.write(toString(a, count) + "\n")
    else:
        for i in range(l, r + 1):
            a[l], a[i] = a[i], a[l]
            permute(a, l + 1, r, count)
            a[l], a[i] = a[i], a[l]  # backtrack

out = open("train_x", "w")
string = "111100000010001010101" \
         "000000010010100000110" \
         "001000000011100001010" \
         "100000010010101000100" \
         "000000010010100010010" \
         "000000001010010000110" \
         "000000010001100001110" \
         "000000000010000000110" \
         "000010010010100000010" \
         "000000010000100000100" \
         "000001010010100000010" \
         "000000001010100100110" \
         "000000010010000010110" \
         "000000010011101000110" \
         "000000010100101000000" \
         "000111010010000000110" \
         "110000000010100000100" \
         "001000010000100000010" \
         "000010010010000000000" \
         "111110111101111111111"
n = len(string)
a = list(string)
permute(a, 0, n - 1, count)

"""
# This code is contributed by Bhavya Jain
