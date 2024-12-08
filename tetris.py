import pygame
import sys
import random

pygame.init()


BLOCK_SIZE = 30  # Размер блока
GRID_WIDTH = 10  # Ширина сетки в блоках
GRID_HEIGHT = 20  # Высота сетки в блоках
GAME_WIDTH, GAME_HEIGHT = GRID_WIDTH * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE


WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700


GAME_OFFSET_X = (WINDOW_WIDTH - GAME_WIDTH) // 2
GAME_OFFSET_Y = 50


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (100, 100, 100)  
COLORS = [
    (255, 0, 0),  # Красный
    (0, 255, 0),  # Зеленый
    (0, 0, 255),  # Синий
    (255, 255, 0),  # Желтый
    (255, 0, 255),  # Розовый
    (0, 255, 255),  # Голубой
    (128, 0, 128)  # Фиолетовый
]


SHAPES = [
    ([[1, 1, 1, 1]], 1),  # I
    ([[1, 1], [1, 1]], 2),  # O
    ([[0, 1, 0], [1, 1, 1]], 3),  # T
    ([[1, 1, 0], [0, 1, 1]], 4),  # S
    ([[0, 1, 1], [1, 1, 0]], 5),  # Z
    ([[1, 0, 0], [1, 1, 1]], 6),  # L
    ([[0, 0, 1], [1, 1, 1]], 7)   # J
]


def create_grid():
    """Создает пустую сетку."""
    return [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    """Рисует сетку и закрепленные блоки."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            color = COLORS[cell - 1] if cell else LIGHT_GRAY
            pygame.draw.rect(
                screen,
                color,
                (GAME_OFFSET_X + x * BLOCK_SIZE, GAME_OFFSET_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            )
            pygame.draw.rect(
                screen,
                BLACK,
                (GAME_OFFSET_X + x * BLOCK_SIZE, GAME_OFFSET_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                1
            )
            if cell:
                pygame.draw.rect(
                    screen,
                    WHITE,
                    (GAME_OFFSET_X + x * BLOCK_SIZE, GAME_OFFSET_Y + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE),
                    1
                )

def draw_shape(shape, x, y, color_index):
    """Рисует текущую фигуру с белыми рамками."""
    color = COLORS[color_index - 1]
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    GAME_OFFSET_X + (x + col_index) * BLOCK_SIZE,
                    GAME_OFFSET_Y + (y + row_index) * BLOCK_SIZE,
                    BLOCK_SIZE,
                    BLOCK_SIZE
                )
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

def draw_score(score):
    """Рисует текущий счёт."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (20, 20))

def draw_level(level):
    """Рисует текущий уровень сложности."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"Level: {level}", True, BLACK)
    screen.blit(text, (WINDOW_WIDTH - 150, 20))

def get_random_shape():
    """Выбирает случайную фигуру и цвет."""
    return random.choice(SHAPES)

def check_collision(grid, shape, x, y):
    """Проверяет столкновения с границами или зафиксированными блоками."""
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                new_x = x + col_index
                new_y = y + row_index
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or (new_y >= 0 and grid[new_y][new_x]):
                    return True
    return False

def lock_shape(grid, shape, x, y, color_index):
    """Фиксирует фигуру в сетке."""
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                grid[y + row_index][x + col_index] = color_index

def clear_lines(grid):
    """Очищает заполненные линии и возвращает количество линий."""
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    cleared = GRID_HEIGHT - len(new_grid)
    new_grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(cleared)] + new_grid
    return new_grid, cleared


def calculate_score(cleared_lines, level):
    """
    Подсчет очков за очищенные линии с учетом уровня.
    Увеличиваем базовые очки в зависимости от уровня.
    """
    base_scores = [0, 50, 100, 200, 300] 
    return base_scores[cleared_lines] * (level + 1)  


def calculate_placement_score(distance, level):
    """
    Подсчет очков за размещение фигуры.
    Учитываем базовые 1 очко за размещение фигуры
    и увеличение на 50% за каждый пройденный блок, а также +1 очко за уровень.
    """
    base_score = 1  
    extra_score = int(base_score * 0.5 * distance)  
    return (base_score + extra_score) * (level + 1)  


def rotate_shape(shape):
    """Вращает фигуру по часовой стрелке."""
    return [list(row) for row in zip(*shape[::-1])]

def drop_to_bottom(grid, shape, x, y):
    """Сбрасывает фигуру до ближайшего препятствия."""
    while not check_collision(grid, shape, x, y + 1):
        y += 1
    return y




def main():
    global screen
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()
    grid = create_grid()
    current_shape, current_color = get_random_shape()
    x, y = 3, 0
    fall_time = 0
    fall_speed = 500
    move_delay = 100
    move_time = 0
    score = 0
    level = 1
    level_time = 0  
    level_up_interval = 10000  

    while True:
        screen.fill(WHITE)  
        level_time += clock.get_rawtime()
        fall_time += clock.get_rawtime()
        move_time += clock.get_rawtime()
        clock.tick()


        if level_time > level_up_interval:
            level_time = 0
            level += 1
            fall_speed *= 0.9  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rotated_shape = rotate_shape(current_shape)
                    if not check_collision(grid, rotated_shape, x, y):
                        current_shape = rotated_shape
                if event.key == pygame.K_SPACE:
                    start_y = y
                    y = drop_to_bottom(grid, current_shape, x, y)
                    placement_score = calculate_placement_score(y - start_y, level)
                    score += placement_score  
                    lock_shape(grid, current_shape, x, y, current_color)
                    grid, cleared = clear_lines(grid)
                    score += calculate_score(cleared, level)  
                    current_shape, current_color = get_random_shape()
                    x, y = 3, 0
                    if check_collision(grid, current_shape, x, y):
                        print("Game Over")
                        pygame.quit()
                        sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and move_time > move_delay:
            if not check_collision(grid, current_shape, x - 1, y):
                x -= 1
            move_time = 0
        if keys[pygame.K_RIGHT] and move_time > move_delay:
            if not check_collision(grid, current_shape, x + 1, y):
                x += 1
            move_time = 0
        if keys[pygame.K_DOWN]:
            if not check_collision(grid, current_shape, x, y + 1):
                y += 1
            fall_time = 0

        if fall_time > fall_speed:
            if not check_collision(grid, current_shape, x, y + 1):
                y += 1
            else:
                placement_score = calculate_placement_score(1, level)  
                score += placement_score
                lock_shape(grid, current_shape, x, y, current_color)
                grid, cleared = clear_lines(grid)
                score += calculate_score(cleared, level)  
                current_shape, current_color = get_random_shape()
                x, y = 3, 0
                if check_collision(grid, current_shape, x, y):
                    print("Game Over")
                    pygame.quit()
                    sys.exit()
            fall_time = 0

        draw_grid(grid)
        draw_shape(current_shape, x, y, current_color)
        draw_score(score)
        draw_level(level)

        pygame.display.update()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and move_time > move_delay:
            if not check_collision(grid, current_shape, x - 1, y):
                x -= 1
            move_time = 0
        if keys[pygame.K_RIGHT] and move_time > move_delay:
            if not check_collision(grid, current_shape, x + 1, y):
                x += 1
            move_time = 0
        if keys[pygame.K_DOWN]:
            if not check_collision(grid, current_shape, x, y + 1):
                y += 1
            fall_time = 0

        if fall_time > fall_speed:
            if not check_collision(grid, current_shape, x, y + 1):
                y += 1
            else:
                lock_shape(grid, current_shape, x, y, current_color)
                grid, cleared = clear_lines(grid)
                score += calculate_score(cleared, level)  
                current_shape, current_color = get_random_shape()
                x, y = 3, 0
                if check_collision(grid, current_shape, x, y):
                    print("Game Over")
                    pygame.quit()
                    sys.exit()
            fall_time = 0

        draw_grid(grid)
        draw_shape(current_shape, x, y, current_color)
        draw_score(score)
        draw_level(level)

        pygame.display.update()





if __name__ == "__main__":
    main()


