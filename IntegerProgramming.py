from ortools.linear_solver import pywraplp
import random

number_of_guards = 30


def generate_guard_shifts():  # this function generate a guard list
    guard_list = []
    days = 7
    shift_h = 3
    took_shift = False
    for guard in range(number_of_guards):
        weekly_shift = {}
        for day in range(days):
            took_shift = False
            for hour in range(shift_h):
                if took_shift:  # if the guard took a shift today, she cant take another one for the same day.
                    weekly_shift[day, hour] = 1
                else:
                    shift = random.randint(0, 1)
                    weekly_shift[day, hour] = shift
                    if shift == 0:  # if shift equal to 0, the guard took the shift
                        took_shift = True
        guard_list.append(weekly_shift)  # insert the weekly shift of the guard

    for guard in range(number_of_guards):
        for day in range(days):
            for hour in range(shift_h):
                if guard_list[guard][day, hour] == 0:
                    print('Guard %d wants to work in day %d at shift %d' % (guard + 1, day + 1, hour))

    print()
    print()
    print()
    print()

    return guard_list


def check_match(given, output):
    days = 7
    shift = 3
    count_correct = 0
    num_of_guard = len(given)
    for guard in range(num_of_guard):
        for day in range(days):
            for hour in range(shift):
                if given[guard][day, hour] == output[guard][day, hour]:
                    count_correct += 1
    print("number of happiness is: " + str((count_correct / (21 * number_of_guards)) * 100) + "%")
    print("correct of all: " + str(count_correct) + " / " + str(number_of_guards * 21))


def give_shifts():
    day = 7
    shift = 3
    solver = pywraplp.Solver.CreateSolver('SCIP')
    guard_list = generate_guard_shifts()
    num_of_guard = len(guard_list)
    prob_list = []
    # make an input for the problem
    for k in range(num_of_guard):
        x = {}
        for i in range(day):
            for j in range(shift):
                x[i, j] = solver.IntVar(0, 1, '')
        prob_list.append(x)

    # any guard can do only one shift a day
    for guard in range(num_of_guard):
        for i in range(day):
            solver.Add(solver.Sum([prob_list[guard][i, j] for j in range(shift)]) >= 2)

    # each shift has to have at least 2 guards
    for days in range(day):
        for hour in range(shift):
            solver.Add(
                solver.Sum([prob_list[guard][days, hour] for guard in range(num_of_guard)]) <= (number_of_guards - 2))

    # insert the guard constraints

    # now define the objective
    objective1 = []
    for guard in range(num_of_guard):
        for days in range(day):
            for hour in range(shift):
                # check for the sub between a guard and the variable
                if guard_list[guard][days, hour] == 1:
                    objective1.append(prob_list[guard][days, hour] - guard_list[guard][days, hour])
                else:  # value equal to 0
                    objective1.append(guard_list[guard][days, hour] - prob_list[guard][days, hour])
    # we want to maximize the sum of happiness of the guards
    solver.Maximize(solver.Sum(objective1))

    # Solve
    status = solver.Solve()

    output = []  # save the output
    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print('Total happiness = ', solver.Objective().Value(), '\n')
        for guard in range(num_of_guard):
            n = {}
            for days in range(day):
                for hour in range(shift):
                    # Test if x[i,j] is 1 (with tolerance for floating point arithmetic).
                    if prob_list[guard][days, hour].solution_value() > 0.5:
                        n[days, hour] = 1
                        print('guard %d assigned to day %d and to shift %d' % (guard + 1, days + 1, hour))
                    else:
                        n[days, hour] = 0
            output.append(n)
            print()
        check_match(guard_list, output)


def main(num_guards, shift_requests, num_days, num_shifts, max_shift):
    all_guards = range(num_guards)
    all_days = range(num_days)
    all_shifts = range(num_shifts)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    # guard_list = generate_guard_shifts()
    guard_list = shift_requests
    prob_list = []
    # make an input for the problem
    for k in all_guards:
        line = []
        for i in all_days:
            column = []
            for j in all_shifts:
                column.append(solver.IntVar(0, 1, ''))
            line.append(column)
        prob_list.append(line)

    # any guard can do only one shift a day
    for guard in all_guards:
        for i in all_days:
            solver.Add(solver.Sum([prob_list[guard][i][j] for j in all_shifts]) <= 1)

    # each shift has to have at least 2 guards
    for days in all_days:
        for hour in all_shifts:
            solver.Add(
                solver.Sum([prob_list[guard][days][hour] for guard in all_guards]) >= 2)

    # insert the guard constraints
    for guard in all_guards:
        # Each guard works at most num of shifts she can do
        solver.Add(solver.Sum(prob_list[guard][d][s] for d in all_days for s in all_shifts) <= max_shift[guard])
        for day in all_days:
            for shift in all_shifts:
                if guard_list[guard][day][shift] == 1:  # if the guard cant take the shift
                    solver.Add(prob_list[guard][day][shift] == 0)  # make it a constraint

    # Each guard don't works two shifts in consecutive
    for n in all_guards:
        for d in all_days:
            next = d + 1
            if next <= num_days - 1:
                solver.Add(prob_list[n][d][2] + prob_list[n][next][0] <= 1)

    # now define the objective
    objective = []
    for guard in all_guards:
        guard_shift = 0
        for days in all_days:
            for hour in all_shifts:
                guard_shift += prob_list[guard][days][hour]  # sum all the shifts the guard take
        objective.append(guard_shift)

    # we want to maximize the sum of shifts of the guards
    solver.Maximize(solver.Sum(objective))

    # Solve
    status = solver.Solve()
    # return solver, prob_list, status

    # Print solution.
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        for d in all_days:
            print('Day', d + 1)
            for n in all_guards:
                for s in all_shifts:
                    if prob_list[n][d][s].solution_value() > 0.5:
                        if shift_requests[n][d][s] == 1:
                            print('Guard', n, 'works shift', s, '(not requested).')
                        else:
                            print('Guard', n, 'works shift', s)
            print("")
        print(
            'Total shifts = ' + str(solver.Objective().Value()) + " / " + str(sum(max_shift)) + " succeed to maximize")
        print("")
    else:
        print("there is no solution!")
