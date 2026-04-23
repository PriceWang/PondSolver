<!--
 * @Author: Guoxin Wang
 * @Date: 2024-09-17 11:29:44
 * @LastEditors: Guoxin Wang
 * @LastEditTime: 2026-04-23 11:20:48
 * @FilePath: /PondSolver/README_EN.md
 * @Description:
 *
 * Copyright (c) 2024 by Guoxin Wang, All Rights Reserved.
-->

<div align="center">

## PondSolver

English / [中文](README.md)

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/30796250/582605764-fb7887d5-fc52-4823-8fa3-a73da5b4ac01.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzY5Mzk5MzMsIm5iZiI6MTc3NjkzOTYzMywicGF0aCI6Ii8zMDc5NjI1MC81ODI2MDU3NjQtZmI3ODg3ZDUtZmM1Mi00ODIzLThmYTMtYTczZGE1YjRhYzAxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MjMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDIzVDEwMjAzM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWFkNTllYWI1MmYxZjU1NjdjNjdkMzk5ODRmZmI5ZjllOTU5MGJkYTRhNTUxMGE0MGM4ZDA3YTJjNDE0NTczYTMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.ty7iHDvlHfr5mD9QQKHEiCZPdu93I-iER56XP4pgM24" width="30%">
</p>

> **A solver for the game '[Pond](https://apps.apple.com/us/app/pond-save-the-little-carp/id1090426612)'**

</div>

### Devlog

- [x] Basic function (v1.0)
- [x] Readme cn version (v1.1)
- [x] Speedup solving (v1.2)
- [x] Readme eng version (v1.3)
- [x] Complete function (v2.0)
- [x] Keyboard control (v2.1)
- [ ] Optimization (v2.2)

### Requirement

Install the required package:

```
pip install pygame
```

### Project Structure

```
Game.py              # Desktop entrypoint
main.py              # Web entrypoint
pondsolver/
  assets.py          # Asset paths and size constants
  game.py            # Pygame loop and interaction logic
  models.py          # Shared data models
  solver.py          # Solver core
```

### Solving

Run the solver:

```
python Game.py
```

- Drag and place blocks for the level.
- Click the bulb for the solution.

Play online:

- itch.io: https://pricewang.itch.io/pondsolver
