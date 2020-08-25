# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# > Author     : lunar
# > Email       : lunar_ubuntu@qq.com
# > Create Time: Tue Aug 25 12:23:49 2020

# 贪吃蛇模块
# 蛇移动的诀窍：总是在头部增加节点，尾部减少节点。
# 当改变方向时，就相当于增加头部节点的方向改变了。

import curses
import time
import sys

RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

class Snake(object):
    def __init__(self, stdscr, head_row=0, head_col=3, length=3):
        self.stdscr = stdscr
        self.stdscr.clear()
        self.stdscr.refresh()
        length = min(length, head_col)
        self.length = length
        self.direction = RIGHT # directions: 0 right, 1 left, 2 up, 3 down
        self.node = "+"
        self.body = [(0,3), (0,2), (0,1)]
        # 采用异步接受键盘输入
        self.stdscr.timeout(0)

    def start(self):
        while True:
            ch = self.stdscr.getch()
            if ch == ord('w') and self.direction != DOWN:
                self.direction = UP
            elif ch == ord('s') and self.direction != UP:
                self.direction = DOWN
            elif ch == ord('a') and self.direction != RIGHT:
                self.direction = LEFT
            elif ch == ord('d') and self.direction != LEFT:
                self.direction = RIGHT
            elif ch == ord('q'):
                self.quit()
            self.move()
            if self.is_dead():
                self.quit()
            time.sleep(0.2)

    # 初期版本，不包含判断用户终端大小的代码。所以用户请全屏体验
    # 由于我的屏幕是172*43，所以就按这个来吧
    def is_dead(self):
        header_pos = self.body[0]
        if header_pos[0] < 0 or header_pos[0] > 43:
            return True
        elif header_pos[1] < 0 or header_pos[1] > 172:
            return True
        return False

    def move(self):
        self.addnode()
        self.delnode()
        self.stdscr.refresh()

    def addnode(self):
        header_pos = self.body[0]
        new_node = [header_pos[0], header_pos[1]]
        if self.direction == UP:
            new_node[0] -= 1
        elif self.direction == DOWN:
            new_node[0] += 1
        elif self.direction == RIGHT:
            new_node[1] += 1
        elif self.direction == LEFT:
            new_node[1] -= 1
        self.stdscr.addstr(new_node[0], new_node[1], self.node, curses.color_pair(1))
        self.body.insert(0, tuple(new_node))

    def delnode(self):
        last = self.body[-1]
        self.stdscr.addstr(last[0], last[1], " ", curses.color_pair(4))
        self.body.pop()

    def quit(self):
        self.stdscr.clear()
        self.stdscr.refresh()
        words = "确认退出游戏?"
        corner = (20, 75)
        #stdscr.addstr(corner[0], corner[1], curses.color_pair(6))
        self.stdscr.addstr(corner[0], corner[1], spacer(30), curses.color_pair(6))
        self.stdscr.addstr(corner[0]+1, corner[1], spacer(8), curses.color_pair(6))
        self.stdscr.addstr(corner[0]+1,corner[1]+8, words, curses.color_pair(5))
        self.stdscr.addstr(corner[0]+1, corner[1]+21, spacer(9), curses.color_pair(6))
        self.stdscr.addstr(corner[0]+2, corner[1], spacer(30), curses.color_pair(6))
        self.stdscr.addstr(corner[0]+3, corner[1], spacer(6), curses.color_pair(6))
        self.stdscr.addstr(corner[0]+3, corner[1]+6, "[quit]", curses.color_pair(5))
        self.stdscr.addstr(corner[0]+3, corner[1]+12, spacer(4), curses.color_pair(6))
        self.stdscr.addstr(corner[0]+3, corner[1]+16, "[cancel]", curses.color_pair(7))
        self.stdscr.addstr(corner[0]+3, corner[1]+24, spacer(6), curses.color_pair(6))
        self.stdscr.refresh()
        is_quit = False
        while True:
            self.stdscr.nodelay(0)
            ch = self.stdscr.getch()
            if ch == 10:
                break
            elif ch == ord('j') or ch == curses.KEY_LEFT:
                if is_quit:
                    continue
                is_quit = True
                self.stdscr.addstr(corner[0]+3, corner[1]+6, "[quit]", curses.color_pair(7))
                self.stdscr.addstr(corner[0]+3, corner[1]+16, "[cancel]", curses.color_pair(5))
                self.stdscr.refresh()
                continue
            elif ch == ord('k') or ch == curses.KEY_RIGHT:
                if not is_quit:
                    continue
                is_quit = False
                self.stdscr.addstr(corner[0]+3, corner[1]+6, "[quit]", curses.color_pair(5))
                self.stdscr.addstr(corner[0]+3, corner[1]+16, "[cancel]", curses.color_pair(7))
                self.stdscr.refresh()
                continue
        if is_quit:
            sys.exit()
        self.stdscr.timeout(0)
        return is_quit


def spacer(x):
    lst = [" " for i in range(x)]
    return "".join(lst)
