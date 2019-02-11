import math
import os
import random
import re
import sys


# Complete the nonDivisibleSubset function below.
def nonDivisibleSubset(S,K):
    cnt = [0] * S
    for x in K:
        cnt[x % k] += 1

    ans = min(cnt[0], 1)
    for rem in range(1, (k + 1) // 2):
        ans += max(cnt[rem], cnt[k - rem])
    if k % 2 == 0:
        ans += min(cnt[k // 2], 1)
    return ans

if __name__ == '__main__':



    n = 1

    k = 3

    S = [1,7,2,4]
    print([1,2,"dsds"])
    result = nonDivisibleSubset(k, S)
    print(result)

