import KBEngine
from KBEDebug import *
from interfaces.Site import Site
from interfaces.Building import Building
"""
当前问题
1. 不是南科大大富翁的逻辑
"""


class StudyRoom(Site, Building):
    def __init__(self, location, room):
        """ 根据角色level 决定可以加多少学力点
        :param room:
        """
        Site.__init__(self, location, room)
        Building.__init__(self)

    def update_viable(self):
        """判断是否可以升级"""
        return True

    def leave_site(self, player_id):
        """ 离开站点 """
        self.enter_player_list.remove(self.find_player_from_list(player_id))
        self.curr_player = None
        self.curr_is_owner = False

    def site_event(self):
        """ 询问是否要进入自习室学习 """
        curr_pos = self.curr_player.position
        if self.curr_player.card_package.is_have_book():
            if self.curr_player.player_id == self.owner.player_id:  # 如果是自习室主人
                INFO_MSG("主人学习")
                self.curr_is_owner = True
                if self.curr_player.card_package.is_have_xiuxian:
                    # 需求（价钱，书籍数量, 是否有修仙卡, 可以获得的学力点）
                    self.curr_player.seat.entity.cell.show_enter_study(0, 1, True, self.level, curr_pos)
                else:
                    self.curr_player.seat.entity.cell.show_enter_study(0, 1, False,self.level, curr_pos)
            else:
                INFO_MSG("别人学习")
                if self.curr_player.card_package.is_have_xiuxian:
                    # 需求（价钱，书籍数量, 是否有修仙卡）
                    self.curr_player.seat.entity.cell.show_enter_study(self.study_pay, 1, True, self.level, curr_pos)
                else:
                    self.curr_player.seat.entity.cell.show_enter_study(self.study_pay, 1, False, self.level, curr_pos)
        else:
            self.curr_player.seat.entity.Next()

    def player_study(self):
        """ 不用卡学习 """
        INFO_MSG("用卡学习")
        if not self.curr_is_owner:
            # 玩家付钱，主人挣钱
            self.curr_player.pay_money(self.study_pay)
            self.owner.earn_money(self.study_pay)
        self.curr_player.card_package.remove_book()
        self.curr_player.get_ability(self.level)

    def player_use_xiuxian_card_study(self):
        """使用休修仙卡学习"""
        INFO_MSG("不用卡学习")
        self.curr_player.card_package.remove_xiuxian()
        if not self.curr_is_owner:
            # 玩家付钱，主人挣钱
            self.curr_player.pay_money(self.study_pay)
            self.owner.earn_money(self.study_pay)
        self.curr_player.card_package.remove_book()
        self.curr_player.get_ability(2 * self.level)

    def try_to_buy(self):
        """ 如果当前玩家有交易卡，且不是主人，尝试去购买此建筑 """

        if self.curr_player.card_package.is_have_transaction() and not self.curr_is_owner:
            self.curr_player.seat.entity.cell.show_weather_to_buy(self.owner, 'StudyRoom')
        else:
            # 没卡买房，下一个王家
            KBEngine.globalData["Halls"].getRoom(int(self.room_id)).next()
        
    def show_update(self):
        """ 客户端显示升级, 传入的location位置"""
        self.curr_player.seat.entity.cell.show_building_update(self.location)

    def show_downgrade(self):
        """ 客户端显示降级, 传入的location位置"""
        self.curr_player.seat.entity.cell.show_building_downgrade(self.location)

    def sell_site(self, older, newer):
        """ 卖房子(玩家第一次建筑的时候也调用)"""
        if older is not None:  # 不是第一次购买
            newer.card_package.remove_transaction()
            # 玩家收钱比率
            self.game_pay /= older.earn_money_rate
            self.study_pay /= older.earn_money_rate
            self.game_pay *= newer.earn_money_rate
            self.study_pay *= newer.earn_money_rate
            older.sell_house(2 * self.price, self)
            newer.buy_house(2 * self.price, self)
        else:
            newer.buy_house(self.price, self)
        self.owner = newer
        INFO_MSG("new owner{}".format(newer.player_id))