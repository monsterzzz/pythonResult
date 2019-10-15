
import pygame
from pygame.locals import *
import sys
import random

# 游戏类
class CORLOR:
    def __init__(self):
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)


# 玩家类
class People(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Call the parent class (Sprite) constructor
        self.image = Point((0,0),(12,12),[1,1,23,23])
        self.rect= self.image.rect #position
        self.rect.top=0
        self.rect.left=0
        self.corlor = Color(0,0,0)
        self.pid = [0,0]
    
    # 移动
    def move_left(self):
        if self.rect.left > 0:
            self.pid[0] -= 1
            self.rect.left -= 24
    
    def move_up(self):
        if self.rect.top > 0:
            self.pid[1] -= 1
            self.rect.top -= 24
    
    def move_down(self):
        if self.rect.top != 552 + 24:
            self.pid[1] += 1
            self.rect.top += 24
    
    def move_right(self):
        if self.rect.left != 720-24:
            self.pid[0] += 1
            self.rect.left += 24

    # 重启
    def restart(self):
        self.pid = [0,0]
        self.rect.top = 0
        self.rect.left = 0

# 点 类
class Point:
    def __init__(self,pid,pos,rect):
        self.pid = pid
        self.pos = pos
        self.rect = Rect(rect)
        self.state = 0

# 生命游戏类
class Life_game:
    def __init__(self):
        self.point = self.map_maker()  # 生成游戏虚拟地图
        self.life_time = 3    # 生命游戏周期
    
    # 获得周围点的状态
    def get_around_point_state(self,current_point):
        x_index = current_point[0]
        y_index = current_point[1]
        # 获得点
        top_side_point_1 = self.get_point([x_index - 1 ,y_index - 1]) # 上左
        top_side_point_2 = self.get_point([x_index     ,y_index - 1]) # 上
        top_side_point_3 = self.get_point([x_index + 1 ,y_index - 1]) # 上右
        left_side_point  = self.get_point([x_index - 1 ,y_index    ]) # 左
        right_side_point = self.get_point([x_index + 1 ,y_index    ]) # 右
        bottom_side_point_1 = self.get_point([x_index - 1 ,y_index + 1]) # 下左
        bottom_side_point_2 = self.get_point([x_index     ,y_index + 1]) # 下
        bottom_side_point_3 = self.get_point([x_index + 1 ,y_index + 1]) # 下右
        # 判断点的状态
        alive_count = 0
        for point in [top_side_point_1,top_side_point_2,top_side_point_3,left_side_point,right_side_point,bottom_side_point_1,bottom_side_point_2,bottom_side_point_3]:
            if point:
                if point.state == 1:
                    alive_count += 1
        return alive_count

    # 生成地图 地图由一个一个点组合而成 点有自己的矩形范围 以及索引 例如 [0,0] [0,1] 
    def map_maker(self):
        pos = []
        x = 12
        y = 12
        rect_x = 0
        rect_y = 0
        for i in range(30):
            temp_pos = []
            for j in range(25):
                temp_pos.append(Point([i,j],[x,y],[rect_x + 1,rect_y + 1,23,23]))
                rect_y += 24
                x += 12
            x = 12
            rect_y = 0
            y += 12
            rect_x += 24
            pos.append(temp_pos)
        return pos

    # 设置随机点
    def random_point(self,current_pos,number = 5): 
        new_x_list = []
        for i in range(30):
            if i != current_pos[0] and i != 29:
                new_x_list.append(i)
        new_y_list = []
        for i in range(25):
            if i != current_pos[1] and i != 24:
                new_y_list.append(i)
        
        # 设置几个点 如果该点已经有个点的话，换另外的点
        count = 0
        while count < number:
            while True:
                x = random.choice(new_x_list)
                y = random.choice(new_y_list)
                if self.point[x][y].state == 1:
                    pass
                else:
                    self.point[x][y].state = 1
                    count += 1
                    break
    
    # 获得点
    def get_point(self,index_list):
        # 如果超出列表索引 说明超出地图外了 返回个None
        try:
            if -1 in index_list:
                return None
            return self.point[index_list[0]][index_list[1]]
        except BaseException as e:
            return None
    # 更新点的状态为 1 存活状态
    def update_point(self,index_list):
        if self.point[index_list[0]][index_list[1]].state == 1:
            print("current point has been alive")
        else:
            self.point[index_list[0]][index_list[1]].state = 1
    # 进行一个生命游戏的迭代
    def life_loop(self):
        should_change_point = self.get_need_change_point()
        self.set_change_point(should_change_point)
    # 获得需要改变的点
    def get_need_change_point(self):
        should_change_point = []
        for line in self.point:
            for point in line:
                around_alive = self.get_around_point_state(point.pid)
                if around_alive == 3:
                    should_change_point.append((point,3,point.state))
                elif around_alive == 2:
                    pass
                else:
                    should_change_point.append((point,0))
        return should_change_point
    # 设置需要改变的点的状态
    def set_change_point(self,point_list):
        should_change_point = point_list
        for point in should_change_point:
            if point[1] == 3:
                point[0].state = 1
            else:
                if point[1] == 0:        
                    point[0].state = 0

    # 重启
    def restart(self):
        for line in self.point:
            for point in line:
                point.state = 0

# 返回需要的点击坐标
# 把坐标变成 索引的格式 这样就可以得到是那个矩形范围被点击了
def click_point_change(pos):
    right_x_index = 0
    right_y_index = 0
    if pos[0] <= 24:
        right_x_index = 0
    else:
        right_x_index = (pos[0] // 24)
    if pos[1] <= 24:
        right_y_index = 0
    else:
        right_y_index = (pos[1] // 24)
    return [right_x_index,right_y_index]
    
# 游戏是否结束
def is_over(point):
    if point.pid == [29,24]:
        return True
    else:
        return False

width = 720   # 游戏窗口 宽度
height = 600  # 游戏窗口 高度
size = width, height
pygame.init() # 初始化pygame
screen = pygame.display.set_mode(size) 
game_corlor = CORLOR() 
life_game = Life_game() 
clock = pygame.time.Clock()
people = People()
life_time = 0
should_change_point = []
key_press_time = 0
bling_time = 0
bling_show = True
should_change_point = life_game.get_need_change_point()


## 难度定义项

random_point_num = 10    # 惩罚，如果玩家未移动的时间大于两倍生命游戏迭代的时间，那么就生成这个数量的点。防止玩家光靠等待生命游戏趋于稳定之后再移动
life_game.life_time = life_game.life_time   # 生命游戏迭代的速度
setp_random_point = 5     # 每移动一次就生成这个数量的点


def hit_cheak(point):   # 碰撞检测  没写得很复杂 因为都是点的重叠 没有点外部到内部这一个过程
    if life_game.get_point(point.pid).state == 1:  # 判断玩家移动到的当前点的状态是否有存活的点
        return True    # 如果有 说明游戏失败
    else:
        return False

def set_init_random():    # 设置地图初始的随机点 不包含在 初始点，结束点 3*3 范围内
    start_around = []
    for i in range(3):
        for j in range(3):
            start_around.append([i,j])
    end_around = []
    for i in range(3):
        for j in range(3):
            end_around.append([29 - i, 24 -j]) 
    for i in life_game.point:
        for point in i:
            if random.randint(1,3) == 1 and point.pid not in (start_around + end_around):
                point.state = 1



# 光标类
class Curor:
    def __init__(self):
        self.rect = Rect(110,110,20,20)  # 光标位置
        self.current_choose = 0   # 当前选择
        self.is_run = False   # 是否是开始  如果是开始 就应该是 4个选项  如果不是就应该是 5个选型

    def move_up(self):  # 向上移动
        if self.current_choose - 1 == -1:
            self.current_choose = 2
            self.rect.top = 210
        else:
            self.current_choose -= 1
            self.rect.top -= 50
    
    def move_down(self): # 向下移动
        if self.is_run:
            select_num = 5
        else:
            select_num = 4
        if self.current_choose + 1 == select_num:
            self.current_choose = 0
            self.rect.top = 110
        else:
            self.current_choose += 1
            self.rect.top += 50

top_title = "start"   # 标题

run = False  # 游戏运行标志符
curor = Curor() # 实例化光标

while True:
    for event in pygame.event.get():   # 事件获取
        # 查找关闭窗口事件
        if event.type == QUIT: # 退出事件
            sys.exit()
        if run == False:  # 如果游戏没有运行 
            if event.type == 2:   # 获取 上下键按下的事件
                if event.key == 273:  # 上
                    curor.move_up()
                if event.key == 274: # 下
                    curor.move_down()
                if event.key == 13: # 回车
                    
                    choose = curor.current_choose  # 获取当前的选择
                    if choose == 3:  # 第四个选型有可能是 quit 或者 continue 判断是quit
                        if top_title == "stop":   # 如果标题是 stop,并且是第4个选项 ,是continue
                            run = True          
                            curor.current_choose = 0
                            curor.rect.top = 110
                        else:  # 不是stop 的话 就是 quit
                            sys.exit()
                    else:  
                        if choose == 0: # easy mode
                            random_point_num = 15
                            life_game.life_time = 2
                            setp_random_point = 8
                        elif choose == 1: # mid mode
                            random_point_num = 20
                            life_game.life_time = 1
                            setp_random_point = 10
                        elif choose == 2: # hard mode
                            random_point_num = 40
                            life_game.life_time = 0.4
                            setp_random_point = 20
                        elif choose == 4: # quit
                            sys.exit()
                        life_game.restart() # 重新开始游戏
                        people.restart() # 玩家初始化
                        set_init_random() # 设置随机点
                        curor.current_choose = 0  # 光标初始化
                        curor.rect.top = 110
                        run = True # 游戏开始
                        
        else:
            if event.type == 2:
                if event.key == 32:
                    life_game.life_loop() # 按下空格键也可以进行一次生命游戏的迭代
                if event.key == 273:  # 移动 上
                    key_press_time = 0     # 设置按键时间 用来这次按下到下次按下的时间，用来惩罚
                    life_game.random_point(people.pid,setp_random_point) # 移动的随机点
                    people.move_up() # 向上移动
                if event.key == 274: # 下
                    key_press_time = 0
                    life_game.random_point(people.pid,setp_random_point)
                    people.move_down()
                if event.key == 276: # 左
                    key_press_time = 0
                    life_game.random_point(people.pid,setp_random_point)
                    people.move_left()
                if event.key == 275: # 右
                    key_press_time = 0
                    life_game.random_point(people.pid,setp_random_point)
                    people.move_right()
                if event.key == 27:  # esc键 暂停游戏
                    run = False
                    top_title = "stop"
    
    display_window = pygame.Surface((400,400))   # 菜单界面
    display_window.fill((0,0,0))
    font1 = pygame.font.SysFont('Time', 30)
    font2 = pygame.font.SysFont('Time', 25)
    title_ = font1.render(top_title,True,(255,255,255))
    easy_ = font2.render("easy mode",True,(255,255,255))
    mid_ = font2.render("mid mode",True,(255,255,255))
    hard_ = font2.render("hard mode",True,(255,255,255))
    continue_ = font2.render("continue",True,(255,255,255))
    quit_ = font2.render("QUIT",True,(255,255,255))
    display_window.blit(title_,(170,40))
    display_window.blit(easy_,(150,110))
    display_window.blit(mid_,(150,160))
    display_window.blit(hard_,(150,210))
    if top_title == "stop":       # 菜单界面逻辑  判断应该显示几个选项
        display_window.blit(continue_,(150,260))
        display_window.blit(quit_,(150,310))
    else:
        display_window.blit(quit_,(150,260))
    screen.fill(game_corlor.WHITE)
    pygame.draw.rect(display_window,(255,255,0),curor.rect)   # 画光标

    # 画线框
    y = 0  
    for i in range(25):
        pygame.draw.line(screen,game_corlor.BLUE , (0, y), (720, y), 1)
        y += 24
    x = 0
    for i in range(30):
        pygame.draw.line(screen,game_corlor.BLUE , (x, 0), (x,600), 1)
        x += 24

    # 画存活点
    for line in life_game.point:
        for point in line:
            if point.state == 1:
                pygame.draw.rect(screen,game_corlor.RED,point.rect)

    # 如果游戏开始了 就开始游戏逻辑
    if run == True:
        time_passed = clock.tick()    # 时钟
        time_passed_second = time_passed / 1000  # 毫秒
        key_press_time += time_passed_second # 按键时间
        bling_time += time_passed_second  # 提示点闪烁时间
        life_time += time_passed_second # 生命游戏更新一代


        if life_time >= life_game.life_time:    # 达到生命游戏该更新的时间了
            life_game.life_loop()   # 更新
            bling_show = True    # 开始闪烁点
            should_change_point = life_game.get_need_change_point() # 获得该闪烁的点
            life_time = 0 # 重置
        
        # 画闪烁点
        for point in should_change_point:
            if point[1] == 3 and point[2] == 0:
                if bling_time < life_game.life_time / 2 and bling_show:
                    #s = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                    pygame.draw.rect(screen,game_corlor.BLUE,point[0].rect)
                else:
                    bling_time = 0
                    bling_show = False
        # 判断按键时间是否大于 两倍生命游戏周期
        if key_press_time >= life_game.life_time * 2:
            life_game.random_point(people.pid,random_point_num)
            key_press_time = 0

        # 画 玩家 位置
        pygame.draw.rect(screen,people.corlor,people.rect)

        # 是否碰撞
        if hit_cheak(people):
            run = False
            top_title = "you fail!"

        # 是否达到了游戏结束
        if is_over(people):
            run = False
            top_title = "you win!"
    # 如果游戏没有运行 就显示菜单栏    
    if run == False:
        if top_title == "stop":
            curor.is_run = True
        else:
            curor.is_run = False
        screen.blit(display_window,(160,100))
    # 界面更新
    pygame.display.flip()
