import re
def analysis(expression):
    num=re.split('[*/+-]',expression)
    symbol=re.findall('[*/+-]',expression)
    # print(num, symbol)
    return judge_sign(num, symbol)

def judge_sign(num_list, symbol_list):
    if '' in num_list:
        temp = []
        for i,j in enumerate(symbol_list):
            if num_list[i]:
                # print(i)
                temp.append(float(num_list[i]))
                temp.append(j)
            else:
                num_list[i]=(-float(num_list[i+1]))
                num_list.pop(i+1)
                symbol_list.pop(i)
                return judge_sign(num_list,symbol_list)
    else:
        temp=[]
        for i,j in enumerate(symbol_list):
            temp.append(num_list[i])
            temp.append(j)
        temp.append(num_list[-1])
        return multiply_divide(temp)

    # multiply_divide(temp)
def multiply_divide(ex_list):
    temp=ex_list.copy()
    if '*' in temp or '/'in temp:
        for i,j in enumerate(temp):
            if j=="*":
                temp[i-1]=float(ex_list[i-1])*float(ex_list[i+1])
                temp.pop(i)
                temp.pop(i)
                return multiply_divide(temp)
            elif j=="/":
                temp[i-1]=float(temp[i-1])/float(temp[i-1])
                temp.pop(i)
                temp.pop(i)
                return multiply_divide(temp)
    else:
        # print(temp)
        return add_subtract(temp)
def add_subtract(ex_list):
    temp = ex_list.copy()
    # print(temp)
    if '+' in temp or '-' in temp:
        for i, j in enumerate(temp):
            if j == "+":
                temp[i - 1] = float(ex_list[i - 1])+float(ex_list[i + 1])
                temp.pop(i)
                temp.pop(i)
                return add_subtract(temp)
            elif j == "-":
                temp[i - 1] = float(temp[i - 1] )- float(temp[i - 1])
                temp.pop(i)
                temp.pop(i)
                return add_subtract(temp)
    print(temp[0],'================')

# num=re.split('[*/+-]','-2+2+3--4')
# # symbol=re.findall('[*/+-]','-2+2+3--4')
# print(num)
# print(symbol)
a=-2+-2*-3--4/5---6*--6
analysis(str(a))
print(a)
# a=[1,2,3]
# a.pop(0,1)