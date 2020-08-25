# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# > Author     : lunar
# > Email       : lunar_ubuntu@qq.com
# > Create Time: Mon 24 Aug 2020 10:11:10 PM CST

import curses
import time
import threading
import sys
from snake import Snake

stdscr = curses.initscr()

def set_win():
    global stdscr
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.nodelay(1)

def unset_win():
    global stdscr
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

start_col = 15
start_row = 10

def menu():
    global stdscr
    stdscr.nodelay(0)
    global lst
    lst = [
            "1. 贪吃蛇",
            "2. 超级玛丽",
            "3. 直升机"
            ]
    games = {
            "1. 贪吃蛇": snake,
            "2. 超级玛丽": mario,
            "3. 直升机": helicopter
            }
    offset = 0
    index = 0
    stdscr.addstr(start_row, start_col, lst[0], curses.color_pair(1))
    for i in range(1, len(lst)):
        stdscr.addstr(start_row+i, start_col, lst[i], curses.color_pair(3))
    stdscr.refresh()
    while True:
        ch = stdscr.getch()
        if ch == ord('q'):
            if quit():
                return True
        elif ch == ord('j'):
            stdscr.addstr(start_row+index, start_col, lst[index], curses.color_pair(3))
            index += 1
            stdscr.addstr(start_row+index, start_col, lst[index], curses.color_pair(1))
            stdscr.refresh()
        elif ch == ord('k'):
            stdscr.addstr(start_row+index, start_col, lst[index], curses.color_pair(3))
            index -= 1
            stdscr.addstr(start_row+index, start_col, lst[index], curses.color_pair(1))
            stdscr.refresh()
        elif ch == ord('l') or ch == 10: # 10表示回车键
            if lst[index] == "1. 贪吃蛇":
                Snake(stdscr).start()
    return True

def spacer(n):
    lst = [" " for i in range(n)]
    return "".join(lst)

# 设计一个是否确认退出游戏的界面
def quit():
    global stdscr
    stdscr.clear()
    stdscr.refresh()
    words = "确认退出游戏?"
    corner = (20, 75)
    #stdscr.addstr(corner[0], corner[1], curses.color_pair(6))
    stdscr.addstr(corner[0], corner[1], spacer(30), curses.color_pair(6))
    stdscr.addstr(corner[0]+1, corner[1], spacer(8), curses.color_pair(6))
    stdscr.addstr(corner[0]+1,corner[1]+8, words, curses.color_pair(5))
    stdscr.addstr(corner[0]+1, corner[1]+21, spacer(9), curses.color_pair(6))
    stdscr.addstr(corner[0]+2, corner[1], spacer(30), curses.color_pair(6))
    stdscr.addstr(corner[0]+3, corner[1], spacer(6), curses.color_pair(6))
    stdscr.addstr(corner[0]+3, corner[1]+6, "[quit]", curses.color_pair(5))
    stdscr.addstr(corner[0]+3, corner[1]+12, spacer(4), curses.color_pair(6))
    stdscr.addstr(corner[0]+3, corner[1]+16, "[cancel]", curses.color_pair(7))
    stdscr.addstr(corner[0]+3, corner[1]+24, spacer(6), curses.color_pair(6))
    stdscr.refresh()
    is_quit = False
    while True:
        stdscr.nodelay(0)
        ch = stdscr.getch()
        if ch == 10:
            break
        elif ch == ord('j') or ch == curses.KEY_LEFT:
            if is_quit:
                continue
            is_quit = True
            stdscr.addstr(corner[0]+3, corner[1]+6, "[quit]", curses.color_pair(7))
            stdscr.addstr(corner[0]+3, corner[1]+16, "[cancel]", curses.color_pair(5))
            stdscr.refresh()
            continue
        elif ch == ord('k') or ch == curses.KEY_RIGHT:
            if not is_quit:
                continue
            is_quit = False
            stdscr.addstr(corner[0]+3, corner[1]+6, "[quit]", curses.color_pair(5))
            stdscr.addstr(corner[0]+3, corner[1]+16, "[cancel]", curses.color_pair(7))
            stdscr.refresh()
            continue
    if is_quit:
        sys.exit()
    return is_quit

def snake():
    global lst
    global stdscr
    stdscr.clear()
    stdscr.refresh()
    stdscr.timeout(0)
    start_col = 3
    start_row = 2
    length = 3
    stdscr.addstr(start_row, start_col, ">", curses.color_pair(1))
    for i in range(1, length):
        stdscr.addstr(start_row, start_col-i, "=", curses.color_pair(3))
    stdscr.refresh()

    while start_col < 100:
        start_col += 1
        stdscr.addstr(start_row, start_col, ">", curses.color_pair(1))
        stdscr.addstr(start_row, start_col-1, "=", curses.color_pair(3))
        stdscr.addstr(start_row, start_col-length-1, " ", curses.color_pair(4))
        stdscr.refresh()
        time.sleep(0.2)
        if stdscr.getch() == ord('q'):
            quit()

def mario():
    pass


def helicopter():
    pass

if __name__ == "__main__":
    try:
        set_win()
        menu()
    except Exception as e:
        raise e
    finally:
        unset_win()

