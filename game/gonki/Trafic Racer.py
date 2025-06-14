from ursina import *  #импортирую основной модуль Ursina
from ursina.prefabs.health_bar import HealthBar  #импортирую компонент здоровья
import random  #использую для генерации случайных чисел
import time  #использую для работы со временем

#инициализирую игровой движок
app = Ursina()
window.title = 'Trafic Racer 2D'  #заголовок окна
window.borderless = False  #показать границы окна
window.fullscreen = True  #полноэкранный режим
window.exit_button.visible = False  #скрыть кнопку выхода

# --- НАСТРОЙКА КАМЕРЫ ---
camera.orthographic = True  #ортографическая проекция
camera.fov = 40  #угол обзора камеры

# --- ЗВУКОВЫЕ ЭФФЕКТЫ ---
try:
    #загрузка звуков с обработкой ошибок
    collision_sound = Audio('assets/collision.wav', autoplay=False, loop=False)
    background_music = Audio('assets/background_music.wav', autoplay=True, loop=True)
    game_over_sound = Audio('assets/game_over.wav', autoplay=False, loop=False)
    bonus_sound = Audio('assets/bonus.mp3', autoplay=False, loop=False)
    finish_sound = Audio('assets/finish.mp3', autoplay=False, loop=False)

    #настройка громкости каждого из звуков
    background_music.volume = 0.5
    collision_sound.volume = 0.7
    game_over_sound.volume = 0.8
    bonus_sound.volume = 0.8
    finish_sound.volume = 0.8
except:
    print("Не удалось загрузить звуки. Продолжаем без звуков.")

# --- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ И НАСТРОЙКИ ---
base_speed = 8  #начальная скорость движения
current_speed = base_speed  #текущая скорость
speed_increase_rate = 0.05  #скорость с которой повышается сложность
max_speed = 25  #максимальная скорость
lives = 3  #жизни игрока
max_lives = 5  #максимальное количество жизней
score = 0  #счет игрока
game_active = True  #состояние игры
start_time = time.time()  #время начала игры
last_collision_time = 0  #время последнего столкновения
collision_cooldown = 1.0  #задержка между столкновениями
speed_boost_active = False  #флаг нитро-ускорения
speed_boost_end_time = 0  #время окончания ускорения
finish_reached = False  #флаг достижения финиша

# --- КОНФИГУРАЦИЯ ДОРОГИ ---
LANE_WIDTH = 1.5  #ширина полосы
LANE_POSITIONS = [-5.15, -3.0, -0.85, 0.85, 3.0, 5.15]  #позиции 6 полос

# --- СОЗДАНИЕ ИГРОВЫХ ОБЪЕКТОВ ---

enemy_car_textures = [
    'assets/car3.png',
    'assets/4x4.png',
    'assets/cabrio.png',
    'assets/escavator.png',
    'assets/gruzovik.png',
    'assets/pickup.png'
]

#машина игрока
car = Entity(
    model='quad',  #стандартная модель
    texture='assets/car_g.png',  #текстура машины
    collider='box',  #коллайдер для столкновений
    scale=(2, 1.3),  #размер машины
    rotation_z=-90,  #поворот(горизонтально)
    y=-3,  #позиция по Y
    x=LANE_POSITIONS[2]  #стартовая полоса (центральная)
)

#текстуры для бонусов
bonus_textures = {
    'health': 'assets/health.png',  #бонус здоровья
    'speed': 'assets/nitro.png'  #бонус ускорения
}


#функция для создания фона
def create_background():
    backgrounds = []
    for i in range(4):  #создаем 4 слоя фона
        #левый фон
        left = Entity(
            model='quad',
            texture='assets/city1.png',
            scale=(10, 30),
            x=-10,
            z=2,
            y=30 * i - 30
        )
        #правый фон
        right = Entity(
            model='quad',
            texture='assets/city2.png',
            scale=(10, 30),
            x=10,
            z=2,
            y=30 * i - 30
        )
        backgrounds.extend([left, right])
    return backgrounds


backgrounds = create_background()  #инициализация фона


#функция создания дороги
def create_road():
    road_segments = []
    for i in range(4):
        road = Entity(
            model='quad',
            texture='assets/roadnew.png',
            scale=(12, 30),
            z=1,
            y=30 * i - 30,
            collider='box',
            texture_scale=(2, 1)  #добавляем повторение текстуры 2 раза по горизонтали
        )
        road_segments.append(road)
    return road_segments


road_segments = create_road()  #инициализация дороги

# --- ИНТЕРФЕЙС ПОЛЬЗОВАТЕЛЯ ---

#панель здоровья
health_bar = HealthBar(
    bar_color=color.red,
    roundness=0.5,
    value=lives * (100 / max_lives),
    max_value=100,
    position=(-0.8, 0.4),
    scale=(0.4, 0.05))

#текст счета
score_text = Text(
    text=f"Score: {score}",
    position=(-0.8, 0.35),
    scale=1.5,
    color=color.white)

#текст скорости
speed_text = Text(
    text=f"Speed: {current_speed:.1f}",
    position=(-0.8, 0.3),
    scale=1.5,
    color=color.white)

#индикатор ускорения
boost_text = Text(
    text="",
    position=(0.7, 0.3),
    scale=1.5,
    color=color.cyan)

#текст "Игра окончена"
game_over_text = Text(
    text="GAME OVER\nPress R to restart\nESC to quit",
    position=(0, 0.1),
    scale=2,
    color=color.red,
    origin=(0, 0),
    enabled=False)  #скрыт по умолчанию

#текст финиша
finish_text = Text(
    text="FINISH!\nThanks for playing my game",
    position=(0, 0.1),
    scale=2,
    color=color.green,
    origin=(0, 0),
    enabled=False)  #скрыт по умолчанию

#списки для врагов и бонусов
enemies = []
bonuses = []


#класс для бонусов
class Bonus(Entity):
    def __init__(self, bonus_type, **kwargs):
        super().__init__(
            model='quad',
            texture=bonus_textures[bonus_type],  #выбор текстуры исходя из типа бонуса
            scale=0.8,
            collider='box',
            bonus_type=bonus_type,  #тип бонуса(health/speed)
            **kwargs
        )
        self.y = 50  #начальная позиция сверху экрана
        self.x = random.choice(LANE_POSITIONS)  #случайная полоса
        self.speed = current_speed * 1.2  #скорость движения


# --- ФУНКЦИИ ГЕЙМПЛЕЯ ---

#создание вражеской машины
def newEnemy():
    if not game_active or len(enemies) > 10 or finish_reached:
        return

    lane = random.choice(LANE_POSITIONS)
    texture = random.choice(enemy_car_textures)  #случайный выбор текстуры

    #определяем направление вращения в зависимости от полосы
    rotation = 90 if lane < 0 else -90

    new = duplicate(
        car,
        texture=texture,  #используем случайную текстуру
        x=lane,
        y=50,
        color=color.white,
        rotation_z=rotation,
        collider='box',
        scale=(2, 1.3))
    enemies.append(new)
    invoke(newEnemy, delay=max(0.2, 0.8 - (current_speed - base_speed) / 20))


#создание бонуса
def spawn_bonus():
    #проверка условий для создания
    if not game_active or len(bonuses) > 2 or finish_reached:
        return

    #случайный выбор типа бонуса
    bonus_type = random.choice(['health', 'speed'])
    bonus = Bonus(bonus_type)
    bonuses.append(bonus)
    #рекурсивный вызов со случайной задержкой
    invoke(spawn_bonus, delay=random.uniform(8, 15))


#активация ускорения
def activate_speed_boost():
    global current_speed, speed_boost_active, speed_boost_end_time
    speed_boost_active = True
    current_speed = min(max_speed, current_speed * 1.5)  #увеличение скорости
    speed_boost_end_time = time.time() + 5  #длительность 5 секунд
    boost_text.text = "BOOST!"  #обновление интерфейса
    boost_text.color = color.cyan


#деактивация ускорения
def deactivate_speed_boost():
    global current_speed, speed_boost_active
    speed_boost_active = False
    #возврат к нормальной скорости
    current_speed = base_speed + (time.time() - start_time) * speed_increase_rate
    boost_text.text = ""  #сброс текста


#проверка достижения финиша
def check_finish():
    global finish_reached, game_active
    if current_speed >= 20 and not finish_reached:
        finish_reached = True
        game_active = False
        finish_sound.play()  #звук финиша
        finish_text.enabled = True  # показ текста
        background_music.stop()  #остановка музыки


#основной игровой цикл
def update():
    global current_speed, lives, game_active, score, last_collision_time, speed_boost_active

    #выход по клавише ESC
    if held_keys['escape']:
        application.quit()
        return

    #рестарт по клавише R
    if not game_active:
        if held_keys['r']:
            reset_game()
        return

    # --- РАСЧЕТ СКОРОСТИ ---
    elapsed_time = time.time() - start_time
    if not speed_boost_active:
        #постепенное увеличение скорости
        current_speed = min(max_speed, base_speed + elapsed_time * speed_increase_rate)
    elif time.time() > speed_boost_end_time:
        deactivate_speed_boost()

    #проверка финиша
    check_finish()

    # --- УПРАВЛЕНИЕ МАШИНОЙ ---
    #движение влево (клавиша A)
    if held_keys['a'] and car.x > min(LANE_POSITIONS):
        car.x -= 5 * time.dt
    #движение вправо (клавиша D)
    if held_keys['d'] and car.x < max(LANE_POSITIONS):
        car.x += 5 * time.dt

    # --- ДВИЖЕНИЕ ОКРУЖЕНИЯ ---
    #фон
    for bg in backgrounds:
        bg.y -= current_speed * time.dt
        if bg.y < -60:  #перемещение в начало при выходе за экран
            bg.y += 120

    #дорога
    for road in road_segments:
        road.y -= current_speed * time.dt
        if road.y < -60:
            road.y += 120
            score += 1  #увеличение счета
            score_text.text = f"Score: {score}"  #обновление текста

    # --- ДВИЖЕНИЕ ОБЪЕКТОВ ---
    #вражеские машины
    for enemy in enemies[:]:  #копия списка для безопасного удаления
        enemy.y -= current_speed * 1.3 * time.dt
        if enemy.y < -15:  #удаление при выходе за экран
            enemies.remove(enemy)
            destroy(enemy)

    #бонусы
    for bonus in bonuses[:]:
        bonus.y -= current_speed * 1.1 * time.dt
        if bonus.y < -15:
            bonuses.remove(bonus)
            destroy(bonus)

    #обновление текста скорости
    speed_text.text = f"Speed: {current_speed:.1f}"

    # --- ОБРАБОТКА СТОЛКНОВЕНИЙ ---
    now = time.time()
    for enemy in enemies:
        #проверка коллизии с задержкой
        if car.intersects(enemy).hit and now - last_collision_time > collision_cooldown:
            handle_collision()
            last_collision_time = now
            break  #одно столкновение за раз

    # --- СБОР БОНУСОВ ---
    for bonus in bonuses[:]:
        if car.intersects(bonus).hit:
            handle_bonus(bonus)
            bonuses.remove(bonus)
            destroy(bonus)


#обработка столкновения с врагом
def handle_collision():
    global lives, game_active
    collision_sound.play()  #звук столкновения
    car.shake(duration=0.5)  #эффект тряски
    lives -= 1  #потеря жизни
    health_bar.value = lives * (100 / max_lives)  #обновление здоровья

    #проверка на проигрыш
    if lives <= 0:
        game_over()
    else:
        #визуальная обратная связь
        original_color = car.color
        car.color = color.red
        invoke(setattr, car, 'color', original_color, delay=0.3)


#обработка сбора бонуса
def handle_bonus(bonus):
    global lives
    bonus_sound.play()  #звук бонуса

    if bonus.bonus_type == 'health':
        #добавление жизни
        lives = min(lives + 1, max_lives)
        health_bar.value = lives * (100 / max_lives)
    elif bonus.bonus_type == 'speed':
        #активация ускорения
        activate_speed_boost()


#окончание игры
def game_over():
    global game_active
    game_active = False
    game_over_sound.play()  #звук проигрыша
    game_over_text.enabled = True  #показ текста
    background_music.stop()  #остановка музыки


#сброс игры
def reset_game():
    global current_speed, lives, game_active, score, start_time, speed_boost_active, finish_reached

    #очистка объектов
    for enemy in enemies[:]:
        enemies.remove(enemy)
        destroy(enemy)
    for bonus in bonuses[:]:
        bonuses.remove(bonus)
        destroy(bonus)

    #сброс переменных
    current_speed = base_speed
    lives = 3
    score = 0
    game_active = True
    start_time = time.time()
    speed_boost_active = False
    finish_reached = False

    #сброс позиций
    for i, road in enumerate(road_segments):
        road.y = 30 * i - 30
    for i, bg in enumerate(backgrounds):
        bg.y = 30 * (i // 2) - 30

    #сброс позиции игрока
    car.x = LANE_POSITIONS[2]

    #сброс интерфейса
    health_bar.value = lives * (100 / max_lives)
    score_text.text = f"Score: {score}"
    speed_text.text = f"Speed: {current_speed:.1f}"
    game_over_text.enabled = False
    finish_text.enabled = False
    boost_text.text = ""

    #запуск генераторов
    background_music.play()
    invoke(newEnemy, delay=0.5)
    invoke(spawn_bonus, delay=3.0)


# --- ЗАПУСК ИГРЫ ---
reset_game()  #инициализация игры
app.run()  #запуск игрового цикла