"""
Author: Guoxin Wang
Date: 2024-01-30 15:01:57
LastEditors: Guoxin Wang
LastEditTime: 2024-02-06 11:59:08
FilePath: /PoolSolver/pool_solver.py
Description: 

Copyright (c) 2024 by Guoxin Wang, All Rights Reserved. 
"""

import copy
from tkinter import END, Button, Entry, Label, Tk

up, down, left, right = 0, 1, 2, 3
step = 0
print_boards = []
message = ""


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
                block.moveable[up] = move_up
                move_down = 0
                while (
                    block.x + move_down + block.num_block < 6
                    and self.board[block.x + move_down + block.num_block][block.y]
                    == "0"
                ):
                    move_down += 1
                block.moveable[down] = move_down
            elif block.direction == "h":
                move_left = 0
                while (
                    block.y - move_left > 0
                    and self.board[block.x][block.y - move_left - 1] == "0"
                ):
                    move_left += 1
                block.moveable[left] = move_left
                move_right = 0
                while (
                    block.y + move_right + block.num_block < 6
                    and self.board[block.x][block.y + move_right + block.num_block]
                    == "0"
                ):
                    move_right += 1
                block.moveable[right] = move_right

    def move(self, x):
        for block in self.blocks:
            if block.name == x[1]:
                if x[0] == up:
                    block.x -= x[2]
                elif x[0] == down:
                    block.x += x[2]
                elif x[0] == left:
                    block.y -= x[2]
                elif x[0] == right:
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


def extract(myList, value):
    index_list = [
        [x, y]
        for x, list in enumerate(myList)
        for y, val in enumerate(list)
        if val == value
    ]
    row = [x[0] for x in index_list]
    col = [x[1] for x in index_list]
    num_row = len(set(row))
    num_col = len(set(col))
    if (
        num_row == 1
        and (len(col) == 2 or len(col) == 3)
        and all(y - x == 1 for x, y in zip(col, col[1:]))
    ):
        return (
            "h",
            len(index_list),
            index_list[0][0],
            index_list[0][1],
            True if value == "1" else False,
        )
    elif (
        num_col == 1
        and (len(row) == 2 or len(row) == 3)
        and all(y - x == 1 for x, y in zip(row, row[1:]))
    ):
        return (
            "v",
            len(index_list),
            index_list[0][0],
            index_list[0][1],
            True if value == "1" else False,
        )
    else:
        return None


def solver(board):
    boards = []
    print_boards = []
    node_queue = []
    root = Node()
    scaned_block = ["0"]
    for i in range(6):
        for j in range(6):
            if board[i][j] not in scaned_block:
                extracted = extract(board, board[i][j])
                if extracted:
                    direction, num_block, x, y, fish = extracted
                    root.place_block(board[i][j], direction, num_block, x, y, fish)
                    scaned_block.append(board[i][j])
                else:
                    return print_boards, "block defination error"
    if "1" not in scaned_block:
        return print_boards, "miss fish"
    root.moveable_update()
    root.queue_generator()
    boards.append(root.board)
    node_queue.append(root)
    while True:
        while True:
            if len(node_queue) == 0:
                return print_boards, "fail"
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
            print_boards.append(node.board)
            while True:
                if node.parent:
                    count += 1
                    node = node.parent
                    print_boards.append(node.board)
                else:
                    break
            print_boards.reverse()
            return print_boards, "{}".format(count)
        else:
            node_queue.append(node)


def tk_init():
    root = Tk(className="pool")
    entrys = []
    texts = []
    for i in range(6):
        entry_temp = []
        text_temp = []
        for j in range(6):
            entry = Entry(
                root,
                justify="center",
                validate="key",
                validatecommand=(
                    root.register(
                        lambda s: len(s) <= 2
                        and (len(s) == 0 or s.isdigit() and int(s) != 0)
                    ),
                    "%P",
                ),
            )
            entry.place(
                relx=1 / 8 * (j + 1),
                rely=1 / 12 * (i + 3),
                relwidth=1 / 8,
                relheight=1 / 12,
            )
            text = Label(root, justify="center")
            entry_temp.append(entry)
            text_temp.append(text)
        entrys.append(entry_temp)
        texts.append(text_temp)
    messages = Label(root, justify="center")
    messages.place(relx=0, rely=1 / 12, relwidth=1, relheight=1 / 12)
    button = Button(
        root, text="restart", command=lambda: restart(entrys, texts, messages)
    )
    button.place(relx=1 / 8, rely=5 / 6, relwidth=1 / 4, relheight=1 / 12)
    button = Button(root, text="next", command=lambda: next(entrys, texts, messages))
    button.place(relx=5 / 8, rely=5 / 6, relwidth=1 / 4, relheight=1 / 12)

    def move_focus(event):
        x = 0
        y = 0
        handle = event.widget.focus_get()
        for i, list in enumerate(entrys):
            for j, value in enumerate(list):
                if value == handle:
                    x = i
                    y = j
        if event.char == "w" and x > 0:
            entrys[x - 1][y].focus()
        elif event.char == "s" and x < 5:
            entrys[x + 1][y].focus()
        elif event.char == "a" and y > 0:
            entrys[x][y - 1].focus()
        elif event.char == "d" and y < 5:
            entrys[x][y + 1].focus()
        return "break"

    root.bind("w", move_focus)
    root.bind("s", move_focus)
    root.bind("a", move_focus)
    root.bind("d", move_focus)
    root.bind("<space>", lambda _, a=entrys, b=texts, c=messages: next(a, b, c))
    root.bind("<Return>", lambda _, a=entrys, b=texts, c=messages: restart(a, b, c))
    root.bind("<Escape>", lambda _: root.destroy())
    root.mainloop()


def next(entrys, texts, messages):
    global print_boards
    global message
    global step
    if step == 0 and len(print_boards) == 0:
        board = [["0", "0", "0", "0", "0", "0"] for _ in range(6)]
        for i in range(6):
            for j in range(6):
                value = entrys[i][j].get()
                if value != "":
                    board[i][j] = value
        print_boards, message = solver(board)
        messages["text"] = (
            "{}/{}".format(step, message) if message.isdigit() else message
        )
    if len(print_boards) != 0:
        for i in range(6):
            for j in range(6):
                entrys[i][j].place_forget()
                texts[i][j]["text"] = (
                    print_boards[step][i][j] if print_boards[step][i][j] != "0" else ""
                )
                texts[i][j].place(
                    relx=1 / 8 * (j + 1),
                    rely=1 / 12 * (i + 3),
                    relwidth=1 / 8,
                    relheight=1 / 12,
                )
        messages["text"] = "{}/{}".format(step, message)
        step += 1
        if step == len(print_boards):
            step = 0


def restart(entrys, texts, messages):
    global print_boards
    global step
    step = 0
    print_boards = []
    messages["text"] = ""
    for i in range(6):
        for j in range(6):
            entrys[i][j].delete(0, END)
            entrys[i][j].place(
                relx=1 / 8 * (j + 1),
                rely=1 / 12 * (i + 3),
                relwidth=1 / 8,
                relheight=1 / 12,
            )
            texts[i][j]["text"] = ""
            texts[i][j].place_forget()


if __name__ == "__main__":
    tk_init()
