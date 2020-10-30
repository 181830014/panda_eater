from wordcloud import WordCloud
import nltk
from nltk.corpus import wordnet
from textblob import TextBlob
import random

def myfilter(x):
    return x[1] <= 50 and x[1] > 5

if __name__ == '__main__':

    freq = {}
    for idx in range(1,121):
        print(idx)
        text = ''
        filepath = './results/data' + str(idx) + '.txt'
        f = open(filepath, 'r', encoding='utf8').read()
        plain_text = f.lower()
        for line in plain_text.splitlines():
            if 'answer' in line:
                continue
            if '[closed]' in line or '[duplicate]' in line:
                continue
            # words = line.split(' ')
            # if(len(words) == 0):
            #     continue
            text += line + ' '
        words = nltk.word_tokenize(text)
        tags = set(['VBG', 'NN', 'NNS'])
        ret = []
        pos_tags = nltk.pos_tag(words)
        for word, pos in pos_tags:
            if pos in tags:
                ret.append(word)
        ret = [word for word in ret if wordnet.synsets(word)]
        for word in ret:
            if word in freq:   
                freq[word] += 1
            else:
                freq[word] = 1
        print(len(ret))
    
    freq = sorted(freq.items(), key=lambda x:x[1], reverse=True)
    top_k = []
    keywords = []
    fp = open('freq.txt', 'w', encoding='utf8')
    for x in freq:
        if myfilter(x):
            for xx in range(0, x[1] + 1):
                keywords.append(x[0])
            fp.write(x[0]+'\t'+str(x[1])+'\n')
    print("Almost done ...")
    # open('log.txt', 'w', encoding='utf8').write(keywords)
    random.shuffle(keywords)
    woc = WordCloud().generate(' '.join(keywords))
    image = woc.to_image()
    image.show()