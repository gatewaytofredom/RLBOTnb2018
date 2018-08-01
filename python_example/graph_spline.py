import matplotlib.pyplot as plt

goal_x = []
goal_y = []

with open("spl.csv", "r") as f:
    for l in f.read().split("\n"):
        row = l.split(",")
        if len(row) != 2:
            continue
        try:
            goal_x.append(float(row[0]))
            goal_y.append(float(row[1]))
        except ValueError:
            continue

# plt.xlim(-0.1, 1.1)
# plt.ylim(-0.2, 1)
plt.plot(goal_x, goal_y, color="green")
plt.show()