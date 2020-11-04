import pygame,math,time

pygame.init()

screen=pygame.display.set_mode((800,600))
pygame.display.set_caption("Space Battle")
#player
class Player():
    def __init__(self,):
        self.player_img=pygame.image.load("space-invaders.png")
        self.player_x=368
        self.player_y=500
        self.player_step=0
        self.bullet_img = pygame.image.load("bullet.png")
        self.bullet_step=0
        self.bullet_x=self.player_x+20
        self.bullet_y=self.player_y
        self.fired=False
        self.game_over=False
        self.score=0

    def spawn_player(self,):
        screen.blit(self.player_img, (self.player_x, self.player_y))

    def fire_bullet(self):
        screen.blit(self.bullet_img, (self.bullet_x+20,self.bullet_y))

#Enemy
class Enemy(Player):

    def __init__(self,intruder_num):

        # Player.__init__(self)
        super().__init__()

        self.enemy_img=pygame.image.load("ufo.png")
        self.enemy_x=336
        self.enemy_y=-10
        self.enemy_step=.1
        self.intruder_num=intruder_num
        self.intruder=[]
        d={}
        for intruder in range(self.intruder_num):
            d["intruder_img"] = pygame.image.load("alien.png")
            d["killed"]=False
            d["intruder_x"] = 336
            d["intruder_y"] = 64
            d["order"]=intruder+1
            d["intruder_step"] =0.4 if d["order"]<2 else math.log10(d["order"])
            d["motion"]=False
            self.intruder.append(d)
            d={}
    def enemy(self,):
        screen.blit(self.enemy_img,(self.enemy_x,self.enemy_y))
    def move_enemy(self):
        self.enemy_x +=self.enemy_step
        if self.enemy_x > 500:
            self.enemy_step *= -1
        if self.enemy_x < 200:
            self.enemy_step *= -1

    def spawn_intruder(self,):
        for i in range(self.intruder_num):
            if not self.intruder[i]["motion"]:
                screen.blit(self.intruder[0]["intruder_img"], (self.intruder[i]["intruder_x"], self.intruder[i]["intruder_y"]))
                self.intruder[i]["motion"] = True
        else:
            pass

    def move_intruder(self):
        # intruder movement
        for i in range(self.intruder_num):
            if ((player.bullet_x-self.intruder[i]["intruder_x"])**2 + (player.bullet_y-self.intruder[i]["intruder_y"])**2 < 40**2 and
                    not self.intruder[i]["killed"]):
                self.intruder[i]["killed"]=True
                if not player.game_over:
                     player.score+=1
                player.bullet_x = player.player_x+20
                player.bullet_y = player.player_y
                player.fired=False

            if self.intruder[i]["motion"] and not self.intruder[i]["killed"]:
                if self.intruder[i]["order"]%2==0:
                    self.intruder[i]["intruder_x"] += self.intruder[i]["intruder_step"]
                else:
                    self.intruder[i]["intruder_x"] -= self.intruder[i]["intruder_step"]
                if self.intruder[i]["intruder_x"]>736:
                    self.intruder[i]["intruder_step"] *= -1
                    self.intruder[i]["intruder_y"] += 50
                if self.intruder[i]["intruder_x"]<0:
                    self.intruder[i]["intruder_step"] *= -1
                    self.intruder[i]["intruder_y"] += 30
                if self.intruder[i]["intruder_y"] + 64 >= player.player_y and (self.intruder[i]["intruder_x"]-player.player_x)**2 <= 64**2:
                    player.game_over=True

                screen.blit(self.intruder[i]["intruder_img"], (self.intruder[i]["intruder_x"], self.intruder[i]["intruder_y"]))
            else:
                pass

font=pygame.font.Font("freesansbold.ttf",32)
def score():
    game_score=font.render(f"Score: {player.score}",True,(255,255,255))
    screen.blit(game_score,(2,2))

def game_over(text):
    game_score=font.render(f"Score: {player.score}",True,(255,255,255))
    game_over_text=font.render(f"{text}",True,(255,255,255))
    screen.blit(game_over_text,(400-game_over_text.get_width()/2,300))
    screen.blit(game_score,(400-game_score.get_width()/2,340))
n=7
player=Player()
enemy=Enemy(n)

bgd_img=pygame.image.load("space_bgd.png")

# main game
game=True
while game:
    screen.blit(bgd_img,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.player_step = .10
            if event.key == pygame.K_LEFT:
                player.player_step = -.10
            if event.key == pygame.K_SPACE:
                if not player.fired:
                    player.fired=True
                    player.bullet_x=player.player_x
                    player.bullet_step= .5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player.player_step = 0
    enemy.enemy()
    enemy.move_enemy()
    enemy.spawn_intruder()
    enemy.move_intruder()
    if not player.game_over:
        score()
        player.player_x += player.player_step
        player.spawn_player()
        if player.score >= n:
            enemy.enemy_y -= .1
            game_over("GAME OVER You Won")

        if player.fired:
            player.bullet_y -= player.bullet_step
            player.fire_bullet()

        if player.bullet_y < 0:
            player.fired=False
            player.bullet_y = player.player_y

    else:
        enemy.enemy_y += .1
        game_over("GAME OVER You Lost")

    pygame.display.update()
