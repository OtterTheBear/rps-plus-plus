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

playerhist = []
playerhp = 3
aihp = 3
exitcode = 0

flashnum = c.A_NORMAL

with open("HELP", "r") as halp:
    halpstr = halp.read()

# Return what a choice wins against
def win_against(num):
    if num == 1:
        return 4
    elif num == 2:
        return 1
    elif num == 3:
        return 2
    elif num == 4:
        return 3



try:
    while True:
        (y, x) = c.getsyx()
        stdscr.addstr(0, 0,
        """+--+--+
|01|02|
+--+--+
|03|04|
+--+--+""")
        y = 2
        x = 1
        stdscr.addstr(8, 0, f"AI HP: {aihp} Your HP: {playerhp}")

        stdscr.move(boxy * 2 + 1, boxx * 3 + 1)
        if (aihp == 0) or (playerhp == 0):
            if aihp == 0:
                exitcode = 2
            elif playerhp == 0:
                exitcode = 1
            break
        
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

        elif c.keyname(k).decode("utf-8") == "h":
            stdscr.clear()
            stdscr.addstr(0, 0, halpstr)
            stdscr.addstr(maxy - 1, 0, "Press any key to continue...")
            stdscr.getch()
            stdscr.clear()

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


            if len(playerhist) > 2:
                if (playerhist[-1] == playerhist[-2] == playerhist[-3]):
                    if r.randint(0, 1):
                        if r.randint(1, 10) < 10:
                            aichoice = win_against(win_against(win_against(playerhist[-1])))
                        else:
                            aichoice = playerhist[-1]
                    else:
                        aichoice = playerhist[-1]
                else:
                    aichoice = r.randint(1, 4)
            else:
                aichoice = r.randint(1, 4)







            stdscr.addstr(6, 0, f"AI chose {aichoice if aichoice != 0 else 4}, you chose {playerchoice}")
            playerhist.append(playerchoice)
            if abs(playerchoice - aichoice) in (2, 0):
                stdscr.addstr(7, 0, "Draw", flashnum)
            else:
                if playerchoice == win_against(aichoice):
                    stdscr.addstr(7, 0, "AI wins", flashnum)
                    playerhp -= 1
                else:
                    stdscr.addstr(7, 0, "Player wins", flashnum)
                    aihp -= 1

            if flashnum == c.A_NORMAL:
                flashnum = c.A_REVERSE
            else:
                flashnum = c.A_NORMAL
        elif k == ord("q"):
            exitcode = 0
            break
    if exitcode == 1:
        stdscr.addstr(9, 0, "You died", c.A_BOLD | c.A_UNDERLINE)
        stdscr.getch()
    elif exitcode == 2:
        stdscr.addstr(9, 0, "You killed the AI", c.A_BOLD | c.A_UNDERLINE)
        stdscr.getch()
    elif exitcode == 0:
        pass

finally:
    c.noraw()
    c.cbreak()
    c.echo()
    stdscr.keypad(False)
    c.endwin()
