# -*- coding=utf8 -*-
"""
# @Author       : jizhongxian@baidu.com
# @Created Time : 2021-12-09 15:16:09
# @Description  : 文本读取相关
"""
import re
from sys import stdin
from io import open
from os import path
from itertools import islice


def readlines(filename=None, encoding='utf-8', separator=None):
    """从文本文件中一行一行地读取数据

    Args:
        filename (str, optional): 文件名称, 默认使用标准输入. Defaults to None.
        split (str, optional): 行内的字段分割符号，默认使用\t分割，不需要分割时指定空即可. Defaults to ''.

    Yields:
        str/list: 可以是一行字符串，也可以是分割后的列表
    """
    if filename is None:
        filename = stdin.fileno()
    with open(filename, 'r', encoding=encoding, newline='\n') as fr:
        for line in fr:
            line = line.strip('\r\n')
            if separator:
                line = line.split(separator)
            yield line


def readcolumns(filename=None, indexs="", separator="\t"):
    """按行读取数据，并返回指定的列，默认全部列

    Args:
        filename (str, optional): 文件名, 默认使用标准输入. Defaults to None.
        index (str, optional): 以空格分割的列索引. Defaults to "".
        separator (str, optional): 列与列的分隔符. Defaults to "\t".

    Yields:
        list: 一行中的列数据
    """
    slice_style = "^(\d+)?:(-?\d+)(:(-?\d+))?$"
    list_style = "^(-?\d+ +)*-?\d+$"
    if re.search(slice_style, indexs):
        match = re.search(slice_style, indexs)
        start, stop, step = match.group(1), match.group(2), match.group(4)
        start = int(start) if start is not None else None
        stop = int(stop) if stop is not None else None
        step = int(step) if step is not None else None
        index = slice(start, stop, step)
        index_style = "slice"
    elif re.search(list_style, indexs.strip()):
        indexs = [int(i) for i in re.split(" +", indexs) if len(i) > 0]
        index_style = "index"
    else:
        raise Exception(f"{indexs}写法有误，写法1:'0 1 3 4', 写法2:切片写法[2:-1]")

    for cols in readlines(filename, separator=separator):
        if index_style == "slice":
            cols = cols[index]
        else:
            if len(indexs) > 0:
                cols = [cols[i] for i in indexs]
        yield cols


def get_dirpath(filename, up=0):
    """获取完整的文件目录
    Args:
        filename (str): 文件名称
        up (int, optional): 向上回溯几次父目录. Defaults to 0.

    Returns:
        [type]: [description]
    """
    dirname, filename = path.split(path.realpath(filename))
    for _ in range(up):
        dirname = path.dirname(dirname)
    return dirname


if __name__ == "__main__":

    def test_readcolumns1():
        for cols in readcolumns(indexs="0 -1"):
            print(cols)

    def test_readcolumns2():
        for cols in readcolumns(indexs=":-2"):
            print(cols)

    def test_get_dir():
        print(get_dirpath(__file__, up=1))

    test_get_dir()
    test_readcolumns1()
    test_readcolumns2()
