def change(s, dau, cuoi):

    n = len(s)
    pre = [0]*(n+1)
    suf = [0]*(n+1)
    cnt_pre = 0
    for i in range(n):
        if int(s[i]) != dau:
            cnt_pre +=1
        pre[i+1] = cnt_pre
    
    cnt_suf = 0
    for i in range(n-1,-1,-1):
        if int(s[i]) != cuoi:
            cnt_suf += 1
        suf[i] = cnt_suf
    
    min_val= pre[1] + suf[1]
    for i in range(1, n):
        if pre[i] + suf[i] < min_val:
            min_val = pre[i] + suf[i]

    return min_val
    
def solve():
    s = input()
    if len(s) <= 2:
        print(0)
    elif len(s) == 3:
        if s == '010' or s == '101':
            print(1)
        else:
            print(0)
    else:
        case1 = change(s, 1, 0)
        case2 = change(s, 0, 1)
        case3 = change(s, 1, 1)
        case4 = change(s, 0, 0)
        print(min(case1, case2, case3, case4))
        
            
def main():
    t = input()
    for _ in range(int(t)):
        solve()

if __name__ == "__main__":
    main()