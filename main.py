import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
CELL_SIZE = 20
FIELD_WIDTH = 30
FIELD_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * FIELD_WIDTH
SCREEN_HEIGHT = CELL_SIZE * FIELD_HEIGHT
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (154, 205, 50)
APPLE_COLOR = (178, 34, 34)
TEXT_SIZE = 24

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

# Начальная и максимальная скорости
INITIAL_SPEED = 5
MAX_SPEED = 15
SPEED_INCREASE = 1
current_speed = INITIAL_SPEED


def reset_snake_attributes(snake):
    """Сбрасывает атрибуты змейки в начальное состояние."""
    snake.length = 1
    snake.positions = [
        (FIELD_WIDTH // 2 * CELL_SIZE, FIELD_HEIGHT // 2 * CELL_SIZE)
    ]
    snake.direction = (CELL_SIZE, 0)  # Начальное направление вправо


class GameObject:
    """Класс для всех игровых объектов."""

    def __init__(self):
        """Инициализирует игровой объект."""
        pass

    def draw_cell(self, screen, position, color):
        """Отрисовывает ячейку на экране."""
        pygame.draw.rect(
            screen, color, (position[0], position[1],
                            CELL_SIZE, CELL_SIZE)
        )


class Apple(GameObject):
    """Класс, представляющий яблоко в игре."""

    def __init__(self):
        """Инициализирует яблоко."""
        super().__init__()
        self.color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока."""
        self.position = (
            random.randrange(0, FIELD_WIDTH) * CELL_SIZE,
            random.randrange(0, FIELD_HEIGHT) * CELL_SIZE,
        )

    def draw(self, screen):
        """Отрисовывает яблоко на экране."""
        self.draw_cell(screen, self.position, self.color)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        """Инициализирует змейку."""
        super().__init__()
        reset_snake_attributes(self)
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        if new_direction[0] != -self.direction[0] or \
           new_direction[1] != -self.direction[1]:
            self.next_direction = new_direction

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        head_position = self.positions[0]
        new_head_position = (
            head_position[0] + self.direction[0],
            head_position[1] + self.direction[1]
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.positions.pop()

    def handle_border_collision(self):
        """Обрабатывает столкновение змейки с границами экрана."""
        head_x, head_y = self.get_head_position()
        if head_x < 0:
            head_x = SCREEN_WIDTH - CELL_SIZE
        elif head_x >= SCREEN_WIDTH:
            head_x = 0
        if head_y < 0:
            head_y = SCREEN_HEIGHT - CELL_SIZE
        elif head_y >= SCREEN_HEIGHT:
            head_y = 0

        self.positions[0] = (head_x, head_y)

    def draw(self, screen):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            self.draw_cell(screen, position, self.body_color)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        global current_speed
        reset_snake_attributes(self)
        current_speed = INITIAL_SPEED


def draw_text(text, size, color, x, y):
    """Отрисовывает текст на экране."""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    SCREEN.blit(text_surface, text_rect)


def handle_input(snake):
    """Обрабатывает ввод пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                return False
            if event.key == pygame.K_UP:
                snake.update_direction((0, -CELL_SIZE))
            elif event.key == pygame.K_DOWN:
                snake.update_direction((0, CELL_SIZE))
            elif event.key == pygame.K_LEFT:
                snake.update_direction((-CELL_SIZE, 0))
            elif event.key == pygame.K_RIGHT:
                snake.update_direction((CELL_SIZE, 0))
    return True


def check_collisions(snake, apple):
    """Проверяет столкновения змейки с яблоком и собой."""
    if snake.get_head_position() == apple.position:
        snake.length += 1
        apple.randomize_position()
        global current_speed
        current_speed = min(current_speed + SPEED_INCREASE, MAX_SPEED)

    if snake.get_head_position() in snake.positions[1:]:
        snake.reset()


def draw_game(snake, apple):
    """Отрисовывает игровое поле и элементы."""
    SCREEN.fill(BACKGROUND_COLOR)
    snake.draw(SCREEN)
    apple.draw(SCREEN)
    draw_text(f"Length: {snake.length}", TEXT_SIZE, (255, 255, 255), 10, 10)
    draw_text(f"Speed: {current_speed}", TEXT_SIZE, (255, 255, 255), 10, 30)
    pygame.display.flip()


def main():
    """Основная функция, содержащая игровой цикл."""
    global current_speed
    snake = Snake()
    apple = Apple()
    running = True

    while running:
        running = handle_input(snake)
        if not running:
            break
        snake.move()
        snake.handle_border_collision()
        check_collisions(snake, apple)
        draw_game(snake, apple)
        CLOCK.tick(current_speed)
    pygame.quit()


if __name__ == "__main__":
    main()
