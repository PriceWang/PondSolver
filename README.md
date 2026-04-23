<!--
 * @Author: Guoxin Wang
 * @Date: 2024-09-17 11:29:44
 * @LastEditors: Guoxin Wang
 * @LastEditTime: 2026-04-23 11:20:43
 * @FilePath: /PondSolver/README.md
 * @Description:
 *
 * Copyright (c) 2024 by Guoxin Wang, All Rights Reserved.
-->

<div align="center">

## 浅塘解题器

[English](README_EN.md) / 中文

<p align="center">
  <img src="https://private-user-images.githubusercontent.com/30796250/582605764-fb7887d5-fc52-4823-8fa3-a73da5b4ac01.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzY5Mzk5MzMsIm5iZiI6MTc3NjkzOTYzMywicGF0aCI6Ii8zMDc5NjI1MC81ODI2MDU3NjQtZmI3ODg3ZDUtZmM1Mi00ODIzLThmYTMtYTczZGE1YjRhYzAxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MjMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDIzVDEwMjAzM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWFkNTllYWI1MmYxZjU1NjdjNjdkMzk5ODRmZmI5ZjllOTU5MGJkYTRhNTUxMGE0MGM4ZDA3YTJjNDE0NTczYTMmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.ty7iHDvlHfr5mD9QQKHEiCZPdu93I-iER56XP4pgM24" width="30%">
</p>

> **为“[浅塘](https://apps.apple.com/us/app/%E6%B5%85%E5%A1%98/id1090426612?l=zh)”游戏快速寻找最优解**

</div>

### 开发日志

- [x] 基础功能 (v1.0)
- [x] Readme 中文版 (v1.1)
- [x] 加速解答计算 (v1.2)
- [x] Readme 英文版 (v1.3)
- [x] 完整功能 (v2.0)
- [x] 键盘控制 (v2.1)
- [ ] 优化 (v2.2)

### 准备工作

安装依赖：

```
pip install pygame
```

### 项目结构

```
Game.py              # 桌面版入口
main.py              # 网页版入口
pondsolver/
  assets.py          # 资源与尺寸常量
  game.py            # Pygame 主循环与交互逻辑
  models.py          # 通用数据结构
  solver.py          # 求解器核心逻辑
```

### 求解

运行解题器：

```
python Game.py
```

- 按照当前关卡拖放块。
- 左键单击灯泡求解

在线体验：

- itch.io: https://pricewang.itch.io/pondsolver
