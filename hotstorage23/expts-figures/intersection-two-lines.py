#!/usr/bin/env python3

#
# Copyright (c) 2020-2024 Yifei Liu
# Copyright (c) 2020-2024 Erez Zadok
# Copyright (c) 2020-2024 Stony Brook University
# Copyright (c) 2020-2024 The Research Foundation of SUNY
#
# You can redistribute it and/or modify it under the terms of the Apache License, 
# Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
#

# Python program to find the point of
# intersection of two lines
 
# Class used to  used to store the X and Y
# coordinates of a point respectively
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
 
    # Method used to display X and Y coordinates
    # of a point
    def displayPoint(self, p):
        print(f"({p.x}, {p.y})")
 
 
def lineLineIntersection(A, B, C, D):
    # Line AB represented as a1x + b1y = c1
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1*(A.x) + b1*(A.y)
 
    # Line CD represented as a2x + b2y = c2
    a2 = D.y - C.y
    b2 = C.x - D.x
    c2 = a2*(C.x) + b2*(C.y)
 
    determinant = a1*b2 - a2*b1
 
    if (determinant == 0):
        # The lines are parallel. This is simplified
        # by returning a pair of FLT_MAX
        return Point(10**9, 10**9)
    else:
        x = (b2*c1 - b1*c2)/determinant
        y = (a1*c2 - a2*c1)/determinant
        return Point(x, y)
 
 
# Driver code
A = Point(1000, 6.72362709812683)
B = Point(10000, 9.259823416151523)
C = Point(1000, 8.615350825213364)
D = Point(10000, 7.132847920586027)
 
intersection = lineLineIntersection(A, B, C, D)
 
if (intersection.x == 10**9 and intersection.y == 10**9):
    print("The given lines AB and CD are parallel.")
else:
    # NOTE: Further check can be applied in case
    # of line segments. Here, we have considered AB
    # and CD as lines
    print("The intersection of the given lines AB " + "and CD is: ")
    intersection.displayPoint(intersection)
 