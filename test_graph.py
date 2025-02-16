import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime

# Define the date range
start_date = datetime.datetime(2025, 1, 13)
end_date = datetime.datetime(2025, 5, 16)

# Define tasks with start dates and durations (in days)
tasks = [
    ('Task 1', start_date, 14),
    ('Task 2', start_date + datetime.timedelta(days=15), 21),
    ('Task 3', start_date + datetime.timedelta(days=37), 28),
    ('Task 4', start_date + datetime.timedelta(days=66), 14),
    ('Task 5', start_date + datetime.timedelta(days=81), 21),
]

# Create the figure and axis
fig, ax = plt.subplots()

# Add the tasks to the Gantt chart
for task, start, duration in tasks:
    end = start + datetime.timedelta(days=duration)

plt.show()