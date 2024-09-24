"""
Author: Guoxin Wang
Date: 2024-09-24 13:43:58
LastEditors: Guoxin Wang
LastEditTime: 2024-09-24 16:17:54
FilePath: \PoolSolver\Solver.py
Description: 

Copyright (c) 2024 by Guoxin Wang, All Rights Reserved. 
"""

import copy

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


class Node:
    def __init__(self):
        self.board = [["0", "0", "0", "0", "0", "0"] for _ in range(6)]
        self.blocks = []
        self.move_index = 0
        self.move_queue = []
        self.parent = None

    def place_block(self, name, direction, num_block, x, y, fish=False):
        block = Block(name, direction, num_block, x, y, fish)
        self.blocks.append(block)
        for i in range(block.num_block):
            if direction == "v":
                self.board[block.x + i][block.y] = block.name
            else:
                self.board[block.x][block.y + i] = block.name

    def queue_generator(self):
        self.move_queue = []
        self.move_index = 0
        for block in self.blocks:
            for i in range(4):
                if block.moveable[i] != 0:
                    for j in range(block.moveable[i]):
                        self.move_queue.append([i, block.name, j + 1])

    def board_update(self):
        self.board = [["0", "0", "0", "0", "0", "0"] for _ in range(6)]
        for block in self.blocks:
            for i in range(block.num_block):
                if block.direction == "v":
                    self.board[block.x + i][block.y] = block.name
                else:
                    self.board[block.x][block.y + i] = block.name

    def moveable_update(self):
        for block in self.blocks:
            if block.direction == "v":
                move_up = 0
                while (
                    block.x - move_up > 0
                    and self.board[block.x - move_up - 1][block.y] == "0"
                ):
                    move_up += 1
                block.moveable[UP] = move_up
                move_down = 0
                while (
                    block.x + move_down + block.num_block < 6
                    and self.board[block.x + move_down + block.num_block][block.y]
                    == "0"
                ):
                    move_down += 1
                block.moveable[DOWN] = move_down
            elif block.direction == "h":
                move_left = 0
                while (
                    block.y - move_left > 0
                    and self.board[block.x][block.y - move_left - 1] == "0"
                ):
                    move_left += 1
                block.moveable[LEFT] = move_left
                move_right = 0
                while (
                    block.y + move_right + block.num_block < 6
                    and self.board[block.x][block.y + move_right + block.num_block]
                    == "0"
                ):
                    move_right += 1
                block.moveable[RIGHT] = move_right

    def move(self, x):
        for block in self.blocks:
            if block.name == x[1]:
                if x[0] == UP:
                    block.x -= x[2]
                elif x[0] == DOWN:
                    block.x += x[2]
                elif x[0] == LEFT:
                    block.y -= x[2]
                elif x[0] == RIGHT:
                    block.y += x[2]

    def fish_out(self):
        for block in self.blocks:
            if block.fish and block.y == 4:
                return True
        return False


class Block:
    def __init__(self, name, direction, num_block, x, y, fish=False):
        self.name = name
        self.direction = direction
        self.num_block = num_block
        self.x = x
        self.y = y
        self.fish = fish
        self.moveable = [0, 0, 0, 0]

    def print_info(self):
        print(
            self.direction,
            self.num_block,
            (self.x, self.y),
            self.moveable,
        )


def extract(board, value):
    # extract pos of all units in a block to two lists: row and col
    index_list = [
        [i, j]
        for i, row in enumerate(board)
        for j, val in enumerate(row)
        if val == value
    ]
    row = [index[0] for index in index_list]
    col = [index[1] for index in index_list]

    # check if all units in a block are at the same row or col
    if len(set(row)) == 1 and (len(col) == 2 or len(col) == 3):
        # horizontal block, possible fish
        return (
            "h",
            len(index_list),
            index_list[0][0],
            index_list[0][1],
            True if value == "1" else False,
        )
    elif len(set(col)) == 1 and (len(row) == 2 or len(row) == 3):
        # vertical block, not fish
        return (
            "v",
            len(index_list),
            index_list[0][0],
            index_list[0][1],
            False,
        )


def solver(board):
    boards = []
    boards_print = []
    node_queue = []
    root = Node()

    # extract a board to blocks
    scaned_block = ["0"]
    for i in range(6):
        for j in range(6):
            if board[i][j] not in scaned_block:
                direction, num_block, x, y, fish = extract(board, board[i][j])
                if fish and x != 2:
                    return boards_print, "No Solution"
                elif fish and y == 4:
                    boards_print.append(board)
                    return boards_print, "0"
                root.place_block(board[i][j], direction, num_block, x, y, fish)
                scaned_block.append(board[i][j])
    if "1" not in scaned_block:
        return boards_print, "No Fish Found"

    root.moveable_update()
    root.queue_generator()
    boards.append(root.board)
    node_queue.append(root)
    while True:
        while True:
            if len(node_queue) == 0:
                return boards_print, "No Solution"
            if node_queue[0].move_index >= len(node_queue[0].move_queue):
                node_queue.pop(0)
                continue
            node = copy.deepcopy(node_queue[0])
            node.move(node.move_queue[node.move_index])
            node_queue[0].move_index += 1
            node.board_update()
            if node.board in boards:
                continue
            else:
                break
        node.moveable_update()
        node.queue_generator()
        node.parent = node_queue[0]
        boards.append(node.board)
        if node.fish_out():
            count = 0
            boards_print.append(node.board)
            while True:
                if node.parent:
                    count += 1
                    node = node.parent
                    boards_print.append(node.board)
                else:
                    break
            boards_print.reverse()
            return boards_print, "{}".format(count)
        else:
            node_queue.append(node)
