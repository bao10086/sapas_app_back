# -*- coding = utf-8 -*-
# @Time : 2022/11/14 17:24
# @Author : 曾佳宝
# @File : Feedback.py
# @Software : PyCharm

class Feedback(object):
    # private
    __feedback_id = 0
    __user_id = 0
    __feedback_time = ''
    __feedback_info = ''
    __feedback_is_feedbackd = 0
    __feedback_image_folder_path = 0
    __admin_feedback = ''

    @property
    def feedback_id(self):
        return self.__feedback_id

    @feedback_id.setter
    def feedback_id(self, feedback_id):
        self.__feedback_id = feedback_id

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id):
        self.__user_id = user_id

    @property
    def feedback_time(self):
        return self.__feedback_time

    @feedback_time.setter
    def feedback_time(self, feedback_time):
        self.__feedback_time = feedback_time

    @property
    def feedback_info(self):
        return self.__feedback_info

    @feedback_info.setter
    def feedback_info(self, feedback_info):
        self.__feedback_info = feedback_info

    @property
    def feedback_is_feedbackd(self):
        return self.__feedback_is_feedbackd

    @feedback_is_feedbackd.setter
    def feedback_is_feedbackd(self, feedback_is_feedbackd):
        self.__feedback_is_feedbackd = feedback_is_feedbackd

    @property
    def feedback_image_folder_path(self):
        return self.__feedback_image_folder_path

    @feedback_image_folder_path.setter
    def feedback_image_folder_path(self, feedback_image_folder_path):
        self.__feedback_image_folder_path = feedback_image_folder_path

    @property
    def admin_feedback(self):
        return self.__admin_feedback

    @admin_feedback.setter
    def admin_feedback(self, admin_feedback):
        self.__admin_feedback = admin_feedback
