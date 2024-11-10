import pygame
import math
import random

# Константы
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Настройки игрока
player_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
player_angle = 0
player_speed = 5
rotation_speed = 2

# Сосед
neighbor_pos = [random.randint(100, 700), random.randint(100, 500)]
neighbor_size = 30
neighbor_speed = 1
neighbor_follow_distance = 200  # Дистанция, на которой сосед начинает двигаться к игроку

# Стены (x1, y1, x2, y2)
walls = [
    (100, 100, 100, 500),
    (100, 500, 500, 500),
    (500, 500, 500, 100),
    (500, 100, 100, 100),
]

def cast_ray(angle):
    ray_angle = angle * math.pi / 180
    ray_length = 0

    while ray_length < 1000:
        ray_length += 1
        ray_x = player_pos[0] + ray_length * math.cos(ray_angle)
        ray_y = player_pos[1] + ray_length * math.sin(ray_angle)

        for wall in walls:
            x1, y1, x2, y2 = wall
            # Проверка вертикальных стен
            if x1 == x2:
                if (min(y1, y2) <= ray_y <= max(y1, y2)) and (ray_x >= x1):
                    return ray_length
            # Проверка горизонтальных стен
            else:
                if (min(x1, x2) <= ray_x <= max(x1, x2)) and (ray_y >= y1):
                    return ray_length
    return -1

def draw_walls(screen):
    for i in range(0, WINDOW_WIDTH, 1):  # шаг между лучами
        angle = player_angle + (i - WINDOW_WIDTH // 2) / 300
        length = cast_ray(angle)

        if length > 0:
            height = 50000 / length  # высота стены, обратно пропорциональна длине
            pygame.draw.rect(screen, RED, (i, (WINDOW_HEIGHT - height) / 2, 1, height))

def move_neighbor():
    # Дистанция до соседа
    distance_to_player = math.sqrt((neighbor_pos[0] - player_pos[0]) ** 2 + (neighbor_pos[1] - player_pos[1]) ** 2)

    if distance_to_player < neighbor_follow_distance:  # Если сосед близко к игроку, он начинает двигаться
        if neighbor_pos[0] < player_pos[0]:
            neighbor_pos[0] += neighbor_speed
        elif neighbor_pos[0] > player_pos[0]:
            neighbor_pos[0] -= neighbor_speed

        if neighbor_pos[1] < player_pos[1]:
            neighbor_pos[1] += neighbor_speed
        elif neighbor_pos[1] > player_pos[1]:
            neighbor_pos[1] -= neighbor_speed

def check_collision():
    player_rect = pygame.Rect(player_pos[0] - 20, player_pos[1] - 20, 40, 40)  # Площадка игрока
    neighbor_rect = pygame.Rect(neighbor_pos[0], neighbor_pos[1], neighbor_size, neighbor_size)  # Площадка соседа
    return player_rect.colliderect(neighbor_rect)

# Основной игровой цикл
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Hello Neighbor Parody - First Person")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Управление игроком
    if keys[pygame.K_LEFT]:
        player_angle -= rotation_speed
    if keys[pygame.K_RIGHT]:
        player_angle += rotation_speed
    if keys[pygame.K_UP]:
        player_pos[0] += player_speed * math.cos(math.radians(player_angle))
        player_pos[1] += player_speed * math.sin(math.radians(player_angle))
    if keys[pygame.K_DOWN]:
        player_pos[0] -= player_speed * math.cos(math.radians(player_angle))
        player_pos[1] -= player_speed * math.sin(math.radians(player_angle))

    # Движение соседа
    move_neighbor()

    # Проверка на столкновение
    if check_collision():
        print("Сосед поймал вас! Игра окончена.")
        running = False

    # Очистка экрана
    screen.fill(WHITE)

    # Отрисовка стен
    draw_walls(screen)

    # Отрисовка соседа
    pygame.draw.rect(screen, GREEN, (neighbor_pos[0], neighbor_pos[1], neighbor_size, neighbor_size))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()