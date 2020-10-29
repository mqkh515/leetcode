"""is subsequence:
   Given a string s and a string t, check if s is subsequence of t.

   A subsequence of a string is a new string which is formed from the original string by deleting some (can be none) of the characters without
   disturbing the relative positions of the remaining characters. (ie, "ace" is a subsequence of "abcde" while "aec" is not).

   Follow up:
   If there are lots of incoming S, say S1, S2, ... , Sk where k >= 1B, and you want to check one by one to see if T has its subsequence. In this scenario, how would you change your code?

   Credits:
   Special thanks to @pbrother for adding this problem and creating all test cases.

   Example 1:
   Input: s = "abc", t = "ahbgdc"
   Output: true

   Example 2:
   Input: s = "axc", t = "ahbgdc"
   Output: false
    
   Constraints:
   0 <= s.length <= 100
   0 <= t.length <= 10^4
   Both strings consists only of lowercase characters.
   """

import string


def sol_1(s, t):
    # each element of t has to be seen
    if len(s) == 0:
        return True
    sc_list = list(s)
    for tc in t:
        if tc == sc_list[0]:
            sc_list.pop(0)
        if len(sc_list) == 0:
            # NOTE substring could be all found before scanning all of t
            return True
    return False


def sol_2(s, t):
    # aim for Credits，思路：按字符全集预处理t中的字符串信息，每次遇到新的s不用扫描t中的所有字符
    if len(s) == 0:
        return True
    if len(t) == 0:
        return False

    def searchsorted(target, val_list):
        # find the first value in val_list that is larger than target
        # val_list is sorted from low to high with no duplication
        if len(val_list) == 0:
            return None
        if val_list[0] > target:
            return val_list[0]
        if val_list[-1] <= target:
            return None
        while len(val_list) > 1:
            mid_idx = int(len(val_list) / 2)
            if val_list[mid_idx] > target >= val_list[mid_idx - 1]:
                return val_list[mid_idx]
            elif len(val_list) == 2:
                print('val_list: %s, target: %s' % (str(val_list), str(target)))
                raise Exception('unexpected result')
            else:
                pass
            if val_list[mid_idx] > target:
                val_list = val_list[:mid_idx + 1]
            else:
                val_list = val_list[mid_idx:]
        raise Exception('unexpected result')

    info = {}
    for c in string.ascii_lowercase:
        info[c] = []
    for idx, c in enumerate(t):
        info[c].append(idx)

    curr_idx = -1
    for c in s:
        tar_idx = searchsorted(curr_idx, info[c])
        if tar_idx is None:
            return False
        else:
            curr_idx = tar_idx
    return True


def sol_3(s, t):
    # 思路同sol_2，将每次查询s的时间复杂度缩短到O(n)，其中n为s的长度。
    # 缓存信息为，对t的每个位置i，从i开始(包括i)，下一个字符j出现的位置(其中j为string.ascii_lowercase中的每一个字符)
    # 相较于sol_2，空间复杂度更高，时间更短

    # 用DP，使得预处理步的时间复杂度为m * 26，m为t的长度。
    # 思路：最后位置的字符信息已知，倒推，在给定位置n的字符信息后，位置n-1的字符信息为 pos(t[n-1]) = n-1，其他字符位置信息不变
    if len(s) == 0:
        return True
    if len(t) == 0:
        return False
    info = {}
    n = len(t)
    letters = string.ascii_lowercase
    for idx in range(n):
        pos = n - idx - 1
        info[pos] = {}
        if idx == 0:
            for c in letters:
                info[pos][c] = -1 if c != t[pos] else pos  # -1表示在pos之后找不到对应字符了
        else:
            for c in letters:
                info[pos][c] = info[pos + 1][c] if c != t[pos] else pos

    # search for s
    pos = 0
    for idx, c in enumerate(s):
        pos = info[pos][c]
        if pos == -1:
            return False
        pos += 1
        # NOTE, special case, when c is not the last char in s and c jumps to the end of t
        # has to use index to check end of list, use c == s[-1] can cause problem as value is allowed to be repeated
        if pos == len(t) and idx != len(s) - 1:
            return False
    return True
