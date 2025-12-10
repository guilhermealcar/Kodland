import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Roguelike Minimal - DEMO"

TILE = 40

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

        # --- SPRITE LISTAS ---
        self.hero_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList()

        # Player
        self.hero = arcade.Sprite("images/hero.png", scale=2)
        self.hero.center_x = TILE * 2
        self.hero.center_y = TILE * 2
        self.hero_list.append(self.hero)

        # Som
        self.sound = arcade.load_sound("sounds/computerNoise_000.ogg")

        # Movimento
        self.speed = 4
        self.dx = 0
        self.dy = 0

        # Score
        self.score = 0

        # Cria paredes
        self.create_walls()

        # Cria moedas
        self.create_coins(5)

        self.game_over = False

    def create_walls(self):
        # Moldura externa
        for x in range(0, SCREEN_WIDTH, TILE):
            wall = arcade.SpriteSolidColor(TILE, TILE, arcade.color.GRAY)
            wall.center_x = x + TILE / 2
            wall.center_y = SCREEN_HEIGHT - TILE / 2
            self.wall_list.append(wall)

            wall = arcade.SpriteSolidColor(TILE, TILE, arcade.color.GRAY)
            wall.center_x = x + TILE / 2
            wall.center_y = TILE / 2
            self.wall_list.append(wall)

        for y in range(0, SCREEN_HEIGHT, TILE):
            wall = arcade.SpriteSolidColor(TILE, TILE, arcade.color.GRAY)
            wall.center_x = TILE / 2
            wall.center_y = y + TILE / 2
            self.wall_list.append(wall)

            wall = arcade.SpriteSolidColor(TILE, TILE, arcade.color.GRAY)
            wall.center_x = SCREEN_WIDTH - TILE / 2
            wall.center_y = y + TILE / 2
            self.wall_list.append(wall)

        # Obstáculos internos simples
        for i in range(4, 14):
            wall = arcade.SpriteSolidColor(TILE, TILE, arcade.color.GRAY)
            wall.center_x = i * TILE
            wall.center_y = TILE * 6
            self.wall_list.append(wall)

    def create_coins(self, qty):
        for _ in range(qty):
            coin = arcade.SpriteSolidColor(TILE // 2, TILE // 2, arcade.color.GOLD)
            coin.center_x = random.randrange(TILE * 2, SCREEN_WIDTH - TILE * 2)
            coin.center_y = random.randrange(TILE * 2, SCREEN_HEIGHT - TILE * 2)

            # garantindo que não nasce dentro da parede
            if not arcade.check_for_collision_with_list(coin, self.wall_list):
                self.coin_list.append(coin)

    def on_draw(self):
        self.clear()

        self.wall_list.draw()
        self.coin_list.draw()
        self.hero_list.draw()

        arcade.draw_text(f"Score: {self.score}", 20, SCREEN_HEIGHT - 40,
                         arcade.color.WHITE, font_size=18)

        if self.game_over:
            arcade.draw_text("🎉 VITÓRIA! Você coletou tudo! 🎉",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                             arcade.color.YELLOW, 24, anchor_x="center")

    def on_update(self, delta_time):
        if self.game_over:
            return

        self.hero.center_x += self.dx
        if arcade.check_for_collision_with_list(self.hero, self.wall_list):
            self.hero.center_x -= self.dx

        self.hero.center_y += self.dy
        if arcade.check_for_collision_with_list(self.hero, self.wall_list):
            self.hero.center_y -= self.dy

        coins_hit = arcade.check_for_collision_with_list(self.hero, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(self.sound)

        if self.score >= 5 and len(self.coin_list) == 0:
            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.dy = self.speed
        elif key == arcade.key.S:
            self.dy = -self.speed
        elif key == arcade.key.A:
            self.dx = -self.speed
        elif key == arcade.key.D:
            self.dx = self.speed

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.dy = 0
        if key in (arcade.key.A, arcade.key.D):
            self.dx = 0


if __name__ == "__main__":
    Game()
    arcade.run()
