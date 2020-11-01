# -*- coding:UTF-8 -*-
import requests
import re


def html2plaintext(mystr):
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


def html2numstr(mystr):
    ret = ''
    for digit in mystr:
        if '0' <= digit <= '9':
            ret += digit
    return ret


if __name__ == '__main__':
    url_h = 'https://stackoverflow.com/questions/tagged/ide?tab=votes&page='
    url_t = '&pagesize=50'
    for index in range(70, 71):
        file_path = './results/data' + str(index) + '.txt'
        f = open(file_path, 'w', encoding='utf-8')
        print(index)
        url_m = str(index)
        target = url_h + url_m + url_t
        mainpage = requests.get(target).text

        votes_pattern = '<span class="vote-count-post(.*?)</strong></span>'
        answers_pattern = 'class="status answered(.*?)</strong>answer'
        questions_pattern = 'class="question-hyperlink">(.*?)</a>'
        suburl_pattern = '<div class="summary">\r\n        <h3><a href="(.*?)" class="question-hyperlink">'
        description_pattern = '<div class="postcell post-layout--right">(.*?)<div class="mt24 mb12">'
        anscell_pattern = '<div class="answercell post-layout--right">(.*?)<div class="mt24">'
        ansvote_pattern = '"upvoteCount" data-value="(.*?)"'

        votes = re.findall(votes_pattern, mainpage, re.S)
        answers = re.findall(answers_pattern, mainpage, re.S)
        questions = re.findall(questions_pattern, mainpage, re.S)
        suburls = re.findall(suburl_pattern, mainpage, re.S)
        # print(suburls)
        for (answer, vote, question, suburl) in zip(answers, votes, questions,suburls):
            answer = html2numstr(answer)
            vote = html2numstr(vote)
            if '[closed]' in question:
                continue
            if int(vote) == 0 or int(answer) == 0:
                continue
            target = 'https://stackoverflow.com/' + suburl
            subpage = requests.get(target).text
            print(target)
            descriptions = re.findall(description_pattern, subpage, re.S)
            anscells = re.findall(anscell_pattern, subpage, re.S)
            ansvotes = re.findall(ansvote_pattern, subpage, re.S)

            anscells = [html2plaintext(ans) for ans in anscells]
            descriptions[0] = html2plaintext(descriptions[0])
            f.write('Title: ' + question + '\n')
            f.write('Description: ' + descriptions[0] + '\n')
            for i in range(0, len(anscells)):
                # if int(ans_votes[j]) < 5:
                #     continue
                f.write('Answer ' + str(i + 1) + ': \n')
                f.write(anscells[i])
                f.write('\n')

        f.close()


# 80, 84