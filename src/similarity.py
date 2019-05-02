def substrsim(S, T):
    L = [ 0 for _ in range(len(S) + len(T)) ]
    tot = 0
    best_len = 0
    best_end = 0
    for i in range(len(S)):
        for j in range(len(T)):
            k = len(S) + j - i
            if S[i] == T[j]:
                L[k] += 1
                if L[k] >= 3:
                   tot += L[k] ** 2
                if L[k] > best_len:
                    best_len = L[k]
                    best_end = i
            else:
                L[k] = 0
    return S[best_end - best_len + 1:best_end + 1], tot * min(len(S), len(T)) ** -2
