import pygame
import glob
pygame.init()

win = pygame.display.set_mode((2200,672))

pygame.display.set_caption("First Game")

def loadImages(folderName,flip,x_size,y_size):
  fileList=glob.glob(folderName+"/*")
  output=[]
  for i in range(len(fileList)):
    output.append(pygame.image.load(fileList[i]))
    output[i]=pygame.transform.scale(output[i],(x_size, y_size))
  
  if flip==1:
    for i in range(len(output)):
      output[i]=pygame.transform.flip(output[i],True,False)

  return output

bgX=0
bg=pygame.image.load('Star_Night.png')
char=pygame.image.load('Pygame-Images/Game/standing.png')

clock=pygame.time.Clock()

bulletSound = pygame.mixer.Sound('Game_bullet.mp3')
hitSound = pygame.mixer.Sound('Game_hit.mp3')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

score = 0
xpos=0


class player(object):

  walkRight=loadImages('hero',0,100,100)
  walkLeft=loadImages('hero',1,100,100)

  
  def __init__(self,x,y,width,height):
    self.initialx=x
    self.initialy=y
    self.x=x
    self.y=y
    self.width=width
    self.height=height
    self.vel=5
    self.isJump=False
    self.left=False
    self.right=False
    self.walkCount=0
    self.jumpCount =10
    self.standing = True
    self.hitbox = (self.x + 17, self.y + 11, 29, 52)

  def draw(self,win):
    if self.walkCount + 1 >= 28:
      self.walkCount=0

    if not(self.standing):
      if self.left:
        win.blit(self.walkLeft[self.walkCount//7], (self.x,self.y))
        self.walkCount +=1
      elif self.right:
        win.blit(self.walkRight[self.walkCount//7], (self.x,self.y))
        self.walkCount +=1
    else:
      if self.right:
        win.blit(self.walkRight[0], (self.x, self.y))
      else:
        win.blit(self.walkLeft[0], (self.x, self.y))
    self.hitbox = (self.x + 17, self.y + 11, 29, 52)
    #pygame.draw.rect(win, (255, 0, 0), self.hitbox,2)
  
  def hit(self):
    self.isJump = False
    self.JumpCount = 10
    self.x = self.initialx
    self.y = self.initialy
    self.walkCount = 0
    font1 = pygame.font.SysFont('comicsans', 100)
    text = font1.render('-5', 1, (255, 0, 0))
    win.blit(text, (250 - (text.get_width()/2),200))
    pygame.display.update()
    i = 0
    while i < 200:
      pygame.time.delay(10)
      i += 1
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          i = 201
          pygame.quit()


class projectile(object):
  def __init__(self,x,y,radius,color,facing):
    self.x = x
    self.y = y
    self.radius = radius
    self.color = color
    self.facing = facing
    self.vel = 8 * facing

  def draw(self,win):
    pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
  walkLeft=loadImages('dino',1,100,100)
  walkRight=loadImages('dino',0,100,100)
  

  def __init__(self, x, y, width, height, end):
    self.initialx=x
    self.initialy=y
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.end = end
    self.path = [self.x, self.end]
    self.walkCount = 0
    self.vel = 3
    self.hitbox = (self.x + 17, self.y + 2, 31, 57)
    self.health = 10
    self.visible = True

  def draw(self,win):
    self.move()
    if self.visible:
      if self.walkCount + 1 >= 28:
        self.walkCount = 0

      if self.vel > 0:
        win.blit(self.walkRight[self.walkCount//7], (self.x, self.y))
        self.walkCount += 1
      else:
        win.blit(self.walkLeft[self.walkCount//7], (self.x, self.y))
        self.walkCount += 1
    
      pygame.draw.rect(win,(255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
      pygame.draw.rect(win,(0,128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
      self.hitbox = (self.x + 17, self.y + 2, 31, 57)
      #pygame.draw.rect(win, (255, 0, 0), self.hitbox,2)

    
  def move(self):
    if self.vel > 0:
      if self.x  + self.vel < self.path [1]:
        self.x += self.vel
      else:
        self.vel = self.vel * -1
        self.walkCount = 0
    else:
      if self.x - self.vel > self.path[0]:
        self.x += self.vel
      else:
        self.vel = self.vel * -1
        self.walkCount = 0

  def hit(self):
    if self.health > 0:
      self.health -= 1
    else:
      self.visible = False
    print('hit')



def redrawGameWindow():
  win.blit(bg,(bgX,0))
  text = font.render('Score: ' + str(score), 1, (0,0,0))
  text2 = font.render('xpos: ' + str(xpos), 1, (0,0,0))
  win.blit(text, (390,10))
  win.blit(text2, (390,30))
  hero.draw(win)
  dino.draw(win)
  for bullet in bullets:
    bullet.draw(win)

  pygame.display.update()

scrolling = True
#main loop
font = pygame.font.SysFont('comicsans', 30, True)
hero=player(50,382,64,64)
dino = enemy(100,386,64,64,300)
shootLoop = 0
bullets = []
run=True
while run:
  clock.tick(27)
  """
  if dino.visible == True:
    if hero.hitbox[1] < dino.hitbox[1] + dino.hitbox[3] and hero.hitbox[1] + hero.hitbox[3] > dino.hitbox[1]:
      if hero.hitbox[0] + hero.hitbox[2] > dino.hitbox[0] and hero.hitbox[0] < dino.hitbox[0] + dino.hitbox[2]:
        hero.hit()
        score -= 5
  """

  if shootLoop > 0:
    shootLoop += 1
  if shootLoop > 3:
    shootLoop =0

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run=False

  for bullet in bullets:
    if bullet.y - bullet.radius < dino.hitbox[1] + dino.hitbox[3] and bullet.y + bullet.radius > dino.hitbox[1]:
      if bullet.x + bullet.radius > dino.hitbox[0] and bullet.x - bullet.radius < dino.hitbox[0] + dino.hitbox[2]:
        hitSound.play()
        dino.hit()
        score += 1
        bullets.pop(bullets.index(bullet))

    if bullet.x < 500 and bullet.x > 0:
      bullet.x += bullet.vel
    else:
      bullets.pop(bullets.index(bullet))
  
  keys = pygame.key.get_pressed()

  if keys[pygame.K_SPACE] and shootLoop ==0:
    bulletSound.play()
    if hero.left:
      facing = -1
    else:
      facing = 1

    if len(bullets) < 5:
      bullets.append(projectile(round(hero.x + hero.width //2), round(hero.y + hero.height//2), 6, (0,0,0), facing))

    shootLoop = 1

  if keys[pygame.K_LEFT] and xpos>0:
    if scrolling:
      bgX += hero.vel
      xpos -= hero.vel
      dino.x += hero.vel
    else:
      hero.x -= hero.vel
    hero.left = True
    hero.right = False
    hero.standing = False
  elif keys[pygame.K_RIGHT] and xpos<1400:
    if scrolling:
      bgX -= hero.vel
      xpos += hero.vel
      dino.x -= hero.vel
    else:
      hero.x += hero.vel

    
    hero.right = True
    hero.left = False
    hero.standing = False
  else:
    hero.standing = True
    hero.walkCount = 0

  if not(hero.isJump):
    if keys[pygame.K_UP]:
      hero.isJump = True
      hero.right = False
      hero.left = False
      hero.walkCount = 0
  else:
    if hero.jumpCount >= -10:
      neg = 1
      if hero.jumpCount < 0:
        neg = -1
      hero.y -= (hero.jumpCount ** 2) * 0.5 * neg
      hero.jumpCount -= 1
    else:
      hero.isJump = False
      hero.jumpCount = 10
  redrawGameWindow()
pygame.quit()