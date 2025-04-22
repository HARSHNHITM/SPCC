class Operation:
    def __init__(self, l, r):
        self.l = l
        self.r = r

ops = []
n = int(input("ENTER THE NUMBER OF VALUES: "))
for _ in range(n):
    l = input("LEFT: ").strip()
    r = input("RIGHT: ").strip()
    ops.append(Operation(l, r))

# Intermediate Code
print("\nINTERMEDIATE CODE")
for op in ops:
    print(f"{op.l}={op.r}")

# DEAD CODE ELIMINATION
pr = []
for i in range(n - 1):
    used = False
    target = ops[i].l
    for j in range(n):
        if target in ops[j].r:
            used = True
            break
    if used:
        pr.append(Operation(ops[i].l, ops[i].r))
pr.append(Operation(ops[n - 1].l, ops[n - 1].r))  # Last line always kept

print("\nAFTER DEAD CODE ELIMINATION")
for op in pr:
    print(f"{op.l} ={op.r}")

# COMMON SUBEXPRESSION ELIMINATION & SUBSTITUTION
for m in range(len(pr)):
    tem = pr[m].r
    for j in range(m + 1, len(pr)):
        if tem == pr[j].r:
            old = pr[j].l
            pr[j].l = pr[m].l
            for i in range(len(pr)):
                pos = pr[i].r.find(old)
                if pos != -1:
                    print(f"pos: {pos}")
                    # Replace at that position
                    pr[i].r = pr[i].r[:pos] + pr[m].l + pr[i].r[pos + 1:]

print("\nELIMINATE COMMON EXPRESSION")
for op in pr:
    print(f"{op.l} ={op.r}")

# OPTIMIZED CODE (remove duplicates by comparing l-value and r-value)
seen = set()
print("\nOPTIMIZED CODE")
for op in pr:
    key = (op.l, op.r)
    if key not in seen:
        seen.add(key)
        print(f"{op.l}={op.r}")

