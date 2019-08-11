import re
def analysis(expression):
    num=re.split('[*/+-]',expression)
    symbol=re.findall('[*/+-]',expression)
    return judge_sign(num, symbol)

def judge_sign(num_list, symbol_list):
    if '' in num_list:
        temp = []
        for i,j in enumerate(symbol_list):
            if num_list[i]:
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

def rm_brackt(expression):
    if '(' in expression:
        brackt_left=re.search('\(',expression).span()
        brackt_right = re.search('\)', expression).span()
        if '\(' in expression[brackt_left[0]:brackt_right[1]]:
            rm_brackt(expression[brackt_left[1]:brackt_right[1]])
        else:
            reslut=analysis(expression[brackt_left[1]:brackt_right[0]])
            new_expression=expression[:brackt_left[0]]+str(reslut)+expression[brackt_right[1]:]
            return rm_brackt(new_expression)
    else:
        return analysis(expression)
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
                temp[i-1]=float(temp[i-1])/float(temp[i+1])
                temp.pop(i)
                temp.pop(i)
                return multiply_divide(temp)
    else:
        return add_subtract(temp)
def add_subtract(ex_list):
    temp = ex_list.copy()
    if '+' in temp or '-' in temp:
        for i, j in enumerate(temp):
            if j == "+":
                temp[i - 1] = float(ex_list[i - 1])+float(ex_list[i + 1])
                temp.pop(i)
                temp.pop(i)
                return add_subtract(temp)
            elif j == "-":
                temp[i - 1] = float(temp[i - 1] )- float(temp[i+1])
                temp.pop(i)
                temp.pop(i)
                return add_subtract(temp)
    else:
        return temp[0]


if __name__=='__main__':
    expression='12+12*5+(-5*2)/((3+7)*0.5)'
    print(rm_brackt(expression))
    print(12+12*5+(-5*2)/(3+7))