num1 = 4
num2 = 7

if num1 < num2:
    greaternum = num2
    lessnum = num1
else:
    greaternum = num1
    lessnum = num2

for i  in range(lessnum, greaternum):
    print("checked " + str(i))