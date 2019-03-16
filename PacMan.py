#import basic pygame modules
import pygame
from pygame.locals import *
import MaColor
import os.path
import numpy
import threading
import time

global SCREEN
global CLOCKTICKFLAG
CLOCKTICKFLAG = False
global IMAGECHANGEFLAG
IMAGECHANGEFLAG = False
global EXITFLAG
EXITFLAG = False
global CLOCKTHREAD,IMAGETHREAD
global FONT
global CLOCK
global Role1
global DIR
global SCREEN_WIDTH
global SCREEN_HEIGHT
class MaGame():
    def __init__(self,SIZE_X = 800,SIZE_Y = 600,_color = (255,255,255)):
        global SCREEN,FONT
        pygame.init()
        SCREEN = pygame.display.set_mode((SIZE_X,SIZE_Y))
        SCREEN.fill(_color)
        pygame.display.update()
        FONT = pygame.font.Font(None,40)
        self.Height = SIZE_Y
        self.Width = SIZE_X
        self.FontColor = MaColor.black
        self.BackColor = _color
    def GamePrint(self,text,location_x_y = None,_font = None):
        global SCREEN,FONT
        if location_x_y is None:
            location_x_y = (self.Width/2,self.Height-50)
        if _font is None:
            _font = FONT
        imgText = FONT.render(text,True,self.FontColor)
        SCREEN.blit(imgText,location_x_y)
        #pygame.display.update()

#初始化pygame游戏主窗口，可以设置窗口大小和SCREEN背景色，默认白色
mygame = MaGame(600,600)

def initialize():
    #变量初始化放这里
    global FONT,CLOCK,DIR
    global SCREEN_WIDTH,SCREEN_HEIGHT
    global CLOCKTHREAD,EXITFLAG
    #在这里修改GamePrint的字体大小
    fontsize = 40
    SCREEN_WIDTH = mygame.Width
    SCREEN_HEIGHT = mygame.Height
    DIR = os.path.split(os.path.abspath(__file__))[0]
    FONT = pygame.font.Font(None,fontsize)
    CLOCK = pygame.time.Clock()#设置帧率
    CLOCKTHREAD = threading.Thread(target = ClockTick,args = (0.02,),name = 'tick')
    IMAGETHREAD = threading.Thread(target = ImageTick,args = (0.5,),name = 'change image')
    CLOCKTHREAD.start()
    IMAGETHREAD.start()
    #join会阻塞主线程
    #CLOCKTHREAD.join()
    
    #end of initialize

def exitall():
    global EXITFLAG
    EXITFLAG = True
    return

def ClearScreen():
    #清屏
    global SCREEN
    SCREEN.fill(mygame.BackColor)
    #pygame.display.update()
    #end of ClearSCreen

def ClockTick(delay):
    global EXITFLAG
    global CLOCKTICKFLAG
    while(not EXITFLAG):
        time.sleep(delay)
        CLOCKTICKFLAG = True

#切换显示图像的速率和移动的速率不一致
def ImageTick(delay):
    global EXITFLAG
    global IMAGECHANGEFLAG
    while(not EXITFLAG):
        time.sleep(delay)
        IMAGECHANGEFLAG = True

def FrameTask():
    #每帧的任务
    global CLOCK,SCREEN
    global Player,Enemy_Orange,Enemy_Blue,Enemy_Red
    global GroupAll,GroupEnemy
    global IMAGECHANGEFLAG
    #Frame = 40 fps   
    #CLOCK.tick(60) 
    #用tick的方法延时会带来卡顿，我决定开一个新的线程来做定时   
    #when you need to clear the screen
    ClearScreen() 
    Player.MoveByXY(Player.Xspeed,Player.Yspeed)
    Enemy_Pink.MoveByXY(Enemy_Pink.Speed,0)
    Enemy_Blue.MoveByXY(Enemy_Blue.Speed,Enemy_Blue.Speed)
    Enemy_Orange.MoveByXY(0,Enemy_Orange.Speed)
    Enemy_Red.MoveByXY(-Enemy_Red.Speed,0)
    Enemy_Pink.IfOnEdgeBounce()
    Enemy_Blue.IfOnEdgeBounce()
    Enemy_Red.IfOnEdgeBounce()
    Enemy_Orange.IfOnEdgeBounce()
    if Player.rect.left >= 600:
        Player.rect.left = 0
    if Player.rect.left < 0:
        Player.rect.left = 600
    if Player.rect.top >= 600:
        Player.rect.top = 0
    if Player.rect.top < 0:
        Player.rect.top = 600
    if(IMAGECHANGEFLAG):
        IMAGECHANGEFLAG = False
        if Player.ImgIndex == 0:
            Player.image = Player.images[1]
            Player.ImgIndex = 1
        else:
            Player.image = Player.images[0]
            Player.ImgIndex = 0
    collidesprite = pygame.sprite.spritecollideany(Player,GroupEnemy)
    if collidesprite != None:
        GroupAll.remove(collidesprite)
        GroupEnemy.remove(collidesprite)        
    GroupAll.draw(SCREEN)  
    #end of FrameTask

#Based on Sprite
class Actor(pygame.sprite.Sprite):
    costumes = []
    def __init__(self,imgpath,position = (0,0)):
        global DIR
        pygame.sprite.Sprite.__init__(self)        
        imgpath = os.path.join(DIR, imgpath)
        #image是用于初始化的，pygame的Sprite必须有一个image对象，用于保存其需要展示的图像
        self.image = pygame.image.load(imgpath).convert_alpha()
        self.images = [self.image]
        #pygame的Sprite必须有一个rect对象，用于设定图像显示的区域
        self.rect = self.image.get_rect()
        #角色尺寸
        self.Width,self.Height = self.image.get_size()
        self.ImgIndex = 0
        #延X、Y方向移动的像素
        self.Speed = 5
        self.Xspeed = self.Speed
        self.Yspeed = 0  
        #角色的角度
        self.Angle = 0 
        self.SetPosition(position[0],position[1])
        print(self.rect)
    def SetPosition(self,_X,_Y):
        self.rect.top = _Y
        self.rect.left = _X     
    def AppendImage(self,imgpath):
        global DIR
        imgpath = os.path.join(DIR, imgpath)
        surf = pygame.image.load(imgpath).convert_alpha()
        self.images.append(surf)
    def MoveByXY(self,dx,dy):
        self.rect.move_ip(dx,dy)
    def Rotate(self,_angle):
        self.Angle = _angle
        tmpsurf = pygame.transform.rotate(self.image,_angle)
        self.image = tmpsurf
        for i in range(len(self.images)):
            tmpsurf = pygame.transform.rotate(self.images[i],_angle)
            self.images[i] = tmpsurf
    def SetAngle(self,_angle):
        self.Rotate(-self.Angle)
        self.Rotate(_angle)
    #Sprite功能很强大，可以不用去定义Show函数，采用下面的方法实现显示会更便捷：
    #先定义一个Group，<group name> = pygame.sprite.Group()
    #然后将先前声明的Sprite实例加入到这个Group中，<group name>.add(<actor name>)
    #最后用<group name>.draw(screen)方法绘制角色，而绘制角色的大小和位置则取决于rect属性
    '''
    def Show(self,_position = None):
        global SCREEN
        global SCREEN_WIDTH,SCREEN_HEIGHT
        if _position is None:
            _position = self.Loc_x,self.Loc_y
        SCREEN.blit(self.images[self.ImgIndex],_position)
    '''
    def SetScale(self,_scale):
        for i in range(len(self.images)):
            _width = int(_scale*self.Width)
            _height = int(_scale*self.Height)
            self.images[i] = pygame.transform.smoothscale(self.images[i],(_width,_height))
        self.image = self.images[0]

class Enemy(Actor):
    def __init__(self,_pos = (0,0)):
        Actor.__init__(self,"Role.png",_pos)
        self.position = _pos
    def SetImage(self,_index):
        #子类直接修改父类的属性，用self访问
        self.rect = pygame.Rect(50*(_index+1),0,50,50)
        self.image = self.image.subsurface(self.rect)
        self.images[0] = self.image
        self.SetPosition(self.position[0],self.position[1])
    #如果撞到屏幕边界，反弹
    def IfOnEdgeBounce(self):
        global SCREEN_WIDTH,SCREEN_HEIGHT
        if(self.rect.left > SCREEN_WIDTH or \
            self.rect.top < 0 or self.rect.left <0 or \
                self.rect.top > SCREEN_HEIGHT):
                self.Speed = -self.Speed

global AllImg #所有的角色的图像都在一副png图片里
global Player,Enemy_Pink,Enemy_Orange,Enemy_Blue,Enemy_Red
global GroupAll,GroupEnemy
global MapMatrix

MapMatrix = numpy.zeros((24,24),numpy.int)

def main():
    global SCREEN
    global Player,Enemy_Pink,Enemy_Orange,Enemy_Blue,Enemy_Red
    global AllImg
    global GroupAll,GroupEnemy
    global CLOCKTICKFLAG
    initialize() 

    AllImg = Actor("Role.png")
    Player = Actor("Role.png")
    
    Enemy_Pink = Enemy(_pos = (100,100))
    Enemy_Pink.SetImage(1)
    Enemy_Blue = Enemy(_pos = (100,200))
    Enemy_Blue.SetImage(2)
    Enemy_Orange = Enemy(_pos = (100,300))
    Enemy_Orange.SetImage(3)
    Enemy_Red = Enemy(_pos = (100,400))
    Enemy_Red.SetImage(4)
    
    Player.rect = pygame.Rect(0,0,50,50)
    Player.image = AllImg.image.subsurface(Player.rect)
    Player.images[0] = Player.image
    tmprect = pygame.Rect(50,0,50,50)
    Player.images.append(AllImg.image.subsurface(tmprect))
    
    GroupAll = pygame.sprite.Group()
    GroupEnemy = pygame.sprite.Group() 
    GroupAll.add(Player) 
    GroupAll.add(Enemy_Pink,Enemy_Blue,Enemy_Orange,Enemy_Red)
    GroupEnemy.add(Enemy_Pink,Enemy_Blue,Enemy_Orange,Enemy_Red)
    GroupAll.draw(SCREEN) 

    while True:          
        pygame.display.update()  
        if(CLOCKTICKFLAG):  
            CLOCKTICKFLAG = False  
            FrameTask()            
        for event in pygame.event.get():
            #事件捕捉          
            if event.type == QUIT:
                exitall()
                return
            if event.type == MOUSEMOTION:
                #鼠标移动事件
                pass
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exitall()
                    return
                #按键处理程序
                if event.key == 13:
                    #回车键
                    print("Enter!")
                if event.key == K_LEFT:
                    Player.Xspeed = -Player.Speed
                    Player.Yspeed = 0
                    Player.SetAngle(-180)
                if event.key == K_RIGHT:
                    Player.Xspeed = Player.Speed
                    Player.Yspeed = 0
                    Player.SetAngle(0)
                if event.key == K_UP:
                    Player.Xspeed = 0
                    Player.Yspeed = -Player.Speed
                    Player.SetAngle(90)
                if event.key == K_DOWN:
                    Player.Xspeed = 0
                    Player.Yspeed = Player.Speed
                    Player.SetAngle(-90)

    #end of main



if __name__ == '__main__': main()