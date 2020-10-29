"""Min Cost Climbing Stairs:

   On a staircase, the i-th step has some non-negative cost cost[i] assigned (0 indexed).
   Once you pay the cost, you can either climb one or two steps. You need to find minimum cost to reach the top of the floor,
   and you can either start from the step with index 0, or the step with index 1.

   Example 1:
   Input: cost = [10, 15, 20]
   Output: 15
   Explanation: Cheapest is start on cost[1], pay that cost and go to the top.

   Example 2:
   Input: cost = [1, 100, 1, 1, 1, 100, 1, 1, 100, 1]
   Output: 6
   Explanation: Cheapest is start on cost[0], and only step on 1s, skipping cost[3].

   Note:
   cost will have a length in the range [2, 1000].
   Every cost[i] will be an integer in the range [0, 999]."""


def sol_1(cost):
    # climbing stairs with cost
    # f(n) min_cost with step(n) as final step, f(n) = cost(n) + min(f(n-1), f(n-2))
    # NOTE: the "top" is not a step and does not have a cost associated to it, so in last step, remove the "cost" term from the induction formula
    f0 = cost[0]
    f1 = cost[1]
    for c in cost[2:]:
        f2 = c + min(f0, f1)
        f0 = f1
        f1 = f2
    return min(f0, f1)
