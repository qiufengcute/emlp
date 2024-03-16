import random
import time

print('[系统]欢迎来到恶魔轮盘游戏！')
time.sleep(1)
print('[系统]游戏规则见https://wwb.lanzout.com/iJA5a1r5ssmh')
time.sleep(1)
exe = input('[系统]你，准备好了吗？(n退出，其他开始游戏)')
if exe == 'n':
    exit()

myhp = 5
global dixd
dixd = 0
global zdsh
zdsh = 1
dihp = 5
shen = 'player'
x = []
yy = ['啤酒','手铐','小刀','放大镜','香烟']
z = ['香烟','空','空','空','空','空','空','空']
s = 0
while True:
    for i in range(random.randint(4,10)):
        y = random.randint(1,2) # 1 = 实,2 = 空
        if y == 1:
            s += 1
        x.append(y)
    if s != 0 and s != len(x):
        break

for i in range(2):
    sy = z.index('空')
    z[sy] = random.choice(yy)

print('[系统]有',len(x) - s,'发空弹,',s,'发实弹',sep='')

def player(x):
    t = int(input('[系统]请选择要打谁(1是自己,2是对方,3是使用道具)'))
    if t == 1:
        if x[0] == 1:
            print('[玩家]你打到了自己')
            return 'mp'
        else:
            print('[玩家]无事发生')
            return 'buhuan'
    elif t == 2:
        if x[0] == 1:
            print('[玩家]你打到了对方')
            return 'dp'
        else:
            print('[玩家]无事发生')
            return 'l'
    else:
        while True:
            print('[系统]你有1.',z[0],'2.',z[1],'3.',z[2],'4.',z[3],'5.',z[4],'6.',z[5],'7.',z[6],'8.',z[7],sep='')
            superm = int(input('[系统]你要使用哪一个？(输编号，9退出)'))
            if superm == 9:
                return player(x)
            elif superm > 0 and superm < 9 and z[superm - 1] != '空':
                if z[superm - 1] == '放大镜':
                    print('[系统]你使用了放大镜，目前的子弹是',x[0],'(1 = 实,2 = 空)',sep='')
                elif z[superm - 1] == '小刀':
                    print('[系统]你使用了小刀，子弹造成的伤害*2')
                    global zdsh
                    zdsh = 2
                elif z[superm - 1] == '啤酒':
                    print('[系统]你使用了啤酒，退掉一发子弹')
                    x.pop(0)
                elif z[superm - 1] == '香烟':
                    print('[系统]你使用了香烟，你加一滴血')
                    global myhp
                    myhp += 1
                elif z[superm - 1] == '手铐':
                    print('[系统]你使用了手铐，敌方禁止行动一回合')
                    global dixd
                    dixd = 1
                z[superm - 1] = '空'
                return player(x)
            else:
                print('[系统]你输入了错误的编号')

def di(s,x):
    if s > len(x) - s:
        t = 1
    else:
        t = 2
    if t == 1:
        if x[0] == 1:
            print('[敌人]对方打到了你')
            return 'mp'
        else:
            print('[敌人]对方打了你，但无事发生')
            return 'l'
    else:
        if x[0] == 1:
            print('[敌人]对方打到了自己')
            return 'dp'
        else:
            print('[敌人]对方打了自己，但无事发生')
            return 'buhuan'

def look():
    if myhp <= 0:
        return 'di'
    elif dihp <= 0:
        return 'player'
    else:
        return 'wu'

while True:
    if shen == 'player':
        h = player(x)
        x.pop(0)
        
        if h != 'buhuan' and dixd == 0:
            shen = 'di'
        else:
            dixd = 0
        if h == 'mp':
            myhp -= zdsh
            zdsh = 1
            s -= 1
        elif h == 'dp':
            dihp -= zdsh
            zdsh = 1
            s -= 1
    else:
        h = di(s,x)
        x.pop(0)
        if h != 'buhuan':
            shen = 'player'
        if h == 'mp':
            myhp -= 1
            s -= 1
        elif h == 'dp':
            dihp -= 1
            s -= 1

    print('[系统]你还有',myhp,'滴血','对方还有',dihp,'滴血',sep='')
    a = look()
    if a == 'di':
        input("[系统]你输了！")
        exit()
    elif a == 'player':
        input("[系统]你赢了！")
        exit()

    if len(x) == 0:
        while True:
            for i in range(random.randint(4,10)):
                y = random.randint(1,2) # 1 = 实，2 = 空
                if y == 1:
                    s += 1
                x.append(y)
            if s != 0 and s != len(x):
                break
        print('[系统]弹药重装完成')
        print('[系统]有',len(x) - s,'发空弹,',s,'发实弹',sep='')
        print('[系统]正在抽取道具')
        for i in range(2):
            if '空' in z:
                sy = z.index('空')
                z[sy] = random.choice(yy)
            else:
                print('[系统]没有空位，无法抽取道具')
