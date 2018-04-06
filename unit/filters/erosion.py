import copy

import numpy as np


class Erosion(object):
    def __init__(self, img, minsize=10):
        self.len_x = len(img)
        self.len_y = len(img[0])
        self.img_orig = copy.deepcopy(img)
        self.img_tail = copy.deepcopy(img)
        self.img_mask = copy.deepcopy(img)
        self.minsize = minsize

    def filter_minsize(self):
        for i in range(2):
            for x in range(self.len_x):
                for y in range(self.len_y):
                    if self.img_mask[x][y]:
                        cnt_x = 0
                        move_x_minus = True
                        move_x_plus = True
                        for xx in range(self.minsize):
                            if move_x_minus and x - xx >= 0 and self.img_mask[x - xx][y]:
                                cnt_x += 1
                            else:
                                move_x_minus = False

                            if move_x_plus and x + xx < self.len_x and self.img_mask[x + xx][y]:
                                cnt_x += 1
                            else:
                                move_x_plus = False

                            if cnt_x - 1 >= self.minsize or not (move_x_plus or move_x_minus):
                                break

                        cnt_y = 0
                        move_y_minus = True
                        move_y_plus = True
                        for yy in range(self.minsize):
                            if move_y_minus and y - yy >= 0 and self.img_mask[x][y - yy]:
                                cnt_y += 1
                            else:
                                move_y_minus = False

                            if move_y_plus and y + yy < self.len_y and self.img_mask[x][y + yy]:
                                cnt_y += 1
                            else:
                                move_y_plus = False

                            if cnt_y - 1 >= self.minsize or not (move_y_plus or move_y_minus):
                                break

                        if cnt_x < self.minsize or cnt_y < self.minsize:
                            self.img_mask[x][y] = False
                        else:
                            self.img_tail[x][y] = False

    def tail_find(self, x, y):

        if not self.img_tail[x][y]:
            return set()

        tail_position = set()
        tail_position.add((x, y))
        self.img_tail[x][y] = False

        pos = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]

        for p in pos:
            if p[0] >= 0 and p[0] < self.len_x and p[1] >= 0 and p[1] < self.len_y:
                tail_position |= self.tail_find(p[0], p[1])

        return tail_position

    def filter_tail(self):
        tail_position = set()
        for x in range(self.len_x):
            for y in range(self.len_y):
                if self.img_tail[x][y]:
                    tail_position = self.tail_find(x, y)
                    for tail_xy in tail_position:
                        pos = [
                            (tail_xy[0] - 1, tail_xy[1]),
                            (tail_xy[0] + 1, tail_xy[1]),
                            (tail_xy[0], tail_xy[1] - 1),
                            (tail_xy[0], tail_xy[1] + 1),
                        ]

                        for p in pos:
                            if p[0] >= 0 and p[0] < self.len_x and p[1] >= 0 and p[1] < self.len_y:
                                if self.img_mask[p[0]][p[1]]:
                                    for xy in tail_position:
                                        self.img_mask[xy[0]][xy[1]] = True
                                    break

    def run(self):
        self.filter_minsize()
        self.filter_tail()
        return self.img_mask


if __name__ == '__main__':

    def from_ascii_to_bool(img):
        out = img
        for x in range(len(img)):
            for y in range(len(img[0])):
                out[x][y] = True if img[x][y] != '.' else False
        return out

    def ascii_plot(img):
        for x in range(len(img)):
            for y in range(len(img[0])):
                if img[x][y]:
                    print('H', end='')
                else:
                    print('.', end='')
            print('')
        print('=' * len(img[0]))

    img = [
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.'],
        ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', 'H', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', 'H', '.', 'H', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', 'H', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', 'H', 'H', 'H', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', 'H', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', 'H', 'H', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.', '.', '.'],
    ]

    img = from_ascii_to_bool(img)
    ascii_plot(img)
    erosion = Erosion(img)
    erosion.filter_minsize()
    ascii_plot(erosion.img_mask)
    ascii_plot(erosion.img_tail)
    erosion.filter_tail()
    ascii_plot(erosion.img_mask)
