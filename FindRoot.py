# -*- coding: utf-8 -*-
# ==================================================================================================
#   FileName:       FindRoot.py
#   Author:         Don Murray
#   Purpose:        Given a function y of x, compute a root of that function within a starting
#                   bracket [xl, xr] and within a specified critierion on y.
#   SubFunctions:   Test_n_Adjust - This is the main sublogic that includes the do while construct
#                   EvalInterval - This function receives left and right x bracket endpoints and
#                                   computes y of x where x is the midpoint of the current interval.
#                   y_of_x - This is the single place where the user codes the function
#                   _Abort_ - This is reached when user supplied settings do not converge. The
#                                   purpose of it is to prevent the local system from catching in
#                                   an endless cycle.
#   Notes           All parameters are specified at the top of the main file (FindRoot.py)
#                   The conceptual process is an interval bisection method.
#   Usage           User sets these values in the code block below
#                   criterion - the value on the y-axis that is sufficiently close to zero
#                               (e.g. criterion = 0.001)
#                   xl - some x value that is believed to be less than the actual root.
#                   xr - some x value that is believed to be greater than the actual root.
#                   The function must be coded in the y_of_x variable as an expression of _x_
#                       to which y is equal.
# ==================================================================================================

import math
import sys

#   Start with y = 0.5 * x ** 2 - x - 1.5 and target roots -1 and 3
#   Another example y = 1.2 * x ** 3 + 0.7 x ** 2 - 2 * x + 3 with root around -2

crit = 1e-9 # on y
ixl = 1
ixr = 4

#   Define the function
#	y = 0.5 * x ** 2 - x - 1.5
# y = 2 * x ** 3 - 40 * x + 48
def yFunc(x):
    y = 2 * x ** 3 - 40 * x + 48  #   <<<=== FUNCTION y of x <<<===
    return y

# Initial interval and function value
def EvalInterval(x1, x2):
    x = (x1 + x2) / 2
    return x

xi = EvalInterval(ixl, ixr)
yi = yFunc(xi)
y = yi

cycles = 0
while (math.fabs(y) > crit):
    cycles += 1
    if cycles > 500:
        sys.exit()     #   This is like my SAS _Abort_ macro
    #   print("cycles: " + str(cycles))
    if cycles == 1:
        xl = ixl
        xr = ixr
    yl = yFunc(xl)
    yr = yFunc(xr)
    #   print("xl: " + str(xl) + " - yl: " + str(yl) + " - xr: " + str(xr) + " - yr: " + str(yr))
    if(((yl < 0) and (yr > 0)) or ((yl > 0) and (yr < 0))):
        if (math.fabs(yl) > math.fabs(yr)):
            xl = (xl + xr) / 2
        else:
            xr = (xl + xr) / 2
    else:
        if (math.fabs(yl) > math.fabs(yr)):
            xr = xr + (xr - xl) + 0.4   #   Need a fuzz factor to keep the two bracken resets from bouncing back and forth
        else:
            xl = xl - (xr - xl) - 0.4   #   Need a fuzz factor to keep the two bracken resets from bouncing back and forth
    x = EvalInterval(xl, xr)
    y = yFunc(x)
    #   print("y = " + str(y) + " - and x = " + str(x))

#   Produce plot of results
import numpy as np
import matplotlib
matplotlib.use('SVG')
import matplotlib.pyplot as plt

xp = np.arange(x - 1.5, x + 1.5, 0.1)
yp = yFunc(xp)

fig, ax = plt.subplots()
ax.plot(xp, yp, 'k--', label='function')
ax.plot(x, y, 'bo', label='root')

plt.xlabel('x')
plt.ylabel('y')
plt.title('Function: y = 0.5x ^ 2 - x - 1.5')

legend = ax.legend(loc='upper left', shadow=True, fontsize='medium')
legend.get_frame().set_facecolor('#EFEFEF')
plt.grid(True)

plt.savefig('Plot_Fnc_Rt_bi.svg')
plt.show()

print("y = " + str(y) + " and x = " + str(x))
print("Convergence in " + str(cycles) + " cycles.")