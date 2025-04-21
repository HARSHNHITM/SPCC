symbols = []
while True:
    ch = input("1.Insert 2.Display 3.Exit: ")
    if ch == "1":
        name = input("Name: ")
        addr = input("Address: ")
        symbols.append({"name": name, "addr": addr})
    elif ch == "2":
        for s in symbols:
            print(f"{s['name']} -> {s['addr']}")
    else:
        break