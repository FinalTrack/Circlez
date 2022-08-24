from operator import truediv
import random
import pygame 
import math 
  
pygame.init()  

screen = pygame.display.set_mode((420, 640))  
pygame.display.set_caption("Circlez")
logo = pygame.image.load('logo.png')

pygame.display.set_icon(logo)

fps = pygame.time.Clock()
vec = pygame.math.Vector2
PI = math.pi

#colors
bg = (0, 0, 45)
spark = (200, 200, 200)
glow = (30, 30, 30)
fire = (200, 0, 0)
fglow = (30, 0, 0)
oran = (200, 100, 0)
oglow = (30, 15, 0)
stripe = pygame.image.load('stripe.png')

ftxt = pygame.font.Font('roboto.ttf', 48)
btxt = pygame.font.Font('roboto.ttf', 180)
etxt = pygame.font.Font('roboto.ttf', 24)


lvls = []
lvls.append(pygame.image.load('redv.png'))
lvls.append(pygame.image.load('bluev.png'))
lvls.append(pygame.image.load('greenv.png'))
lvls.append(pygame.image.load('yellowv.png'))
lvls.append(pygame.image.load('pinkv.png'))
lvls.append(pygame.image.load('purplev.png'))
lvls.append(pygame.image.load('bomb.png'))

line = pygame.image.load('line.png')
redo = pygame.image.load('redo.png')
redo2 = pygame.image.load('redo2.png')

pop = pygame.mixer.Sound('pop.mp3')
xplode = pygame.mixer.Sound('explode.mp3')
wrong = pygame.mixer.Sound('wrong.mp3')
click = pygame.mixer.Sound('click.wav')

pygame.mixer.music.load('unity.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

#for i in range(0, len(lvls)):
    #lvls[i] = pygame.transform.scale(lvls[i], (48, 48))

shake = 0
best = 0

try:
    f = open('best.txt', 'r')
    best = int(f.read())
    f.close()
except:
    best = 0

def board(s, x, y, w, h, top, bot):
    pygame.draw.rect(s, (200, 150, 200), (x - w/2, y - h/2, w, h), 0, 10)
    pygame.draw.rect(s, (20, 0, 20), (x - w/2, y - h/2, w, h), 3, 10)
    stxt = etxt.render("Score:  " + str(top), True, (20, 0, 20))
    bstxt = etxt.render("  Best:  " + str(bot), True, (20, 0, 20))
    s.blit(stxt, (x - w/2 + 15, y - h/2 + 15))
    s.blit(bstxt, (x - w/2 + 15, y + h/2 - 15 - bstxt.get_height()))
    m = vec(pygame.mouse.get_pos())
    if fback and m.x >= (x + w/4) and m.x <= (x + w/4 + 40) and m.y >= y - redo.get_height()/2 and m.y <= y + redo.get_height()/2:
        s.blit(redo2, (x + w/4, y - redo.get_height()/2))
    else:
        s.blit(redo, (x + w/4, y - redo.get_height()/2))

class cross:
    def __init__(self, pos):
        self.pos = pos
        self.w = 1
        self.d = False
    def move(self):
        if self.w > 30:
            self.d = True
        if self.d:
            self.w /= 1.5
        else:
            self.w *= 1.5
    def draw(self, s):
        pygame.draw.rect(s, oran, (self.pos.x - self.w/2, 0, self.w, 640))
        pygame.draw.rect(s, oran, (0, self.pos.y - self.w/2, 420, self.w))
        s1 = pygame.Surface((4*self.w, 640))
        s2 = pygame.Surface((420, 4*self.w))
        s1.fill(oglow)
        s2.fill(oglow)
        s.blit(s1, (self.pos.x - 2*self.w, 0), special_flags = pygame.BLEND_RGB_ADD)
        s.blit(s2, (0, self.pos.y - 2*self.w), special_flags = pygame.BLEND_RGB_ADD)


class part:
    def __init__ (self, pos, vel, size, col1, col2, x = True, follow = None):
        self.pos = pos
        self.vel = vel
        self.size = size
        self.x = x
        self.c1 = col1
        self.c2 = col2
        self.follow = follow
    def move(self):
        if self.follow != None:
            if self.follow.next >= 60 and self.follow.next < 120:
                self.pos.y -= speed
        if self.x:
            self.vel.y += 0.25
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        if self.x:
            self.size *= 0.9
        else:
            self.size *= 0.95
    def draw(self, surf):
        pygame.draw.rect(surf, self.c1, (self.pos.x - self.size, shake + self.pos.y - self.size, 2 * self.size, 2 * self.size))
        s = pygame.Surface((self.size * 8, self.size * 8))
        pygame.draw.circle(s, self.c2, (self.size * 4, self.size * 4), self.size * 4)
        surf.blit(s, (self.pos.x - self.size * 4, shake + self.pos.y - self.size * 4), special_flags = pygame.BLEND_RGB_ADD)
        


class ball:
    def __init__(self, pos, lvl):
        self.pos = pos
        self.lvl = lvl
        self.sX = 0
        self.sY = 0
    def move(self, w):
        self.sX *= 0.8
        self.sY *= 0.8
        if abs(self.sX) < 0.1:
            self.sX = 0
        if abs(self.sY) < 0.1:
            self.sY = 0
        if w.next >= 60 and w.next < 120:
            self.pos.y -= speed
        if self.lvl == 6 and scrollY % 5 == 0:
            parts.append(part(vec(b.pos.x - 22 + random.randint(0, 6), b.pos.y - 24 + random.randint(0, 6)), vec(0, 0), random.randint(2, 4), oran, oglow, False, w))
    def draw(self, surf):
        warnX = 0
        warnY = 0
        global fail
        if self.pos.y < 125 and fail < 2:
            warnX = random.randint(-2, 2)
            warnY = random.randint(-2, 2)
        surf.blit(lvls[self.lvl], (self.pos.x - 24 + self.sX + warnX, self.pos.y - 24 + self.sY + shake + warnY))
        if fail >= 2 and fail < 62 and self.pos.y < 65:
            failX = ftxt.render('X', True, (255, 255, 255))
            surf.blit(failX, (self.pos.x - failX.get_width()/2, self.pos.y - failX.get_height()/2))




run = True


balls = []
speed = 2

wlvl = pygame.image.load('whitev.png')
#wlvl = pygame.transform.scale(wlvl, (48, 48))


parts = []

def spawn(pos):
    for i in range(0, 20):
        mag = random.random() * 5 + 1
        ang = random.random() * 2 * PI
        vel = vec(mag * math.cos(ang), mag * math.sin(ang))
        parts.append(part(vec(pos.x, pos.y), vel, mag, spark, glow))
def explode(pos):
    ang = 0
    for i in range(0, 20):
        ang += PI / 10
        vel = vec(2 * math.cos(ang), 2 * math.sin(ang))
        parts.append(part(vec(pos.x, pos.y), vel, 10, fire, fglow, False))
        vel = vec(math.cos(ang), math.sin(ang))
        parts.append(part(vec(pos.x, pos.y), vel, 5, fire, fglow, False))

pred = []
for i in range(0, 6):
    pred.append(0)

def predict(spos):
    p = vec(spos.x, spos.y)
    m = vec(pygame.mouse.get_pos())
    v = vec((m.x - p.x)/30, (m.y - p.y)/30)
    if v.length() > 8:
        v = v.normalize()
        v.x *= 8
        v.y *= 8 
    for i in range(1, 31):
        v.y += 0.25
        p.x += v.x
        p.y += v.y
        if i % 5 == 0:
            pred[(i - 5) // 5] = vec(p.x, p.y) 

diff = 0
fail = 0

def nRow():
    global speed
    global fail
    if minY > 250:
        speed = 2
    else:
        speed = 1
    i = 30
    a = random.randint(0, 6) * 60 + 30
    b = random.randint(0, 6) * 60 + 30
    mlvl = 0
    global diff
    if diff > 30:
        mlvl = 5
    elif diff > 20:
        mlvl = 4
    elif diff > 12:
        mlvl = 3
    elif diff > 6:
        mlvl = 2
    elif diff > 2:
        mlvl = 1 

    bAdd = total >= 8 and bombs < 2
    prob = 5
    if bombs > 0:
        prob = 10
    while i < 420:
        
        if random.randint(1, 10) > 8 or i == a:
            if bAdd and random.randint(1, prob) == prob:
                balls.append(ball(vec(i, 664), 6))
                bAdd = False
            else:
                balls.append(ball(vec(i, 664), random.randint(0, mlvl)))
        if speed == 2 and (random.randint(1, 10) > 8 or i == b):
            if bAdd and random.randint(1, prob) == prob:
                balls.append(ball(vec(i, 724), 6))
                bAdd = False
            else:
                balls.append(ball(vec(i, 724), random.randint(0, mlvl)))
        i += 60
    diff += 1

class white:
    def __init__(self, spos):
        self.pos = vec(0, 800)
        self.spos = spos
        self.vel = vec(0, 0)
        self.start = True
        self.next = 1
    def draw(self, surf):
        surf.blit(wlvl, (self.pos.x - 24, self.pos.y - 24 + shake))
    def move(self):
        global fail
        global score
        if fail > 1:
            fail += 1
            if fail > 120:
                fail = 2
            return
        if self.next > 150:
            if minY < 65:
                fail += 2
                wrong.play()
                global best
                best = max(score, best)
                return
            self.next = 0
            self.pos.x = self.spos.x
            self.pos.y = self.spos.y
            self.start = False
        elif self.next > 0:
            self.next += 1
            if self.next == 2:
                nRow()
            return

        if not self.start:
            predict(self.spos)
            return
            
        self.vel.y += 0.25
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        if self.pos.y > 640 + 24:
            self.next = 1

        e = 0.95
        p = vec(0, 0)
        i = 0
        bounce = side
        while i < len(balls):
            b = balls[i]
            v = vec(b.pos.x - self.pos.x, b.pos.y - self.pos.y)
            if v.length() < 48 and v.length() > 0:
                o = 48 - v.length()
                v = v.normalize()
                d = v.dot(self.vel)
                p.x -= o * v.x * 0.2
                p.y -= o * v.y * 0.2
                if d > 0:
                    bounce = max(bounce, 1)
                    self.vel.x += -(1 + e) * d * v.x
                    self.vel.y += -(1 + e) * d * v.y 
                    b.lvl -= 1
                    b.sX += 1.5 * d * v.x
                    b.sY += 1.5 * d * v.y
                    spawn(vec((self.pos.x + b.pos.x)/2, (self.pos.y + b.pos.y)/2))
                    global shake
                    if abs(shake) < 4:
                        shake = 4
                    score += 1
                    if b.lvl == 5:
                        shake = 30
                        bounce = 2
                        balls.pop(i)
                        crosses.append(cross(b.pos))
                        continue
                    elif b.lvl < 0:
                        if abs(shake) < 15:
                            shake = 15
                        explode(b.pos)
                        balls.pop(i)
                        continue
            i += 1
        if bounce == 2:
            xplode.play()
        elif bounce == 1:
            pop.play()

        if self.pos.x < 24:
            p.x += (24 - self.pos.x) * 0.2
            if self.vel.x < 0:
                self.vel.x = -e * self.vel.x
                spawn(vec(0, self.pos.y))
                if abs(shake) < 4:
                    shake = 4
        elif self.pos.x > (420 - 24):
            p.x -= (self.pos.x - (420 - 24)) * 0.2
            if self.vel.x > 0:
                self.vel.x = -e * self.vel.x
                spawn(vec(420, self.pos.y))
                if abs(shake) < 4:
                    shake = 4

        self.pos.x += p.x
        self.pos.y += p.y

w = white(vec(210, 48))

trail = []
crosses = []

shine = 0
scrollY = 0
side = 0
total = 0
bombs = 0

score = 0
boardY = 700
fback = 0

while run:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            f = open('best.txt', 'w')
            f.write(str(best))
            f.close()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and (not w.start):
            w.start = True
            m = vec(pygame.mouse.get_pos())
            w.vel.x = (m.x - w.pos.x)/30
            w.vel.y = (m.y - w.pos.y)/30
            if w.vel.length() > 8:
                w.vel = w.vel.normalize()
                w.vel.x *= 8
                w.vel.y *= 8
        elif event.type == pygame.MOUSEBUTTONDOWN and fback == 1:
            m = vec(pygame.mouse.get_pos())
            if m.x >= (210 + 250/4) and m.x <= (210 + 250/4 + 40) and m.y >= 340 - 42/2 and m.y <= 340 + 42/2:
                fback = 2
                click.play()


    shake *= -0.8
    if abs(shake) < 0.1:
        shake = 0

    i = 0
    while i < len(trail):
        trail[i].move()
        if trail[i].size < 0.5:
            trail.pop(i)
            continue
        i += 1

    i = 0
    while i < len(parts):
        parts[i].move()
        if parts[i].size < 0.5:
            parts.pop(i)
            continue
        i += 1

    i = 0
    while i < len(crosses):
        c = crosses[i]
        c.move()
        if c.w < 1:
            crosses.pop(i)
            continue
        i += 1

    i = 0
    side = 0
    total = 0
    bombs = 0
    minY = 640
    while i < len(balls):
        b = balls[i]
        b.move(w)
        flag = False
        for c in crosses:
            if c.w > 10 and (c.pos.x == b.pos.x or c.pos.y == b.pos.y):
                flag = True
                break
        if flag:
            balls.pop(i)
            if b.lvl == 6:
                score += 1
                crosses.append(cross(b.pos))
                side = 2
                shake = 30
            else:
                score += (b.lvl+1)
                explode(b.pos)
                side = max(side, 1)
                if abs(shake) < 15:
                    shake = 15
            continue  
        if b.lvl == 6:
            bombs += 1
        elif b.lvl > 2:
            total += 2
        else:
            total += 1
        minY = min(minY, b.pos.y)
        i += 1

    w.move()

    if shine % 10 == 0 and shine // 10 < len(balls):
        b = balls[shine // 10]
        parts.append(part(vec(b.pos.x + 12, b.pos.y - 12), vec(0, 0), 4, spark, glow, False, w))
    shine += 1
    if shine > max(len(balls) * 10, 300):
        shine = 0

    if w.start and w.next == 0:
        trail.append(part(vec(w.pos.x, w.pos.y), vec(0, 0), 6, spark, bg, False))

    screen.fill(bg)
    scrollY += 1
    scrollY %= 640
    screen.blit(stripe, (0, scrollY))
    screen.blit(stripe, (0, scrollY - 640))

    stxt = btxt.render(str(score), True, (50, 25, 50))
    screen.blit(stxt, (210 - stxt.get_width()/2, 340 - stxt.get_height()/2))

    shadow = pygame.Surface((420, 90))
    shadow.fill((25, 0, 25))
    pygame.draw.circle(shadow, (15, 0, 15), w.spos, 30)
    screen.blit(shadow, (0, 0), special_flags = pygame.BLEND_RGB_MIN)

    screen.blit(line, (0, -4))
    

    for t in trail:
        t.draw(screen)

    w.draw(screen)

    for b in balls:
        b.draw(screen)

    for p in parts:
        p.draw(screen)

    if not w.start:
        for p in pred:
            pygame.draw.circle(screen, spark, p, 3)
    
    for c in crosses:
        c.draw(screen)

    if fail > 1:
        board(screen, 210, boardY, 250, 100, score, best)
        if fback == 0:
            boardY += (340 - boardY)*0.1
            if(boardY < 341):
                boardY = 340
                fback = 1
        elif fback == 2:
            boardY += (700 - boardY)*0.1
            if(boardY > 699):
                boardY = 700
                fback = 0
                while len(balls) > 0:
                    balls.pop()
                while len(parts) > 0:
                    parts.pop()
                score = 0
                fail = 0
                w.next = 1
                diff = 0


    
    pygame.display.update()
    fps.tick(60)