# -*- coding:UTF-8 -*-
import requests
import re
from bs4 import BeautifulSoup

def solve2(mystr):
    result = ''
    match = 0
    for s in mystr:
        if s == '<':
            match += 1
            continue
        if s == '>':
            match -= 1
            continue
        if match == 0:
            result += s
    return result


if __name__ == '__main__':
    str1 = 'https://stackoverflow.com/questions/tagged/ide?tab=votes&page='
    str3 = '&pagesize=50'
    for index in range(1, 201):
        file_name = 'data' + str(index) + '.txt'
        f = open(file_name, 'w', encoding='utf-8')
        print(index)
        str2 = str(index)
        target = str1 + str2 + str3
        mainpage = requests.get(url=target).text
        # soup = BeautifulSoup(page, "html.parser")
        # answers = soup.find_all('div', class_="status answered")
        # print(soup)
        votes_num = re.findall('<span class="vote-count-post(.*?)</strong></span>', mainpage, re.S)
        answers_num = re.findall('class="status answered(.*?)</strong>answer', mainpage, re.S)
        questions = re.findall('class="question-hyperlink">(.*?)</a>', mainpage, re.S)
        subpages_address = re.findall('<div class="summary">\r\n        <h3><a href="(.*?)" class="question-hyperlink">',\
                                      mainpage, re.S)
        # print(subpages_address)
        size = len(answers_num)
        for i in range(0, size):
            temp = ''
            for s in answers_num[i]:
                if '0' <= s <= '9':
                    temp += s
            answers_num[i] = temp
            temp = ''
            for s in votes_num[i]:
                if '0' <= s <= '9':
                    temp += s
            votes_num[i] = temp
        for i in range(0, size):        # 遍历问题
            if '[closed]' in questions[i]:
                continue
            if int(votes_num[i]) == 0 or int(answers_num[i]) == 0:
                continue
            target = 'https://stackoverflow.com/' + subpages_address[i]
            print(target)
            subpage = requests.get(url=target).text
            # print(subpage)
            description = re.findall('<div class="postcell post-layout--right">(.*?)<div class="mt24 mb12">',\
                                     subpage, re.S)
            answers = re.findall('<div class="answercell post-layout--right">(.*?)<div class="mt24">',\
                                 subpage, re.S)
            ans_votes = re.findall('"upvoteCount" data-value="(.*?)"', subpage, re.S)
            ans_size = len(answers)
            for j in range(0, ans_size):
                answers[j] = solve2(answers[j])
            description[0] = solve2(description[0])
            f.write('Title: ' + questions[i] + '\n')
            f.write('Description: ' + description[0] + '\n')
            for j in range(0, ans_size):
                # if int(ans_votes[j]) < 5:
                #     continue
                f.write('Answer ' + str(j + 1) + ': \n')
                f.write(answers[j])
                f.write('\n')
        f.close()


