def fun(n):
    str_n = str(n)
    int_list = []
    decimal = 2
    for i in str_n:
        if i not in "0123456789":
            decimal = 16
            break

        i = int(i)
        if i > 1 and i < 8:
            decimal = 8
        elif i >= 8:
            decimal = 16
            break

    for i in range(len(str_n)):
        if str_n[i] not in "0123456789":
            int_num = "abcdef".index(str_n[i]) + 10 
        else:
            int_num = int(str_n[i])
        current_num = int_num *  ( decimal ** (len(str_n) - i - 1))
        int_list.append(current_num)
    return sum(int_list)

def fun1(n):
    
    while True:
        str_n = str(n)
        current_num_list = []
        show_str = "{} 平方和: ".format(n)
        for i in str_n:
            current_pow = int(i) ** 2
            show_str += str(current_pow) + "+"
            current_num_list.append(current_pow)
        pow_sum = sum(current_num_list)
        if len(str_n) > 1:
            show_str = show_str[:-1] + "=" + str(pow_sum)
        else:
            show_str = show_str[:-1]
        print(show_str)
        if pow_sum == 1 or pow_sum == 145:
            return pow_sum
        n = pow_sum
    
print(fun("f2"))


