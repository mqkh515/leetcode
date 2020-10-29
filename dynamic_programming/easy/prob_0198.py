"""House Robber:
   ou are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed,
   the only constraint stopping you from robbing each of them is that adjacent houses have security system connected
   and it will automatically contact the police if two adjacent houses were broken into on the same night.
   Given a list of non-negative integers representing the amount of money of each house,
   determine the maximum amount of money you can rob tonight without alerting the police.

    Example 1:
    Input: nums = [1,2,3,1]
    Output: 4
    Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
                 Total amount you can rob = 1 + 3 = 4.

    Example 2:
    Input: nums = [2,7,9,3,1]
    Output: 12
    Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
                 Total amount you can rob = 2 + 9 + 1 = 12.
     
    Constraints:
    0 <= nums.length <= 100
    0 <= nums[i] <= 400"""


def sol_1(nums):
    # define state f(n): given nums[i], f(n) = max value with numbers whose index i <= n
    # each state maintains 2 values:
    # state[0]: max-value-subset without nums[n]
    # state[1]: max-value-subset with nums[n]
    # then f(n+1)[0] = max(f(n)[1], f(n)[0]); f(n+1)[1] = f(n)[0] + nums[n]
    if len(nums) == 0:
        return 0
    state = [0, nums[0]]  # init state, f(0)
    for n in nums[1:]:
        new_state = [None, None]
        new_state[0] = max(state[0], state[1])
        new_state[1] = state[0] + n
        state = new_state
    return max(state)


def sol_2(nums):
    # 同楼梯问题，分情况讨论，f(n)的最大值有两种可能，包含nums[n]和不包含nums[n]
    # f(n) = max(f(n-2) + nums[n], f(n-1))
    if len(nums) == 0:
        return 0
    if len(nums) == 1:
        return nums[0]
    f0 = nums[0]
    f1 = max(nums[0], nums[1])
    for n in nums[2:]:
        f_temp = max(f0 + n, f1)
        f0 = f1
        f1 = f_temp
    return f1


