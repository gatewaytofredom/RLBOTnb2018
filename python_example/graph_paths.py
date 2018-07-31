import matplotlib.pyplot as plt

car_x = []
car_y = []
goal_x = []
goal_y = []

with open("test.csv", "r") as f:
    for l in f.read().split("\n"):
        row = l.split(",")
        if len(row) != 10:
            continue
        try:
            car_x.append(float(row[4]))
            car_y.append(float(row[5]))
            goal_x.append(float(row[2]))
            goal_y.append(float(row[3]))
        except ValueError:
            continue

plt.plot(goal_x, goal_y, color="green")
plt.plot(car_x, car_y, color="red")
plt.show()