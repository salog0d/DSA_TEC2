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

        