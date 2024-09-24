def get_Count(binary):
    unique_decimals = set()
    n = len(binary)
    for i in range(1,1<<n):
        subseq = ""
        for j in range(n):
            if i & (1<<j):
                subseq += binary[j]
        if subseq:
            unique_decimals.add(int(subseq,2))
    return len(unique_decimals)

print(get_Count("11")) 
