# 导入 jieba 分词包
import jieba
import jieba.analyse
# 导入数据集处理包
from datasketch import MinHash
import sys
from re import sub


# 传入一段内容将其中的符号，html标签等内容过滤，再提取关键字
def extract_keyword(text):
    # 过滤所有标点符号和 html 标签
    clean = "[^0-9A-Za-z\u4e00-\u9fa5]"
    text = sub(clean, '', text)
    # 使用 jieba 分词 将一段文字分成词
    seg = [i for i in jieba.cut(text, cut_all=True) if i != '']
    # 将所有关键词提取出来并返回
    keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
    return keywords


# 根据两篇文章的关键词计算相似度
def calc_of_similarity(text1, text2):
    # MinHash计算
    minhash1, minhash2 = MinHash(), MinHash()
    # 提取关键词
    keywords1 = extract_keyword(text1)
    keywords2 = extract_keyword(text2)

    for data in keywords1:
        minhash1.update(data.encode('utf8'))
    for data in keywords2:
        minhash2.update(data.encode('utf8'))

    return minhash1.jaccard(minhash2)


if __name__ == '__main__':
    # 标志位, 初始化为 False, 为 True 标志长生异常
    status = False
    # 判断输入的三个文件路径是否有问题, 捕捉该异常
    try:
        # 使用sys库, 从命令行获取两篇文章的文件路径与输出文件路径
        compare_address1 = sys.argv[1]
        compare_address2 = sys.argv[2]
        output_address = sys.argv[3]
    except Exception as e:
        print("请输入三个完整的文件的绝对路径")
        status = True

    # 打开包含两篇文章的文件, 并捕捉 打开文件时 可能产生的异常
    try:
        with open(compare_address1, 'r', encoding='utf-8') as text1, open(compare_address2, 'r',
                                                                          encoding='utf-8') as text2:
            content1 = text1.read()
            content2 = text2.read()
    except Exception as error:
        print("读取文件失败，请检查文件或文件的绝对路径是否有问题")
        status = True
    # 未产生异常才继续计算两篇文章的相似度
    if not status:
        similarity = calc_of_similarity(content1, content2)
        # 将计算得出的相似度写入到指定文件中
        with open(output_address, 'w', encoding='utf-8') as output_file:
            output_file.write('两篇文章的相似度: %.2f%%' % (similarity * 100))
