import arcade
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height, "EyeTrainer", True)
        arcade.set_background_color(arcade.color.BLACK)
        self.rows = 16
        self.cols = 32
        self.cycle_time = 5
        self.center_enabled = False
        self.pressed = False
        self.score_text = ""
        self.all_quadrants = [(0, -1, 1), (1, 1, 1), (2, 1, -1), (3, -1, -1)]

    def cell_to_pixel(self, x, y):
        i, j = x + self.cols, y + self.rows
        w, h = self.get_size()
        return i / (self.cols * 2 + 1) * w, j / (self.rows * 2 + 1) * h

    def draw_square(self, x, y, color):
        left, top = self.cell_to_pixel(x, y)
        right, bottom = self.cell_to_pixel(x + 1, y - 1)
        arcade.draw_lrtb_rectangle_filled(left, right, top, bottom, color)

    def setup(self):
        self.time_since_start = 0
        self.t = 0
        self.count_pressed = [0] * 4
        self.count_occured = [0] * 4
        self.scores = [0] * 4
        self.running = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.t > 1/3 and self.t < 2/3:
            self.pressed = True
        elif key == arcade.key.ESCAPE:
            if self.running:
                self.running = False
            else:
                self.setup()

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        if self.running:
            if self.t < 2/3:
                self.draw_square(self.x, self.y, arcade.color.WHITE)
        else:
            for score, q in zip(self.scores, self.all_quadrants):
                x,y = self.cell_to_pixel(self.cols / 2 * q[1], self.rows / 2 * q[2])
                arcade.draw_text("{:.2f}%".format(score), x, y, arcade.color.WHITE, 32, align="center", anchor_x="center", anchor_y="center")

    def get_quadrant(self):
        return random.choices(self.all_quadrants, [3, 1, 1, 2])[0]

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        
        if self.running:
            self.time_since_start += delta_time
            last_t = self.t
            self.t = (self.time_since_start % self.cycle_time) / self.cycle_time

            if self.t < 1/3:
                self.x = 0
                self.y = 0
            if self.t > 1/3 and last_t < 1/3:
                self.q = self.get_quadrant()
                self.x = random.randrange(1, self.cols) * self.q[1]
                self.y = random.randrange(1, self.rows) * self.q[2]
            if self.t > 2/3 and last_t < 2/3:
                if self.pressed:
                    self.count_pressed[self.q[0]] += 1
                self.count_occured[self.q[0]] += 1
                self.pressed = False
        else:
            self.scores = [pressed * 100 / occured if occured > 0 else 0 for pressed, occured in zip(self.count_pressed, self.count_occured)]


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
