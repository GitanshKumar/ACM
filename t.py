# B = int(input())
# n = int(input())
# wt = [int(input()) for _ in range(n)]

# def take(wt, B, n):
#     dp = [0] * (B + 1)

#     dp[0] = 1

#     for i in range(n):
#         for w in range(B, wt[i] - 1, -1):
#             dp[w] += dp[w - wt[i]]
    
#     return sum(dp)

# ans = take(wt, B, n)
# print(ans)

# n, m = [int(_) for _ in input().split()] # 3 3
n, m = 3, 3
# mat = [[int(i) for i in input().split()] for _ in range(n)]
mat = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# x, y = [int(_) for _ in input().split()] # 1 2
x, y = 1, 2
# dx, dy = [int(_) for _ in input().split()] # 2 3
dx, dy = 2, 3

def is_valid_cell(row, col):
    return 1 <= row <= n and 1 <= col <= m

def bfs(i, j, end, mat):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def helper(r, c, visited: set):
        if (r, c) == end:
            return mat[r - 1][c - 1]
        
        visited.add((r, c))

        min_charge = float('inf')
        for dir in directions:
            newX = r + dir[0]
            newY = c + dir[1]
            if is_valid_cell(newX, newY) and (newX, newY) not in visited:
                if newX - r > 0 and (newY - c) / (newX - r) < 0: continue
                charge = helper(newX, newY, visited)
                if charge != -1:
                    min_charge = min(min_charge, charge)
        
        visited.remove((r, c))
        return -1 if min_charge == float('inf') else min_charge
    
    return helper(i, j, set())

print(bfs(x, y, [dx, dy], mat))