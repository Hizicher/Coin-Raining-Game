import pygame
from random import randint
 
#IDEA OF THE GAME: The player collects the coins that raining from above while trying to avoid the monsters on the ground by jumping. 
# When player collects 100 coins an exit door opens. Player wins the game by making it to the exit

class Character:
    def __init__(self,x,y):
        self.x=x
        self.y=y


class Robot(Character):
 
    def __init__(self,x,y):
 
        self.__robot=pygame.image.load("robot.png")
        self.x=x
        self.y=y
        self.health=4
        self.directions={"left":False, "right":False,"up":False}
        self.coins_obtained=0
        self.jump_velocity=20
        self.height=self.__robot.get_height()
        self.width=self.__robot.get_width()
 
    def head_right(self):
        if self.directions["right"] and self.x+self.width<635:
 
            self.x+=6
    
    def head_left(self):
        if self.directions["left"] and self.x>5:
            self.x-=6
 
    def blit_robot(self,window):
        window.blit(self.__robot,(self.x,self.y))
    
    def jump_robot(self):
        if self.directions["up"]:
            self.y-=self.jump_velocity
            self.jump_velocity-=1
 
            if self.jump_velocity<-20:
                self.jump_velocity=20
                self.directions["up"]=False
    
    @property
    def robot(self):
        return self.__robot
    
class Monster(Character):
    def __init__(self,x,y):
        self.__monster=pygame.image.load("monster.png")
        self.x=640+self.monster.get_width()
        self.y=420-self.monster.get_height()
        self.is_attack=False
        self.monster_speed=5
        self.height=self.monster.get_height()
        self.width=self.monster.get_width()
    
    def spawn_monster(self,window):
        window.blit(self.monster, (self.x,self.y))
        self.x-=self.monster_speed
 
    
    @property
    def monster(self):
        return self.__monster
class Coin:
    def __init__(self):
        self.__coin=pygame.image.load("coin.png")
        self.coins=[]
        self.height=self.coin.get_height()
        self.width=self.coin.get_width()
    
    def coin_or_not(self):
        if randint(1,33)==1:
            self.coins.append([randint(0,640-self.coin.get_width()),0-self.coin.get_height()])
 
    def blit_coin(self, window,x,y):
        window.blit(self.coin, (x,y))
    
    @property
    def coin(self):
        return self.__coin
 
class PayToEscape:
    def __init__(self):
        pygame.init()
        while True:
            self.create_display()
            self.set_parameters()
            self.game_loop()
 
    def create_display(self):
 
        pygame.display.set_caption("100 Coins To Win")
        self.window=pygame.display.set_mode((640,480))
        self.window.fill((173,216,230))
        
        self.font_10= pygame.font.SysFont("Arial", 10)
        self.font_12 = pygame.font.SysFont("Arial", 12)
        self.font_14=pygame.font.SysFont("Arial", 14)
        self.font_20 = pygame.font.SysFont("Arial", 20)
        self.font_40 = pygame.font.SysFont("Arial", 40)
        self.font_50 = pygame.font.SysFont("Arial", 50)
 
 
    def set_parameters(self):
       self.robot=Robot(0,420-pygame.image.load("robot.png").get_height())
       self.coin=Coin()
       self.monster=Monster(640+pygame.image.load("monster.png").get_width(),420-pygame.image.load("monster.png").get_height())
       self.door=pygame.image.load("door.png")
       self.is_restart=False
       self.game_over=False
       self.clock=pygame.time.Clock()
 
    def rain_coins(self):
        
        self.coin.coin_or_not()
        
        for i in [coin for coin in self.coin.coins]:
            if self.robot.x+5<=i[0]+self.coin.width<=self.robot.x+self.robot.width-5 or self.robot.x+5<=i[0]<=self.robot.x+self.robot.width-5: #+5 and -5 is added in order to give a visual effect that makes the robot slightly touch to the coins when obtaining them
                    self.robot.coins_obtained+=1
                    self.coin.coins.remove(i)
                    continue
 
            elif i[1]==420-self.coin.height:
                self.monster.monster_speed+=1  # the more coins the player misses the faster monsters are going to be attacking at the robot
                continue
            
            self.coin.blit_coin(self.window, i[0],i[1])
            i[1]+=2
                
    def spawn_monster(self):
        
        self.monster.spawn_monster(self.window)
 
        if self.robot.x+20<=self.monster.x+self.monster.width<=self.robot.x+self.robot.width-5 or self.robot.x+20<=self.monster.x<=self.robot.x+self.robot.width-5: #+20 when giving the "touching effect" instead of 5, because the monster's bottom half in front is wider than the top half in front, it seems thus a bit odd when the monster touches to the robot. Hence it is better to add 20 instead of 5
            if self.robot.y+5<=420-self.monster.height<=self.robot.y+self.robot.height-5:
                if self.monster.is_attack==False:
                    self.robot.health-=1
                    self.monster.is_attack=True
        
        if self.monster.x+self.monster.width<=0:
            self.monster.x=640+self.monster.width
            self.monster.is_attack=False
 
    def spawn_door(self):
        if self.robot.coins_obtained>=100:
            self.window.blit(self.door,(5,420-self.door.get_height()))
            if self.robot.x+self.robot.width<=self.door.get_width()+10: 
                if 440-self.door.get_height()<=self.robot.y+self.robot.height: 
                    self.game_over=True
          
    def update_display(self):
 
        if not self.game_over:
            
            pygame.display.set_caption("100 Coins To Win")
            self.window.fill((173,216,230))
            self.rain_coins()
            self.spawn_door()
            self.spawn_monster()
            self.robot.blit_robot(self.window)
            self.coins_amount = self.font_20.render(f"Coins obtained: {self.robot.coins_obtained}", True, (255, 0, 0))
            self.health = self.font_20.render(f"Health: ", True, (255, 0, 0))
            self.instruction_text= self.font_10.render("W = jump, A = head left, D = head right, F2 = restart", True, (255,0,0))
            self.window.blit(self.coins_amount, (10, 430))
            self.window.blit(self.health,(430,430))
            self.window.blit(self.instruction_text,(188,435))
        
            pygame.draw.rect(self.window, (0, 255, 0), (500, 430, 100, 20))
        
            if self.robot.health<4:
             pygame.draw.rect(self.window, (255, 0, 0), (500+self.robot.health*25, 430, 100-self.robot.health*25, 20))
 
            pygame.display.flip()
            if self.robot.health==0:
                self.game_over=True
        
            self.clock.tick(60)
            self.last_screen=self.window.copy()
 
    def game_over_display(self):
        pygame.draw.rect(self.window,(128,128,128),(55,55,self.window.get_width()-55*2,self.window.get_height()-55*2))
        pygame.draw.rect(self.window,(0,0,0),(60,60,self.window.get_width()-60*2,self.window.get_height()-60*2))
        pygame.draw.rect(self.window,(128,128,128),(106,340,204,54)) # Gray background at the end screen
        pygame.draw.rect(self.window,(128,128,128),(330,340,204,54))
        pygame.draw.rect(self.window,(0,0,0),(332,342,200,50)) # And black background
        pygame.draw.rect(self.window,(0,0,0),(108,342,200,50))
 
        self.window.blit(self.font_20.render(f"QUIT", True, (255, 0, 0)), (108+(200/2-self.font_20.size("QUIT")[0]//2),342+((50/2-self.font_20.size("QUIT")[1]//2))))
        self.window.blit(self.font_20.render(f"RESTART", True, (255, 0, 0)), (332+(200/2-self.font_20.size("RESTART")[0]//2),342+(50/2-self.font_20.size("RESTART")[1]//2)))
        
        if self.robot.health>0:
            self.window.blit(self.font_50.render("CONGRATULATIONS!", True, (255, 0, 0)), (60+((self.window.get_width()-60*2)//2-self.font_50.size("CONGRATULATIONS!")[0]//2),60+10))
            self.window.blit(self.font_12.render("You were able to collect at least 100 coins while successfully escaping from the monsters!", True, (255, 0, 0)), (60+((self.window.get_width()-60*2)//2-self.font_12.size("You were able to collect at least 100 coins while successfully escaping from the monsters!")[0]//2),60+((self.window.get_height()-60*2)//2-self.font_12.size("You were able to collect at least 100 coins while successfully escaping from the monsters!")[1]//2)))
 
        else:
            if self.robot.coins_obtained<100:
            
                self.window.blit(self.font_50.render("MAYBE NEXT TIME", True, (255, 0, 0)), (60+((self.window.get_width()-60*2)//2-self.font_50.size("MAYBE NEXT TIME")[0]//2),60+10))
                self.window.blit(self.font_14.render("You were not able to escape from the monsters nor to collect 100 coins", True, (255, 0, 0)), (60+((self.window.get_width()-60*2)//2-self.font_14.size("You were not able to escape from the monsters nor to collect 100 coins")[0]//2),60+((self.window.get_height()-60*2)//2-self.font_14.size("You were not able to escape from the monsters nor to collect 100 coins")[1]//2)))
 
            else: 
                self.window.blit(self.font_40.render("THIS WAS A CLOSE ONE", True, (255, 0, 0)), (60+((self.window.get_width()-60*2)//2-self.font_40.size("THIS WAS A CLOSE ONE")[0]//2),60+10))
                self.window.blit(self.font_14.render("You were able to collect 100 coins but could not make it to the exit", True, (255, 0, 0)), (60+((self.window.get_width()-60*2)//2-self.font_14.size("You were able to collect 100 coins but could not make it to the exit")[0]//2),60+((self.window.get_height()-60*2)//2-self.font_14.size("You were able to collect 100 coins but could not make it to the exit")[1]//2)))
      
    def events(self):
 
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
 
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_d:
                    self.robot.directions["right"]=True
                if event.key==pygame.K_a:
                     self.robot.directions["left"]=True
                if event.key==pygame.K_w:
                     self.robot.directions["up"]=True
                if event.key==pygame.K_F2:
                    self.is_restart=True
 
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_d:
                     self.robot.directions["right"]=False
                    
                if event.key==pygame.K_a:
                     self.robot.directions["left"]=False
            if event.type==pygame.MOUSEBUTTONDOWN:
                if 110<=event.pos[0]<=310 and 342<=event.pos[1]<=392:
                    exit()
                
                if 332<=event.pos[0]<=532 and 342<=event.pos[1]<=392:
                    self.is_restart=True
 
        self.robot.head_right()
        self.robot.head_left()
        self.robot.jump_robot()
            
    def game_loop(self):
        while True:
            self.events()
            if not self.game_over and not self.is_restart:
                self.update_display()
            
            elif not self.game_over and self.is_restart:
                
                break
            
            else:
                self.window.blit(self.last_screen,(0,0))
                self.game_over_display()
                if self.is_restart:
                    break
                pygame.display.flip()
            
            self.clock.tick(60)
        
PayToEscape()