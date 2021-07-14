"""You are given k identical eggs and you have access to a building with n floors labeled from 1 to n.

   You know that there exists a floor f where 0 <= f <= n such that any egg dropped at a floor higher than f will break,
   and any egg dropped at or below floor f will not break.

   Each move, you may take an unbroken egg and drop it from any floor x (where 1 <= x <= n).
   If the egg breaks, you can no longer use it.
   However, if the egg does not break, you may reuse it in future moves.

   Return the minimum number of moves that you need to determine with certainty what the value of f is."""


import numpy as np


def strategy_table(n, k):
    """n: number of floors
       k: number of eggs

       DP status transformation function:
       choose the first trail floor x:
       if break, to status: f(x - 1, k - 1)
       if not break, to status: f(n - x, k)
       given x, following number of trails to ensure finding thresh is max(f(x - 1, k - 1), f(n - x, k)).
       to minimize total possible number of trails, need to choose x that gives minimum of above values.
       f(n, k) = min_x(max(f(x - 1, k - 1) + 1, f(n - x, k) + 1)),

       execution strategy:
       given (n, k), choose 1 <= x <= n, s.t. max(f(x - 1, k - 1) + 1, f(n - x, k) + 1) is minimum"""

    f_vals = {}  # key: n, k pair, value: v0 = number of drops, v1: optimal first drop
    for ki in range(1, k + 1):
        f_vals[(1, ki)] = (1, 1)  # with only one floor, we only need one drop
        f_vals[(0, ki)] = (0, 0)  # zero floor is prepared in case first drop is top floor
    for ni in range(1, n + 1):
        # with only one egg, we can only try it from bottom to up
        f_vals[(ni, 1)] = (ni, 1)

    for ki in range(2, k + 1):
        # fill all n for each k at a time, as f(n, k) need all n values for k and k - 1
        for ni in range(2, n + 1):
            max_vals = [max(f_vals[(x - 1, ki - 1)][0] + 1, f_vals[(ni - x, ki)][0] + 1) for x in range(1, ni + 1)]
            f_vals[(ni, ki)] = (min(max_vals), list(range(1, ni + 1))[np.argmin(max_vals)])

    return f_vals


def sol_1(n, k):
    f_vals = strategy_table(n, k)
    return f_vals[(n, k)][0]


def sol_1_2(n, k):
    """given (n, k), f(x) = max(dp(x - 1, k - 1), dp(n - x, k)) is convex
       can use bi-section search to reduce time-complexity from O(n * k * n) to O(n * k * log(n))

       space complexity: full table is O(n * k), for each k, only values of recent two lines are needed, so can reduce to O(n)"""
    pass


def sol_1_3(n, k):
    """further reduce time complexity to O(n * k)

       bi-section search, given {n, k}
       f1(x) = dp(x - 1, k - 1), strictly increasing w.r.t x
       f2(x) = dp(n - x, k), strictly decreasing w.r.t. x

       x take values from 1 to n
       we have f1 < f2 for small values of x, f1 > f2 for large values fo x.
       bi-section search solution is the smallest int x for f1 > f2 (one of {x - 1, x})

       given k, x_opt(n, k) is strictly increasing w.r.t. n, i.e. if n1 > n2, then x_opt(n1, k) >= x_opt(n2, k)
       f1 does not move, f2 parallel moves higher with larger n

       so, we can first loop through k,
       given each k, we don't need to separately search x_opt for each ni,
       only need to scan x_opt from 1 to n once for all ni,
       i.e. after we find x_opt(i) for ni, for ni + 1, we only need to gradually add 1 to x_opt(i) until we find first f1(x; ni + 1) > f2(x; ni + 1),
       we know for ni + 2, x_opt(i + 2) will not be missed in numbers smaller than x_opt(i + 1)
       """
    # space complexity == O(n) solution
    dp1 = list(range(0, n + 1))  # n vec for k - 1
    dp2 = [0, 1] + [0] * (n - 1)  # n vec for k
    for ki in range(2, k + 1):
        x = 1
        for ni in range(2, n + 1):
            # t1 = dp(x - 1, k - 1)
            # t2 = dp(n - x, k)
            # find first t1 > t2
            while x <= ni and dp1[x - 1] < dp2[ni - x]:
                # floor idx to list idx, since dp records from n == 0, no offset needed
                x += 1
            dp2[ni] = max(dp1[x - 1], dp2[ni - x]) + 1
        dp1 = dp2
        dp2 = [0, 1] + [0] * (n - 1)
    return dp1[-1]


def sol_2(n, k):
    """k: number of eggs
       m: number of trails
       dp(k, m): maximum number of floors to test.

       execution strategy (to realize this maximum number):
       first trail at dp(k - 1, m - 1) + 1,
       if the first trail breaks, we still have k - 1 eggs and m - 1 trails to fully try the lower dp(k - 1, m - 1) floors.
       if the first trail survives, we can further try with m - 1 trails and k - 1 eggs, i.e. dp(k, m - 1).

       dp status transformation function:
       dp(k, m) = dp(k - 1, m - 1) + 1 + dp(k, m - 1)
       boundaries: dp(k, 1) = 1; dp(1, m) = m

       find m for n: minimum m s.t. dp(k, m) >= n
       time complexity: O(n * k),
       NOTE, looks we need to loop m from 1 to n, but as k increases, for dp(k, m) > n, we only need an "m" far more smaller than n.
             to get the effective time complexity needs some math, but the actual complexity is much smaller than O(n * k) at n dim.
             that's why we find sol_2 is much faster than sol_1_3 with large "n".
       space complexity: O(n * k), similar as above, can reduce to O(k)
       """
    dp = {}
    for ki in range(1, k + 1):
        dp[(ki, 1)] = 1
    for mi in range(1, n + 1):
        # given n, 1 <= mi <= n
        dp[(1, mi)] = mi

    m = 0
    for mi in range(2, n + 1):
        for ki in range(2, k + 1):
            dp[(ki, mi)] = dp[(ki - 1, mi - 1)] + 1 + dp[(ki, mi - 1)]
        if dp[(k, mi)] >= n:
            m = mi
            break

    return m
