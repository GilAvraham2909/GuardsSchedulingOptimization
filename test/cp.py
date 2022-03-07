from ortools.constraint_solver.pywrapcp import Solver
from ortools.sat.python import cp_model

# This program tries to find an optimal assignment of guards to shifts
# (3 shifts per day, for 7 days), subject to some constraints (see below).
# Each guard can request to be assigned to specific shifts.
# The optimal assignment maximizes the number of fulfilled shift requests.
def main(num_guards, shift_requests, num_days, num_shifts, num_shift):
    all_guards = range(num_guards)
    all_days = range(num_days)
    all_shifts = range(num_shifts)

    #value of shift for each guard in week.


    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: guard 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_guards:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d, s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # Each shift is assigned to at least two guards in shift.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_guards) >= 2)

    # Each shift is assigned to at most four guards in shift.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_guards) <= 4)

    # Each guard works at most one shift per day.
    for n in all_guards:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    #Each guard don't works two shifts in consecutive
    for n in all_guards:
        for d in all_days:
            next = d + 1
            if next <= num_days - 1:
                model.Add(shifts[(n, d, 2)] + shifts[(n, next, 0)] < 2)

    # Each guard works at exactly num of shifts he needs
    for n in all_guards:
            model.Add(sum(shifts[(n, d, s)] for d in all_days for s in all_shifts) == num_shift[n])

    #for n in all_guards:
    #     model.Add(sum(shifts[(n, d, s)] for d in all_days for s in all_shifts) <= num_shift[n])

    #minimize the request
    model.Minimize(
        sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_guards
            for d in all_days for s in all_shifts))
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # request len
    request_len = 0
    for n in all_guards:
        for d in all_days:
            for s in all_shifts:
                if shift_requests[n][d][s] == 1:
                    request_len += 1

    # print just if there is a solution
    sol = 0
    ret = []
    try:
        sol = 1
        for d in all_days:
            print('Day', d + 1)
            for n in all_guards:
                for s in all_shifts:
                    ret.append(solver.Value(shifts[(n, d, s)]))
                    if solver.Value(shifts[(n, d, s)]) == 1:
                        if shift_requests[n][d][s] == 1:
                            print('Guard', n, 'works shift', s, '(not requested).')
                        else:
                            print('Guard', n, 'works shift', s)
            print("")
            # Statistics.
        print('Statistics')
        print('  - Number of shift requests met = %i' % solver.ObjectiveValue(),
                  '(out of', request_len, ')')

        print('  - wall time       : %f s' % solver.WallTime())
        print("")
        return ret
    finally:
        if sol == 0:
            for i in range(420):
                ret.append(0)
            return ret
            print("there is no solution!")

