class Worker:
    def __init__(self, name: str, morning_timeslot: list, afternoon_timeslot: list):
        self.name = name
        self.morning = morning_timeslot
        self.afternoon = afternoon_timeslot
        self.workload = 0

    def get_available_hours(self):
        if self.morning and self.afternoon:
            return self.afternoon[1] - self.morning[0] - 1
        elif self.morning and not self.afternoon:
            return self.morning[1] - self.morning[0]
        elif not self.morning and self.afternoon:
            return self.afternoon[1] - self.afternoon[0]
        else:
            return 0

    def update_timeslot(self, hours_taken: int):
        if self.morning:
            end_time = self.morning[0] + hours_taken
            time_gap = self.afternoon[0] - self.morning[1]
            if end_time > self.morning[1]:
                self.afternoon = [self.morning[0] + hours_taken + time_gap, self.afternoon[1]]
                self.morning = []
            else:
                self.morning = [self.morning[0] + hours_taken, self.morning[1]]
        else:
            self.afternoon = [self.afternoon[0] + hours_taken, self.afternoon[1]]


class Task:
    def __init__(self, name: str, hours: int, deadline: int):
        self.name = name
        self.hours = hours
        self.deadline = deadline


def schedule_tasks(workers, tasks) -> None:
    # Sort tasks by deadline
    tasks = sorted(tasks, key=lambda task: task.deadline)

    # To check if any task is assigned at the end of the while loop
    task_after = len(tasks)

    while len(tasks) > 0:
        task_before = task_after

        # Sort workers by workload and available hours
        workers = sorted(workers, key=lambda worker: (worker.workload, worker.get_available_hours()), reverse=True)

        for i, task in enumerate(tasks):
            for worker in workers:
                # Check worker's availability
                available_hours = worker.get_available_hours()
                if available_hours < task.hours:
                    continue

                # Calculate start time and end time
                start_time = worker.morning[0] if worker.morning else worker.afternoon[0]
                end_time = start_time + task.hours
                if start_time < 12 < end_time:
                    end_time += 1

                # Check deadline
                if end_time > task.deadline:
                    continue

                # Print result
                print(f"{task.name.ljust(10)} [{worker.name.ljust(10)}] hours needed: {task.hours}, start at: {start_time}, end at/ deadline: {end_time}/{task.deadline}")

                # Update worker's timesot and workload
                worker.update_timeslot(task.hours)
                worker.workload += task.hours

                # Remove the task and go to the next task
                tasks.pop(i)
                task_after -= 1
                break

        # Check any task can't be scheduled
        if task_before == task_after:
            if len(tasks) == 1:
                print(f"'{task.name}' can't be scheduled.")
            else:
                print(f"'{', '.join([task.name for task in tasks])}' can't be scheduled.")
            break


# Initialize workers
worker1 = Worker('Jason', [9, 12], [13, 18])
worker2 = Worker('Dick', [9, 12], [13, 18])
worker3 = Worker('Neo', [9, 12], [13, 18])
# Just add some random workers
worker4 = Worker('Tim', [], [13, 18])  # he is not available in morning
worker5 = Worker('Tony', [9, 12], [])  # he is not available in afternoon
total_workers = [worker1, worker2, worker3, worker4, worker5]

# Rules:
# - task hours must be less than 8 (8 hours per day per worker)
# - deadline must be less than 18
# - deadline > 9 + hours
task1 = Task('Task 1', 3, 18)
task2 = Task('Task 2', 2, 15)
task3 = Task('Task 3', 1, 16)
task4 = Task('Task 4', 4, 17)
# Just add some random tasks
task5 = Task('Task 5', 5, 16)
task6 = Task('Task 6', 3, 17)
task7 = Task('Task 7', 8, 18)
total_tasks = [task1, task2, task3, task4, task5, task6, task7]

task_valid = True
for task in total_tasks:
    if task.hours > 8 or task.deadline > 18 or not task.deadline > 9 + task.hours:
        print(f"Task {task.name} is invalid.")
        task_valid = False


# Count total manpower
total_manpower = sum(worker.get_available_hours() for worker in total_workers)
print(f"Total manpower: {total_manpower} hrs")

# Count total task hours
total_task_hours = sum(task.hours for task in total_tasks)
print(f"Total task: {total_task_hours} hrs")

# Check possibility
if total_task_hours > total_manpower:
    print("Not enough man power for the tasks.")
else:
    if task_valid:
        schedule_tasks(total_workers, total_tasks)

        # Count workload
        print("\nWorkload counting:")
        for worker in total_workers:
            print(f"{worker.name} workload: {worker.workload}")