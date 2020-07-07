import argparse
import requests
import os
from bs4 import BeautifulSoup
LEN_OF_THE_STRING = 80


class UsefulInformation:
    def __init__(self, path):
        self.path = path

    def GetText(self, text):
        # Процедура для сформирования текста с максимальной длиной текста не более 80символов в строке,
        # c переводом на другую строку

        ListOfWords = text.split(' ')
        print(ListOfWords)


        #Необходимо убрать переводы на следующую строки


        ResultString = ''
        CurLen = 0  # Переменная, отвечающая за текущуюдлину строки
        for s in ListOfWords:
            if s != '\n':
                if len(s) + CurLen + 1 > LEN_OF_THE_STRING:
                    ResultString += '\n' + s
                    CurLen = len(s)
                else:
                    ResultString += ' ' + s
                    CurLen += len(s) + 1
            else:
                ResultString += '\n'
                CurLen = 0
        return ResultString

    def GetUsefulInformation(self):
        # Процедура для сформирования текста с максимальной длиной текста не более 80символов в строке,
        # c переводом на другую строку
        response = requests.get(self.path)
        # В дальнейшем необходимо составить список кортежей url и текста ссылок, для того чтобы вставить их в необходимое место

        soup = BeautifulSoup(response.text)

        #считывание параметров для извлечения информации с сайта

        param = open('parametr.txt')

        tags = param.read().split()




        ph_tags = soup.find_all(tags)  # Нахождение всех тегов p

        result_without_a = ''  # Результирующая строка без тегов, только с текстом

        for text in ph_tags:
            a_tags_in_ph = text.find_all('a')  # Нахождение всех тегов a, включенных в тег p
            for t_i in a_tags_in_ph:
                t_i.string += '[' + t_i['href'] + ']'
            result_without_a += ''.join(text.get_text().split('\n')) + ' \n '

        return result_without_a

    def make_path_file(self):
        #создание пути, где будет соханятся файл
        #Здесь проиходит отсечение, для формирования пути для директории
        result_dir = self.path.split('//')[1]
        if '/' in result_dir.split('/'):
            result_dir = '/'.join(result_dir.split('/')[:-1])

        os.makedirs(result_dir, exist_ok=True)
        if '.' in self.path.split('/')[-1]:
            result = ''.join(self.path.split('.')[:-1]) + '.txt'
        else:
            result = self.path + '.txt'
        result = result.split('//')[1]
        f = open(result, 'w')
        f.write(self.GetText(self.GetUsefulInformation()))
        return






parser = argparse.ArgumentParser()

parser.add_argument('path')

args = parser.parse_args()


Info = UsefulInformation(args.path)
Info.make_path_file()






























