from guard_class import GuardSchedulingProblem
import random
import matplotlib.pyplot as plt

HARD_CONSTRAINT_PENALTY = 10  # the penalty factor for a hard-constraint violation


def generate_random_start(guard_num, num_days, num_shifts):  # this function builds a random start state
    length = guard_num * num_days * num_shifts  # will tell me the size of the array
    shifts_arr = []
    for i in range(length):
        shifts_arr.append(random.randint(0, 1))
    return shifts_arr


def get_neighbors(current_shifts):  # this function builds all the neighbors of the current state
    neighbors = []
    length = len(current_shifts)
    for i in range(length):
        temp_shifts = current_shifts[0:length]
        if temp_shifts[i] == 1:
            temp_shifts[i] = 0
        else:
            temp_shifts[i] = 1
        neighbors.append(temp_shifts)
    return neighbors


# convert the array into vector
def getVec(state, guard, num_days, num_shifts):
    guard_shift = []
    for n in range(guard):
        for day in range(num_days):
            for hour in range(num_shifts):
                guard_shift.append(state[n][day][hour])
    return guard_shift


def main(guard, shift_requests, num_days, num_shifts, num_shift, num_of_new_starts):
    nsp = GuardSchedulingProblem(HARD_CONSTRAINT_PENALTY, guard, shift_requests, num_days, num_shifts,
                                 num_shift)
    current_state = getVec(shift_requests, guard, num_days, num_shifts)
    cost = []
    counter = 1
    iteration = []
    highest_scores = []
    while num_of_new_starts > 0:
        neighbors = get_neighbors(current_state)  # take the neighbors of the current state
        next_eval = float('inf')
        next_node = 0
        for neighbor in neighbors:
            neighbor_cost = nsp.getCost(neighbor)
            if neighbor_cost < next_eval:
                cost.insert(len(cost), neighbor_cost)  # insert the neighbor cost
                iteration.insert(len(iteration), counter)  # insert the number of the iteration
                counter += 1
                # print("found better state, with :" + str(neighbor_cost))
                next_eval = neighbor_cost
                next_node = neighbor
        if next_eval >= nsp.getCost(current_state):  # return the current node, couldn't find any better state
            highest_scores.append(current_state)  # save the object
            num_of_new_starts -= 1
            current_state = generate_random_start(guard, num_days, num_shifts)  # create a random start
        else:
            current_state = next_node

    min_state = highest_scores[0]  # find the state with the minimum cost
    for state in highest_scores:
        if nsp.getCost(min_state) > nsp.getCost(state):
            min_state = state
    current_state = min_state
    plt.ylabel("states cost")
    plt.xlabel("iteration")
    plt.plot(iteration, cost)
    plt.show()
    print("the Minimum local cost is: " + str(nsp.getCost(current_state)))
    nsp.printScheduleInfo(current_state)  # print the current state info