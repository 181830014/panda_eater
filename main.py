# -*- coding:UTF-8 -*-
import requests
import re

if __name__ == '__main__':
    f = open('D:\\assignment\\software_need\\data.txt', 'w')
    str1 = 'https://stackoverflow.com/questions/tagged/ide?tab=newest&page='
    str3 = '&pagesize=50'
    for i in range(129, 130):
        print(i)
        str2 = str(i)
        target = str1 + str2 + str3
        page = requests.get(url=target).text
        items = re.findall('class="question-hyperlink">(.*?)</a>', page, re.S)
        for item in items:
            f.write(item)
            f.write('\n')
            print(item)
    f.close()