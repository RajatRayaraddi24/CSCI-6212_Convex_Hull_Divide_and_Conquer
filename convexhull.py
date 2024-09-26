#Submitted by: Rajat Rayaraddi (G23127315)

from functools import cmp_to_key
import matplotlib.pyplot as plt
import random
import time

mid = [0, 0]

def findquadrant(point):
    if point[0] >= 0 and point[1] >= 0:
        return 1
    if point[0] <= 0 and point[1] >= 0:
        return 2
    if point[0] <= 0 and point[1] <= 0:
        return 3
    return 4

def checkintersection(x, y, z):
    res = (y[1]-x[1]) * (z[0]-y[0]) - (z[1]-y[1]) * (y[0]-x[0])
    if res == 0:
        return 0
    if res > 0:
        return 1
    return -1

def sorting(x1, y1):
    x = [x1[0]-mid[0], x1[1]-mid[1]]
    y = [y1[0]-mid[0], y1[1]-mid[1]]
    one = findquadrant(x)
    two = findquadrant(y)
    if one != two:
        if one < two:
            return -1
        return 1
    if x[1]*y[0] < y[1]*x[0]:
        return -1
    return 1

def mergehull(left, right):
    n1, n2 = len(left), len(right)
    rightmost, leftmost = 0, 0

    #Finding the rightmost point of the left sub-hull and the leftmost point of the right sub-hull
    for i in range(1, n1):
        if left[i][0] > left[rightmost][0]:
            rightmost = i

    for i in range(1, n2):
        if right[i][0] < right[leftmost][0]:
            leftmost = i

    tempa, tempb = rightmost, leftmost
    done = 0
    # Calculating the upper tangent
    while not done:
        done = 1
        while checkintersection(right[tempb], left[tempa], left[(tempa+1) % n1]) >= 0:
            tempa = (tempa + 1) % n1
        while checkintersection(left[tempa], right[tempb], right[(n2+tempb-1) % n2]) <= 0:
            tempb = (tempb - 1) % n2
            done = 0
    upper_left, upper_right = tempa, tempb
    
    tempa, tempb = rightmost, leftmost
    done = 0
    g = 0
    # Calculating the upper tangent
    while not done:
        done = 1
        while checkintersection(left[tempa], right[tempb], right[(tempb+1) % n2]) >= 0:
            tempb = (tempb + 1) % n2
        while checkintersection(right[tempb], left[tempa], left[(n1+tempa-1) % n1]) <= 0:
            tempa = (tempa - 1) % n1
            done = 0
   
    ret = []
    lower_left, lower_right = tempa, tempb
    temp = upper_left
    ret.append(left[upper_left])
    while temp != lower_left:
        temp = (temp+1) % n1
        ret.append(left[temp])
    temp = lower_right
    ret.append(right[lower_right])
    while temp != upper_right:
        temp = (temp+1) % n2
        ret.append(right[temp])
    #'ret' returns the points that form the convex hull after merging the left and right sub-hulls
    return ret

def bruteHull(points):
    global mid
    s = set()
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            x1, x2 = points[i][0], points[j][0]
            y1, y2 = points[i][1], points[j][1]
            a1, b1, c1 = y1-y2, x2-x1, x1*y2-y1*x2
            pos, neg = 0, 0
            for k in range(len(points)):
                if (k == i) or (k == j) or (a1*points[k][0]+b1*points[k][1]+c1 <= 0):
                        neg += 1
                if (k == i) or (k == j) or (a1*points[k][0]+b1*points[k][1]+c1 >= 0):
                        pos += 1
            if pos == len(points) or neg == len(points):
                s.add(tuple(points[i]))
                s.add(tuple(points[j]))
    ret = []
    for x in s:
        ret.append(list(x))

    mid = [0, 0]
    n = len(ret)
    for i in range(n):
        mid[0] += ret[i][0]
        mid[1] += ret[i][1]
        ret[i][0] *= n
        ret[i][1] *= n
    ret = sorted(ret, key=cmp_to_key(sorting))
    for i in range(n):
        ret[i] = [ret[i][0]/n, ret[i][1]/n]
    return ret

def divide(points):
    if len(points) <= 5:
        return bruteHull(points)
    
    #Splitting the points into two halves, left and right
    left, right = [], []
    start = int(len(points)/2)
    for i in range(start):
        left.append(points[i])
    for i in range(start, len(points)):
        right.append(points[i])
    left_hull = divide(left)
    right_hull = divide(right)
    return mergehull(left_hull, right_hull)


ns = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000]
# ns = [100]
times = []

for n in ns:
    points = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]
    n = len(points)
    start_time = time.perf_counter_ns()
    points.sort() #Sorting the points by their x-coordinate
    convexhull = divide(points)
    elapsed_time = time.perf_counter_ns() - start_time
    times.append(elapsed_time)
    print(f"n = {n}, Time = {elapsed_time} ns")
    
    # print("Convex Hull: ", ans)

    # x_vals, y_vals = zip(*points)
    # plt.scatter(x_vals, y_vals, marker = 'o')
    # ans.append(convexhull[0])
    # i_vals, j_vals = zip(*convexhull)
    # plt.plot(i_vals, j_vals, marker = 'x', color = "orange")
    # plt.show()

plt.figure(figsize=(10, 6))
plt.plot(ns, times, marker='o', label='Experimental Time', color = 'blue')
plt.title('Experimental Time v/s n')
plt.xlabel('Number of Points (n)')
plt.ylabel('Time (ns)')
plt.legend()
plt.grid(True)
plt.show()
