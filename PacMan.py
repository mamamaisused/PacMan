#import basic pygame modules
import pygame
from pygame.locals import *
import MaColor
import os.path
import numpy

global SCREEN
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
mygame = MaGame(600,600,MaColor.black)

def initialize():
    #变量初始化放这里
    global FONT,CLOCK,DIR
    global SCREEN_WIDTH,SCREEN_HEIGHT
    #在这里修改GamePrint的字体大小
    fontsize = 40
    SCREEN_WIDTH = mygame.Width
    SCREEN_HEIGHT = mygame.Height
    DIR = os.path.split(os.path.abspath(__file__))[0]
    FONT = pygame.font.Font(None,fontsize)
    CLOCK = pygame.time.Clock()#设置帧率
    #end of initialize

def ClearScreen():
    #清屏
    global SCREEN
    SCREEN.fill(mygame.BackColor)
    #pygame.display.update()
    #end of ClearSCreen

def FrameTask():
    #每帧的任务
    global CLOCK,SCREEN
    global Player
    global GroupAll
    #Frame = 40 fps   
    CLOCK.tick(5)    
    #when you need to clear the screen
    ClearScreen() 
    Player.MoveByXY(Player.Xspeed,Player.Yspeed)
    if Player.ImgIndex == 0:
        Player.image = Player.images[1]
        Player.ImgIndex = 1
    else:
        Player.image = Player.images[0]
        Player.ImgIndex = 0
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
        self.Speed = 25
        self.Xspeed = self.Speed
        self.Yspeed = 0        
    def AppendImage(self,imgpath):
        global DIR
        imgpath = os.path.join(DIR, imgpath)
        surf = pygame.image.load(imgpath).convert_alpha()
        self.images.append(surf)
    def MoveByXY(self,dx,dy):
        self.rect.move_ip(dx,dy)
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

global AllImg #所有的角色的图像都在一副png图片里
global Player
global GroupAll
global MapMatrix

MapMatrix = numpy.zeros((24,24),numpy.int)

def main():
    global SCREEN
    global Player
    global AllImg
    global GroupAll
    initialize() 

    AllImg = Actor("Role.png")
    Player = Actor("Role.png")
    Player.rect = pygame.Rect(0,0,50,50)
    Player.image = AllImg.image.subsurface(Player.rect)
    Player.images[0] = Player.image
    tmprect = pygame.Rect(50,0,50,50)
    Player.images.append(AllImg.image.subsurface(tmprect))

    GroupAll = pygame.sprite.Group() 
    GroupAll.add(Player) 
    GroupAll.draw(SCREEN) 
    while True:          
        pygame.display.update()      
        FrameTask()
        for event in pygame.event.get():
            #事件捕捉          
            if event.type == QUIT:
                return
            if event.type == MOUSEMOTION:
                #鼠标移动事件
                pass
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                #按键处理程序
                if event.key == 13:
                    #回车键
                    print("Enter!")
                if event.key == K_LEFT:
                    Player.Xspeed = -Player.Speed
                    Player.Yspeed = 0
                if event.key == K_RIGHT:
                    Player.Xspeed = Player.Speed
                    Player.Yspeed = 0
                if event.key == K_UP:
                    Player.Xspeed = 0
                    Player.Yspeed = -Player.Speed
                if event.key == K_DOWN:
                    Player.Xspeed = 0
                    Player.Yspeed = Player.Speed

    #end of main



if __name__ == '__main__': main()