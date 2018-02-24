import pygame


WHITE = (255, 255, 255)
BLACK = (0,0,0)
PURPLE = (152, 79, 209)


WWIDTH = 500
WHEIGHT = 750


w = pygame.display.set_mode((WWIDTH, WHEIGHT))
pygame.display.set_caption("dolgčas-o-meter")


def main():

    running = True

    startpos = 200
    
    while running:

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                running = False
            if e.type==pygame.MOUSEBUTTONDOWN:
                p = pygame.mouse.get_pos()
                p = p[1]-75
                if p > 600 or p<0:
                    continue
                startpos = p+75
                

        w.fill(WHITE)

        w.fill(PURPLE, (50, startpos, 400, 675-startpos))

        # crte
        w.fill(BLACK, (50, 75, 400, 3))
        w.fill(BLACK, (50, 75, 3, 600))
        w.fill(BLACK, (450, 75, 3, 600))
        w.fill(BLACK, (50, 675, 403, 3))

        pygame.display.update()

pygame.init()
main()
