input_number=int(input("輸入金字塔層數="))
for i in range(0,input_number):
    space= " "*(input_number-i)
    star = "*"*(i*2-1)
    print(space+star)