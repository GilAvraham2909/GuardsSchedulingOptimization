import random

def input_requerst(shift_requests):
    s = []
    guard_len = len(shift_requests)
    len_str = len(shift_requests[0])
    for guard in range(guard_len):
        row = []
        day = []
        for i in range(len_str):
            if shift_requests[guard][i] != ' ':
                day.append(int(shift_requests[guard][i]))
            else:
                row.append(day)
                day = []
        row.append(day)
        s.append(row)
    return s

def random_100():
    shift = []
    per_shift = []
    for i in range(100000):
        per_shift.append(random.randint(3,5))
        c = ""
        for j in range(7):
            for k in range(3):
                c += str(random.randint(0,1))
            if j < 6:
                c+= " "
        shift.append(c)
    print(per_shift)
    print(shift)
