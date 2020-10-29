"""Maximum-subarray:
   Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum."""


def sol_1(nums):
    """DP solution, define f(n) as 'val of maximum-subarray with nth element as its right end'"""
    max_val = None
    fn = None
    for n in nums:
        if fn is None:
            fn = n
            max_val = n
        else:
            fn = max(fn + n, n)
            if fn > max_val:
                max_val = fn
    return max_val


def sol_2(nums):
    """divide-conquer solution.
       merge info between two contingent subarrays"""

    def get_sum_info(a):
        """ output in order:
        lsum = max sum from left
        rsum = max sum from right
        bsum = best sum overall
        tsum = sum of all elements"""

        if len(a) == 1:
            return a[0], a[0], a[0], a[0]
        else:
            mid_point = int(len(a) / 2)
            # split into left and right
            array_left = a[:mid_point]
            array_right = a[mid_point:]
            # get left and right info separately
            lsum_left, rsum_left, bsum_left, tsum_left = get_sum_info(array_left)
            lsum_right, rsum_right, bsum_right, tsum_right = get_sum_info(array_right)
            # merge left and right info
            lsum = max(lsum_left, tsum_left + lsum_right)
            rsum = max(rsum_right, tsum_right + rsum_left)
            tsum = tsum_left + tsum_right
            bsum = max(bsum_left, bsum_right, rsum_left + lsum_right)
            return lsum, rsum, bsum, tsum

    return get_sum_info(nums)[2]
