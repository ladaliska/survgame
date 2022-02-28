import opensimplex as simplex, random, pygame

width = 500
height = 500
color = 0


def generate_noise(width, height, island_size):
    seed = simplex.seed(random.randint(1, 10000000))
    iterable = [[simplex.noise2(j / island_size,i / island_size)
                 for j in range(width)] for i in range(height)]
    return iterable
            
def fill_canvas(iterable, pixel_size, surface):
    for y in range(len(iterable)):
        for x in range(len(iterable[y])):
            if -0.6667 > iterable[y][x]:
                color = (0,0,105)
            elif -0.6667 <= iterable[y][x] < 0:
                color = (0,0,255)
            elif 0 <= iterable[y][x] < 0.2:
                color = (255, 255, 102)
            elif 0.2 <= iterable[y][x] < 0.6667:
                color = (0, 153, 0)
            elif 0.6667 <= iterable[y][x] < 0.8:
                color = (204, 204, 204)
            elif 0.8 <= iterable[y][x] < 1:
                color = (238, 238, 238)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(surface, color, (x * pixel_size - pixel_size // 2, y * pixel_size - pixel_size // 2,pixel_size,pixel_size))


def main():
    pygame.init()
    surface = pygame.display.set_mode([width, height])
    running = True
    surface.fill((255,255,255))
    pixel_size = 1
    new_map = generate_noise(width, height, 100)
    fill_canvas(new_map, pixel_size, surface)
    while running == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
             running = False
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
