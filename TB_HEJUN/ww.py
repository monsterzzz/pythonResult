x = 15
y = 15

for i in range(25):
    temp_pos = []
    for j in range(30):
        temp_pos.append([x,y])
        x += 15
    x = 15
    y += 15
    print(temp_pos)

