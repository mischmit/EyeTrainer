import arcade
import random

ALL_QUADRANTS = [(-1, 1), (1, 1), (1, -1), (-1, -1)]


def count_pressed(tests):
    result = {}
    for test in tests:
        result[(test.x, test.y)]


class TestTemplate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.count_total = 0
        self.count_hit = 0
        self.count_missed = 0

    def hit(self):
        self.count_hit += 1

    def missed(self):
        self.count_missed += 1

    def is_quadrant(self, quadrant):
        return self.x * quadrant[0] > 0 and self.y * quadrant[1] > 0


class Test:
    def __init__(self, template):
        self.template = template
        self.pressed = None
        self.template.count_total += 1

    def press(self):
        self.pressed = True

    def done(self):
        if self.pressed is None:
            self.pressed = False
        if self.pressed:
            self.template.hit()
        else:
            self.template.missed()


class Level:
    def __init__(self, rows, cols, quadrant_frequency):
        self.rows = rows
        self.cols = cols
        self.tests = []
        self.test_templates = []
        for quadrant, frequency in zip(ALL_QUADRANTS, quadrant_frequency):
            for x in range(1, cols + 1):
                for y in range(1, rows + 1):
                    template = TestTemplate(x * quadrant[0], y * quadrant[1])
                    self.test_templates.append(template)
                    self.tests += [Test(template) for x in range(frequency)]
        random.shuffle(self.tests)
        self.current_test_index = 0

    def current_test(self):
        return self.tests[self.current_test_index]

    def cell_to_pixel(self, x, y, size):
        i, j = x + self.cols, y + self.rows + 1
        w, h = size
        return i / (self.cols * 2 + 1) * w, j / (self.rows * 2 + 1) * h

    def draw_test_template(self, test, size):
        self.draw_square(test.x, test.y, arcade.color.WHITE, size)

    def draw_current_test(self, size):
        self.draw_test_template(self.current_test().template, size)

    def draw_center(self, size):
        self.draw_square(0, 0, arcade.color.WHITE, size)

    def draw_square(self, x, y, color, size):
        left, top = self.cell_to_pixel(x, y, size)
        right, bottom = self.cell_to_pixel(x + 1, y - 1, size)
        arcade.draw_lrtb_rectangle_filled(left, right, top, bottom, color)

    def draw_score(self, size):
        for t in self.test_templates:
            r = 255 * t.count_missed / t.count_total
            g = 255 * t.count_hit / t.count_total
            self.draw_square(t.x, t.y, (r, g, 50), size)

        for score, q in zip(self.sum_scores(), ALL_QUADRANTS):
            x, y = self.cell_to_pixel(
                (self.cols + 1)/ 2 * q[0] + 0.5, (self.rows + 1) / 2 * q[1] - 0.5, size)
            played_count = score[1] + score[2]
            if played_count == 0:
                hit_ratio = 0
            else:
                hit_ratio = 100 * score[1] / played_count
            arcade.draw_text("Hit {:.2f}%".format(hit_ratio), x, y, arcade.color.WHITE,
                             32, align="center", anchor_x="center", anchor_y="center")
            played_ratio = 100 * played_count / score[0]
            arcade.draw_text("Completed {:.2f}%".format(played_ratio), x, y - 50, arcade.color.WHITE,
                             32, align="center", anchor_x="center", anchor_y="center")

    def start_next_test(self):
        if not(self.is_done()):
            self.current_test_index += 1

    def on_press(self):
        self.current_test().press()

    def end_test(self):
        self.current_test().done()

    def is_done(self):
        return self.current_test_index >= len(self.tests) - 1

    def sum_scores(self):
        return [self.sum_scores_per_quadrant(q) for q in ALL_QUADRANTS]

    def get_templates_for_quadrant(self, quadrant):
        return [t for t in self.test_templates if t.is_quadrant(quadrant)]

    def sum_scores_per_quadrant(self, quadrant):
        count_total = 0
        count_hit = 0
        count_missed = 0
        for t in self.get_templates_for_quadrant(quadrant):
            count_total += t.count_total
            count_hit += t.count_hit
            count_missed += t.count_missed
        return (count_total, count_hit, count_missed)
