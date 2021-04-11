import arcade
import random
from level import Level
from datetime import timedelta

START_CENTER = 0/8
END_CENTER = 3/8
START_TEST = 4/8
END_TEST = 7/8
ROWS = 16
COLS = 32

CYCLE_TIME = 4 # seconds

class ScoreView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(PauseView(self.game_view))

    def on_draw(self):
        arcade.start_render()
        self.game_view.level.draw_score(self.window.get_size())
        duration = timedelta(seconds=self.game_view.time_since_start)
        w, h = self.window.get_size()
        arcade.draw_text("Time elapsed: {}".format(str(duration)),
                         w/2,
                         50,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_key_press(self, key, modifiers):
        if not(self.game_view.level.is_done()) and key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        if key == arcade.key.S:
            self.window.show_view(ScoreView(self.game_view))
        if key == arcade.key.R:
            self.window.show_view(GameView())
        if key == arcade.key.Q:
            self.window.close()
        if key == arcade.key.F:
            self.window.set_fullscreen(True)
        if key == arcade.key.W:
            self.window.set_fullscreen(False)

    def on_draw(self):
        arcade.start_render()
        w, h = self.window.get_size()
        if not(self.game_view.level.is_done()):
            arcade.draw_text("Press Esc to continue",
                            w/2,
                            h/2,
                            arcade.color.WHITE,
                            font_size=20,
                            anchor_x="center")
        arcade.draw_text("Press S to show score",
                         w/2,
                         h/2-30,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press R to restart",
                         w/2,
                         h/2-60,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Q to quit",
                         w/2,
                         h/2-90,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press F for fullscreen / W for windowed mode",
                         w/2,
                         h/2-120,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("While playing, focus on the center and hit Space when you can see a square.",
                         w/2,
                         50,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)
        self.cycle_time = CYCLE_TIME
        self.level = Level(ROWS, COLS, [3, 1, 1, 2])
        self.time_since_start = 0
        self.t = 0

    def pause(self):
        self.window.show_view(PauseView(self))

    def show_score(self):
        self.window.show_view(ScoreView(self))

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE and self.t > 1/3 and self.t < 2/3:
            self.level.on_press()
        elif key == arcade.key.ESCAPE:
            self.pause()

    def on_draw(self):
        arcade.start_render()
        if START_CENTER < self.t and self.t < END_CENTER:
            self.level.draw_center(self.window.get_size())
        if START_TEST < self.t and self.t < END_TEST:
            self.level.draw_current_test(self.window.get_size())

    def update(self, delta_time):
        self.time_since_start += delta_time
        last_t = self.t
        self.t = (self.time_since_start %
                  self.cycle_time) / self.cycle_time
        if self.t > START_TEST and last_t < START_TEST:
            self.level.start_next_test()
        if self.t > END_TEST and last_t < END_TEST:
            self.level.end_test()
            if self.level.is_done():
                self.show_score()


def main():
    window = arcade.Window(1280, 720)
    window.show_view(PauseView(GameView()))
    arcade.run()


if __name__ == "__main__":
    main()
