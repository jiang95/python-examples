#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author : lingjun.jlj
# @create : 2018/8/7
# @description:

def MiTest2(n):
    result = []
    for i in range(n):
        result = result[-1:] + result[:-1]
        result = [(n - i)] + result
    print(result)


if __name__:
    MiTest2(5)
