"""Climing-stairs
   You are climbing a stair case. It takes n steps to reach to the top.
   Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?"""


def sol_1(n):
    """recursive DP, f(n) = f(n-1) + f(n-2).
       cache n -> f(n) map to speed up"""
    vals_cache = {}

    def get_val(m):
        if m in vals_cache:
            return vals_cache[m]
        assert m > 0
        if m == 1:
            out = 1
        elif m == 2:
            out = 2
        else:
            out = get_val(m - 1) + get_val(m - 2)
        vals_cache[m] = out
        return out

    return get_val(n)


def sol_2(n):
    """transform recursion to induction.
       space complexity from O(n) to O(1)"""
    if n == 1:
        return 1
    elif n == 2:
        return 2
    else:
        f0, f1 = 1, 2
        for _ in range(n - 2):
            next_val = f0 + f1
            f0 = f1
            f1 = next_val
        return f1


# sol_3 & sol_4
# f(n) = f(n-1) + f(n-2)转换为矩阵乘法递推式


"""sol_3
   快速幂运算：https://blog.csdn.net/qq_19782019/article/details/85621386
   1，加速思路：增大底数，减少幂数，以减少循环次数
   a^b = (a^2)^(b / 2) if b % 2 == 0 else (a^2)^((b - 1) / 2)) * a 
   2，C中可以用位运算进一步加速：
   (1)，判断b是否为偶数：b & 1 （位与运算）
   (2)，floor(b / 2)：b >> 1 （位右移）"""

"""sol_4
   矩阵的特征值分解
   A = Q * Lambda * Q^-1
   其中Q为A的特征向量矩阵，Lambda为对应的特征值对角阵
   A^n = Q * Lambda^n * Q^-1"""