import arcade
import random
from level import Level

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

ROWS = 16
COLS = 32

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, "EyeTrainer", False)
        arcade.set_background_color(arcade.color.BLACK)
        self.cycle_time = 5

    def setup(self):
        self.level = Level(ROWS, COLS, [3,1,1,2], self.get_size)
        self.time_since_start = 0
        self.t = 0
        self.running = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.t > 1/3 and self.t < 2/3:
            self.level.on_press()
        elif key == arcade.key.ESCAPE:
            if self.running:
                self.running = False
            else:
                self.setup()

    def on_draw(self):
        arcade.start_render()
        if self.running:
            if self.t < 1/3:
                self.level.draw_center()
            elif self.t < 2/3:
                self.level.draw_current_test()
        else:
            self.level.draw_score()

    def update(self, delta_time):
        if self.running:
            self.time_since_start += delta_time
            last_t = self.t
            self.t = (self.time_since_start %
                      self.cycle_time) / self.cycle_time
            if self.t > 1/3 and last_t < 1/3:
                self.level.start_next_test()
            if self.t > 2/3 and last_t < 2/3:
                self.level.end_test()


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
