 
def cheak_qipan(point,current_qipan):
    x,y = point[0],point[1]

    current_pos = [x,y]
    point_cout = 1
    while True:
        if [current_pos[0] - 40,current_pos[1]] in current_qipan:
            current_pos = [current_pos[0] - 40,current_pos[1]]
            point_cout += 1
        else:
            break
    current_pos = [x,y]
    while True:
        if [current_pos[0] + 40,current_pos[1]] in current_qipan:
            current_pos = [current_pos[0] + 40,current_pos[1]]
            point_cout += 1
        else:
            break
    if point_cout >= 5:
        return True
    
    
    current_pos = [x,y]
    point_cout = 1
    while True:
        if [current_pos[0],current_pos[1] - 40 ] in current_qipan:
            current_pos = [current_pos[0],current_pos[1]  - 40]
            point_cout += 1
        else:
            break
    current_pos = [x,y]
    while True:
        if [current_pos[0],current_pos[1] + 40 ] in current_qipan:
            current_pos = [current_pos[0] ,current_pos[1] + 40]
            point_cout += 1
        else:
            break
    if point_cout >= 5:
        return True
    

    x,y = point[0],point[1]
    current_pos = [x,y]
    point_cout = 1
    while True:
        if [current_pos[0] - 40 ,current_pos[1] - 40 ] in current_qipan:
            current_pos = [current_pos[0] - 40,current_pos[1]  - 40]
            point_cout += 1
        else:
            break
    current_pos = [x,y]
    while True:
        if [current_pos[0] + 40 ,current_pos[1] + 40 ] in current_qipan:
            current_pos = [current_pos[0] + 40,current_pos[1]  + 40]
            point_cout += 1
        else:
            break
    if point_cout >= 5:
        return True

    
    current_pos = [x,y]
    point_cout = 1
    while True:
        if [current_pos[0] - 40 ,current_pos[1] + 40 ] in current_qipan:
            current_pos = [current_pos[0] - 40,current_pos[1]  + 40]
            point_cout += 1
        else:
            break
    current_pos = [x,y]
    while True:
        if [current_pos[0] + 40 ,current_pos[1] - 40 ] in current_qipan:
            current_pos = [current_pos[0] + 40,current_pos[1]  - 40]
            point_cout += 1
        else:
            break
    if point_cout >= 5:
        return True

    return False

#a = [[265, 95], [225, 135], [305, 55], [225, 175], [305, 15], [185, 95], [185, 55], [225, 215], [185, 215], [265, 215], [265, 255]]

#a = [[305, 15], [345, 55], [385, 95], [425, 135],[465, 175]]

# a = [[40,15]]

a = [[225, 15], [225, 55], [225, 95], [225, 135], [225, 175]]

#a = [[305, 55], [305, 95], [305, 135], [305, 175], [25, 255], [105, 255], [105, 215], [105, 175], [105, 135]]
print(cheak_qipan(a[-1],a))