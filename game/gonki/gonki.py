from ursina import *
from ursina.prefabs.health_bar import HealthBar
import random
import time

app = Ursina()
window.title = 'Racing Game'
window.borderless = False
window.fullscreen = True
window.exit_button.visible = False

# Настройки камеры
camera.orthographic = True
camera.fov = 40

# Звуковые эффекты
try:
    collision_sound = Audio('assets/collision.wav', autoplay=False, loop=False)
    background_music = Audio('assets/background_music.wav', autoplay=True, loop=True)
    game_over_sound = Audio('assets/game_over.wav', autoplay=False, loop=False)
    bonus_sound = Audio('assets/bonus.wav', autoplay=False, loop=False)
    background_music.volume = 0.5
    collision_sound.volume = 0.7
    game_over_sound.volume = 0.8
    bonus_sound.volume = 0.8
except:
    print("Не удалось загрузить звуки. Продолжаем без звуков.")

# Настройки игры
base_speed = 8  # Увеличена базовая скорость
current_speed = base_speed
speed_increase_rate = 0.05
max_speed = 25
lives = 3
max_lives = 5
score = 0
game_active = True
start_time = time.time()
last_collision_time = 0
collision_cooldown = 1.0
speed_boost_active = False
speed_boost_end_time = 0

# Полосы дороги (6 полос)
LANE_WIDTH = 1.5
LANE_POSITIONS = [-3.75, -2.25, -0.75, 0.75, 2.25, 3.75]

# Игровые элементы
car = Entity(
    model='quad',
    texture='assets/car2.png',
    collider='box',
    scale=(2, 1.3),  # Более узкая машина для полос
    rotation_z=-90,
    y=-3,
    x=LANE_POSITIONS[2]  # Начинаем на центральной полосе
)

# Текстуры для бонусов и фона
bonus_textures = {
    'health': 'assets/health.png',
    'speed': 'assets/nitro.png'
}


# Фоновые элементы
def create_background():
    # Увеличиваем количество фоновых элементов для плавного скролла
    backgrounds = []
    for i in range(4):  # 4 фона вместо 2 для лучшего перекрытия
        left = Entity(
            model='quad',
            texture='assets/city.png',
            scale=(10, 30),  # Увеличиваем высоту
            x=-10,
            z=2,
            y=30 * i - 30
        )
        right = Entity(
            model='quad',
            texture='assets/sea.png',
            scale=(10, 30),
            x=10,
            z=2,
            y=30 * i - 30
        )
        backgrounds.extend([left, right])
    return backgrounds


backgrounds = create_background()


# Дорожные сегменты (6 полос)
def create_road():
    road_segments = []
    for i in range(4):  # Увеличиваем количество сегментов
        road = Entity(
            model='quad',
            texture='assets/roads.png',  # Текстура с 6 полосами
            scale=(12, 30),  # Шире и выше
            z=1,
            y=30 * i - 30,
            collider='box'  # Коллайдер для всей дороги
        )



        road_segments.append(road)
    return road_segments


road_segments = create_road()

# Интерфейс
health_bar = HealthBar(
    bar_color=color.red,
    roundness=0.5,
    value=lives * (100 / max_lives),
    max_value=100,
    position=(-0.7, 0.4),
    scale=(0.4, 0.05))

score_text = Text(
    text=f"Score: {score}",
    position=(-0.7, 0.35),
    scale=1.5,
    color=color.white)

speed_text = Text(
    text=f"Speed: {current_speed:.1f}",
    position=(-0.7, 0.3),
    scale=1.5,
    color=color.white)

boost_text = Text(
    text="",
    position=(0.7, 0.3),
    scale=1.5,
    color=color.cyan)

game_over_text = Text(
    text="GAME OVER\nPress R to restart\nESC to quit",
    position=(0, 0),
    scale=2,
    color=color.red,
    enabled=False)

enemies = []
bonuses = []


class Bonus(Entity):
    def __init__(self, bonus_type, **kwargs):
        super().__init__(
            model='quad',
            texture=bonus_textures[bonus_type],
            scale=0.8,
            collider='box',
            bonus_type=bonus_type,
            **kwargs
        )
        self.y = 50
        self.x = random.choice(LANE_POSITIONS)
        self.speed = current_speed * 1.2


def newEnemy():
    if not game_active or len(enemies) > 10:
        return

    # Машины появляются только на полосах
    lane = random.choice(LANE_POSITIONS)
    new = duplicate(
        car,
        texture='assets/car3.png',
        x=lane,
        y=50,
        color=color.random_color(),
        rotation_z=90 if lane < 0 else -90,
        collider='box',
        scale=(2, 1.3)
    )
    enemies.append(new)
    invoke(newEnemy, delay=max(0.2, 0.8 - (current_speed - base_speed) / 20))  # Чаще спавн


def spawn_bonus():
    if not game_active or len(bonuses) > 2:
        return

    bonus_type = random.choice(['health', 'speed'])
    bonus = Bonus(bonus_type)
    bonuses.append(bonus)
    invoke(spawn_bonus, delay=random.uniform(8, 15))  # Чаще бонусы


def activate_speed_boost():
    global current_speed, speed_boost_active, speed_boost_end_time
    speed_boost_active = True
    current_speed = min(max_speed, current_speed * 1.5)
    speed_boost_end_time = time.time() + 5
    boost_text.text = "BOOST!"
    boost_text.color = color.cyan


def deactivate_speed_boost():
    global current_speed, speed_boost_active
    speed_boost_active = False
    current_speed = base_speed + (time.time() - start_time) * speed_increase_rate
    boost_text.text = ""


def update():
    global current_speed, lives, game_active, score, last_collision_time, speed_boost_active

    # Выход по ESC
    if held_keys['escape']:
        application.quit()
        return

    if not game_active:
        if held_keys['r']:
            reset_game()
        return

    # Увеличение сложности
    elapsed_time = time.time() - start_time
    if not speed_boost_active:
        current_speed = min(max_speed, base_speed + elapsed_time * speed_increase_rate)
    elif time.time() > speed_boost_end_time:
        deactivate_speed_boost()

    # Управление машиной (переключение полос)
    if held_keys['a'] and car.x > min(LANE_POSITIONS):
        car.x -= 5 * time.dt
    if held_keys['d'] and car.x < max(LANE_POSITIONS):
        car.x += 5 * time.dt

    # Движение всех элементов
    for bg in backgrounds:
        bg.y -= current_speed * time.dt
        if bg.y < -60:
            bg.y += 120

    for road in road_segments:
        road.y -= current_speed * time.dt
        if road.y < -60:
            road.y += 120
            score += 1
            score_text.text = f"Score: {score}"

    # Движение врагов и бонусов
    for enemy in enemies[:]:
        enemy.y -= current_speed * 1.3 * time.dt
        if enemy.y < -15:
            enemies.remove(enemy)
            destroy(enemy)

    for bonus in bonuses[:]:
        bonus.y -= current_speed * 1.1 * time.dt
        if bonus.y < -15:
            bonuses.remove(bonus)
            destroy(bonus)

    # Обновление UI
    speed_text.text = f"Speed: {current_speed:.1f}"

    # Проверка столкновений
    now = time.time()
    for enemy in enemies:
        if car.intersects(enemy).hit and now - last_collision_time > collision_cooldown:
            handle_collision()
            last_collision_time = now
            break

    # Проверка бонусов
    for bonus in bonuses[:]:
        if car.intersects(bonus).hit:
            handle_bonus(bonus)
            bonuses.remove(bonus)
            destroy(bonus)


def handle_bonus(bonus):
    global lives
    bonus_sound.play()

    if bonus.bonus_type == 'health':
        lives = min(lives + 1, max_lives)
        health_bar.value = lives * (100 / max_lives)
    elif bonus.bonus_type == 'speed':
        activate_speed_boost()


def handle_collision():
    global lives, game_active
    collision_sound.play()
    car.shake(duration=0.5)
    lives -= 1
    health_bar.value = lives * (100 / max_lives)

    if lives <= 0:
        game_over()
    else:
        original_color = car.color
        car.color = color.red
        invoke(setattr, car, 'color', original_color, delay=0.3)


def game_over():
    global game_active
    game_active = False
    game_over_sound.play()
    game_over_text.enabled = True
    background_music.stop()


def reset_game():
    global current_speed, lives, game_active, score, start_time, speed_boost_active

    # Очистка
    for enemy in enemies[:]:
        enemies.remove(enemy)
        destroy(enemy)
    for bonus in bonuses[:]:
        bonuses.remove(bonus)
        destroy(bonus)

    # Сброс параметров
    current_speed = base_speed
    lives = 3
    score = 0
    game_active = True
    start_time = time.time()
    speed_boost_active = False

    # Сброс позиций
    for i, road in enumerate(road_segments):
        road.y = 30 * i - 30
    for i, bg in enumerate(backgrounds):
        bg.y = 30 * (i // 2) - 30

    # Сброс машины
    car.x = LANE_POSITIONS[2]

    # Сброс UI
    health_bar.value = lives * (100 / max_lives)
    score_text.text = f"Score: {score}"
    speed_text.text = f"Speed: {current_speed:.1f}"
    game_over_text.enabled = False
    boost_text.text = ""

    # Перезапуск
    background_music.play()
    invoke(newEnemy, delay=0.5)
    invoke(spawn_bonus, delay=3.0)


# Начало игры
reset_game()

app.run()