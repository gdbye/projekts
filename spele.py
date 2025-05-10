import pygame, sys, random, subprocess
from os import path
from pygame.locals import *
pygame.init()

# Colors
fons = (16, 0, 22) 
gaissfons=(26, 0, 37)
white = (255, 255, 255)
gaiss=(170, 170, 170)
tumss=(100, 100, 100) 
color=(100, 187, 20)
input_krasa=(187, 28, 255)
# Game Setup

screen_WIDTH = 450
screen_HEIGHT = 600
size = [screen_WIDTH, screen_HEIGHT]

zvaigznes = []
for i in range(125):
    punktsx = random.randrange(0, screen_WIDTH)
    punktsy = random.randrange(0, screen_HEIGHT)
    zvaigznes.append([punktsx, punktsy])

clock = pygame.time.Clock()

screen = pygame.display.set_mode(size)
screen.fill(fons)
pygame.display.set_caption('Praktiskais darbs')

fonts = pygame.font.SysFont("Arial", 32)
fonts1 = pygame.font.SysFont("Arial", 20)

text_render_start = fonts.render('Spēlēt', 1 , color)
text_render_kontroles = fonts.render('Kontroles', 1 , color)
text_render_quit = fonts.render('Iziet' , 1 , color)
text_render_kontroles1 = fonts.render("W- uz augšu   A- pa kreisi", 3, color)
text_render_kontroles2 = fonts.render("S- uz leju    Q- iziet", 1, color)
text_render_kontroles3 = fonts.render("D- pa labi", 1, color)
text_varda_ievade = fonts.render("Ievadi vārdu ", 1, color)
text_varda_ievade1 = fonts1.render("(lai sāktu spēli nospied nost no kvadrāta)", 1, color)

lidmasinas_platums= 80
lidmasinas_augstums=45

class Lidmasina:    
        def __init__(self, x, y):
            self.lidmasina_png="kugis.png"
            self.png=pygame.image.load(self.lidmasina_png)
            self.lidmasina_PNG=pygame.transform.scale(self.png,(lidmasinas_platums, lidmasinas_augstums))

            self.x = int(x)
            self.y = int(y)
            self.velX = 0
            self.velY = 0
            self.left_pressed = False
            self.right_pressed = False
            self.up_pressed = False
            self.down_pressed = False
            self.speed = 2.3
            self.hitbox = (self.x+10, self.y, lidmasinas_platums-28, lidmasinas_augstums)
        
        def update(self):
            self.velX = 0
            self.velY = 0
            if self.left_pressed and not self.right_pressed:
                self.velX = -self.speed
            if self.right_pressed and not self.left_pressed:
                self.velX = self.speed
            if self.up_pressed and not self.down_pressed:
                self.velY = -self.speed
            if self.down_pressed and not self.up_pressed:
                self.velY = self.speed
        
            self.x += self.velX
            self.y += self.velY
            self.hitbox = (self.x+10, self.y, lidmasinas_platums-28, lidmasinas_augstums)

meteora_platums=80
meteora_augstums=45

class Meteors:
    def __init__(self, x, y):
        self.meteors_png="meteors.png"
        self.png=pygame.image.load(self.meteors_png) 
        self.meteors_PNG=pygame.transform.scale(self.png,(meteora_platums, meteora_augstums))
          
        self.x = int(x)
        self.y = int(y)
        self.hitbox = (self.x, self.y, meteora_platums, meteora_augstums)   
        
    def update(self):
           self.y-=0
           self.hitbox = (self.x, self.y, meteora_platums, meteora_augstums)     
      
lidmasina = Lidmasina(screen_WIDTH/2, screen_HEIGHT/2)
meteors = Meteors(188, 525)

meteors_kresais_PNG=pygame.transform.rotate(meteors.meteors_PNG, 90)
meteors_laba_PNG=pygame.transform.flip(meteors_kresais_PNG,True,False)

def vizualais():
        screen.fill(fons)
        for i in range(len(zvaigznes)):
            pygame.draw.circle(screen, white, zvaigznes[i], 2)

            zvaigznes[i][1] += 0.3
            if zvaigznes[i][1] > screen_HEIGHT:
                punktsy = random.randrange(-50, -10)
                zvaigznes[i][1] = punktsy
            
                punktsx = random.randrange(0, screen_HEIGHT)
                zvaigznes[i][0] = punktsx

def lidmasinas_lokacija():
        if lidmasina.x<=-20:
            lidmasina.x=-19
        if lidmasina.x>=393:
            lidmasina.x=392.7
        if lidmasina.y>=557.2:
            lidmasina.y=557
        if lidmasina.y<=-2:
            lidmasina.y=-1
        
meteori_kreisa = [] #meteori no kreisas
for i in range(5):
    meteorix=random.randrange(-20, 0)
    metoriy = random.randrange(-50, 300)
    meteori_kreisa.append([meteorix,metoriy])

meteori_laba = [] #meteori no labas
for i in range(5):
    meteorix = random.randrange(450, 470)
    metoriy = random.randrange(-50, 300)
    meteori_laba.append([meteorix, metoriy])

def ievada_vardu():
    global sakuma_teksts
    input_kvadrats = pygame.Rect(0, 90, 200, 32)
    sakuma_teksts = ''

    active=True
    while active:
        for event in pygame.event.get():
            match event.type: 
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                case pygame.MOUSEBUTTONDOWN:
                    if input_kvadrats.collidepoint(event.pos):
                        active = True
                    else:
                        active = False

                case pygame.KEYDOWN:

                    if event.key == pygame.K_BACKSPACE:
                        sakuma_teksts = sakuma_teksts[:-1]

                    else:
                        sakuma_teksts += event.unicode

        vizualais()
        screen.blit(text_varda_ievade,(0,0))
        screen.blit(text_varda_ievade1,(0,40))

        pygame.draw.rect(screen, input_krasa, input_kvadrats)
        text_surface = fonts.render(sakuma_teksts, True, (255, 255, 255))
        screen.blit(text_surface, (input_kvadrats.x, input_kvadrats.y))
        input_kvadrats.w = max(100, text_surface.get_width()+10)

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
  
def meteori_krit():
    global met
    global met2
    global met3
    global met4
    global met5
    global met6
    global met7
    global met8
    global met9
    global met10

    for i in range(len(meteori_kreisa)):

            meteori_kreisa[i][1] += 1
            meteori_kreisa[i][0] += 1

            if meteori_kreisa[i][1] > screen_HEIGHT+50:
                metoriy = random.randrange(-200, 300)
                meteori_kreisa[i][1] = metoriy
                meteorix=random.randrange(-20, 0)
                meteori_kreisa[i][0] = meteorix

    meteori_kreisa_list=(meteori_kreisa[0][0],meteori_kreisa[0][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_kresais_PNG, meteori_kreisa[0])
    met=pygame.draw.rect(screen, (0,0,0),meteori_kreisa_list,2)
    met

    meteori_kreisa_list2=(meteori_kreisa[1][0],meteori_kreisa[1][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_kresais_PNG, meteori_kreisa[1])
    met2=pygame.draw.rect(screen, (0,0,0),meteori_kreisa_list2,2)
    met2

    meteori_kreisa_list3=(meteori_kreisa[2][0],meteori_kreisa[2][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_kresais_PNG, meteori_kreisa[2])
    met3=pygame.draw.rect(screen, (0,0,0),meteori_kreisa_list3,2)
    met3

    meteori_kreisa_list4=(meteori_kreisa[3][0],meteori_kreisa[3][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_kresais_PNG, meteori_kreisa[3])
    met4=pygame.draw.rect(screen, (0,0,0),meteori_kreisa_list4,2)
    met4

    meteori_kreisa_list5=(meteori_kreisa[4][0],meteori_kreisa[4][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_kresais_PNG, meteori_kreisa[4])
    met5=pygame.draw.rect(screen, (0,0,0),meteori_kreisa_list5,2)
    met5

    for i in range(len(meteori_laba)):

            meteori_laba[i][1] += 1
            meteori_laba[i][0] -= 1

            if meteori_laba[i][1] > screen_HEIGHT+50:
                metoriy = random.randrange(-200, 300)
                meteori_laba[i][1] = metoriy
                meteorix=random.randrange(450, 470)
                meteori_laba[i][0] = meteorix
    

    meteori_laba_list=(meteori_laba[0][0],meteori_laba[0][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_laba_PNG, meteori_laba[0])
    met6=pygame.draw.rect(screen, (0,0,0),meteori_laba_list,2)
    met6

    meteori_laba_list2=(meteori_laba[1][0],meteori_laba[1][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_laba_PNG, meteori_laba[1])
    met7=pygame.draw.rect(screen, (0,0,0),meteori_laba_list2,2)
    met7

    meteori_laba_list3=(meteori_laba[2][0],meteori_laba[2][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_laba_PNG, meteori_laba[2])
    met8=pygame.draw.rect(screen, (0,0,0),meteori_laba_list3,2)
    met8

    meteori_laba_list4=(meteori_laba[3][0],meteori_laba[3][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_laba_PNG, meteori_laba[3])
    met9=pygame.draw.rect(screen, (0,0,0),meteori_laba_list4,2)
    met9

    meteori_laba_list5=(meteori_laba[4][0],meteori_laba[4][1],meteora_augstums,meteora_platums)
    screen.blit(meteors_laba_PNG, meteori_laba[4])
    met10=pygame.draw.rect(screen, (0,0,0),meteori_laba_list5,2)
    met10

def sakums():#prieks sakuma ekrana
    atbilde=0
    loop=True
    while loop:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            match event.type: 
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.MOUSEBUTTONDOWN:
                    if 155<= mouse[0] <= 295 and (screen_HEIGHT/4)*3 <= mouse[1] <= (screen_HEIGHT/4)*3+40:
                        pygame.quit()
                        sys.exit()
                    match atbilde:
                        case 0:   
                            if 155<= mouse[0] <= 295 and (screen_HEIGHT/4)*2 <= mouse[1] <= (screen_HEIGHT/4)*2+40:
                                atbilde+=1               
                    if 155<= mouse[0] <= 295 and (screen_HEIGHT/4) <= mouse[1] <= (screen_HEIGHT/4)+40:
                        loop=False

        vizualais() 

        if 155<= mouse[0] <= 295 and (screen_HEIGHT/4)*3 <= mouse[1] <= (screen_HEIGHT/4)*3+40:

            pygame.draw.rect(screen,gaiss,[155,(screen_HEIGHT/4)*3,140,40])
        else:

            pygame.draw.rect(screen,tumss,[155,(screen_HEIGHT/4)*3,140,40])

        match atbilde:
            case 0:
                if 155<= mouse[0] <= 295 and (screen_HEIGHT/4)*2 <= mouse[1] <= (screen_HEIGHT/4)*2+40:
                    
                    pygame.draw.rect(screen,gaiss,[155,(screen_HEIGHT/4)*2,140,40])
                    screen.blit(text_render_kontroles,(170,(screen_HEIGHT/4)*2))

                else:

                    pygame.draw.rect(screen,tumss,[155,(screen_HEIGHT/4)*2,140,40])
                    screen.blit(text_render_kontroles,(170,(screen_HEIGHT/4)*2))
            
            case 1:
                pygame.draw.rect(screen, tumss,[75,(screen_HEIGHT/4)*2-70,300,200])
                screen.blit(text_render_kontroles1,(75,(screen_HEIGHT/4)*2-55,300,200))
                screen.blit(text_render_kontroles2,(75,(screen_HEIGHT/4)*2-15,300,200))
                screen.blit(text_render_kontroles3,(75,(screen_HEIGHT/4)*2+20,300,200))

        if 155<= mouse[0] <= 295 and (screen_HEIGHT/4) <= mouse[1] <= (screen_HEIGHT/4)+40:
            pygame.draw.rect(screen,gaiss,[155,(screen_HEIGHT/4),140,40])

        else:
            pygame.draw.rect(screen,tumss,[155,(screen_HEIGHT/4),140,40])    

        screen.blit(text_render_start,(185,(screen_HEIGHT/4)))
        screen.blit(text_render_quit,(195,(screen_HEIGHT/4)*3))

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

def beigas():
    if path.exists('highscore.txt'):
        f = open("highscore.txt", "a")

        point=str(points)

        f.write(f"{sakuma_teksts} ")
        f.write(point)
        f.write("""
 """)
        f.close()
    else:
        f = open("highscore.txt", "x")
        f.close
        f = open("highscore.txt", "a")

        point=str(points)

        f.write(f"{sakuma_teksts} ")
        f.write(point)
        f.write("""
""")
        f.close()

    Teksts_prieks_notepad_atvešanas=fonts.render("Nospied J ja gribi redzēt rezultātus", 1, color)
    Teksts_prieks_notepad_atvešanas2=fonts.render("Nospied N ja negribi redzēt rezultātus", 1, color)
    Teksts_prieks_notepad_atvešanas3=fonts.render("Nospied N lai izietu", 1, color)
    game_over_teksts=fonts.render("SPĒLE BEIDZĀS", 1, color)

    while True:
        for event in pygame.event.get():
            match event.type: 
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_j:
                            subprocess.call(['notepad.exe', "highscore.txt"])
                        case pygame.K_n:
                            pygame.quit()
                            sys.exit()
        
        vizualais()

        screen.blit(Teksts_prieks_notepad_atvešanas, (20, 300))
        screen.blit(Teksts_prieks_notepad_atvešanas2, (5, 340))
        screen.blit(Teksts_prieks_notepad_atvešanas3, (65, 380))
        screen.blit(game_over_teksts, (130, 40))
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

def main(): #pati spele

    global points

    points=0

    sakums()
    ievada_vardu()   
    loop=True
    # The main game loop
    while loop:
        points+=1
        text=fonts.render(f"Score:{points}", 1, color)
        # Get inputs
        for event in pygame.event.get():
            match event.type: 
                case pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_q:
                            pygame.quit()
                            sys.exit()
                        case pygame.K_w:
                            lidmasina.up_pressed = True

                        case pygame.K_s:
                            lidmasina.down_pressed = True

                        case pygame.K_a:
                            lidmasina.left_pressed = True

                        case pygame.K_d:
                            lidmasina.right_pressed = True
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_q:
                            pygame.quit()
                            sys.exit()

                        case pygame.K_w:
                            lidmasina.up_pressed = False

                        case pygame.K_s:
                            lidmasina.down_pressed = False

                        case pygame.K_a:
                            lidmasina.left_pressed = False

                        case pygame.K_d:
                            lidmasina.right_pressed = False

        lidmasinas_lokacija()
        vizualais()     
        meteori_krit()

        lidmas=pygame.draw.rect(screen, (0,0,0,0), lidmasina.hitbox,2)
        lidmas

        met_list=(met,met2,met3,met4,met5,met6,met7,met8,met9,met10)

        for i in range(len(met_list)):
            collide = pygame.Rect.colliderect(lidmas, met_list[i])
            if collide:
                loop=False
                beigas()
        
        # Render elements of the game
        screen.blit(text, (0,0))

        screen.blit(lidmasina.lidmasina_PNG, (lidmasina.x, lidmasina.y))

        lidmasina.update()
        meteors.update()

        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)
        
main()
