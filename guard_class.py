import numpy as np


class GuardSchedulingProblem:
    """This class encapsulates the Guard Scheduling problem
    """

    def __init__(self, hardConstraintPenalty, guard, shift_requests, num_days, num_shifts, num_shift):
        """
        :param hardConstraintPenalty: the penalty factor for a hard-constraint violation
        """
        self.hardConstraintPenalty = hardConstraintPenalty

        # list of guards:
        self.guards = []
        for i in range(guard):
            self.guards.append(str(i))

        # guards' respective shift preferences - morning, evening, night:
        #self.shiftPreference = [[1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 1, 1], [1, 1, 1]]

        # min and max number of guards allowed for each shift - morning, evening, night:
        self.shiftMin = [2, 2, 2]
        self.shiftMax = [100, 100, 100]

        # max shifts per week allowed for each guard
        self.ShiftsPerWeek = num_shift

        #guard request 0 -dont want to work
        self.shiftPreference = shift_requests

        # number of weeks we create a schedule for:
        self.weeks = 1

        # useful values:
        self.shiftPerDay = num_shifts
        self.days = num_days
        self.shiftsPerWeek = self.days * self.shiftPerDay

    def __len__(self):
        """
        :return: the number of shifts in the schedule
        """
        return len(self.guards) * self.shiftsPerWeek * self.weeks


    def getCost(self, schedule):
        """
        Calculates the total cost of the various violations in the given schedule
        ...
        :param schedule: a list of binary values describing the given schedule
        :return: the calculated cost
        """

        if len(schedule) != self.__len__():
            raise ValueError("size of schedule list should be equal to ", self.__len__())

        # convert entire schedule into a dictionary with a separate schedule for each guard:
        guardShiftsDict = self.getGuardShifts(schedule)

        # count the various violations:
        consecutiveShiftViolations = self.countConsecutiveShiftViolations(guardShiftsDict)
        shiftsPerWeekViolations = self.countShiftsPerWeekViolations(guardShiftsDict)[1]
        guardsPerShiftViolations = self.countGuardsPerShiftViolations(guardShiftsDict)[1]
        shiftPreferenceViolations = self.countShiftPreferenceViolations(guardShiftsDict)

        # calculate the cost of the violations:
        hardContstraintViolations = consecutiveShiftViolations + guardsPerShiftViolations + shiftsPerWeekViolations
        softContstraintViolations = shiftPreferenceViolations

        return self.hardConstraintPenalty * hardContstraintViolations + softContstraintViolations

    def getGuardShifts(self, schedule):
        """
        Converts the entire schedule into a dictionary with a separate schedule for each guard
        :param schedule: a list of binary values describing the given schedule
        :return: a dictionary with each guard as a key and the corresponding shifts as the value
        """
        shiftsPerGuard = self.__len__() // len(self.guards)
        guardShiftsDict = {}
        shiftIndex = 0

        for guard in self.guards:
            guardShiftsDict[guard] = schedule[shiftIndex:shiftIndex + shiftsPerGuard]
            shiftIndex += shiftsPerGuard

        return guardShiftsDict

    def countConsecutiveShiftViolations(self, guardShiftsDict):
        """
        Counts the consecutive shift violations in the schedule
        :param guardShiftsDict: a dictionary with a separate schedule for each guard
        :return: count of violations found
        """
        violations = 0
        # iterate over the shifts of each guard:
        for guardShifts in guardShiftsDict.values():
            # look for two cosecutive '1's:
            for shift1, shift2 in zip(guardShifts, guardShifts[1:]):
                if shift1 == 1 and shift2 == 1:
                    violations += 1
        return violations

    def countShiftsPerWeekViolations(self, guardShiftsDict):
        """
        Counts the max-shifts-per-week violations in the schedule
        :param guardShiftsDict: a dictionary with a separate schedule for each guard
        :return: count of violations found
        """
        violations = 0
        weeklyShiftsList = []
        # iterate over the shifts of each guard:
        for index, guardShifts in enumerate(guardShiftsDict.values()):  # all shifts of a single guard
            # iterate over the shifts of each weeks:
            for i in range(0, self.weeks * self.shiftsPerWeek, self.shiftsPerWeek):
                # count all the '1's over the week:
                weeklyShifts = sum(guardShifts[i:i + self.shiftsPerWeek])
                weeklyShiftsList.append(weeklyShifts)
                if weeklyShifts > self.ShiftsPerWeek[index]:
                    violations += weeklyShifts - self.ShiftsPerWeek[index]
                else:
                    violations += self.ShiftsPerWeek[index] - weeklyShifts


        return weeklyShiftsList, violations

    def countGuardsPerShiftViolations(self, guardShiftsDict):
        """
        Counts the number-of-guards-per-shift violations in the schedule
        :param guardShiftsDict: a dictionary with a separate schedule for each guard
        :return: count of violations found
        """
        # sum the shifts over all guards:
        totalPerShiftList = [sum(shift) for shift in zip(*guardShiftsDict.values())]

        violations = 0
        # iterate over all shifts and count violations:
        for shiftIndex, numOfGuards in enumerate(totalPerShiftList):
            dailyShiftIndex = shiftIndex % self.shiftPerDay  # -> 0, 1, or 2 for the 3 shifts per day
            if (numOfGuards > self.shiftMax[dailyShiftIndex]):
                violations += numOfGuards - self.shiftMax[dailyShiftIndex]
            elif (numOfGuards < self.shiftMin[dailyShiftIndex]):
                violations += self.shiftMin[dailyShiftIndex] - numOfGuards

        return totalPerShiftList, violations

    def countShiftPreferenceViolations(self, guardShiftsDict):
        """
        Counts the guard-preferences violations in the schedule
        :param guardShiftsDict: a dictionary with a separate schedule for each guard
        :return: count of violations found
        """
        violations = 0
        for guardIndex, shiftPreference in enumerate(self.shiftPreference):
            # duplicate the shift-preference over the days of the period
#            # iterate over the shifts and compare to preferences:
            temp = []
            for i in range(len(shiftPreference)):
                for j in range(len(shiftPreference[i])):
                    temp.append(shiftPreference[i][j])
            shifts = guardShiftsDict[self.guards[guardIndex]]
            for pref, shift in zip(temp, shifts):
                if pref == 1 and shift == 1:
                    violations += 1

        return violations

    def printScheduleInfo(self, schedule):
        """
        Prints the schedule and violations details
        :param schedule: a list of binary values describing the given schedule
        """
        guardShiftsDict = self.getGuardShifts(schedule)

        print("Schedule for the week:")

        for d in range(self.days):
            print('Day', d + 1)
            for n in self.guards:
                for s in range(self.shiftPerDay):
                    if (guardShiftsDict[n])[(d * self.shiftPerDay) + s] == 1:
                        if self.shiftPreference[int(n)][d][s] == 1:
                            print('Guard', n, 'works shift', s, '(not requested).')
                        else:
                            print('Guard', n, 'works shift', s)
            print("")

        print("")
        print("Statistics:")
        print("consecutive shift violations = ", self.countConsecutiveShiftViolations(guardShiftsDict))
        print()

        weeklyShiftsList, violations = self.countShiftsPerWeekViolations(guardShiftsDict)
        print("number of Shifts for each guard = ", weeklyShiftsList)
        print("Shifts Per Week Violations = ", violations)
        print()

        totalPerShiftList, violations = self.countGuardsPerShiftViolations(guardShiftsDict)
        print("number of Guards Per Shift = ", totalPerShiftList)
        print("Guards Per Shift Violations = ", violations)
        print()

        shiftPreferenceViolations = self.countShiftPreferenceViolations(guardShiftsDict)
        print("num of conflict in guards requests: ", shiftPreferenceViolations)
        print()

# testing the class:
def main():
    # create a problem instance:
    guards = GuardSchedulingProblem(10)

    randomSolution = np.random.randint(2, size=len(guards))
    print("Random Solution = ")
    print(randomSolution)
    print()

    guards.printScheduleInfo(randomSolution)

    print("Total Cost = ", guards.getCost(randomSolution))


if __name__ == "__main__":
    main()