"""
Subsets (Power Set as binary vectors)

Description:
Generates all subsets (as binary vectors) of size n using recursion.
The idea: for subsets of size n-1, duplicate them by appending a 0 and a 1
to each, obtaining all subsets of size n.

ALGORITHM subsets(n)
Generates all binary subsets of length n
Input: integer n (size of the binary vector)
Output: list of lists with 0/1 representing each subset

- Time complexity:  O(2^n)
"""


class Solution:
    
    @staticmethod
    def subsets(n):
        if n <= 0:
            return []
        if n == 1:
            return [[0], [1]]

        prev = Solution.subsets(n - 1)
        result = []

        for s in prev:
            result.append(s + [0])

        for s in prev:
            result.append(s + [1])

        return result


if __name__ == "__main__":
    n = 3   
    sol = Solution()
    subsets = sol.subsets(n)

    print(f"Subsets de tamaño {n}:")
    for s in subsets:
        print(s)

        