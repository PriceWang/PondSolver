"""
Author: Guoxin Wang
Date: 2024-09-17 13:04:35
LastEditors: Guoxin Wang
LastEditTime: 2024-09-25 11:43:28
FilePath: \PondSolver\Game.py
Description: 

Copyright (c) 2024 by Guoxin Wang, All Rights Reserved. 
"""

import pygame

from Solver import solver


class Rect:
    def __init__(self, x_1: float, y_1: float, x_2: float = None, y_2: float = None):
        self.x_1 = x_1
        self.y_1 = y_1
        self.x_2 = x_2
        self.y_2 = y_2

    def point(self):
        return (self.x_1, self.y_1)

    def width(self):
        return self.x_2 - self.x_1

    def height(self):
        return self.y_2 - self.y_1


SIZE = {
    "bg": Rect(0, 0, 1000, 1624),
    "frame": Rect(90, 249, 910, 1069),
    "fish_nor": Rect(0, 0, 224, 112),
    "block_1_2_nor": Rect(0, 0, 220, 108),
    "block_1_3_nor": Rect(0, 0, 332, 108),
    "block_2_1_nor": Rect(0, 0, 108, 220),
    "block_3_1_nor": Rect(0, 0, 108, 332),
    "btn_reset": Rect(0, 0, 99, 99),
    "btn_solve": Rect(0, 0, 99, 99),
    "btn_exit": Rect(0, 0, 99, 99),
    "btn_home": Rect(0, 0, 99, 99),
    "btn_back": Rect(0, 0, 99, 99),
    "btn_forward": Rect(0, 0, 99, 99),
}


class Game:
    def __init__(self, current_w: float, current_h: float):
        # set relative value
        if current_w > current_h:
            screen_w = current_w / 5
            screen_h = current_w / 5 * (SIZE["bg"].height() / SIZE["bg"].width())
        else:
            screen_w = current_h / 5
            screen_h = current_h / 5 * (SIZE["bg"].height() / SIZE["bg"].width())
        self.grid_w = screen_w * (SIZE["frame"].width() / SIZE["bg"].width()) / 6
        self.anchor = Rect(
            screen_w * (SIZE["frame"].x_1 / SIZE["bg"].width()),
            screen_w * (SIZE["frame"].y_1 / SIZE["bg"].width()),
        )

        # load images and preset positions
        imgs_size = {
            "bg": Rect(0, 0, screen_w, screen_h),
            "frame": Rect(0, 0, screen_w, screen_h),
            "fish_nor": Rect(0, 0, self.grid_w * 2, self.grid_w),
            "block_1_2_nor": Rect(
                0,
                0,
                self.grid_w
                * (SIZE["block_1_2_nor"].width() / SIZE["fish_nor"].height()),
                self.grid_w
                * (SIZE["block_1_2_nor"].height() / SIZE["fish_nor"].height()),
            ),
            "block_1_3_nor": Rect(
                0,
                0,
                self.grid_w
                * (SIZE["block_1_3_nor"].width() / SIZE["fish_nor"].height()),
                self.grid_w
                * (SIZE["block_1_3_nor"].height() / SIZE["fish_nor"].height()),
            ),
            "block_2_1_nor": Rect(
                0,
                0,
                self.grid_w
                * (SIZE["block_2_1_nor"].width() / SIZE["fish_nor"].height()),
                self.grid_w
                * (SIZE["block_2_1_nor"].height() / SIZE["fish_nor"].height()),
            ),
            "block_3_1_nor": Rect(
                0,
                0,
                self.grid_w
                * (SIZE["block_3_1_nor"].width() / SIZE["fish_nor"].height()),
                self.grid_w
                * (SIZE["block_3_1_nor"].height() / SIZE["fish_nor"].height()),
            ),
            "btn_reset": Rect(0, 0, self.grid_w, self.grid_w),
            "btn_solve": Rect(0, 0, self.grid_w, self.grid_w),
            "btn_exit": Rect(0, 0, self.grid_w, self.grid_w),
            "btn_home": Rect(0, 0, self.grid_w, self.grid_w),
            "btn_back": Rect(0, 0, self.grid_w, self.grid_w),
            "btn_forward": Rect(0, 0, self.grid_w, self.grid_w),
        }
        self.imgs = self.load_imgs(imgs_size)
        self.init_pos = {
            "bg": Rect(0, 0, imgs_size["bg"].width(), imgs_size["bg"].height()),
            "frame": Rect(
                0, 0, imgs_size["frame"].width(), imgs_size["frame"].height()
            ),
            "fish_nor": Rect(
                self.anchor.x_1 + self.grid_w,
                self.anchor.y_1 + self.grid_w * 6.6,
                self.anchor.x_1 + self.grid_w + imgs_size["fish_nor"].width(),
                self.anchor.y_1 + self.grid_w * 6.6 + imgs_size["fish_nor"].height(),
            ),
            "block_1_2_nor": Rect(
                self.anchor.x_1 + self.grid_w,
                self.anchor.y_1 + self.grid_w * 7.6,
                self.anchor.x_1 + self.grid_w + imgs_size["block_1_2_nor"].width(),
                self.anchor.y_1
                + self.grid_w * 7.6
                + imgs_size["block_1_2_nor"].height(),
            ),
            "block_1_3_nor": Rect(
                self.anchor.x_1 + self.grid_w,
                self.anchor.y_1 + self.grid_w * 8.6,
                self.anchor.x_1 + self.grid_w + imgs_size["block_1_3_nor"].width(),
                self.anchor.y_1
                + self.grid_w * 8.6
                + imgs_size["block_1_3_nor"].height(),
            ),
            "block_2_1_nor": Rect(
                self.anchor.x_1 + self.grid_w * 3,
                self.anchor.y_1 + self.grid_w * 6.6,
                self.anchor.x_1 + self.grid_w * 3 + imgs_size["block_2_1_nor"].width(),
                self.anchor.y_1
                + self.grid_w * 6.6
                + imgs_size["block_2_1_nor"].height(),
            ),
            "block_3_1_nor": Rect(
                self.anchor.x_1 + self.grid_w * 4,
                self.anchor.y_1 + self.grid_w * 6.6,
                self.anchor.x_1 + self.grid_w * 4 + imgs_size["block_3_1_nor"].width(),
                self.anchor.y_1
                + self.grid_w * 6.6
                + imgs_size["block_3_1_nor"].height(),
            ),
            "btn_reset": Rect(
                self.anchor.x_1 + self.grid_w,
                self.anchor.y_1 - self.grid_w * 1.4,
                self.anchor.x_1 + self.grid_w + imgs_size["btn_reset"].width(),
                self.anchor.y_1 - self.grid_w * 1.4 + imgs_size["btn_reset"].height(),
            ),
            "btn_solve": Rect(
                self.anchor.x_1 + self.grid_w * 2.5,
                self.anchor.y_1 - self.grid_w * 1.4,
                self.anchor.x_1 + self.grid_w * 2.5 + imgs_size["btn_solve"].width(),
                self.anchor.y_1 - self.grid_w * 1.4 + imgs_size["btn_solve"].height(),
            ),
            "btn_exit": Rect(
                self.anchor.x_1 + self.grid_w * 4,
                self.anchor.y_1 - self.grid_w * 1.4,
                self.anchor.x_1 + self.grid_w * 4 + imgs_size["btn_exit"].width(),
                self.anchor.y_1 - self.grid_w * 1.4 + imgs_size["btn_exit"].height(),
            ),
        }
        self.solution_pos = {
            "bg": Rect(0, 0, imgs_size["bg"].width(), imgs_size["bg"].height()),
            "frame": Rect(
                0, 0, imgs_size["frame"].width(), imgs_size["frame"].height()
            ),
            "btn_home": Rect(
                self.anchor.x_1 + self.grid_w / 6,
                self.anchor.y_1 - self.grid_w * 1.4,
                self.anchor.x_1 + self.grid_w / 6 + imgs_size["btn_home"].width(),
                self.anchor.y_1 - self.grid_w * 1.4 + imgs_size["btn_home"].height(),
            ),
            "btn_back": Rect(
                self.anchor.x_1 + self.grid_w * 4 / 3,
                self.anchor.y_1 - self.grid_w * 1.4,
                self.anchor.x_1 + self.grid_w * 4 / 3 + imgs_size["btn_back"].width(),
                self.anchor.y_1 - self.grid_w * 1.4 + imgs_size["btn_back"].height(),
            ),
            "btn_forward": Rect(
                self.anchor.x_1 + self.grid_w * 2.5,
                self.anchor.y_1 - self.grid_w * 1.4,
                self.anchor.x_1 + self.grid_w * 2.5 + imgs_size["btn_forward"].width(),
                self.anchor.y_1 - self.grid_w * 1.4 + imgs_size["btn_forward"].height(),
            ),
            "btn_reset": Rect(
                self.anchor.x_1 + self.grid_w * 11 / 3,
                self.anchor.y_1 - self.grid_w * 1.4,
                self.anchor.x_1 + self.grid_w * 11 / 3 + imgs_size["btn_reset"].width(),
                self.anchor.y_1 - self.grid_w * 1.4 + imgs_size["btn_reset"].height(),
            ),
            "btn_exit": Rect(
                self.anchor.x_1 + self.grid_w * 29 / 6,
                self.anchor.y_1 - self.grid_w * 1.4,
                self.anchor.x_1 + self.grid_w * 29 / 6 + imgs_size["btn_exit"].width(),
                self.anchor.y_1 - self.grid_w * 1.4 + imgs_size["btn_exit"].height(),
            ),
            "msg_box": Rect(
                screen_w / 2,
                screen_h / 2 + self.anchor.y_1 / 2 + self.grid_w * 3,
            ),
        }

        # set parameters
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        pygame.display.set_caption("PondSolver")
        icon = pygame.image.load("assets/icon.png")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

        # init all flags
        self.run = True
        self.solution = False
        self.block_select = None, None, None
        self.blocks_place = {}
        self.board = [["0", "0", "0", "0", "0", "0"] for _ in range(6)]
        self.step_print = 0

    def reset(self):
        # reset all flags
        self.solution = False
        self.block_select = None, None, None
        self.blocks_place = {}
        self.board = [["0", "0", "0", "0", "0", "0"] for _ in range(6)]
        self.step_print = 0

    def load_imgs(self, imgs_size: dict):
        imgs = {}
        for img_name in imgs_size:
            img = pygame.image.load("assets/{}.png".format(img_name))
            img = pygame.transform.scale(
                img, (imgs_size[img_name].width(), imgs_size[img_name].height())
            )
            imgs[img_name] = img
        return imgs

    def update_board(self):
        self.board = [["0", "0", "0", "0", "0", "0"] for _ in range(6)]
        count = 2
        for blk_name in self.blocks_place:
            for blk in self.blocks_place[blk_name]:
                x_start = (blk.x_1 - self.anchor.x_1) / self.grid_w
                x_end = (blk.x_2 - self.anchor.x_1) / self.grid_w
                y_start = (blk.y_1 - self.anchor.y_1) / self.grid_w
                y_end = (blk.y_2 - self.anchor.y_1) / self.grid_w
                for i in range(round(x_start), round(x_end)):
                    for j in range(round(y_start), round(y_end)):
                        self.board[j][i] = "1" if blk_name == "fish_nor" else str(count)
                count += 1

    def click_btn(self, mouse: Rect):
        if self.solution:
            if (
                self.solution_pos["btn_home"].x_1 < mouse.x_1
                and mouse.x_1 < self.solution_pos["btn_home"].x_2
                and self.solution_pos["btn_home"].y_1 < mouse.y_1
                and mouse.y_1 < self.solution_pos["btn_home"].y_2
            ):
                self.solution = False
            elif (
                self.solution_pos["btn_back"].x_1 < mouse.x_1
                and mouse.x_1 < self.solution_pos["btn_back"].x_2
                and self.solution_pos["btn_back"].y_1 < mouse.y_1
                and mouse.y_1 < self.solution_pos["btn_back"].y_2
            ):
                if self.step_print > 0:
                    self.step_print -= 1
            elif (
                self.solution_pos["btn_forward"].x_1 < mouse.x_1
                and mouse.x_1 < self.solution_pos["btn_forward"].x_2
                and self.solution_pos["btn_forward"].y_1 < mouse.y_1
                and mouse.y_1 < self.solution_pos["btn_forward"].y_2
            ):
                if self.msg.isdigit():
                    if self.step_print < int(self.msg):
                        self.step_print += 1
            elif (
                self.solution_pos["btn_reset"].x_1 < mouse.x_1
                and mouse.x_1 < self.solution_pos["btn_reset"].x_2
                and self.solution_pos["btn_reset"].y_1 < mouse.y_1
                and mouse.y_1 < self.solution_pos["btn_reset"].y_2
            ):
                self.step_print = 0
            elif (
                self.solution_pos["btn_exit"].x_1 < mouse.x_1
                and mouse.x_1 < self.solution_pos["btn_exit"].x_2
                and self.solution_pos["btn_exit"].y_1 < mouse.y_1
                and mouse.y_1 < self.solution_pos["btn_exit"].y_2
            ):
                self.run = False
        else:
            if (
                self.init_pos["btn_reset"].x_1 < mouse.x_1
                and mouse.x_1 < self.init_pos["btn_reset"].x_2
                and self.init_pos["btn_reset"].y_1 < mouse.y_1
                and mouse.y_1 < self.init_pos["btn_reset"].y_2
            ):
                self.reset()
            elif (
                self.init_pos["btn_solve"].x_1 < mouse.x_1
                and mouse.x_1 < self.init_pos["btn_solve"].x_2
                and self.init_pos["btn_solve"].y_1 < mouse.y_1
                and mouse.y_1 < self.init_pos["btn_solve"].y_2
            ):
                if len(self.blocks_place) > 0:
                    self.step_print = 0
                    self.update_board()
                    self.boards_print, self.msg = solver(self.board)
                    self.solution = True
            elif (
                self.init_pos["btn_exit"].x_1 < mouse.x_1
                and mouse.x_1 < self.init_pos["btn_exit"].x_2
                and self.init_pos["btn_exit"].y_1 < mouse.y_1
                and mouse.y_1 < self.init_pos["btn_exit"].y_2
            ):
                self.run = False

    def select_block(self, mouse: Rect):
        for blk_name in self.blocks_place:
            for blk in self.blocks_place[blk_name]:
                if (
                    blk.x_1 < mouse.x_1
                    and mouse.x_1 < blk.x_2
                    and blk.y_1 < mouse.y_1
                    and mouse.y_1 < blk.y_2
                ):
                    self.blocks_place[blk_name].remove(blk)
                    return (
                        blk_name,
                        mouse.x_1 - blk.x_1,
                        mouse.y_1 - blk.y_1,
                    )
        if (
            self.init_pos["fish_nor"].x_1 < mouse.x_1
            and mouse.x_1 < self.init_pos["fish_nor"].x_2
            and self.init_pos["fish_nor"].y_1 < mouse.y_1
            and mouse.y_1 < self.init_pos["fish_nor"].y_2
            and (
                "fish_nor" not in self.blocks_place
                or self.blocks_place["fish_nor"] == []
            )
        ):
            return (
                "fish_nor",
                mouse.x_1 - self.init_pos["fish_nor"].x_1,
                mouse.y_1 - self.init_pos["fish_nor"].y_1,
            )
        elif (
            self.init_pos["block_1_2_nor"].x_1 < mouse.x_1
            and mouse.x_1 < self.init_pos["block_1_2_nor"].x_2
            and self.init_pos["block_1_2_nor"].y_1 < mouse.y_1
            and mouse.y_1 < self.init_pos["block_1_2_nor"].y_2
        ):
            return (
                "block_1_2_nor",
                mouse.x_1 - self.init_pos["block_1_2_nor"].x_1,
                mouse.y_1 - self.init_pos["block_1_2_nor"].y_1,
            )
        elif (
            self.init_pos["block_1_3_nor"].x_1 < mouse.x_1
            and mouse.x_1 < self.init_pos["block_1_3_nor"].x_2
            and self.init_pos["block_1_3_nor"].y_1 < mouse.y_1
            and mouse.y_1 < self.init_pos["block_1_3_nor"].y_2
        ):
            return (
                "block_1_3_nor",
                mouse.x_1 - self.init_pos["block_1_3_nor"].x_1,
                mouse.y_1 - self.init_pos["block_1_3_nor"].y_1,
            )
        elif (
            self.init_pos["block_2_1_nor"].x_1 < mouse.x_1
            and mouse.x_1 < self.init_pos["block_2_1_nor"].x_2
            and self.init_pos["block_2_1_nor"].y_1 < mouse.y_1
            and mouse.y_1 < self.init_pos["block_2_1_nor"].y_2
        ):
            return (
                "block_2_1_nor",
                mouse.x_1 - self.init_pos["block_2_1_nor"].x_1,
                mouse.y_1 - self.init_pos["block_2_1_nor"].y_1,
            )
        elif (
            self.init_pos["block_3_1_nor"].x_1 < mouse.x_1
            and mouse.x_1 < self.init_pos["block_3_1_nor"].x_2
            and self.init_pos["block_3_1_nor"].y_1 < mouse.y_1
            and mouse.y_1 < self.init_pos["block_3_1_nor"].y_2
        ):
            return (
                "block_3_1_nor",
                mouse.x_1 - self.init_pos["block_3_1_nor"].x_1,
                mouse.y_1 - self.init_pos["block_3_1_nor"].y_1,
            )
        return None, None, None

    def place_block(self, pos_place: Rect):
        num_x = (pos_place.x_1 - self.anchor.x_1) // self.grid_w + round(
            ((pos_place.x_1 - self.anchor.x_1) % self.grid_w) / self.grid_w
        )
        num_y = (pos_place.y_1 - self.anchor.y_1) // self.grid_w + round(
            ((pos_place.y_1 - self.anchor.y_1) % self.grid_w) / self.grid_w
        )
        x_1 = round(self.anchor.x_1 + num_x * self.grid_w, 4)
        y_1 = round(self.anchor.y_1 + num_y * self.grid_w, 4)
        x_2 = round(x_1 + pos_place.width(), 4)
        y_2 = round(y_1 + pos_place.height(), 4)
        ax_1 = round(self.anchor.x_1, 4)
        ax_2 = round(self.anchor.x_1 + self.grid_w * 6, 4)
        ay_1 = round(self.anchor.y_1, 4)
        ay_2 = round(self.anchor.y_1 + self.grid_w * 6, 4)
        if ax_1 > x_1 or ay_1 > y_1 or ax_2 < x_2 or ay_2 < y_2:
            return False, None
        for blk_name in self.blocks_place:
            for blk in self.blocks_place[blk_name]:
                if round(abs(blk.x_2 + blk.x_1 - x_2 - x_1), 4) < round(
                    blk.x_2 - blk.x_1 + x_2 - x_1, 4
                ) and round(abs(blk.y_2 + blk.y_1 - y_2 - y_1), 4) < round(
                    blk.y_2 - blk.y_1 + y_2 - y_1, 4
                ):
                    return False, None
        return True, Rect(x_1, y_1, x_2, y_2)

    def draw_init(self):
        # fill the screen with initial images
        for img in self.init_pos:
            if img != "fish_nor":
                self.screen.blit(
                    self.imgs[img], (self.init_pos[img].x_1, self.init_pos[img].y_1)
                )
        # only one fish is allowed
        if self.block_select[0] != "fish_nor" and (
            "fish_nor" not in self.blocks_place or self.blocks_place["fish_nor"] == []
        ):
            self.screen.blit(
                self.imgs["fish_nor"],
                (self.init_pos["fish_nor"].x_1, self.init_pos["fish_nor"].y_1),
            )

        # if self.fish_click:
        #     # TODO: click animation
        #     pass

        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close the window
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    self.block_select = self.select_block(Rect(mouse_x, mouse_y))
                    self.click_btn(Rect(mouse_x, mouse_y))
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if self.block_select[0]:
                        pos_place = self.place_block(
                            Rect(
                                mouse_x - self.block_select[1],
                                mouse_y - self.block_select[2],
                                mouse_x
                                - self.block_select[1]
                                + self.init_pos[self.block_select[0]].width(),
                                mouse_y
                                - self.block_select[2]
                                + self.init_pos[self.block_select[0]].height(),
                            )
                        )
                        if pos_place[0]:
                            self.blocks_place.setdefault(
                                self.block_select[0], []
                            ).append(pos_place[1])
                        self.block_select = None, None, None

        for blk_name in self.blocks_place:
            for blk in self.blocks_place[blk_name]:
                self.screen.blit(
                    self.imgs[blk_name],
                    (
                        blk.x_1,
                        blk.y_1,
                    ),
                )

        if self.block_select[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(
                self.imgs[self.block_select[0]],
                (
                    mouse_x - self.block_select[1],
                    mouse_y - self.block_select[2],
                ),
            )

        # limits FPS to 60
        self.clock.tick(60)

    def extract_block(self, board):
        block_extract = {}
        scaned_block = ["0"]
        for i in range(6):
            for j in range(6):
                if board[i][j] not in scaned_block:
                    # extract pos of all units in a block to two lists: row and col
                    index_list = [
                        [a, b]
                        for a, row in enumerate(board)
                        for b, val in enumerate(row)
                        if val == board[i][j]
                    ]
                    row = [index[0] for index in index_list]
                    col = [index[1] for index in index_list]

                    if len(set(row)) == 1 and len(col) == 2:
                        # horizontal 1*2 block, possible fish
                        if board[i][j] == "1":
                            block_extract.setdefault("fish_nor", []).append(
                                Rect(
                                    self.anchor.x_1 + self.grid_w * index_list[0][1],
                                    self.anchor.y_1 + self.grid_w * index_list[0][0],
                                )
                            )
                        else:
                            block_extract.setdefault("block_1_2_nor", []).append(
                                Rect(
                                    self.anchor.x_1 + self.grid_w * index_list[0][1],
                                    self.anchor.y_1 + self.grid_w * index_list[0][0],
                                )
                            )
                    elif len(set(row)) == 1 and len(col) == 3:
                        block_extract.setdefault("block_1_3_nor", []).append(
                            Rect(
                                self.anchor.x_1 + self.grid_w * index_list[0][1],
                                self.anchor.y_1 + self.grid_w * index_list[0][0],
                            )
                        )
                    elif len(set(col)) == 1 and len(row) == 2:
                        block_extract.setdefault("block_2_1_nor", []).append(
                            Rect(
                                self.anchor.x_1 + self.grid_w * index_list[0][1],
                                self.anchor.y_1 + self.grid_w * index_list[0][0],
                            )
                        )
                    elif len(set(col)) == 1 and len(row) == 3:
                        block_extract.setdefault("block_3_1_nor", []).append(
                            Rect(
                                self.anchor.x_1 + self.grid_w * index_list[0][1],
                                self.anchor.y_1 + self.grid_w * index_list[0][0],
                            )
                        )
                    scaned_block.append(board[i][j])
        return block_extract

    def draw_solution(self):
        # fill the screen with solution images
        for img in self.solution_pos:
            if img == "msg_box":
                text = pygame.font.SysFont("Comic Sans MS", int(self.grid_w))
                if self.msg.isdigit():
                    text_width, text_height = text.size(
                        "{}/{}".format(self.step_print, self.msg)
                    )
                    text_surface = text.render(
                        "{}/{}".format(self.step_print, self.msg),
                        False,
                        (255, 255, 255),
                    )
                else:
                    text_width, text_height = text.size("{}".format(self.msg))
                    text_surface = text.render(
                        "{}".format(self.msg), False, (255, 255, 255)
                    )
                self.screen.blit(
                    text_surface,
                    (
                        self.solution_pos[img].x_1 - text_width / 2,
                        self.solution_pos[img].y_1 - text_height / 2,
                    ),
                )
            else:
                self.screen.blit(
                    self.imgs[img],
                    (self.solution_pos[img].x_1, self.solution_pos[img].y_1),
                )

        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close the window
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    self.click_btn(Rect(mouse_x, mouse_y))

        blocks_extract = (
            self.extract_block(self.boards_print[self.step_print])
            if len(self.boards_print) != 0
            else self.blocks_place
        )
        for blk_name in blocks_extract:
            for blk in blocks_extract[blk_name]:
                self.screen.blit(
                    self.imgs[blk_name],
                    (
                        blk.x_1,
                        blk.y_1,
                    ),
                )

        # limits FPS to 60
        self.clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    current_w, current_h = (
        pygame.display.Info().current_w,
        pygame.display.Info().current_h,
    )
    game = Game(current_w, current_h)
    while game.run:
        if game.solution:
            game.draw_solution()
        else:
            game.draw_init()

        # flip() the display to put all changes on screen
        pygame.display.flip()
    pygame.quit()
