def ques1():
    from collections import Counter
    def longest_common_substring(strings, n, smallest):
        max_longest = len(smallest)
        max_alpha = Counter(smallest)
        alpha = Counter()
        for char in smallest:
            alpha[char] = 0
        
        for string in strings:
            cur_count = Counter()
            for char in string:
                if char in alpha and cur_count[char] < max_alpha[char]:
                    cur_count[char] += 1    
            alpha += cur_count
        
        ans = 0
        for char in alpha:
            if alpha[char] > n:
                if max_longest == 1:
                    ans += alpha[char]
                else: 
                    ans += alpha[char] % n
            elif alpha[char] == n:
                ans += 1
        
        return ans

    n = int(input())
    strings = input().split()
    smallest = strings[0]

    for string in strings[1:]:
        if len(smallest) > len(string): smallest = string

    print(longest_common_substring(strings, n, smallest))


def max_string_product(strings):
    res = 1
    for string in strings:
        cur_value = ""
        for char in string:
            if char.isdigit(): cur_value += char
        if not cur_value:
            cur_value = len(string)
        res *= int(cur_value)
    
    return res

# n = int(input().replace("     -- denotes n ", ""))
# strings = input().replace("   -- denotes n space-separated array elements.").split()
# print(max_string_product(strings))

