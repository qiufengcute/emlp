import random
import time

print('[系统]欢迎来到恶魔轮盘游戏！')
time.sleep(1)
print('[系统]游戏规则是你要选择打谁，如果打敌人而且是实弹的话敌人掉一滴血，空弹不掉血，如果打自己而且是实弹的话自己掉一滴血，空弹不掉血，且你继续行动。如果敌人没血了，那你就赢了，如果你没血了，那敌人就赢了。如果没子弹了，就重新装子弹。每次装子弹都会抽两个道具，最多拿8个道具，如果超过8个就不能抽道具了。')
time.sleep(1)
print('[系统]道具规则是')
time.sleep(1)
print('[系统]啤酒：退掉目前的第一发子弹，会告诉你退掉的子弹是实弹还是空弹。')
time.sleep(1)
print('[系统]手铐：禁止敌人行动一回合。')
time.sleep(1)
print('[系统]小刀：子弹造成的伤害*2，对自己也*2。')
time.sleep(1)
print('[系统]放大镜：告诉你目前的子弹是实弹还是空弹。')
time.sleep(1)
print('[系统]香烟：回一滴血，但血满时不能回血，并且还会消耗')
time.sleep(1)
print('[系统]药片：%40加2滴血，%60扣1滴血。')
time.sleep(1)
print('[系统]转换器：把实弹变成空弹，空弹变成实弹。')
time.sleep(1)
print('[系统]电话：告诉你某一发是什么子弹。')
time.sleep(1)
exe = input('[系统]你，准备好了吗？(n退出，其他开始游戏)')
if exe == 'n':
    exit()

VERSION = '1.1.1'
global myhp
myhp = 5
global dixd
dixd = 0
global zdsh
zdsh = 1
dihp = 5
shen = 'player'
x = []
yy = ['啤酒','手铐','小刀','放大镜','香烟','药片','转换器','电话']
z = ['空','空','空','空','空','空','空','空']
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
zdz = len(x)
e = x

def player(x):
    global myhp
    while True:
        t = input('[系统]请选择要打谁(1是自己,2是对方,3是使用道具,4是关于,5是退出)')
        if t == '1':
            if x[0] == 1:
                print('[玩家]你打到了自己')
                return 'mp'
            else:
                print('[玩家]无事发生')
                return 'buhuan'
        elif t == '2':
            if x[0] == 1:
                print('[玩家]你打到了对方')
                return 'dp'
            else:
                print('[玩家]无事发生')
                return 'l'
        elif t == '3':
            while True:
                print('[系统]你有1.',z[0],'2.',z[1],'3.',z[2],'4.',z[3],'5.',z[4],'6.',z[5],'7.',z[6],'8.',z[7],sep='')
                superm = int(input('[系统]你要使用哪一个？(输编号，9退出)'))
                if superm == 9:
                    break
                elif superm > 0 and superm < 9 and z[superm - 1] != '空':
                    if z[superm - 1] == '放大镜':
                        print('[系统]你使用了放大镜，目前的子弹是',x[0],'(1 = 实,2 = 空)',sep='')
                    elif z[superm - 1] == '小刀':
                        print('[系统]你使用了小刀，子弹造成的伤害*2')
                        global zdsh
                        zdsh = 2
                    elif z[superm - 1] == '啤酒':
                        print('[系统]你使用了啤酒，退掉一发子弹，目前的子弹是',x[0],'(1 = 实,2 = 空)',sep='')
                        x.pop(0)
                    elif z[superm - 1] == '香烟':
                        if myhp == 5:
                            print('[系统]你使用了香烟，但你的血量满了，无法加血')
                        else:
                            print('[系统]你使用了香烟，你加一滴血')
                            myhp += 1
                    elif z[superm - 1] == '手铐':
                        global dixd
                        if dixd == 1:
                            print('[系统]你使用了手铐，但对方已经禁止行动了，无法使用')
                            break
                        else:
                            print('[系统]你使用了手铐，敌方禁止行动一回合')
                            dixd = 1
                    elif z[superm - 1] == '药片':
                        if myhp == 5:
                            print('[系统]你使用了药片，但你的血量满了，无法使用')
                            break
                        else:
                            if random.randint(1,100) < 41:
                                print('[系统]你使用了药片，你加两滴血')
                                myhp += 2
                            else:
                                print('[系统]你使用了药片，但失败了，你扣一滴血')
                                myhp -= 1
                    elif z[superm - 1] == '转换器':
                        if x[0] == 1:
                            print('[系统]你使用了转换器，把实弹变成了空弹')
                            x[0] = 2
                        else:
                            print('[系统]你使用了转换器，把空弹变成了实弹')
                            x[0] = 1
                    elif z[superm - 1] == '电话':
                        global zdz,e
                        r = random.randint(1,zdz)
                        print('[系统]你使用了电话，第',r,'发子弹是',e[r - 1],'(1 = 实,2 = 空)',sep='')
                    z[superm - 1] = '空' 
                else:
                    print('[系统]你输入了错误的编号')
        elif t == '4':
            print('[系统]目前版本:',VERSION,'作者:秋风')
        elif t == '5':
            exit()
        else:
            print('[系统]输入错误')

def di(s,x):
    def da(fang,x):
        if fang == 'player':
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
    ran = random.randint(1,10)
    if s > len(x) - s:
        t = 1
    else:
        t = 2
    if t == 1:
        if ran <= 8:
            return da('player',x)
        else:
            return da('di',x)
    else:
        if ran <= 4:
            return da('player',x)
        else:
            return da('di',x)

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
