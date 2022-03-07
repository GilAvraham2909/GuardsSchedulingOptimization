import random

import IntegerPrograming
import function as f
import genetic
import new_starts_hill_climbing

# const value
num_shifts = 3
num_days = 7
option = 1
# default value
guards = 10
per_shift = [3, 5, 4, 4, 5, 3, 4, 4, 4, 5]
shift = ["011 101 000 010 111 010 101",
         "000 010 010 010 100 111 111",
         "001 000 000 011 100 001 010",
         "100 000 010 010 101 001 100",
         "000 000 010 010 100 010 010",
         "100 000 001 010 010 000 110",
         "000 000 010 001 100 001 110",
         "000 111 010 010 000 010 110",
         "010 010 010 010 100 000 010",
         "111 000 010 000 100 111 100", ]


# # const value
# num_shifts = 3
# num_days = 7
# option = 1
# # default value
# guard = 20
# per_shift = [2, 2, 2, 3, 3, 3, 4, 4, 4, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 2]
# shift = ["111 100 000 010 001 010 101",
#          "000 000 010 010 100 000 110",
#          "001 000 000 011 100 001 010",
#          "100 000 010 010 101 000 100",
#          "000 000 010 010 100 010 010",
#          "000 000 001 010 010 000 110",
#          "000 000 010 001 100 001 110",
#          "000 000 000 010 000 000 110",
#          "000 010 010 010 100 000 010",
#          "000 000 010 000 100 000 100",
#          "000 001 010 010 100 000 010",
#          "000 000 001 010 100 100 110",
#          "000 000 010 010 000 010 110",
#          "000 000 010 011 101 000 110",
#          "000 000 010 100 101 000 000",
#          "000 111 010 010 000 000 110",
#          "110 000 000 010 100 000 100",
#          "001 000 010 000 100 000 010",
#          "000 010 010 010 000 000 000",
#          "110 111 111 101 111 111 111"]


def generate_guard_shifts(guard):  # this function generate a guard list
    guard_list = []
    nuers_schedual = ""
    for n in range(guard):
        nuers_schedual = ""
        for day in range(num_days):
            for hour in range(num_shifts):
                nuers_schedual += str(random.randint(0, 1))  # random a number
            if day != num_days - 1:
                nuers_schedual += " "  # do a backspace
        guard_list.append(nuers_schedual)  # insert the weekly shift of the guard

    for n in range(guard):
        print('Guard %d wants to work in:' % (n + 1))
        print(guard_list[n])
        print()

    print()
    print()
    print()
    print()

    return guard_list


def generate_shift_num():
    shift_l = []
    for index in range(guard):
        shift_l.append(random.randint(2, 4))

    for n in range(guard):
        print("guard " + str(n) + " can work only " + str(shift_l[n]) + " shifts")

    return shift_l


def insert_shift_num(guard):
    shift_l = []
    print("insert guards shifts percentage.")
    print("an number from 2-4 when 4 is full time job.")
    for index in range(1, guard + 1):
        print("please insert number of shift to guard number: " + str(index))
        shift_per = input()
        shift_l.append(shift_per)

    for n in range(1, guard + 1):
        print("guard " + str(n) + " can work only " + str(shift_l[n]) + " shifts")

    return shift_l


if __name__ == '__main__':
    print("welcome to Scheduling guard problem")
    print("")

    save_values = False
    shift_requests = []
    num_shift = per_shift
    while option != -1:
        if not save_values:
            print('Choose a number of guard:')
            print('1 - To define a value')
            print('2 - To a default value')
            print('3 - To a random value')
            print('0 - Quit')
            option = int(input())

            if option == 1:
                print("write number of guard: ")
                guard = int(input())
                s = []
                print("insert guards shifts request.")
                print("the input need to look like:\n000 101 000 011 111 000 010")
                print("3 numbers for each day in week.")
                print("1 - request for don't work in this shift")
                print("0 - request for work in this shift")
                print("")
                for i in range(1, guard + 1):
                    print("please insert shift to guard number: " + str(i))
                    shift = input()
                    s.append(shift)
                shift_requests = f.input_requerst(s)
                print('would you like to create random shift percentage?')
                print('1 - no')
                print('2 - yes')
                option = int(input())
                if option == 2:
                    num_shift = generate_shift_num()  # generate a random one
                else:
                    num_shift = insert_shift_num(guard)
            elif option == 2:
                shift_requests = f.input_requerst(shift)  # create static
                guard = guards
            elif option == 0:
                exit(0)
            else:
                print("write number of guard: ")
                guard = int(input())
                shift_requests = f.input_requerst(generate_guard_shifts(guard))  # create random
                print('would you like to create random shift percentage?')
                print('1 - no')
                print('2 - yes')
                option = int(input())
                if option == 2:
                    num_shift = generate_shift_num()  # generate a random one
                else:
                    num_shift = insert_shift_num(guard)
        print('Choose a technique for scheduling:')
        print('1 - Integer Programing')
        print('2 - Hill Climb with n random start')
        print('3 - Genetic algorithm')
        print('0 - Quit')
        option = int(input())
        # option 1
        if option == 1:
            print("")
            print("Maximize shifts Result:")
            IntegerPrograming.main(guard, shift_requests, num_days, num_shifts, num_shift)
            # f.print_result(solve, shift, shift_requests, guard, num_days, num_shifts, "", status)
        # option 2
        elif option == 2:
            print("")
            print("how much random start would you like to do?")
            n_start = int(input())
            print("")
            print("Hill Climb with %d random start Result:" % n_start)
            new_starts_hill_climbing.main(guard, shift_requests, num_days, num_shifts, num_shift, n_start)
        # option 3
        elif option == 3:
            print("")
            print("Please insert number of generate: ")
            gen = int(input())
            print("")
            print("Genetic algorithm Result:")
            genetic.main(guard, shift_requests, num_days, num_shifts, num_shift, gen)
        # option 0
        elif option == 0:
            exit(0)

        else:
            print("Wrong answer. Please, choose a valid option.")

        print("would you like to use same values for shift percentage and guard input?")
        print('1 - yes')
        print('other number - no')
        option = int(input())
        if option == 1:
            save_values = True
        else:
            save_values = False

        option = 1
