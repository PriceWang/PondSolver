from __future__ import annotations

import asyncio
import pygame

from .assets import ASSETS_DIR, BOARD_SIZE, PALETTE_BLOCKS, SIZE
from .models import DragState, Rect
from .solver import Block, block_to_asset, extract_board_info, solver

DEFAULT_SCREEN_W = 500
FALLBACK_BG_COLOR = (28, 85, 120)
FALLBACK_FRAME_COLOR = (234, 228, 194)
FALLBACK_BLOCK_COLOR = (212, 160, 79)
FALLBACK_BUTTON_COLOR = (104, 66, 39)


class Game:
    def __init__(self, current_w: float, current_h: float, web_mode: bool = False):
        self.web_mode = web_mode
        self.screen_w, self.screen_h = self._calculate_screen_size(current_w, current_h)
        self.grid_w = self.screen_w * (SIZE["frame"].width() / SIZE["bg"].width()) / BOARD_SIZE
        self.anchor = Rect(
            self.screen_w * (SIZE["frame"].x_1 / SIZE["bg"].width()),
            self.screen_w * (SIZE["frame"].y_1 / SIZE["bg"].width()),
        )
        self.image_sizes = self._build_image_sizes()
        self.imgs = self._load_images(self.image_sizes)
        self.init_pos = self._build_init_positions()
        self.solution_pos = self._build_solution_positions()

        self.screen = pygame.display.set_mode((int(self.screen_w), int(self.screen_h)))
        pygame.display.set_caption("PondSolver")
        try:
            pygame.display.set_icon(pygame.image.load(str(ASSETS_DIR / "icon.png")))
        except pygame.error:
            # Browsers may ignore or reject window icons.
            pass
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, int(self.grid_w))

        self.run = True
        self.solution = False
        self.drag_state = DragState()
        self.blocks_place: dict[str, list[Rect]] = {}
        self.board = self._empty_board()
        self.step_print = 0
        self.boards_print: list[list[list[str]]] = []
        self.msg = ""

    def reset(self):
        self.solution = False
        self.drag_state = DragState()
        self.blocks_place = {}
        self.board = self._empty_board()
        self.step_print = 0
        self.boards_print = []
        self.msg = ""

    def draw_init(self):
        for name, rect in self.init_pos.items():
            if name != "fish_nor":
                self.screen.blit(self.imgs[name], rect.point())

        if not self.drag_state.active or self.drag_state.name != "fish_nor":
            if not self.blocks_place.get("fish_nor"):
                self.screen.blit(self.imgs["fish_nor"], self.init_pos["fish_nor"].point())

        self._handle_init_events()
        self._draw_placed_blocks(self.blocks_place)
        self._draw_dragging_block()
        self.clock.tick(60)

    def draw_solution(self):
        for name, rect in self.solution_pos.items():
            if name == "msg_box":
                self._draw_message(rect)
            else:
                self.screen.blit(self.imgs[name], rect.point())

        self._handle_solution_events()
        blocks = self._extract_blocks(self.boards_print[self.step_print]) if self.boards_print else self.blocks_place
        self._draw_placed_blocks(blocks)
        self.clock.tick(60)

    def tick(self):
        if self.solution:
            self.draw_solution()
        else:
            self.draw_init()
        pygame.display.flip()

    def _calculate_screen_size(self, current_w: float, current_h: float) -> tuple[float, float]:
        if current_w <= 0 or current_h <= 0:
            return self._default_screen_size()
        side = current_w / 5 if current_w > current_h else current_h / 5
        if side <= 0:
            return self._default_screen_size()
        return side, side * (SIZE["bg"].height() / SIZE["bg"].width())

    def _default_screen_size(self) -> tuple[float, float]:
        return DEFAULT_SCREEN_W, DEFAULT_SCREEN_W * (
            SIZE["bg"].height() / SIZE["bg"].width()
        )

    def _build_image_sizes(self) -> dict[str, Rect]:
        grid = self.grid_w
        fish_ratio = SIZE["fish_nor"].height()
        return {
            "bg": Rect(0, 0, self.screen_w, self.screen_h),
            "frame": Rect(0, 0, self.screen_w, self.screen_h),
            "fish_nor": Rect(0, 0, grid * 2, grid),
            "block_1_2_nor": Rect(0, 0, grid * (SIZE["block_1_2_nor"].width() / fish_ratio), grid * (SIZE["block_1_2_nor"].height() / fish_ratio)),
            "block_1_3_nor": Rect(0, 0, grid * (SIZE["block_1_3_nor"].width() / fish_ratio), grid * (SIZE["block_1_3_nor"].height() / fish_ratio)),
            "block_2_1_nor": Rect(0, 0, grid * (SIZE["block_2_1_nor"].width() / fish_ratio), grid * (SIZE["block_2_1_nor"].height() / fish_ratio)),
            "block_3_1_nor": Rect(0, 0, grid * (SIZE["block_3_1_nor"].width() / fish_ratio), grid * (SIZE["block_3_1_nor"].height() / fish_ratio)),
            "btn_reset": Rect(0, 0, grid, grid),
            "btn_solve": Rect(0, 0, grid, grid),
            "btn_exit": Rect(0, 0, grid, grid),
            "btn_home": Rect(0, 0, grid, grid),
            "btn_back": Rect(0, 0, grid, grid),
            "btn_forward": Rect(0, 0, grid, grid),
        }

    def _load_images(self, image_sizes: dict[str, Rect]):
        images = {}
        for name, rect in image_sizes.items():
            image = self._load_image(name, rect)
            images[name] = image
        return images

    def _load_image(self, name: str, rect: Rect):
        size = (max(1, int(rect.width())), max(1, int(rect.height())))
        try:
            image = pygame.image.load(str(ASSETS_DIR / f"{name}.png"))
            return pygame.transform.scale(image, size)
        except pygame.error:
            surface = pygame.Surface(size)
            surface.fill(self._fallback_color(name))
            return surface

    def _fallback_color(self, name: str) -> tuple[int, int, int]:
        if name == "bg":
            return FALLBACK_BG_COLOR
        if name == "frame":
            return FALLBACK_FRAME_COLOR
        if name.startswith("btn_"):
            return FALLBACK_BUTTON_COLOR
        return FALLBACK_BLOCK_COLOR

    def _build_init_positions(self) -> dict[str, Rect]:
        grid = self.grid_w
        anchor_x = self.anchor.x_1
        anchor_y = self.anchor.y_1
        sizes = self.image_sizes
        button_y = anchor_y - grid * 1.4
        button_xs = self._toolbar_positions(
            [("btn_reset", 1.0), ("btn_solve", 2.5), ("btn_exit", 4.0)],
            [("btn_reset", 1.5), ("btn_solve", 3.5)],
        )
        positions = {
            "bg": Rect(0, 0, sizes["bg"].width(), sizes["bg"].height()),
            "frame": Rect(0, 0, sizes["frame"].width(), sizes["frame"].height()),
            "fish_nor": self._rect_at(anchor_x + grid, anchor_y + grid * 6.6, "fish_nor"),
            "block_1_2_nor": self._rect_at(anchor_x + grid, anchor_y + grid * 7.6, "block_1_2_nor"),
            "block_1_3_nor": self._rect_at(anchor_x + grid, anchor_y + grid * 8.6, "block_1_3_nor"),
            "block_2_1_nor": self._rect_at(anchor_x + grid * 3, anchor_y + grid * 6.6, "block_2_1_nor"),
            "block_3_1_nor": self._rect_at(anchor_x + grid * 4, anchor_y + grid * 6.6, "block_3_1_nor"),
            "btn_reset": self._rect_at(button_xs["btn_reset"], button_y, "btn_reset"),
            "btn_solve": self._rect_at(button_xs["btn_solve"], button_y, "btn_solve"),
        }
        if not self.web_mode:
            positions["btn_exit"] = self._rect_at(button_xs["btn_exit"], button_y, "btn_exit")
        return positions

    def _build_solution_positions(self) -> dict[str, Rect]:
        grid = self.grid_w
        anchor_x = self.anchor.x_1
        anchor_y = self.anchor.y_1
        button_y = anchor_y - grid * 1.4
        button_xs = self._toolbar_positions(
            [
                ("btn_home", 1 / 6),
                ("btn_back", 4 / 3),
                ("btn_forward", 2.5),
                ("btn_reset", 11 / 3),
                ("btn_exit", 29 / 6),
            ],
            [
                ("btn_home", 0.5),
                ("btn_back", 1.9),
                ("btn_forward", 3.3),
                ("btn_reset", 4.7),
            ],
        )
        positions = {
            "bg": Rect(0, 0, self.image_sizes["bg"].width(), self.image_sizes["bg"].height()),
            "frame": Rect(0, 0, self.image_sizes["frame"].width(), self.image_sizes["frame"].height()),
            "btn_home": self._rect_at(button_xs["btn_home"], button_y, "btn_home"),
            "btn_back": self._rect_at(button_xs["btn_back"], button_y, "btn_back"),
            "btn_forward": self._rect_at(button_xs["btn_forward"], button_y, "btn_forward"),
            "btn_reset": self._rect_at(button_xs["btn_reset"], button_y, "btn_reset"),
            "msg_box": Rect(self.screen_w / 2, self.screen_h / 2 + self.anchor.y_1 / 2 + grid * 3),
        }
        if not self.web_mode:
            positions["btn_exit"] = self._rect_at(button_xs["btn_exit"], button_y, "btn_exit")
        return positions

    def _toolbar_positions(
        self,
        desktop_layout: list[tuple[str, float]],
        web_layout: list[tuple[str, float]],
    ) -> dict[str, float]:
        layout = web_layout if self.web_mode else desktop_layout
        return {
            name: self.anchor.x_1 + self.grid_w * grid_offset
            for name, grid_offset in layout
        }

    def _rect_at(self, x_1: float, y_1: float, image_name: str) -> Rect:
        size = self.image_sizes[image_name]
        return Rect(x_1, y_1, x_1 + size.width(), y_1 + size.height())

    def _empty_board(self) -> list[list[str]]:
        return [["0" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def _handle_init_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYUP:
                self._handle_init_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self._handle_mouse_up(event.pos)

    def _handle_solution_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            elif event.type == pygame.KEYUP:
                self._handle_solution_key(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._click_button(Rect(*event.pos))

    def _handle_init_key(self, key: int):
        if key == pygame.K_SPACE:
            self.reset()
        elif key == pygame.K_RETURN:
            self._solve_current_board()
        elif key == pygame.K_ESCAPE and not self.web_mode:
            self.run = False

    def _handle_solution_key(self, key: int):
        if key == pygame.K_BACKSPACE:
            self.solution = False
        elif key in (pygame.K_a, pygame.K_LEFT) and self.step_print > 0:
            self.step_print -= 1
        elif key in (pygame.K_d, pygame.K_RIGHT) and self.msg.isdigit() and self.step_print < int(self.msg):
            self.step_print += 1
        elif key == pygame.K_SPACE:
            self.step_print = 0
        elif key == pygame.K_ESCAPE and not self.web_mode:
            self.run = False

    def _handle_mouse_down(self, pos: tuple[int, int]):
        mouse = Rect(*pos)
        self.drag_state = self._select_block(mouse)
        self._click_button(mouse)

    def _handle_mouse_up(self, pos: tuple[int, int]):
        if not self.drag_state.active:
            return
        name = self.drag_state.name
        assert name is not None
        offset_x = self.drag_state.offset_x or 0
        offset_y = self.drag_state.offset_y or 0
        width = self.init_pos[name].width()
        height = self.init_pos[name].height()
        can_place, rect = self._place_block(
            Rect(pos[0] - offset_x, pos[1] - offset_y, pos[0] - offset_x + width, pos[1] - offset_y + height)
        )
        if can_place and rect is not None:
            self.blocks_place.setdefault(name, []).append(rect)
        self.drag_state = DragState()

    def _solve_current_board(self):
        self.step_print = 0
        self._update_board()
        self.boards_print, self.msg = solver(self.board)
        self.solution = True

    def _click_button(self, mouse: Rect):
        if self.solution:
            if self.solution_pos["btn_home"].contains(mouse.x_1, mouse.y_1):
                self.solution = False
            elif self.solution_pos["btn_back"].contains(mouse.x_1, mouse.y_1) and self.step_print > 0:
                self.step_print -= 1
            elif self.solution_pos["btn_forward"].contains(mouse.x_1, mouse.y_1) and self.msg.isdigit() and self.step_print < int(self.msg):
                self.step_print += 1
            elif self.solution_pos["btn_reset"].contains(mouse.x_1, mouse.y_1):
                self.step_print = 0
            elif (
                not self.web_mode
                and "btn_exit" in self.solution_pos
                and self.solution_pos["btn_exit"].contains(mouse.x_1, mouse.y_1)
            ):
                self.run = False
            return

        if self.init_pos["btn_reset"].contains(mouse.x_1, mouse.y_1):
            self.reset()
        elif self.init_pos["btn_solve"].contains(mouse.x_1, mouse.y_1):
            self._solve_current_board()
        elif (
            not self.web_mode
            and "btn_exit" in self.init_pos
            and self.init_pos["btn_exit"].contains(mouse.x_1, mouse.y_1)
        ):
            self.run = False

    def _select_block(self, mouse: Rect) -> DragState:
        for name, blocks in self.blocks_place.items():
            for block in list(blocks):
                if block.contains(mouse.x_1, mouse.y_1):
                    blocks.remove(block)
                    return DragState(name, mouse.x_1 - block.x_1, mouse.y_1 - block.y_1)

        for name in PALETTE_BLOCKS:
            if self.init_pos[name].contains(mouse.x_1, mouse.y_1):
                if name == "fish_nor" and self.blocks_place.get("fish_nor"):
                    return DragState()
                return DragState(name, mouse.x_1 - self.init_pos[name].x_1, mouse.y_1 - self.init_pos[name].y_1)
        return DragState()

    def _place_block(self, pos_place: Rect) -> tuple[bool, Rect | None]:
        num_x = round((pos_place.x_1 - self.anchor.x_1) / self.grid_w)
        num_y = round((pos_place.y_1 - self.anchor.y_1) / self.grid_w)
        x_1 = round(self.anchor.x_1 + num_x * self.grid_w, 4)
        y_1 = round(self.anchor.y_1 + num_y * self.grid_w, 4)
        x_2 = round(x_1 + pos_place.width(), 4)
        y_2 = round(y_1 + pos_place.height(), 4)
        candidate = Rect(x_1, y_1, x_2, y_2)
        if not self._within_board(candidate):
            return False, None
        if self._overlaps_existing(candidate):
            return False, None
        return True, candidate

    def _within_board(self, rect: Rect) -> bool:
        board_rect = Rect(
            round(self.anchor.x_1, 4),
            round(self.anchor.y_1, 4),
            round(self.anchor.x_1 + self.grid_w * BOARD_SIZE, 4),
            round(self.anchor.y_1 + self.grid_w * BOARD_SIZE, 4),
        )
        return (
            board_rect.x_1 <= rect.x_1
            and board_rect.y_1 <= rect.y_1
            and board_rect.x_2 >= rect.x_2
            and board_rect.y_2 >= rect.y_2
        )

    def _overlaps_existing(self, candidate: Rect) -> bool:
        for blocks in self.blocks_place.values():
            for block in blocks:
                if round(abs(block.x_2 + block.x_1 - candidate.x_2 - candidate.x_1), 4) < round(block.x_2 - block.x_1 + candidate.x_2 - candidate.x_1, 4) and round(abs(block.y_2 + block.y_1 - candidate.y_2 - candidate.y_1), 4) < round(block.y_2 - block.y_1 + candidate.y_2 - candidate.y_1, 4):
                    return True
        return False

    def _update_board(self):
        self.board = self._empty_board()
        count = 2
        for block_name, blocks in self.blocks_place.items():
            for block in blocks:
                col_start = round((block.x_1 - self.anchor.x_1) / self.grid_w)
                col_end = round((block.x_2 - self.anchor.x_1) / self.grid_w)
                row_start = round((block.y_1 - self.anchor.y_1) / self.grid_w)
                row_end = round((block.y_2 - self.anchor.y_1) / self.grid_w)
                for row in range(row_start, row_end):
                    for col in range(col_start, col_end):
                        self.board[row][col] = "1" if block_name == "fish_nor" else str(count)
                count += 1

    def _extract_blocks(self, board: list[list[str]]) -> dict[str, list[Rect]]:
        extracted: dict[str, list[Rect]] = {}
        for block in extract_board_info(board):
            asset_name = block_to_asset(block)
            extracted.setdefault(asset_name, []).append(self._block_rect(block))
        return extracted

    def _block_rect(self, block: Block) -> Rect:
        asset_name = block_to_asset(block)
        width = self.image_sizes[asset_name].width()
        height = self.image_sizes[asset_name].height()
        x_1 = self.anchor.x_1 + self.grid_w * block.col
        y_1 = self.anchor.y_1 + self.grid_w * block.row
        return Rect(x_1, y_1, x_1 + width, y_1 + height)

    def _draw_placed_blocks(self, blocks_place: dict[str, list[Rect]]):
        for name, blocks in blocks_place.items():
            for block in blocks:
                self.screen.blit(self.imgs[name], block.point())

    def _draw_dragging_block(self):
        if not self.drag_state.active or self.drag_state.name is None:
            return
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.screen.blit(
            self.imgs[self.drag_state.name],
            (mouse_x - (self.drag_state.offset_x or 0), mouse_y - (self.drag_state.offset_y or 0)),
        )

    def _draw_message(self, rect: Rect):
        label = f"{self.step_print}/{self.msg}" if self.msg.isdigit() else self.msg
        text_width, text_height = self.font.size(label)
        text_surface = self.font.render(label, False, (255, 255, 255))
        self.screen.blit(text_surface, (rect.x_1 - text_width / 2, rect.y_1 - text_height / 2))


def create_game(web_mode: bool = False) -> Game:
    current_w = pygame.display.Info().current_w
    current_h = pygame.display.Info().current_h
    return Game(current_w, current_h, web_mode=web_mode)


def main():
    pygame.init()
    game = create_game(web_mode=False)
    while game.run:
        game.tick()
    pygame.quit()


async def async_main():
    pygame.init()
    await asyncio.sleep(0)
    game = create_game(web_mode=True)
    while game.run:
        game.tick()
        await asyncio.sleep(0)
    pygame.quit()
