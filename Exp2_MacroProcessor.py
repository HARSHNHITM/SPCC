mdt = ["L 1,&ARG1", "ST 2,&ARG2", "MEND"]
call = "MACRO CALL1 DATA1,DATA2"
args = call.split()[2].split(',')
for line in mdt:
    if line == "MEND": break
    temp = line.replace("&ARG1", args[0]).replace("&ARG2", args[1])
    print(temp)