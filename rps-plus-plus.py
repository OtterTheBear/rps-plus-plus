#! /usr/bin/python3

import curses as c
import random as r
stdscr = c.initscr()
(maxy, maxx) = stdscr.getmaxyx()
# The method returns sizes not "maximum values"
maxy -= 1
maxx -= 1

c.raw()
c.noecho()
stdscr.keypad(True)

boxx = 0
boxy = 0

flashnum = c.A_NORMAL

def win_against(num):
    if num % 2 == 0:
        return num - 1
    else:
        return (num + 3) % 4



try:
    while True:
        aichoice = r.randint(1, 4)
        (y, x) = c.getsyx()
        stdscr.addstr(0, 0,
        """+--+--+
|01|02|
+--+--+
|03|04|
+--+--+""")
        y = 2
        x = 1
        stdscr.move(boxy * 2 + 1, boxx * 3 + 1)

        k = stdscr.getch()
        stdscr.addstr(maxy, 0, (c.keyname(k).decode("utf-8") + (" " * (maxx + 1)))[:maxx])
        stdscr.move(7, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, 0, str(boxx))
        if k == c.KEY_RIGHT:
            boxx += 1
        elif k == c.KEY_LEFT:
            if boxx > 0:
                boxx -= 1
        elif k == c.KEY_DOWN:
            boxy += 1
        elif k == c.KEY_UP:
            if boxy > 0:
                boxy -= 1

        elif c.keyname(k).decode("utf-8") == "^J":
            playerchoice = 1
            if (boxx, boxy) == (0, 0):
                pass
            elif boxx == 1 and boxy == 0:
                playerchoice = 2
            elif boxx == 0 and boxy == 1:
                playerchoice = 3
            elif (boxx, boxy) == (1, 1):
                playerchoice = 4

            stdscr.addstr(6, 0, f"AI chose {aichoice}, you chose {playerchoice}")

            if abs(playerchoice - aichoice) in (2, 0):
                stdscr.addstr(7, 0, "Draw", flashnum)
            else:
                if playerchoice == win_against(aichoice):
                    stdscr.addstr(7, 0, "AI wins", flashnum)
                else:
                    stdscr.addstr(7, 0, "Player wins", flashnum)
            if flashnum == c.A_NORMAL:
                flashnum = c.A_REVERSE
            else:
                flashnum = c.A_NORMAL
        elif k == ord("q"):
            break
finally:
    c.noraw()
    c.cbreak()
    c.echo()
    stdscr.keypad(False)
    c.endwin()
