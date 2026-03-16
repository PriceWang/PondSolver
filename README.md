<!--
 * @Author: Guoxin Wang
 * @Date: 2024-09-17 11:29:44
 * @LastEditors: Guoxin Wang
 * @LastEditTime: 2026-03-16 16:51:06
 * @FilePath: /PondSolver/README.md
 * @Description:
 *
 * Copyright (c) 2024 by Guoxin Wang, All Rights Reserved.
-->

<div align="center">

## 浅塘解题器

[English](README_EN.md) / 中文

<p align="center">
  <img src="https://github.com/user-attachments/assets/e5b71922-b4d4-4cf4-a984-f51cef8ca73a" width="30%">
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
