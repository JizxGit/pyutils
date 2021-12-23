# -*- coding=utf8 -*-
"""
# @Author       : jizhongxian@baidu.com
# @Created Time : 2021-12-09 15:13:30
# @Description  : 日志、报表相关
"""
from sys import stderr, path
from .debug import IS_DEBUG
from datetime import datetime
from prettytable import PrettyTable
from builtins import repr as sys_repr

# log
def log(msg, show_time=True, show_mode=True, inline=False, for_debug=False):
    """info
    Args:
        msg (object): 要打印的内容str/int/float
        show_time (bool, optional): 是否显示日志时间 。Defaults to True.
        show_mode (bool, optional): 是否显示运行日志等级。 Defaults to True.
        inline (bool, optional): 是否添加\r。 Defaults to False.
        for_debug (bool, optional): 是否只在debug模式下打印. Defaults to False.
    """

    if not isinstance(msg, str):
        msg = str(msg)

    if msg.startswith("\r"):
        inline = True
        msg = msg.strip('\r')  # 后面统一加回来

    if show_mode:
        if for_debug:
            mode = f"\033[32;1mDEBUG\033[0m"
        else:
            mode = f"\033[37;1mINFO\033[0m"
        msg = f"{mode} {msg}"

    if show_time:
        now = datetime.now().strftime("%F %H:%M:%S")
        msg = f"\033[31;1m{now:.22}\033[0m {msg}"

    if inline:  # 通过参数指定
        msg = "\r" + msg
    else:  # 否则添加换行符
        msg = msg + "\n"

    if for_debug:
        if not IS_DEBUG:
            return

    stderr.write(msg)
    stderr.flush()


# table
def get_prettytable(header, rows=None, columns=None, align={}):
    """打印报表

    Args:
        header (list/str): 表头
        rows (list, optional): 行数据. Defaults to None.
        columns (list, optional): 列数据. Defaults to None.
        align (dict, optional): 列的对齐方式，支持的对齐方式：l c r. Defaults to {}.

    Raises:
        Exception: 表头类型异常
        Exception: 行列数据异常

    Returns:
        pretty table: 格式化后的表格
    """

    table = PrettyTable()

    # header处理
    if isinstance(header, str):
        header = header.split()
    elif isinstance(header, list):
        pass
    else:
        type_ = type(header)
        raise Exception(f"不支持的表头类型:{type_}")

    # datas
    if rows:
        table.field_names = header
        table.add_rows(rows)
    elif columns:
        for title, column in zip(header, columns):
            table.add_column(title, column)
    else:
        raise Exception("rows或columns必须二选一")

    # align
    for title, al in align.items():
        table.align[title] = al

    return table


def repr(object):
    """自动打印对象的repr方法

    Args:
        object (object): 对象
    """
    writer = stderr

    writer.write(sys_repr(object))
    writer.write("\n")
    writer.flush()


if __name__ == "__main__":

    def test_log():
        from time import sleep
        for i in range(5):
            sleep(1)
            log("当前编号" + str(i))
        for i in range(5):
            sleep(1)
            log("\r当前编号" + str(i))

    def test_get_prettytable():
        header = "title1 title2 title3 title4"
        datas = [[1, 2, 3, 4.56], [4, "23日", 5, 6],
                 ["水电费", "sdfwe", "稳如", "水电"]]
        rows = datas
        table = get_prettytable(header, rows)
        print(table)

        header = header.split()
        columns = datas
        table = get_prettytable(header, columns=columns, align={"title1": 'l'})
        print(table)
        print(table.align)

    def test_repr():
        repr(1)
        repr("1")
        repr([1, 2, 3, "sd水电"])

    test_get_prettytable()
    print()
    test_log()
    test_repr()
