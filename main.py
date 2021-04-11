import arcade
import random
from level import Level

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ROWS = 16
COLS = 32

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        if key == arcade.key.R:
            self.window.show_view(GameView())

    def on_draw(self):
        arcade.start_render()
        self.game_view.level.draw_score(self.window.get_size())

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.cycle_time = 5
        self.level = Level(ROWS, COLS, [3,1,1,2])
        self.time_since_start = 0
        self.t = 0

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.t > 1/3 and self.t < 2/3:
            self.level.on_press()
        elif key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self))

    def on_draw(self):
        arcade.start_render()
        if self.t < 1/3:
            self.level.draw_center(self.window.get_size())
        elif self.t < 2/3:
            self.level.draw_current_test(self.window.get_size())

    def update(self, delta_time):
        self.time_since_start += delta_time
        last_t = self.t
        self.t = (self.time_since_start %
                    self.cycle_time) / self.cycle_time
        if self.t > 1/3 and last_t < 1/3:
            self.level.start_next_test()
        if self.t > 2/3 and last_t < 2/3:
            self.level.end_test()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.show_view(GameView())
    arcade.run()

if __name__ == "__main__":
    main()
