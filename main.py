# 导入 jieba 分词包
import jieba
import jieba.analyse
# 导入 html 包
import html
# 导入正则包
import re
# 导入数据集处理包
from datasketch import MinHash
# 从命令行获取参数包
import sys


# 传入一段内容将其中的符号，html标签等内容过滤，再提取关键字
def extract_keyword(content):
    # 过滤掉 html 标签
    re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
    content = re_exp.sub(' ', content)
    content = html.unescape(content)
    # 使用 jieba 分词 将一段文字分成词
    seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
    # 将所有关键词提取出来并返回
    keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
    return keywords


# 根据两篇文章的关键词计算相似度
def calc_of_similarity(x, y):
    # MinHash计算
    minhash_x, minhash_y = MinHash(), MinHash()
    # 提取关键词
    s1 = extract_keyword(x)
    s2 = extract_keyword(y)

    for data in s1:
        minhash_x.update(data.encode('utf8'))
    for data in s2:
        minhash_y.update(data.encode('utf8'))

    return minhash_x.jaccard(minhash_y)


# 测试
if __name__ == '__main__':
    # 使用sys库, 从命令行获取两篇文章的文件地址参数与输出文件地址参数
    # 并赋值给对应的参数
    compare_address1 = sys.argv[1]
    compare_address2 = sys.argv[2]
    output_address = sys.argv[3]
    # 打开包含两篇文章的文件, 并将其内容比较相似度
    with open(compare_address1, 'r') as x, open(compare_address2, 'r') as y:
        content1 = x.read()
        content2 = y.read()
        similarity = calc_of_similarity(content1, content2)
        # 将计算得出的相似度写入到指定文件中
        with open(output_address, 'w') as f:
            f.write('两篇文章的相似度: %.2f%%' % (similarity * 100))
