# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:21
# @Author : 曾佳宝
# @File : ClassicProblem.py
# @Software : PyCharm

class ClassicProblem(object):
    # private
    __classic_problem_id = 0
    __class_problem_type = ''

    @property
    def classic_problem_id(self):
        return self.__classic_problem_id

    @classic_problem_id.setter
    def classic_problem_id(self, classic_problem_id):
        self.__classic_problem_id = classic_problem_id

    @property
    def class_problem_type(self):
        return self.__class_problem_type

    @class_problem_type.setter
    def class_problem_type(self, class_problem_type):
        self.__class_problem_type = class_problem_type
