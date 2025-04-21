code = [("a", "b+c"), ("b", "d+e"), ("c", "a+1")]
used = {"a", "c"}
optimized = [stmt for stmt in code if stmt[0] in used]
print("Optimized Code:")
for var, exp in optimized:
    print(f"{var} = {exp}")