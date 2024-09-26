"""
Author: Guoxin Wang
Date: 2024-09-24 23:55:56
LastEditors: Guoxin Wang
LastEditTime: 2024-09-26 16:01:58
FilePath: /PondSolver/Solver.py
Description: 

Copyright (c) 2024 by Guoxin Wang, All Rights Reserved. 
"""

import copy
from collections import deque

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3


def extract_board_info(board):
    board_info = []
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

                if len(set(row)) == 1 and len(col) in (2, 3):  # horizontal block
                    board_info.append(
                        (
                            board[i][j],
                            "h",
                            len(index_list),
                            index_list[0][0],
                            index_list[0][1],
                            board[i][j] == "1",
                        )
                    )
                elif len(set(col)) == 1 and len(row) in (2, 3):  # vertical block
                    board_info.append(
                        (
                            board[i][j],
                            "v",
                            len(index_list),
                            index_list[0][0],
                            index_list[0][1],
                            False,
                        )
                    )
                scaned_block.append(board[i][j])
    return board_info


def create_blocks(board_info):
    blocks = []
    for info in board_info:
        name, direction, block_num, x, y, fish = info
        block = Block(name, direction, block_num, x, y, fish)
        blocks.append(block)
    return blocks


def update_moveable(blocks, board):
    for blk in blocks:
        moveable = [0, 0, 0, 0]  # Reset movement capacities
        if blk.direction == "v":
            while (
                blk.x - moveable[UP] - 1 >= 0
                and board[blk.x - moveable[UP] - 1][blk.y] == "0"
            ):
                moveable[UP] += 1
            while (
                blk.x + blk.block_num + moveable[DOWN] < 6
                and board[blk.x + blk.block_num + moveable[DOWN]][blk.y] == "0"
            ):
                moveable[DOWN] += 1
        else:  # horizontal
            while (
                blk.y - moveable[LEFT] - 1 >= 0
                and board[blk.x][blk.y - moveable[LEFT] - 1] == "0"
            ):
                moveable[LEFT] += 1
            while (
                blk.y + blk.block_num + moveable[RIGHT] < 6
                and board[blk.x][blk.y + blk.block_num + moveable[RIGHT]] == "0"
            ):
                moveable[RIGHT] += 1
        blk.moveable = moveable
    return blocks


def move_blocks(blocks, command):
    updated_blocks = []
    for blk in blocks:
        direction, block_name, distance = command
        if blk.name == block_name:
            updated_blk = copy.deepcopy(blk)
            if direction == UP:
                updated_blk.x -= distance
            elif direction == DOWN:
                updated_blk.x += distance
            elif direction == LEFT:
                updated_blk.y -= distance
            elif direction == RIGHT:
                updated_blk.y += distance
            updated_blocks.append(updated_blk)
        else:
            updated_blocks.append(blk)
    return updated_blocks


def place_blocks(blocks):
    board = [["0", "0", "0", "0", "0", "0"] for _ in range(6)]
    for blk in blocks:
        for i in range(blk.block_num):
            if blk.direction == "v":
                board[blk.x + i][blk.y] = blk.name
            else:
                board[blk.x][blk.y + i] = blk.name
    return board


def fish_out(blocks):
    return any(blk.fish and blk.y == 4 for blk in blocks)


class StateNode:
    def __init__(self, board=None, blocks=[]):
        self.board = board
        self.blocks = blocks
        self.parent = None
        self.queue_generator()

    def queue_generator(self):
        self.move_count = 0
        self.command_queue = []
        for blk in self.blocks:
            for i in range(4):
                if blk.moveable[i] != 0:
                    for j in range(blk.moveable[i]):
                        command = (i, blk.name, j + 1)
                        self.command_queue.append(command)


class Block:
    def __init__(self, name, direction, block_num, x, y, fish=False):
        self.name = name
        self.direction = direction
        self.block_num = block_num
        self.x = x
        self.y = y
        self.fish = fish
        self.moveable = [0, 0, 0, 0]

    def print_info(self):
        print(self.direction, self.block_num, (self.x, self.y), self.moveable)


def solver(board):
    # record for solution
    boards_print = []

    fish_found = False
    board_info = extract_board_info(board)
    for block_info in board_info:
        _, _, _, x, y, fish = block_info
        if fish:
            fish_found = True
            if x != 2:
                return boards_print, "No Solution"
            elif y == 4:
                boards_print.append(board)
                return boards_print, "0"
    if not fish_found:
        return boards_print, "No Fish Found"

    # Set to track visited states
    visited_boards = set()
    state_queue = deque()
    # Create the root node
    blocks = create_blocks(board_info)
    blocks = update_moveable(blocks, board)
    root = StateNode(board, blocks)

    # Create a hashable representation of the board state
    board_tuple = tuple(tuple(row) for row in root.board)
    visited_boards.add(board_tuple)
    state_queue.append(root)

    while True:
        while True:
            if len(state_queue) == 0:
                return boards_print, "No Solution"
            if state_queue[0].move_count >= len(state_queue[0].command_queue):
                state_queue.popleft()
                continue

            command = state_queue[0].command_queue[state_queue[0].move_count]
            updated_blocks = move_blocks(state_queue[0].blocks, command)
            updated_board = place_blocks(updated_blocks)

            state_queue[0].move_count += 1
            board_tuple = tuple(tuple(row) for row in updated_board)
            if board_tuple in visited_boards:
                continue
            else:
                break

        updated_blocks = update_moveable(updated_blocks, updated_board)
        next_state = StateNode(updated_board, updated_blocks)
        next_state.parent = state_queue[0]
        visited_boards.add(board_tuple)

        if fish_out(next_state.blocks):
            count = 0
            boards_print.append(next_state.board)
            while True:
                if next_state.parent:
                    count += 1
                    next_state = next_state.parent
                    boards_print.append(next_state.board)
                else:
                    break
            boards_print.reverse()
            return boards_print, "{}".format(count)
        else:
            state_queue.append(next_state)
