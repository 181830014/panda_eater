import functools
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import jieba
import jieba.posseg as posseg
from jieba import analyse
import string
import math
from gensim import corpora, models


# jieba分词
def seg_to_list(sentence, pos=False):
    if not pos:
        seg_list = jieba.cut(sentence)
    else:
        seg_list = posseg.cut(sentence)
    return seg_list


# 去除干扰词
def word_filter(seg_list, pos=False):
    stopword_list = [stopword.replace('\n', ' ') for stopword in open("stopwords.txt", encoding='utf-8').readlines()]
    filter_list = []
    for seg in seg_list:
        if not pos:
            word = seg
            flag = 'n'
        else:
            word = seg.word
            flag = seg.flag
        if not flag.startswith('n'):
            continue
        if word not in stopword_list and len(word)>1:
            filter_list.append(word)
    return filter_list


# 排序函数， 用于topK关键字按值排序
def cmp(e1, e2):
    res = np.sign(e1[1] - e2[1])
    if res != 0:
        return res
    else:
        a = e1[0] + e2[0]
        b = e2[0] + e1[0]
        if a > b:
            return 1
        elif a == b:
            return 0
        else:
            return -1


def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if (i not in stop or i.lower() not in stop)])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


class TopicModel(object):
    # 三个传入参数：处理后的数据集，关键词数量，具体模型（LSI、LDA），主题数量
    def __init__(self, doc_list, keyword_num, model='LSI', num_topics=10):
        # 使用gensim的接口，将文本转为向量化表示
        # 先构建词空间
        self.dictionary = corpora.Dictionary(doc_list)
        # 使用BOW模型向量化
        corpus = [self.dictionary.doc2bow(doc) for doc in doc_list]
        # 对每个词，根据tf-idf进行加权，得到加权后的向量表示
        self.tfidf_model = models.TfidfModel(corpus)
        self.corpus_tfidf = self.tfidf_model[corpus]

        self.keyword_num = keyword_num
        self.num_topics = num_topics
        # 选择加载的模型
        if model == 'LSI':
            self.model = self.train_lsi()
        else:
            self.model = self.train_lda()

        # 得到数据集的主题-词分布
        word_dic = self.word_dictionary(doc_list)
        self.wordtopic_dic = self.get_wordtopic(word_dic)

    def train_lsi(self):
        lsi = models.LsiModel(self.corpus_tfidf, id2word=self.dictionary, num_topics=self.num_topics)
        return lsi

    def train_lda(self):
        lda = models.LdaModel(self.corpus_tfidf, id2word=self.dictionary, num_topics=self.num_topics)
        return lda

    def get_wordtopic(self, word_dic):
        wordtopic_dic = {}

        for word in word_dic:
            single_list = [word]
            wordcorpus = self.tfidf_model[self.dictionary.doc2bow(single_list)]
            wordtopic = self.model[wordcorpus]
            wordtopic_dic[word] = wordtopic
        return wordtopic_dic

    # 计算词的分布和文档的分布的相似度，取相似度最高的keyword_num个词作为关键词
    def get_simword(self, word_list):
        sentcorpus = self.tfidf_model[self.dictionary.doc2bow(word_list)]
        senttopic = self.model[sentcorpus]

        # 余弦相似度计算
        def calsim(l1, l2):
            a, b, c = 0.0, 0.0, 0.0
            for t1, t2 in zip(l1, l2):
                x1 = t1[1]
                x2 = t2[1]
                a += x1 * x1
                b += x1 * x1
                c += x2 * x2
            sim = a / math.sqrt(b * c) if not (b * c) == 0.0 else 0.0
            return sim

        # 计算输入文本和每个词的主题分布相似度
        sim_dic = {}
        for k, v in self.wordtopic_dic.items():
            if k not in word_list:
                continue
            sim = calsim(v, senttopic)
            sim_dic[k] = sim

        for k, v in sorted(sim_dic.items(), key=functools.cmp_to_key(cmp), reverse=True)[:self.keyword_num]:
            print(k + "/", end='')
        print()

    @staticmethod
    # 词空间构建方法和向量化方法，在没有gensim接口时的一般处理方法
    def word_dictionary(doc_list):
        dictionary = []
        for doc in doc_list:
            dictionary.extend(doc)

        dictionary = list(set(dictionary))
        return dictionary

    def doc2bowvec(self, word_list):
        vec_list = [1 if word in word_list else 0 for word in self.dictionary]
        return vec_list


def topic_extract(word_list, model, doc_clean, keyword_num=10):
    topic_model = TopicModel(doc_clean, keyword_num, model=model)
    topic_model.get_simword(word_list)


if __name__ == '__main__':
    stop = set(stopwords.words('english'))
    # for w in ['!', ',', '.', '?', 'Android', 'Studio', 'studio', 'How', 'Eclipse', 'IntelliJ', 'IDEA',
    #           'PyCharm', 'JetBrains', 'Xcode']:
    #     stop.add(w)
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    file_object = open('text.txt', encoding='utf-8')
    line = file_object.readline()
    doc_list = []
    while line:
        doc_list.append(line)
        line = file_object.readline()
    # print(text)
    doc_clean = [clean(line).split() for line in doc_list]

    # dictionary = corpora.Dictionary(doc_clean)
    # doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # Lda = models.ldamodel.LdaModel
    # ldamodel = Lda(doc_term_matrix, num_topics=10, id2word=dictionary, passes=50)
    # print(ldamodel.print_topics(num_topics=10, num_words=1))

    file_object_2 = open('text.txt', encoding='utf-8')
    text = file_object_2.read()
    seg_list = seg_to_list(text, pos=False)
    filter_list = word_filter(seg_list, pos=False)
    print('LSI模型结果：')
    topic_extract(filter_list, 'LSI', doc_clean)
    print('LDA模型结果：')
    topic_extract(filter_list, 'LDA', doc_clean)
