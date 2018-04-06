import numpy as np
import copy


class Erosion(object):
    def __init__(self, img, minsize=10):
        self.len_x = len(img)
        self.len_y = len(img[0])
        self.img = img
        self.minsize = minsize

    def filter(self):
        out = copy.deepcopy(img)
        for x in range(len_x):
            for y in range(len_y):
                if img[x][y]:
                    cnt_x = 0
                    move_x_minus = True
                    move_x_plus = True
                    for xx in range(self.minsize):
                        if any((
                            x - xx >= 0 and move_x_minus and img[x - xx][y],
                            x + xx < self.len_x and move_x_plus and img[x + xx][y]
                        )):
                            cnt_x += 1
                        else:
                            move_x_minus = False

                        if cnt_x >= self.minsize or not (move_x_plus or move_x_minus):
                            break

                    cnt_y = 0
                    move_y_minus = True
                    move_y_plus = True
                    for yy in range(self.minsize):
                        if any((
                            y - yy >= 0 and move_y_minus and img[x][y - yy],
                            y + yy < self.len_y and move_y_plus and img[x][y + yy]
                        )):
                            cnt_y += 1
                        else:
                            move_x_minus = False

                        if cnt_y >= self.minsize or not (move_y_plus or move_y_minus):
                            break

                    if cnt_x < self.minsize and cnt_y < self.minsize:
                        out[x][y] = False

        return out




if __name__ == '__main__':
    pass
