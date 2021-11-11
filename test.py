import re

def test1():
    file = open('3.txt', 'r')
    lines = file.readline()
    languages = ''
    c = 0

    while lines:
        str1 = re.findall('(.*?)\;', lines)
        str2 = re.findall('(?<=\;).*$', lines)
        languages += str1[0] + ' or ' + str2[0] + '\n'
        lines = file.readline()

        print(languages)


def test():
    file = open('3.txt', 'r')
    lines = file.readline()
    language = input()

    while lines:
        str1 = re.findall('(.*?)\;', lines)
        print(str1[0])
        str2 = re.findall('(?<=\;).*$', lines)
        print(str2[0])
        lines = file.readline()
        if str1[0] == language or str2[0] == language:
            print("yes")
            break

def find1():
    file = open('3.txt', 'r')
    language = input()

    if language in file.read():
        print("1")
    else:
        print("0")

find1()


    