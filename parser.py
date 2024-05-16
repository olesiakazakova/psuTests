

def simple_test(ans):
    line = ""
    itog = ""
    var_answers = "АБВГДЕЖЗИКЛМНОПРСТУФХКЦЧШЩЭЮЯ"
    line = ans.readline()
    while True:
        line = ans.readline()

        if not line:
            break

        if line[0] in var_answers and line[1] == ")" and line[-2] == "*":
            itog += line[0] + line[1] + "*\n"
        else:
            itog += line[0] + line[1] + "\n"

    itog = itog.rstrip()

    return itog


def vstavka_slova_predlozhenia(ans):
    itog = ""
    while True:
        line = ans.readline()

        if not line:
            break
        if line[0] == "[" and (line[-1] == "]" or line[-2] == "]"):
            if line[-2] == "]":
                for simv in range(1, len(line) - 2):
                    itog += line[simv]
            else:
                for simv in range(1, len(line) - 1):
                    itog += line[simv]

    return itog


def sootv_func(ans):
    itog = {}
    simv = 0

    while True:
        first_word = ""
        second_word = ""
        line = ans.readline()

        if not line:
            break

        if "==" in line:
            for simv in range(len(line)):
                if line[simv] == "=":
                    simv += 2
                    break
                first_word += line[simv]

            if line[-1] == "\n":
                for simv1 in range(simv, len(line) - 1):
                    second_word += line[simv1]
            else:
                for simv1 in range(simv, len(line)):
                    second_word += line[simv1]

            itog[first_word] = second_word

    return itog


##############################################
def vstav():
    questvst = open("quest.txt", "r", encoding="utf-16")

    linevst = questvst.readline()

    if linevst[2] == "В" and linevst[3] == "с":
        itog.write(linevst)
        questvst.close()
        questvst = open("quest.txt", "r", encoding="utf-16")
        vst = vstavka_slova_predlozhenia(questvst)
        itog.write(vst)
    else:
        questvst.close()


def smpl():
    questsmpl = open("quest.txt", "r", encoding="utf-16")
    linesmpl = questsmpl.readline()

    if len(linesmpl) >= 4 and linesmpl[2] == "В" and linesmpl[3] == "ы":
        itog.write(linesmpl)
        questsmpl.close()
        questsmpl = open("quest.txt", "r", encoding="utf-16")
        smpl = simple_test(questsmpl)
        itog.write(smpl)
    else:
        questsmpl.close()


def sootv():
    questsootv = open("quest.txt", "r", encoding="utf-16")
    linesootv = questsootv.readline()

    if len(linesootv) >= 4 and linesootv[2] == "У" and linesootv[3] == "с":
        itog.write(linesootv)
        questsootv.close()
        questsootv = open("quest.txt", "r", encoding="utf-16")
        sotv = sootv_func(questsootv)
        for i, (key, value) in enumerate(sotv.items()):
            if i == len(sotv) - 1:
                itog.write(f"{key} == {value}")
            else:
                itog.write(f"{key} == {value}\n")

    else:
        questsootv.close()


###############################################


# a = open("example_simple.txt", "r",encoding = "utf-8")
# g = simple_test(a)
# print (g)
##print("------------------------")
##a.close()
##
##
# a = open("example_vstavka.txt", "r",encoding = "utf-8")
# b=vstavka_slova_predlozhenia(a)
# print(b)
##a.close()
##print("------------------------")
##a = open("example_sootv.txt", "r",encoding = "utf-8")
##c = sootv(a)
##print(c.items())

test = open("full_test.txt", "r", encoding="utf-8")
quest = open("quest.txt", "w+", encoding="utf-16")
itog = open("itog.txt", "w+", encoding="utf-16")
k = 1
g = 0
line = ""

while True:
    g += 1
    line = test.readline()
    if not line:
        break

    print(g)
    if (line[1] == ")" and line[0].isdigit()) and k != 1:
        quest.close()
        vstav()
        smpl()
        sootv()
        itog.write("\n")

        quest.close()
        open("quest.txt", "w+", encoding="utf-16").close()
        quest = open("quest.txt", "w+", encoding="utf-16")
        quest.write(line)
        k = 1
    else:
        quest.write(line)
        k = 0
# Открываем файл в режиме чтения и записи ('rb+' для бинарного режима)
quest.close()
vstav()
smpl()
sootv()
itog.write("\n")
quest.close()
print(g)
# quest = open("quest.txt","w+",encoding = "utf-16")
# d = simple_test(quest)
# itog.write(d)
# print(d)


# vstav()

# g = str(input())












