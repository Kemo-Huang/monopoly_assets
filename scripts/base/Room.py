import Functor
from KBEDebug import *

class Room(KBEngine.Entity):
    def __init__(self):
        KBEngine.Entity.__init__(self)
        self.createCellEntityInNewSpace(None)
        self.roomKey = self.cellData["roomKey"]
        self.MaxPlayerCount = self.cellData["playerMaxCount"]
        self.RoomType = self.cellData["RoomType"]

    def NeedPlayersCount(self):
        if self.isDestroyed:
            return 0
        print(str(self.roomKey) + "-需要玩家数量--" + str(self.MaxPlayerCount - len(self.EnterPlayerList)))
        return self.MaxPlayerCount - len(self.EnterPlayerList)

    def enterRoom(self, entityCall):
        if entityCall not in self.EnterPlayerList:
            self.EnterPlayerList.append(entityCall)
        if len(self.EnterPlayerList) == self.MaxPlayerCount and self.RoomType == 0:
            KBEngine.globalData["Halls"].roomIsFull(self, self.roomKey)

        if self.cell is not None:
            # 向cell投送玩家
            self.cell.enterRoom(entityCall)

    def leaveRoom(self, entityID):
        for i in range(len(self.EnterPlayerList)):
            if self.EnterPlayerList[i].id == entityID:
                self.EnterPlayerList.pop(i)
                break

        if self.RoomType == 0:
            KBEngine.globalData["Halls"].roomNeedPlayer(self, self.roomKey)

    def onGetCell(self):
        """
        KBEngine method.
        entity的cell部分实体被创建成功
        """
        for playerEntity in self.EnterPlayerList:
            self.enterRoom(playerEntity)

        if self.MaxPlayerCount > len(self.EnterPlayerList) and self.RoomType == 0:
            KBEngine.globalData["Halls"].roomNeedPlayer(self, self.roomKey)

        self._createSiteEntity(None)

    def CanEnterRoom(self, entityCall):
        if entityCall.cell is None:
            print("没有cell")
            entityCall.createCell(self.cell)
        else:
            entityCall.OnTeleport(self)

    def changeRoomSuccess(self, playerEntity):
        for i in range(len(self.EnterPlayerList)):
            if self.EnterPlayerList[i] == playerEntity:
                self.EnterPlayerList.pop(i)
                if self.RoomType == 0:
                    KBEngine.globalData["Halls"].roomNeedPlayer(self, self.roomKey)
                self.cell.changeRoomSuccess(playerEntity.id)
                break

    def _createSiteEntity(self, entityCall):
        site_id = 0
        KBEngine.createEntityAnywhere("AdminBuilding",
                                        {
                                            "name": "Admin Building",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 3
        KBEngine.createEntityAnywhere("Library",
                                        {
                                            "name": "Library",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 6
        KBEngine.createEntityAnywhere("BuildingOne",
                                        {
                                            "name": "Building One",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 8
        KBEngine.createEntityAnywhere("Canteen",
                                        {
                                            "name": "Canteen",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 10
        KBEngine.createEntityAnywhere("Lakeside",
                                        {
                                            "name": "Lake Side",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 12
        KBEngine.createEntityAnywhere("Lychee",
                                        {
                                            "name": "Lychee Shop",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 14
        KBEngine.createEntityAnywhere("Supply",
                                        {
                                            "name": "Supply",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 16
        KBEngine.createEntityAnywhere("BusStation",
                                        {
                                            "name": "Bus Station",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 18
        KBEngine.createEntityAnywhere("Stadium",
                                        {
                                            "name": "Stadium",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 20
        KBEngine.createEntityAnywhere("Hospital",
                                        {
                                            "name": "Hospital",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )
        site_id = 22
        KBEngine.createEntityAnywhere("Hotel",
                                        {
                                            "name": "Hotel",
                                            "room_id": self.roomKey,
                                            "location": site_id,
                                            "curr_player": entityCall
                                        },
                                        Functor.Functor(self._createSiteCB, site_id)
                                        )

    def _createSiteCB(self, site_id, entityCall):
        self.site_list[site_id] = entityCall
        if site_id == 22:
            self.cell.pass_site(self.site_list)
