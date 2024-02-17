#By Mine is Zarox
#https://github.com/MineisZarox

import time
import pygame
import random
from itertools import combinations

#Button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface, *args):
		action = False
		pos = pygame.mouse.get_pos()

		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
        
		surface.blit(self.image, (self.rect.x if not args else args[0], self.rect.y if not args else args[1]))
		return action


class Game():
    def __init__(self, size: int = 500):
        self.size = size
        self.xoCords = self.get_xo_cords()
        self.indexes = [{0,1,2}, {3,4,5}, {6,7,8}, {0,3,6}, {1,4,7}, {2,5,8}, {0,4,8}, {2,4,6}]
        pygame.init()
        self.window = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Tic Tac Toe")
        pygame.display.update()
        
        # Music and sound
        pygame.mixer.init()
        pygame.mixer.music.load(str("assets/minecraft.mp3"))
        pygame.mixer.music.play(-1)

        # Asset images
        self.back = pygame.transform.scale(pygame.image.load("assets/back.jpg"), [self.size, self.size]).convert_alpha()
        self.win = pygame.transform.scale(pygame.image.load("assets/win.jpg"), [self.size, self.size]).convert_alpha()
        self.lose = pygame.transform.scale(pygame.image.load("assets/lose.jpg"), [self.size, self.size]).convert_alpha()
        self.tic = pygame.image.load("assets/tic.png")
        self.start = pygame.image.load("assets/start.png")
        self.exit = pygame.image.load("assets/close.png")
        self.reset = pygame.image.load("assets/reset.png")
        self.tie = pygame.image.load("assets/tie.jpg")


    def get_xo_cords(self):
        axisPoints = [int(((self.size/3)/2)+(i*(self.size/3))) for i in range(0, 3)]
        return [(i, o) for i in axisPoints for o in axisPoints]
        

    def get_block_by_cords(self, cords):
        sections = {
            (0, 0): 0,
            (0, 1): 1,
            (0, 2): 2,
            (1, 0): 3,
            (1, 1): 4,
            (1, 2): 5,
            (2, 0): 6,
            (2, 1): 7,
            (2, 2): 8
        }
        x, y = cords
        cords = (x//166, y//166)
        if cords in sections.keys():
            return sections[cords]
        else:
            return None


    def draw_xo(self, surface, turn, center, size: int = 100, thickness: int = 8):
        pygame.draw.line(surface, (0, 0, 0), (166, 0), (166, 500), 6)
        pygame.draw.line(surface, (0, 0, 0), (333, 0), (333, 500), 6)
        pygame.draw.line(surface, (0, 0, 0), (0, 166), (500, 166), 6)
        pygame.draw.line(surface, (0, 0, 0), (0, 333), (500, 333), 6)
        
        if turn == "x":
            x, y = center
            pygame.draw.line(surface, (255, 30, 30), (x - size // 2, y - size // 2), (x + size // 2, y + size // 2), thickness)
            pygame.draw.line(surface, (255, 30, 20), (x - size // 2, y + size // 2), (x + size // 2, y - size // 2), thickness)
        if turn == "o":
            pygame.draw.circle(surface, (0, 0, 0), center, size/2, 8)


    def xoCheck(self, xo, secs):
        xoIn = [i for i, xo_cords in enumerate(secs) if xo_cords[0] == xo]
        if len(xoIn) > 2:
            cmbntns = list(map(lambda x: set(x), list(combinations(xoIn, 3))))
            check = True in [index == cmbt for index in self.indexes for cmbt in cmbntns]
            if check: return xo
        return "0" if "0" not in [xo[0] for xo in secs] else None


    def oBrain(self, secs, xo):
        xoIn = [i for i, xo_cords in enumerate(secs) if xo_cords[0] == xo]
        if len(xoIn) > 1:
            cmbntns = list(map(lambda x: set(x), list(combinations(xoIn, 2))))
            extra = {list(index.difference(cmbt))[0] for index in self.indexes for cmbt in cmbntns if cmbt.issubset(index)}
            axoIn = {i for i, xo_cords in enumerate(secs) if xo_cords[0] != "0"}
            diff = list(extra.difference(axoIn))
            if diff: return diff
        return None
    

    def welcome(self):
        """The welcome screen"""
        exit = False
        fps = 30
        clock = pygame.time.Clock()
        
        startB = Button(150, 250, self.start, 0.6)
        exitB = Button(150, 330, self.exit, 0.6)
        tic = Button(70, 70, self.tic, 0.4)
        while not exit:    
            self.window.fill((0,0,0))
            self.window.blit(self.back, [0, 0])
            ifstart = startB.draw(self.window)
            ifexit = exitB.draw(self.window)
            tic.draw(self.window)
            

            if ifstart:
                pygame.mixer.Sound("assets/button.wav").play()
                self.main_loop()
                exit = True
            if ifexit:
                pygame.mixer.Sound("assets/button.wav").play()
                exit = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    self.main_loop()
                    exit = True
            
            pygame.display.update()
            clock.tick(fps)


    def main_loop(self):
        """Main game loop"""
        #usable vars
        time.sleep(1)
        exit = False
        game_over = False
        fps = 5
        clock = pygame.time.Clock()
        x, o = "x", "o"
        turn = x
        secs = [("0", (0,0)) for _ in range(9)]
        loseAudio = False

        while not exit:
            game_over = self.xoCheck("x", secs)
            if not game_over:
                game_over = self.xoCheck("o", secs)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
            
            if game_over:
                
                startB = Button(100, 350, self.reset, 0.4)
                exitB = Button(268, 350, self.exit, 0.4)   
                

                self.window.blit(self.back, [0, 0])
                if game_over == "x":
                    self.window.blit(self.win, [0, 0])
                elif game_over == "o":
                    self.window.blit(self.lose, [0, 0])
                    if loseAudio: pygame.mixer.Sound("assets/gameover.wav").play()
                    loseAudio = False
                else:
                    tie = Button(130, 200, self.tie, 0.7)          
                    tie.draw(self.window)
                    
                    
                
                ifstart = startB.draw(self.window)
                ifexit = exitB.draw(self.window)

                if ifstart:
                    pygame.mixer.Sound("assets/button.wav").play()
                    self.main_loop()
                    exit = True
                if ifexit:
                    pygame.mixer.Sound("assets/button.wav").play()
                    exit = True


            else:
                self.window.blit(self.back, [0, 0])
                [self.draw_xo(self.window, xo, cords) for xo, cords in secs]
                loseAudio = True
                
                if turn == x:
                    if pygame.mouse.get_pressed()[0] == 1:
                        cords = pygame.mouse.get_pos()
                        section = self.get_block_by_cords(cords)
                        if section in [i for i, xo_cords in enumerate(secs) if xo_cords[0] == "0"]:
                            pygame.mixer.Sound("assets/button.wav").play()
                            self.draw_xo(self.window, x, self.xoCords[section]) 
                            turn = o
                            secs[section] = (x, self.xoCords[section])
                else:
                    xoInNot = [i for i, xo_cords in enumerate(secs) if xo_cords[0] == "0"]
                    extra = self.oBrain(secs, o)
                    if not extra: extra = self.oBrain(secs, x)
                    section = random.choice(extra if extra else xoInNot)

                    self.draw_xo(self.window, o, self.xoCords[section])
                    turn = x
                    secs[section] = (o, self.xoCords[section])
                        
            pygame.display.update()
            clock.tick(fps)



if __name__ == "__main__":
    game = Game()
    game.welcome()

    pygame.mixer.quit()
    pygame.quit()