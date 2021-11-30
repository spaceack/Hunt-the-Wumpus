from rich import print
import random

MAP = []
MAP_X = 5
MAP_Y = 5
PALYING = "playing"
WIN = "win"
FAIL = "fail"
WUMPUS = "W"
PLAYER = "M"
SPACE = "."
STATUS = PALYING
p_local = []


def random_local(x, y) -> tuple:
    """随机生成坐标"""
    return random.randint(0, x - 1), random.randint(0, y - 1)


def create_player_local(x, y) -> tuple:
    """生成怪物和玩家的唯一坐标
    wumpas_local 怪物坐标
    player_local 玩家坐标
    """
    wumpas_local = random_local(x, y)
    player_local = random_local(x, y)
    if wumpas_local == player_local:
        wumpas_local, player_local = create_player_local(x, y)
    if wumpas_local != player_local:
        return (wumpas_local, player_local)


def create_map(x=5, y=5):
    # 生成地图
    yj = []
    for _ in range(y):
        xi = []
        for _ in range(x):
            xi.append(SPACE)
        yj.append(xi)
    wumpas_local, player_local = create_player_local(x, y)

    yj[wumpas_local[0]][wumpas_local[1]] = WUMPUS
    yj[player_local[0]][player_local[1]] = PLAYER
    global p_local
    p_local = [player_local[0], player_local[1]]
    return yj


def map_str(wmap: list):
    """打印地图，通过状态判断是否打印怪物和玩家"""

    gmap = {WUMPUS: "😈", PLAYER: "🤔", SPACE: "⬜️"}
    if STATUS == PALYING:
        gmap[WUMPUS] = "⬜️"
    if STATUS == WIN:
        gmap[WUMPUS] = "🤢"
        gmap[PLAYER] = "😆"
    if STATUS == FAIL:
        gmap[PLAYER] = "😭"
    for line in wmap:
        print("".join([gmap.get(block) for block in line]))


def smell(x, y) -> bool:
    """判断附近是否有怪物"""
    x1 = MAP_X - 1 if p_local[0] == 0 else p_local[0] - 1
    x2 = 0 if p_local[0] == MAP_X - 1 else p_local[0] + 1
    y1 = MAP_Y - 1 if p_local[1] == 0 else p_local[1] - 1
    y2 = 0 if p_local[1] == MAP_Y - 1 else p_local[1] + 1

    round = [(x1, y), (x2, y), (x, y1), (x, y2), (x1, y1), (x1, y2), (x2, y1), (x2, y2)]

    for r in round:
        if MAP[r[0]][r[1]] == WUMPUS:
            return True
    return False


def shoot():
    """"""
    x = p_local[0]
    y = p_local[1]
    ch = input("请选择射箭方向 1.向上，2. 向下，3. 向左 4.向右")
    if ch == "1":
        x = MAP_X - 1 if p_local[0] == 0 else p_local[0] - 1
    if ch == "2":
        x = 0 if p_local[0] == MAP_X - 1 else p_local[0] + 1
    if ch == "3":
        y = MAP_Y - 1 if p_local[1] == 0 else p_local[1] - 1
    if ch == "4":
        y = 0 if p_local[1] == MAP_Y - 1 else p_local[1] + 1
    return x, y


def pre_walk(mehod):
    x = p_local[0]
    y = p_local[1]
    if mehod == "1":
        print("你向上走了一步\n")
        x = MAP_X - 1 if p_local[0] == 0 else p_local[0] - 1
    if mehod == "2":
        print("你向下走了一步\n")
        x = 0 if p_local[0] == MAP_X - 1 else p_local[0] + 1
    if mehod == "3":
        print("你向左走了一步\n")
        y = MAP_Y - 1 if p_local[1] == 0 else p_local[1] - 1
    if mehod == "4":
        print("你向右走了一步\n")
        y = 0 if p_local[1] == MAP_Y - 1 else p_local[1] + 1
    if mehod == "5":
        x, y = shoot()
    return x, y


def begin():
    # 生成地图
    global MAP
    MAP = create_map(MAP_X, MAP_X)
    # 打印地图
    map_str(MAP)


def action():
    global STATUS
    method = input("你想\n1.向上走\n2.向下走\n3.向左走\n4.向右走\n5.射箭\n->")
    x, y = pre_walk(method)
    if MAP[x][y] == SPACE and method != "5":
        MAP[x][y] = PLAYER
        MAP[p_local[0]][p_local[1]] = SPACE
        p_local[0] = x
        p_local[1] = y
        map_str(MAP)
        if smell(x, y):
            print("[bold yellow]你嗅到了乌姆帕斯的气息[/bold yellow]")

    elif MAP[x][y] == WUMPUS and method != "5":
        print("你被怪物吃掉了，游戏失败, 请重新开始")
        STATUS = FAIL
        map_str(MAP)
        menu()
    elif MAP[x][y] == WUMPUS and method == "5":
        print("你战胜了怪物，恭喜您获得了胜利, 请开始新的一局")
        STATUS = WIN
        map_str(MAP)
        menu()
    elif MAP[x][y] != WUMPUS and method == "5":
        print("你的箭用完了,并没有杀掉怪物，游戏失败 请开始新的一局")
        STATUS = FAIL
        map_str(MAP)
        menu()
    else:
        map_str(MAP)


def menu():
    global STATUS
    STATUS = PALYING
    print("===欢迎进入乌姆帕斯的世界===")
    ch = input("1. 开始\n2. 退出\n->")
    if ch == "1":
        begin()
    if ch == "2":
        print("好吧， 下次再见👋")


def main():
    # 欢迎菜单
    menu()
    # 事件循环
    while STATUS != WIN or STATUS != FAIL:
        action()


if __name__ == "__main__":
    main()
