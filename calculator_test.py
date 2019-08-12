import re
def test_validity(expression):
    '''初步检测计算式的正确性'''
    warning_text='输入的算术表达式有误:'
    if re.search('[a-zA-z()=@#!$%~^&]',expression):
        warning_text1='计算式中存在字母或存在不支持的运算符'
        print(warning_text+warning_text1)
    else:
        if len(re.findall('[(]',expression))!=len(re.findall('[)]',expression)):
            warning_text2='计算式中的()没有成对，无法计算'
            print(warning_text + warning_text2)
        else:
            return rm_brackt(expression)
def rm_brackt(expression):
    '''判断计算式是否存在()，若存在作去除()处理，若不存在进行下一步计算'''
    if '(' in expression and ')' in expression:#计算式中存在()
        brackt_right = re.search('\)', expression).span()[1]#第一个右括号位置
        temp=expression[:brackt_right]
        brackt_left = brackt_right-re.search('\(', temp[::-1]).span()[1]#与第一个右括号配对的左括号位置
        result=analysis(expression[brackt_left+1:brackt_right-1])#括号内层计算式传入analysis()得到其计算后的值
        new_expression=expression[:brackt_left]+str(result)+expression[brackt_right:]#构建新的计算式
        return rm_brackt(new_expression)#重新判断计算式是否存在（）
    else:#计算式中不存在()
        return analysis(expression)
def analysis(expression):
    '''拆分无括号计算式'''
    num=re.split('[*/+-]',expression)#所有数字列表
    symbol=re.findall('[*/+-]',expression)#所有符号列表，弱存在负数以‘’表示
    return judge_sign(num, symbol)
def judge_sign(num_list, symbol_list):
    '''判断负号是否存在，若存在做负数处理，若不存在进行下一步计算'''
    if '' in num_list:#存在负数
        temp = []
        for i,j in enumerate(symbol_list):
            if num_list[i]:
                temp.append(float(num_list[i]))
                temp.append(j)
            else:#定位第一个负号所在位置，并作负数处理,生成新的计算式
                num_list[i]=(-float(num_list[i+1]))
                num_list.pop(i+1)
                symbol_list.pop(i)
                return judge_sign(num_list,symbol_list)#重新判断负号是否存在
    else:#不含负号
        temp=[]
        for i,j in enumerate(symbol_list):#将数字和符号按顺序组成一个列表
            temp.append(num_list[i])
            temp.append(j)
        temp.append(num_list[-1])
        return multiply_divide(temp)
def multiply_divide(ex_list):
    '''判断列表中是否存在 "*"  "/",若存在作乘除处理，若不存在进行下一步计算'''
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
    '''判断列表中是否存在 "+"  "-",若存在作加减处理，若不存在返回其值'''
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
    try:
        expression=input('请输入正确的算术表达式：')
        result=test_validity(expression)
        print(expression+'=',result)
    except:
        print("出错啦,请仔细核对计算式是否有误")