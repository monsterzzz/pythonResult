#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from copy import deepcopy
"""
Assignment 3: The Ship Rendezvous Problem

Your code should:

1. Read a problem instance (data) from a CSV file;
2. Run the greedy heuristic against the problem instance to obtain a solution.
3. Output the resulting path to a CSV file.
4. Output key performance indicators of the solution to a second CSV file.

See the assignment specification for details of the greedy heuristic,
calculation of key performance indicators and file formats for the CSVs.

Advice for completing the assignment:

1. Create and test alternative problem instances of the SRP.
2. Design your solution code carefully and write efficient, readable code.
3. Check that your code outputs files in the correct format.
4. Make regular backups of your code.
5. Before you submit your code - do one final test that it runs without error.

"""

import numpy as np

def main(csv_file):
    '''
    Main function for running and solving an instance of the SRP.

    Keyword arguments:
    csv_file -- the csv file name and path to a data for an instance of
                ship rendezvous problem.
    '''
    #read in the csv file to a numpy array
    problem_data = read_srp_input_data(csv_file)

    #These print statements can be deleted
    #They are just here to check what data has been loaded
    print(problem_data)
    print(problem_data.shape)
    #print(list(map(lambda x : list(x),problem_data)))

    solution = []
    error_ship = 0

    port_info = [problem_data[0][0],problem_data[0][1],0,0]

    sup_ship = list2dict(problem_data[0],0)
    start_idx = 0
    wait_solution = []
    for ship_info in problem_data[1:]:
        if can_visit(sup_ship['info'],ship_info):
            wait_solution.append(list2dict(ship_info,start_idx))
        else:
            #ship_info = [-1,-1,-1,-1]
            #error_ship.append(list2dict(ship_info,-1))
            print(ship_info)
            error_ship += 1
        start_idx += 1

    print(error_ship)
    
    number_ship_visited = 0
    total_time = 0
    max_wait_time = 0
    highest_y_pos = 0
    furthest_away = 0
    average_time = 0  
    
    #port_pos = [sup_ship['info'][0],sup_ship['info'][1]]

    dd = [[0, 1, 2, 3, 4], [0, 1, 2, 4, 3], [0, 1, 3, 2, 4], [0, 1, 3, 4, 2], [0, 1, 4, 2, 3], [0, 1, 4, 3, 2], [0, 2, 1, 3, 4], [0, 2, 1, 4, 3], [0, 2, 3, 1, 4], [0, 2, 3, 4, 1], [0, 2, 4, 1, 3], [0, 2, 4, 3, 1], [0,
3, 1, 2, 4], [0, 3, 1, 4, 2], [0, 3, 2, 1, 4], [0, 3, 2, 4, 1], [0, 3, 4, 1, 2], [0, 3, 4, 2, 1], [0, 4, 1, 2, 3], [0, 4, 1, 3, 2], [0, 4, 2, 1, 3], [0, 4, 2, 3, 1], [0, 4, 3, 1, 2], [0, 4, 3, 2, 1], [1, 0, 2, 3, 4], [1, 0, 2, 4, 3], [1, 0, 3, 2, 4], [1, 0, 3, 4, 2], [1, 0, 4, 2, 3], [1, 0, 4, 3, 2], [1, 2, 0, 3, 4], [1, 2, 0, 4, 3], [1, 2, 3, 0, 4], [1, 2, 3, 4, 0], [1, 2, 4, 0, 3], [1, 2, 4, 3, 0], [1, 3, 0, 2, 4], [1, 3, 0, 4, 2], [1, 3, 2, 0, 4], [1, 3, 2, 4, 0], [1, 3, 4, 0, 2], [1, 3, 4, 2, 0], [1, 4, 0, 2, 3], [1, 4, 0, 3, 2], [1, 4, 2, 0, 3], [1, 4, 2, 3, 0], [1, 4, 3, 0, 2], [1, 4, 3, 2, 0], [2, 0, 1, 3, 4], [2, 0, 1, 4, 3], [2, 0, 3, 1, 4], [2, 0, 3, 4, 1], [2, 0, 4, 1, 3], [2, 0, 4, 3, 1], [2, 1, 0, 3, 4], [2, 1, 0, 4, 3], [2, 1, 3, 0, 4], [2, 1, 3, 4, 0], [2, 1, 4, 0, 3], [2, 1, 4, 3, 0], [2, 3, 0, 1, 4], [2, 3,
0, 4, 1], [2, 3, 1, 0, 4], [2, 3, 1, 4, 0], [2, 3, 4, 0, 1], [2, 3, 4, 1, 0], [2, 4, 0, 1, 3], [2, 4, 0, 3, 1], [2, 4, 1, 0, 3], [2, 4, 1, 3, 0], [2, 4, 3, 0, 1], [2, 4, 3, 1, 0], [3, 0, 1, 2, 4], [3, 0, 1, 4, 2], [3, 0, 2, 1, 4], [3, 0, 2, 4, 1], [3, 0, 4, 1, 2], [3, 0, 4, 2, 1], [3, 1, 0, 2, 4], [3, 1, 0, 4, 2], [3, 1, 2, 0, 4], [3, 1, 2, 4, 0], [3, 1, 4, 0, 2], [3, 1, 4, 2, 0], [3, 2, 0, 1, 4], [3, 2, 0, 4, 1],
[3, 2, 1, 0, 4], [3, 2, 1, 4, 0], [3, 2, 4, 0, 1], [3, 2, 4, 1, 0], [3, 4, 0, 1, 2], [3, 4, 0, 2, 1], [3, 4, 1, 0, 2], [3, 4, 1, 2, 0], [3, 4, 2, 0, 1], [3, 4, 2, 1, 0], [4, 0, 1, 2, 3], [4, 0, 1, 3, 2], [4, 0, 2, 1, 3], [4, 0, 2, 3, 1], [4, 0, 3, 1, 2], [4, 0, 3, 2, 1], [4, 1, 0, 2, 3], [4, 1, 0, 3, 2], [4, 1, 2, 0, 3], [4, 1, 2, 3, 0], [4, 1, 3, 0, 2], [4, 1, 3, 2, 0], [4, 2, 0, 1, 3], [4, 2, 0, 3, 1], [4, 2, 1,
0, 3], [4, 2, 1, 3, 0], [4, 2, 3, 0, 1], [4, 2, 3, 1, 0], [4, 3, 0, 1, 2], [4, 3, 0, 2, 1], [4, 3, 1, 0, 2], [4, 3, 1, 2, 0], [4, 3, 2, 0, 1], [4, 3, 2, 1, 0]]

    t_list = []
    show_list = []
    for i in dd:
        pp = deepcopy(wait_solution)
        ss = deepcopy(sup_ship)
        result_l = calc_list_t(i,ss,pp)
        show_list.append(result_l)
        t_list.append(sum(result_l))
       
      
    print(t_list.index(min(t_list)))
    print(t_list[t_list.index(min(t_list))])
    print(dd[t_list.index(min(t_list))])
    print(show_list[t_list.index(min(t_list))])


    for i in range(len(dd)):
        print("{}   {}  : {}   {}" .format(i,dd[i],show_list[i],t_list[i]))
    
    # result = []
    # for i in dd:
    #     tmp_result = []
    #     tmp_sup = sup_ship['info'].copy()
    #     tmp_wait = wait_solution.copy()
    #     print(i)
    #     print(sup_ship)
    #     print(tmp_sup)
    #     for j in i:
    #         print("***********")
    #         print("sup",tmp_sup)
    #         t = cala_visit_time(tmp_sup,tmp_wait[j]['info'])
    #         print("current_ship",update_pos(tmp_wait[j]['info'],t)[:2])
    #         tmp_sup[:2] = update_pos(tmp_wait[j]['info'],t)[:2]
    #         for k in tmp_wait:
    #             k['info'] = update_pos(k['info'],t)
    #         tmp_result.append(t)
    #     result.append(tmp_result)
    # print(result)
        #tmp_result.append()

        # for ship in i:
        #     tmp_result.append(cala_visit_time(sup_ship['info'],wait_solution[i]['info']))
        # result.append(tmp_result)


    # =========================================================================
    # To do:
    # 1. pre-process input_data into variables usable by your algorithm.
    # 2. Run the greedy algorithm provided in the assignment document.
    # 3. Write the solution to a CSV file "solution.csv".
    # 4. Write the KPIs to a CSV file "kpi.csv".
    # =========================================================================

def calc_list_t(list_idx,sup_ship,wait_solution):

    result = []
    print(wait_solution)
    for j in list_idx:
        print(j)
        t = cala_visit_time(sup_ship['info'],wait_solution[j]['info'])
        sup_ship['info'][:2] = update_pos(wait_solution[j]['info'],t)[:2]
        for k in wait_solution:
            k['info'] = update_pos(k['info'],t)
        result.append(t)
    return result

def get_distance(port,ship_info):
    """
    获得两点之间的距离
    参数：
    port : 列表 [港口的x坐标,港口y坐标]
    ship_info： 列表 [船的 x坐标,船的y坐标]
    返回值:
    distance : 两点间距离，保留两位小数
    """
    port_x,port_y = port
    ship_x,ship_y = ship_info
    distance = np.sqrt(((port_x - ship_x)**2) + ((port_y - ship_y)**2))
    return round(distance,2)
   
import matplotlib.pyplot as plt
from numpy import *

def pplot(start_point,org_point,solution_point,ship_path):
    """
    画图函数
    将寻路结果可视化
    参数
    start_point ： 列表 [港口的x坐标,港口y坐标]
    org_point ： 所有游轮的原始坐标  来自读取csv的 numpy array 
    solution_point : 解决方案的点，就是最后所有船相遇的点
    ship_path : 船的索引
    返回值:
    无返回值 ： 会保存一个解决方案可视化的图片
    """
    start_x,start_y = start_point
    #plt.plot(org_point[:,0],org_point[:,1],"ro") # 原始坐标 红点
    plt.plot(start_x,start_y,"bo")  # 起始坐标 蓝点
    plt.annotate('',xy=(solution_point[0][0],solution_point[0][1]),xytext=(start_x,start_y),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
    for i in range(len(solution_point)):
        plt.plot(solution_point[i][0],solution_point[i][1],"go") # 拦截坐标 绿点
        # 起始点指向解决路径
        try:
            plt.annotate('',xy=(solution_point[i+1][0],solution_point[i+1][1]),xytext=(solution_point[i][0],solution_point[i][1]),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
        except IndexError:
            break
            
    plt.annotate('',xy=(start_x,start_y),xytext=(solution_point[-1][0],solution_point[-1][1]),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
    
    # # 游轮原来的位置指向被拦截的位置
    # for i in ship_path:
    #     print(i,solution_point[i],org_point[i+1])
    #     plt.annotate('',xy=(solution_point[i][0],solution_point[i][1]),xytext=(org_point[i][0],org_point[i][1]),arrowprops=dict(arrowstyle="->",connectionstyle="arc3"))
    # plt.plot(solution_point[-1][0],solution_point[-1][1],"yo")

    #plt.show()
    plt.savefig("solution.jpg")

def write_solution_to_csv(solution,error_ship):
    """
    解决方案写入csv文件中
    参数
    solution : 解决方案 一个列表 列表中保存着字典 字典信息为 船的坐标 索引 以及拦截时间
    err_ship ：整数 ，表示不能够到达的船的数量
    返回值：
    无返回值 ： 会生成一个csv文件，保存需要的信息
    """
    csv_header = ["Ship_index","interception_x_coordinate","interception_y_coordinate","estimated_time_of_interception"]
    csv_body = []
    err_info = "\n-1,-1,-1,-1"
    for ship in solution:
        temp_row = [str(ship['idx']),str(ship['x_pos']),str(ship['y_pos']),str(ship['time'])]
        csv_body.append(",".join(temp_row))
    with open("solution.csv","w+",encoding="utf-8") as f:
        f.write(",".join(csv_header) + "\n")
        f.write("\n".join(csv_body))
        for i in range(error_ship):
            f.write(err_info)

def write_kpi_file(n_ships, total_time, max_wait, max_y, furthest_distance,avg_time):
    """
    kpi写入csv文件
    参数：
    和下面的print_kpi参数含义相同
    返回值：
    无返回值 ： 会生成一个csv文件，保存kpi信息
    """
    arg = list(map(lambda x : str(x),[n_ships, total_time, max_wait, max_y, furthest_distance,avg_time]))
    string = "\n".join(arg)
    with open("kpi.csv","w+",encoding="utf-8") as f:
        f.write(string)


def list2dict(ship_info,idx):
    """
    把numpy array转换为 python字典，用于保存船的索引
    参数:
    ship_info : numpy array  船的坐标以及速度 来自numpy读取csv文件
    idx ： 船的索引
    返回值：
    ship ： 字典 保存索引以及坐标速度的信息
    """
    ship = {
        "idx" : idx,
        "info" : ship_info
    }
    return ship

def cala_speed(x_speed,y_speed):
    """
    计算船的速度
    参数
    x_speed: x轴的速度
    y_speed : y轴的速度
    返回值:
    速度
    """
    return np.sqrt((x_speed**2 + y_speed**2))

def can_visit(sup_ship,visit_ship):
    """
    判断能否到达目标船，通过速度判断
    参数：
    sup_ship : 列表  支援船的信息  [x_pos,y_pos,x_speed,y_speed]
    visit_ship : 列表 游轮 的信息  [x_pos,y_pos,x_speed,y_speed]
    返回值:
    boolen  是否能够到达
    """
    sup_ship_speed = cala_speed(sup_ship[2],sup_ship[3])
    visit_ship_speed = cala_speed(visit_ship[2],visit_ship[3])
    #print(sup_ship_speed,visit_ship_speed,sup_ship_speed >= visit_ship_speed)
    return sup_ship_speed >= visit_ship_speed
   
def cala_visit_time(ship1_info,ship2_info):
    """
    计算拦截时间
    参数:
    ship1_info : 列表 支援船的坐标以及速度 
    ship2_info : 列表 船的坐标以及速度
    返回值
    t  : 拦截时间 保留两位小数
    """
    # ax^2+bx+c = 0 
    # x = [-b±√(b2-4ac)]/(2a)
    # a(T**2) + bT + c = 0
    a = (ship2_info[2] ** 2)  + (ship2_info[3] ** 2)  - (cala_speed(ship1_info[2],ship1_info[3]) ** 2)
    b = 2 * ((ship2_info[2]*(ship2_info[0] - ship1_info[0])) + (ship2_info[3] * (ship2_info[1] - ship1_info[1])))
    c = ((ship2_info[0] - ship1_info[0]) ** 2)  + ((ship2_info[1] - ship1_info[1]) ** 2)
    T1 = ((-1 * b) + (np.sqrt((b ** 2) - (4 * a * c)))) / (2 * a)
    T2 = ((-1 * b) - (np.sqrt((b ** 2) - (4 * a * c)))) / (2 * a)
    flag = False
    t = 0
    for i in [T1,T2]:
        if i >= 0 :
            if t == 0:
                t = i
            elif t != 0 and i < t:
                t = i
            flag = True
        else:
            flag = False
    if not flag:
        raise Exception("error result of cala_visit_time")
  
    return round(t,2)      

        
def update_pos(ship_info,t):
    """
    更新船的位置信息
    参数:
    ship_info : 船的坐标以及速度 列表
    t : 拦截时间
    """
    x_pos,y_pos,x_speed,y_speed = ship_info
    new_x_pos = round(x_pos + x_speed * t,2)
    new_y_pos = round(y_pos + y_speed * t,2)
    new_ship_info = [new_x_pos,new_y_pos,x_speed,y_speed]
    return np.array(new_ship_info)



def read_srp_input_data(csv_file):
    '''
    Problem instances for the SRP are stored within a .csv file
    This function reads the problem instance into Python.
    Returns a 2D np.ndarray (4 columns).
    Skips the headers and the first column.
    Columns are:
    x-coordinate, y-coordinate, x-speed and y-speed

    Keyword arguments:
    csv_file -- the file path and name to the problem instance file
    '''

    input_data = np.genfromtxt(csv_file, delimiter=',',
                               dtype=np.float64,
                               skip_header=1,
                               usecols=tuple(range(1, 5)))

    return input_data



def print_kpis(n_ships, total_time, max_wait, max_y, furthest_distance,
               avg_time):
    '''
    An OPTIONAL utility function to print the key performance measures
    of the SRP optimisation to the Python console.

    This function is designed to help with debugging the algorithm.
    It is NOT mandatory to use it. It can be removed from your code
    if it is not required.

    Keyword arguments:
    n_ships -- the number of ships
    total_time -- total time for the support ship to complete its tour
    max_wait -- the max time a ship waited for the support ship to rendezvous
    max_y -- the maximum y coordinate to which the support ship travelled
    furthest_distance -- the max distance travelled to rendezvous
    avg_time -- The average time to visit each ship

    '''
    #pylint: disable-msg=too-many-arguments
    print('\n === Key Performance Indicators ===')
    print('Ships visited    :\t{0}'.format(n_ships))
    print('Total time       :\t{0}'.format(total_time))
    print('Max. waiting time:\t{0}'.format(max_wait))
    print('Furthest Y coord.:\t{0}'.format(max_y))
    print('Furthest distance:\t{0}'.format(furthest_distance))
    print('Avg. waiting time:\t{0}'.format(avg_time))
    print('\n')


if __name__ == '__main__':
    # =========================================================================
    # you can change the name of the input file
    # to test different problem instances.
    # Please DOT NOT delete the 'if __name__ == '__main__':
    # =========================================================================
    PROBLEM_FILE = 'sample_srp_data.1.csv'
    main(PROBLEM_FILE)
