from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

from .assets import BLOCK_TO_ASSET, BOARD_SIZE

UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

Board = list[list[str]]
State = tuple[tuple[int, int], ...]


@dataclass(frozen=True, slots=True)
class Block:
    name: str
    direction: str
    length: int
    row: int
    col: int
    fish: bool = False
    moveable: tuple[int, int, int, int] = field(default=(0, 0, 0, 0))


@dataclass(slots=True)
class SearchNode:
    state: State
    parent: SearchNode | None = None


def extract_board_info(board: Board) -> list[Block]:
    blocks: list[Block] = []
    scanned: set[str] = {"0"}
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            name = board[row][col]
            if name in scanned:
                continue

            length = 1
            direction = ""
            if col + 1 < BOARD_SIZE and board[row][col + 1] == name:
                direction = "h"
                while col + length < BOARD_SIZE and board[row][col + length] == name:
                    length += 1
            elif row + 1 < BOARD_SIZE and board[row + 1][col] == name:
                direction = "v"
                while row + length < BOARD_SIZE and board[row + length][col] == name:
                    length += 1

            if direction and length in (2, 3):
                blocks.append(Block(name, direction, length, row, col, name == "1"))
            scanned.add(name)
    return blocks


def create_blocks(board_info: list[Block]) -> list[Block]:
    return list(board_info)


def update_moveable(blocks: list[Block], board: Board) -> list[Block]:
    updated: list[Block] = []
    for block in blocks:
        distances = _movement_distances(block, board)
        updated.append(
            Block(
                block.name,
                block.direction,
                block.length,
                block.row,
                block.col,
                block.fish,
                distances,
            )
        )
    return updated


def move_blocks(blocks: list[Block], command: tuple[int, str, int]) -> list[Block]:
    direction, block_name, distance = command
    moved: list[Block] = []
    for block in blocks:
        if block.name != block_name:
            moved.append(block)
            continue
        moved.append(_move_block(block, direction, distance))
    return moved


def place_blocks(blocks: list[Block]) -> Board:
    return _build_board(tuple(blocks))


def fish_out(blocks: list[Block]) -> bool:
    return any(block.fish and block.col == BOARD_SIZE - 2 for block in blocks)


def solver(board: Board) -> tuple[list[Board], str]:
    blocks = tuple(extract_board_info(board))
    if not blocks:
        return [], "No Fish Found"

    fish_index = next((index for index, block in enumerate(blocks) if block.fish), None)
    if fish_index is None:
        return [], "No Fish Found"

    fish = blocks[fish_index]
    if fish.row != 2:
        return [], "No Solution"

    initial_state = _state_from_blocks(blocks)
    if initial_state[fish_index][1] == BOARD_SIZE - 2:
        return [[row[:] for row in board]], "0"

    root = SearchNode(initial_state)
    queue: deque[SearchNode] = deque([root])
    visited: set[State] = {initial_state}

    while queue:
        node = queue.popleft()
        occupancy = _build_occupancy(blocks, node.state)
        for next_state in _generate_moves(blocks, node.state, occupancy):
            if next_state in visited:
                continue
            visited.add(next_state)
            child = SearchNode(next_state, node)
            if next_state[fish_index][1] == BOARD_SIZE - 2:
                path = _collect_path(child, blocks)
                return path, str(len(path) - 1)
            queue.append(child)

    return [], "No Solution"


def block_to_asset(block: Block) -> str:
    return BLOCK_TO_ASSET[(block.direction, block.length, block.fish)]


def _state_from_blocks(blocks: tuple[Block, ...]) -> State:
    return tuple((block.row, block.col) for block in blocks)


def _build_board(blocks: tuple[Block, ...]) -> Board:
    board = [["0" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for block in blocks:
        _paint_block(board, block.name, block.row, block.col, block.direction, block.length)
    return board


def _build_board_from_state(blocks: tuple[Block, ...], state: State) -> Board:
    board = [["0" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for block, (row, col) in zip(blocks, state):
        _paint_block(board, block.name, row, col, block.direction, block.length)
    return board


def _paint_block(
    board: Board,
    name: str,
    row: int,
    col: int,
    direction: str,
    length: int,
):
    if direction == "v":
        for offset in range(length):
            board[row + offset][col] = name
        return
    for offset in range(length):
        board[row][col + offset] = name


def _build_occupancy(blocks: tuple[Block, ...], state: State) -> list[list[int]]:
    occupancy = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for index, (block, (row, col)) in enumerate(zip(blocks, state)):
        if block.direction == "v":
            for offset in range(block.length):
                occupancy[row + offset][col] = index
        else:
            for offset in range(block.length):
                occupancy[row][col + offset] = index
    return occupancy


def _generate_moves(blocks: tuple[Block, ...], state: State, occupancy: list[list[int]]):
    for index, block in enumerate(blocks):
        row, col = state[index]
        if block.direction == "v":
            distance = 1
            while row - distance >= 0 and occupancy[row - distance][col] == -1:
                yield _replace_state_position(state, index, row - distance, col)
                distance += 1
            distance = 1
            tail_row = row + block.length - 1
            while tail_row + distance < BOARD_SIZE and occupancy[tail_row + distance][col] == -1:
                yield _replace_state_position(state, index, row + distance, col)
                distance += 1
            continue

        distance = 1
        while col - distance >= 0 and occupancy[row][col - distance] == -1:
            yield _replace_state_position(state, index, row, col - distance)
            distance += 1
        distance = 1
        tail_col = col + block.length - 1
        while tail_col + distance < BOARD_SIZE and occupancy[row][tail_col + distance] == -1:
            yield _replace_state_position(state, index, row, col + distance)
            distance += 1


def _replace_state_position(state: State, index: int, row: int, col: int) -> State:
    mutable = list(state)
    mutable[index] = (row, col)
    return tuple(mutable)


def _movement_distances(block: Block, board: Board) -> tuple[int, int, int, int]:
    up = down = left = right = 0
    if block.direction == "v":
        while block.row - up - 1 >= 0 and board[block.row - up - 1][block.col] == "0":
            up += 1
        while (
            block.row + block.length + down < BOARD_SIZE
            and board[block.row + block.length + down][block.col] == "0"
        ):
            down += 1
        return (up, down, left, right)

    while block.col - left - 1 >= 0 and board[block.row][block.col - left - 1] == "0":
        left += 1
    while (
        block.col + block.length + right < BOARD_SIZE
        and board[block.row][block.col + block.length + right] == "0"
    ):
        right += 1
    return (up, down, left, right)


def _move_block(block: Block, direction: int, distance: int) -> Block:
    row, col = block.row, block.col
    if direction == UP:
        row -= distance
    elif direction == DOWN:
        row += distance
    elif direction == LEFT:
        col -= distance
    elif direction == RIGHT:
        col += distance
    return Block(
        block.name,
        block.direction,
        block.length,
        row,
        col,
        block.fish,
        block.moveable,
    )


def _collect_path(node: SearchNode, blocks: tuple[Block, ...]) -> list[Board]:
    states: list[State] = []
    current: SearchNode | None = node
    while current is not None:
        states.append(current.state)
        current = current.parent
    states.reverse()
    return [_build_board_from_state(blocks, state) for state in states]
