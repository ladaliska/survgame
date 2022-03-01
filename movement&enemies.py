import  pygame,random,os
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
player_speed = 5
enemy_speed = 3

from pygame.locals import (
    K_UP,
    K_h,
    K_SPACE,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


#Hráč
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'character.png')).convert()
        self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.current_health = 1000
        self.maximum_health = 1000
        self.health_bar_lenght = 400
        self.health_ration = self.maximum_health / self.health_bar_lenght
        self.food = 1000
        self.heal_cooldown = False
        self.heal_press_time = 0




    def update(self, pressed_keys):
        self.health_bar()
        if pressed_keys[K_h]:
            if self.heal_cooldown == False:
                if self.food >= 50:
                    self.heal_cooldown = True
                    self.heal_press_time = pygame.time.get_ticks()
                    self.food += -50
                    self.heal_get(100)
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -player_speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, player_speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-player_speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(player_speed, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def damage_get(self,amount):
        if self.current_health <= 0:
            self.current_health =0
        if self.current_health >0:
            self.current_health += -amount

    def heal_get(self,amount):
        if self.current_health < self.maximum_health:
            self.current_health += +amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health

    def health_bar(self):
        pygame.draw.rect(screen, (255,105,180), (10, 10, self.current_health/self.health_ration, 25))
        pygame.draw.rect(screen, (255,255,255),(10,10,self.health_bar_lenght,25),4 )

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'character.png')).convert()
        self.images.append(img)
        self.image = self.images[0]
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 0, 0))
        self.health = 100
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    def update(self,player_position):
        if player_position[0] > self.rect[0]:
            self.rect.move_ip(enemy_speed,0)
        else:
            self.rect.move_ip(-enemy_speed, 0)
        if player_position[1] > self.rect[1]:
            self.rect.move_ip(0, enemy_speed)
        else:
            self.rect.move_ip(0, -enemy_speed)
        

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
running = True
clock = pygame.time.Clock()
current_time = 0
last_spawn = 0
spawn_time = 10000
ADDENEMY = pygame.USEREVENT + 1
#Běžení hry
while running:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    current_time = pygame.time.get_ticks()
    if current_time - player.heal_press_time > 10000:
        player.heal_cooldown = False
    if current_time - last_spawn >16000:
        spawn_time += -1000
        if spawn_time < 1 :
            spawn_time =1
        last_spawn =pygame.time.get_ticks()
        pygame.time.set_timer(ADDENEMY,10 + spawn_time)

    pressed_keys = pygame.key.get_pressed()
    screen.fill((0, 0, 0))
    player.update(pressed_keys)

    enemies.update(player.rect)
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
    if pygame.sprite.spritecollideany(player, enemies):
        player.damage_get(10)
        if player.current_health == 0:
            running = False
    screen.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(60)
