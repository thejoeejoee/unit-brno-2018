import numpy as np


class Erosion(object):
    def __init__(self, img, minsize=10):
        self.len_x = len(img)
        self.len_y = len(img[0])
        self.img = img
        self.minsize = minsize

    def filter(self):
        for i in range(2):
            for x in range(self.len_x):
                for y in range(self.len_y):
                    if img[x][y]:
                        cnt_x = 0
                        move_x_minus = True
                        move_x_plus = True
                        for xx in range(self.minsize):
                            if x - xx >= 0 and move_x_minus and img[x - xx][y]:
                                cnt_x += 1
                            else:
                                move_x_minus = False

                            if x + xx < self.len_x and move_x_plus and img[x + xx][y]:
                                cnt_x += 1
                            else:
                                move_x_plus = False

                            if cnt_x >= self.minsize or not (move_x_plus or move_x_minus):
                                break

                        cnt_y = 0
                        move_y_minus = True
                        move_y_plus = True
                        for yy in range(self.minsize):
                            if y - yy >= 0 and move_y_minus and img[x][y - yy]:
                                cnt_y += 1
                            else:
                                move_y_minus = False

                            if y + yy < self.len_y and move_y_plus and img[x][y + yy]:
                                cnt_y += 1
                            else:
                                move_y_plus = False

                            if cnt_y >= self.minsize or not (move_y_plus or move_y_minus):
                                break

                        if cnt_x < self.minsize or cnt_y < self.minsize:
                            img[x][y] = False

        return img


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
        ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
        #['.','.','.','.','.','.','.','.','.','.','.','.','.','.','.','.'],
        ['.', '.', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', '.', '.', '.', '.'],
    ]

    img = from_ascii_to_bool(img)
    ascii_plot(img)
    erosion = Erosion(img)
    img = erosion.filter()
    ascii_plot(img)
