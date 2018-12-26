from KBEDebug import *
from interfaces.Site import Site
import random
"""
当前问题
"""


class Lakeside(KBEngine.Entity, Site):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        Site.__init__(self)

    def site_event(self):
        """ 随机事件区 """
        r = random.random(0, 1)
        if r <= 0.3:  # 丢失校卡，损失金钱
            self.curr_player.pay_money(100)
            self.curr_player.seat.entity.cell.random_event(1)
        elif r <= 0.35:  # 见到喜欢的异性，上去搭讪, 人格魅力提升
            self.curr_player.seat.entity.cell.random_event(2)
        elif r <= 0.36:  # 看见六栋楼下的情侣缠绵，冲上去打了人，获得行政警告
            self.curr_player.add_administrative_warnning(1)
            self.curr_player.seat.entity.cell.random_event(3)
        elif r <= 0.38:  # 主动到宿舍自习室学习，学力点提升
            self.curr_player.get_ability(1)
            self.curr_player.seat.entity.cell.random_event(4)
        elif r <= 0.49:  # 到舞蹈房练习舞蹈
            self.curr_player.personality.add_art_point(1)
            self.curr_player.seat.entity.cell.random_event(5)
        elif r <= 0.4:  # 骑滑板车被刘主任发现，跑/不跑
            self.curr_player.seat.entity.cell.select_event()
        elif r <= 0.6:  # 看见校长，上前打招呼/走开
            self.curr_player.seat.entity.cell.select_event()
        elif r <= 0.8:  # 活动室赶第二天的project，通宵做完美/赶紧随便做完睡觉
            self.curr_player.seat.entity.cell.select_event()
        elif r <= 0.9:  # 考试周，一个人复习/一群人复习
            self.curr_player.seat.entity.cell.select_event()
        elif r <= 1:  # 宿舍有点脏乱了，立即打扫/先等一等
            self.curr_player.seat.entity.cell.select_event()

    def say_hello_to_schoolmaster(self):
        """ 遇见校长打招呼 """
        self.curr_player.personality.add_social_point(1)

    def not_say_hello_to_schoolmaster(self):
        """ 遇见校长不打招呼"""
        self.curr_player.personality.sub_real_point(1)
        self.curr_player.personality.add_social_point(2)

    def run_away(self):
        """ 骑滑板车跑 """
        self.curr_player.personality.add_real_point(1)

    def not_run_away(self):
        """ 骑滑板车不跑 """
        self.curr_player.personality.add_social_point(1)
        r = random.random(0, 1)
        if r < 0.8:
            self.curr_player.seat.entity.run_successful()
        else:
            # 没跑掉，行政警告
            self.curr_player.add_administrative_warnning()
            self.curr_player.seat.entity.run_fail()

    def stay_up_for_project(self):
        """ 熬夜做project """
        self.curr_player.personality.add_research_point(2)
        self.curr_player.personality.sub_social_point(2)

    def not_stay_up_for_project(self):
        """ 熬夜做project """
        self.curr_player.personality.sub_research_point(2)
        self.curr_player.personality.add_social_point(2)

    def review_alone(self):
        """ 一个人复习 """
        self.curr_player.personality.sub_social_point(1)
        self.curr_player.personality.add_research_point(2)

    def review_together(self):
        """ 一群人复习 """
        self.curr_player.personality.add_social_point(2)
        self.curr_player.personality.sub_research_point(1)

    def clean_right_now(self):
        """ 立马打扫 """
        self.curr_player.personality.add_real_point(2)

    def clean_later(self):
        """ 之后再打扫 """
        self.curr_player.personality.add_social_point(2)
