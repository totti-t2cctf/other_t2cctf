# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------------------------------------
# Import

import sys
import math
import random

from logging import getLogger, FileHandler,DEBUG, Formatter
logger = getLogger(__name__)
logger_format = Formatter('[%(levelname)s]:[%(name)s]:[%(asctime)s]|%(message)s')
handler = FileHandler("egf_vf_debug.log")
handler.setLevel(DEBUG)
handler.setFormatter(logger_format)
logger.setLevel(DEBUG)
logger.addHandler(handler)

# ---------------------------------------------------------------------------------------------------------
# Define

# リストの番号
# todo:2016-04-13: 設定？のリストを呼び出すための番号なので、あんまり良くない。辞書化するか、ConfigParserで生成した辞書で扱おう

TOTAL_NODE = 0
MAP_SIZE_X = 1
MAP_SIZE_Y = 2
RADIUS = 3
MAX_SPEED = 4
MAX_WAIT = 5
MAX_KHRONOS = 6
ONE_FRAME = 7
HELLO_PERIOD = 8
TRIALS = 9
SF_CHECK = 10
EXEC_EGF = 11
EGF_DEPTH = 12
ARTIFICIAL = 13
CELL_DIV = 14
VZ_COUNT = 15
NODE_COUNT = 16

# ??
PACKET_SEND_TIME = 0
PACKET_RECV_TIME = 1
PACKET_SEND_BITE = 0
PACKET_RECV_BITE = 1

# ??
REACHSF = 0
REACHGF = 1
REACHEGF = 2

# ??
ID_LENGTH = 4

# ??
TYPE_HELLO = 0
TYPE_SF = 1
TYPE_GF = 2
TYPE_EGF = 3

# ??
SOURCENODE = 0
DESTNODE = 1

# ??
EGF_HOP_FLAG = 0
gf_hop_log = 0
egf_hop_log = 0

# ---------------------------------------------------------------------------------------------------------
def calc_pythagorean_theorem(a, b):
    """ピタゴラスの定理の計算を行う。"""
    # Todo:2016-05-18: 計算するような機能はいずれutils or calcモジュールとして外に出す
    return math.sqrt(a ** 2 + b ** 2)


class Node(object):
    """
    ノードの処理を司る（らしい）
    """

    # todo:2016-04-15: 手を付ける前に処理の構造を学ぶ必要がある
    def __init__(self):

        # todo:2016-04-27:initされる各アトリビュートにコメントしたが、ほとんどのアトリビュートの意味が現時点で把握できてない
        # ID
        self.id = "NaN"

        # location
        self.location = []
        self.dest_location = []

        # 時間っぽいけど秒か不明
        self.speed = -1

        # 方向？ 何が入るか不明
        self.direction = -1

        # 時間っぽいけど秒か不明
        self.wait = -1

        # バッファーらしいけど何が入るか不明
        self.hello_buffer = []

        # 以下の２つのリストに時間とバイトが入るらしいけど、具体的な内容不明
        self.packet_sr_times = [0, 0]
        self.packet_sr_bites = [0, 0]

        # ハローのタイミング?
        self.hello_timing = -1

        # パケットデータのキュー（らしい、未確認）
        self.packet_queue = []

        # 具体的に入る値が不明
        self.hello_list = []

        # ３つの値が入っているが、値の意味やフラグとしての扱われ方がわからない
        self.reach_flag = [0, 0, 0]

    def move(self, one_frame):

        # todo:2016-04-27:メモ:ノードを動かしているらしい。locationは多分x,yの順番, directionは方向らしい？ベクトル？

        self.location[0] = int(self.location[0] +
                               (one_frame * self.speed * math.cos(self.direction)))
        self.location[1] = int(self.location[1] +
                               (one_frame * self.speed * math.sin(self.direction)))
        self.direction = math.atan2((self.dest_location[1] - self.location[1]),
                                    (self.dest_location[0] - self.location[0]))

    def hello_packet_process(self):
        pass

    def sf_packet_process(self):
        pass

    def gf_packet_process(self):
        pass

    def egf_packet_process(self):
        pass

    def _create_packet_data(self, kronos):
        """ハローパケットを作る？ 結果は文字列として返す"""
        HelloPacket = []
        PacketData = []

        # 参考: `0:QFpm:723223:180607:200`
        # 区切り文字が`:` で以下の6つのHelloPacketのappendされている箇所がそのものらしい？

        # はじめから文字列で扱ってもおｋ、現状利用してるのは分岐みやすくするためのみ
        HelloPacket.append(str(TYPE_HELLO))  # パケットのタイプ, helloかどうかを見てる
        HelloPacket.append(self.id)  # ID
        HelloPacket.append(str(self.location[0]))  # ノードの位置（x?
        HelloPacket.append(str(self.location[1]))  # ノードの位置（y?
        HelloPacket.append(str(kronos))

        PacketData.append(":".join(HelloPacket))

        # この辺全体一纏めすることが可能
        # todo:2016-05-14:hello_bufferとは何？
        if len(self.hello_buffer) == 0:
            PacketData = ";".join(PacketData)

        else:
            # todo:2016-05-14: hello_listは何？
            if len(self.hello_list) == 0:
                PacketData = ";".join(PacketData)
                PacketData += "@"

                for hello_buffer_data in self.hello_buffer:
                    PacketData += hello_buffer_data
                    PacketData += "="

                PacketData = PacketData[:len(PacketData) - 1]

            else:
                PacketData = ";".join(PacketData)
                PacketData += "@"

                for hello_buffer_data in self.hello_buffer:
                    PacketData += hello_buffer_data
                    PacketData += "="

                PacketData = PacketData[:len(PacketData) - 1]

                for hello_list_data in self.hello_list:
                    PacketData += ";"
                    PacketData += hello_list_data
        return PacketData

        # logger.debug("{}".format(PacketData))

    def packet_processing(self, Node_List, Config_List, Kronos):

        # 一連のパケット処理をしているらしい。
        PacketData = ""

        # このif文は意味無いと思われる。
        if self.hello_timing < Kronos:
            PacketData = self._create_packet_data(Kronos)

            # self.packet_broadcast(PacketData, Node_List, Config_List[RADIUS])
            self.hello_timing += Config_List[HELLO_PERIOD]

        # 各パケットの生成処理？

        if len(self.packet_queue) != 0:

            # キューからパケットを取り出す
            rawdata = self.packet_queue.pop()

            self.packet_sr_times[1] += 1
            self.packet_sr_bites[1] += len(rawdata)

            # ------------------------------------------------------------------------------------------------
            # [Hello Packet Process]
            if rawdata[0] == str(TYPE_HELLO):

                # パケットのヘッダ？
                rawdata_h = rawdata[2:]

                # ヘッダに@がない場合
                if rawdata_h.find("@") == -1:
                    datalist = rawdata_h.split(":")

                    id_search_flag = 0
                    for i in range(len(self.hello_buffer)):
                        # datalist[0] には rawdata_h.split(":") して
                        if self.hello_buffer[i].find(datalist[0]) != -1:
                            self.hello_buffer[i] = rawdata_h
                            id_search_flag = 1
                            break

                    if id_search_flag == 0:
                        self.hello_buffer.append(rawdata_h)

                # ヘッダに@がある場合
                else:
                    # これは何をしている？
                    if rawdata_h.find(";") == -1:
                        data = rawdata_h.split("@")
                        datalist = data[0].split(":")
                        id_search_flag = 0
                        for i in range(len(self.hello_buffer)):
                            if self.hello_buffer[i].find(datalist[0]) != -1:
                                self.hello_buffer[i] = data[0]
                                id_search_flag = 1
                                break

                        if id_search_flag == 0:
                            self.hello_buffer.append(data[0])

                        # これは何をしている？
                        id_search_flag = 0
                        for i in range(len(self.hello_list)):
                            if self.hello_list[i].startswith(datalist[0]):
                                time_comp = self.hello_list[i].split("@")
                                time_comp = time_comp[0].split(":")
                                if time_comp[3] < datalist[3]:
                                    self.hello_list[i] = rawdata_h

                                id_search_flag = 1
                                break

                        if id_search_flag == 0:
                            self.hello_list.append(rawdata_h)

                    else:
                        # これは何をしている？
                        alldatalist = rawdata_h.split(";")
                        data = alldatalist[0].split("@")
                        datalist = data[0].split(":")

                        id_search_flag = 0
                        for i in range(len(self.hello_buffer)):
                            if self.hello_buffer[i].find(datalist[0]) != -1:
                                self.hello_buffer[i] = data[0]
                                id_search_flag = 1
                                break

                        if id_search_flag == 0:
                            self.hello_buffer.append(data[0])

                        # これは何をしている？
                        id_search_flag = 0
                        for i in range(len(self.hello_list)):
                            if self.hello_list[i].startswith(datalist[0]):
                                time_comp = self.hello_list[i].split("@")
                                time_comp = time_comp[0].split(":")
                                if time_comp[3] < datalist[3]:
                                    self.hello_list[i] = alldatalist[0]

                                id_search_flag = 1
                                break

                        if id_search_flag == 0:
                            self.hello_list.append(alldatalist[0])

                        # これは何をしている？
                        for i in range(1, len(alldatalist)):
                            data = alldatalist[i].split("@")
                            datalist = data[0].split(":")

                            id_search_flag = 0
                            for j in range(len(self.hello_list)):
                                if self.hello_list[j].startswith(datalist[0]):
                                    time_comp = self.hello_list[j].split("@")
                                    time_comp = time_comp[0].split(":")
                                    if time_comp[3] < datalist[3]:
                                        self.hello_list[j] = alldatalist[i]

                                    id_search_flag = 1
                                    break

                            if id_search_flag == 0:
                                self.hello_list.append(alldatalist[i])

            # ------------------------------------------------------------------------------------------------
            # [SF Packet Process]
            elif rawdata[0] == str(TYPE_SF):
                #
                if self.reach_flag[REACHSF] == 0:
                    self.reach_flag[REACHSF] = 1
                    self.packet_broadcast(rawdata,
                                          Node_List,
                                          Config_List[RADIUS])

            # ------------------------------------------------------------------------------------------------
            # [GF Packet Process]
            elif rawdata[0] == str(TYPE_GF):
                temp_raw_data = rawdata[2:]
                datalist = temp_raw_data.split(";")
                destlist = datalist[2].split(":")
                relay_list = datalist[1].split("-")


                if self.id == destlist[0]:
                    self.reach_flag[REACHGF] = 1
                    # print "\ndata =", temprawdata

                    t1 = temp_raw_data.split(";")
                    t2 = t1[1].split("-")

                    # print "hops =", len(t2)-1

                    global gf_hop_log
                    gf_hop_log += len(t2) - 1

                elif self.id == relay_list[len(relay_list) - 1] and self.reach_flag[REACHGF] != 1:
                    PacketData = str(TYPE_GF)

                    # print "data1 =", temprawdata
                    #  print "Chec :", Node_List[DESTNODE].reach_flag

                    self_distance = calc_pythagorean_theorem((int(destlist[1]) - self.location[0]),
                                                             (int(destlist[2]) - self.location[1]))

                    nodes_around_list = self.search_nodes_around(Node_List, Config_List[RADIUS])

                    temp_id = ""
                    temp_distance = self_distance + 1

                    for nodes_around_list_data in nodes_around_list:
                        datalist_t = [nodes_around_list_data.id,
                                      nodes_around_list_data.location[0],
                                      nodes_around_list_data.location[1]]

                        # 距離？
                        temp = calc_pythagorean_theorem((int(destlist[1]) - int(datalist_t[1])), (int(destlist[2]) - int(datalist_t[2])))

                        if temp < temp_distance:
                            temp_id = datalist_t[0]
                            temp_distance = temp

                    if temp_distance < self_distance:
                        datalist[1] += "-" + temp_id
                        adddata = ";".join(datalist)
                        PacketData += ";" + adddata

                        self.packet_broadcast(
                            PacketData, Node_List, Config_List[RADIUS])
                        self.reach_flag[REACHGF] = 1

                        # if Node_List[DESTNODE].reach_flag[1] == 1:
                            # print "data2 =", temprawdata

            # ------------------------------------------------------------------------------------------------
            # [EGF Packet Process]
            elif rawdata[0] == str(TYPE_EGF):
                temp_raw_data = rawdata[2:]
                datalist = temp_raw_data.split(";")
                destlist = datalist[2].split(":")
                relay_list = datalist[1].split("-")

                if self.id == destlist[0]:
                    self.reach_flag[REACHEGF] = 1

                elif self.id == relay_list[len(relay_list) - 1] and self.reach_flag[REACHEGF] != 1:
                    PacketData = str(TYPE_EGF)

                    global EGF_HOP_FLAG
                    if Node_List[DESTNODE].reach_flag[2] == 1 and EGF_HOP_FLAG == 0:
                        # print "data =", temprawdata
                        EGF_HOP_FLAG = 1
                        t1 = temp_raw_data.split(";")
                        t2 = t1[1].split("-")
                        # print "hops =", len(t2)+Config_List[EGFDEPTH]

                        global egf_hop_log
                        egf_hop_log += len(t2) + Config_List[EGF_DEPTH]

                    self_distance = calc_pythagorean_theorem((int(destlist[1]) - self.location[0]), (int(destlist[2]) - self.location[1]))

                    s_v = self.search_nodes_around(Node_List, Config_List[RADIUS])

                    s_vt = []
                    for s_v_data in s_v:
                        datalist_t = [s_v_data.id, s_v_data.location[0], s_v_data.location[1]]

                        temp = calc_pythagorean_theorem((int(destlist[1]) - int(datalist_t[1])),
                                                        (int(destlist[2]) - int(datalist_t[2])))
                        if temp < self_distance:
                            s_vt.append(s_v_data)

                    obj_and_nearest = {}
                    obj_t = []
                    for s_vt_data in s_vt:
                        egf_depth = Config_List[EGF_DEPTH]
                        egf_depth -= 1

                        n_d = []
                        nearest_distance(egf_depth,
                                         s_vt_data,
                                         n_d,
                                         Node_List,
                                         Config_List)

                        if len(n_d) != 0:
                            n_d.sort()
                            obj_and_nearest[s_vt_data] = n_d[0]
                            obj_t.append(s_vt_data)

                    tempid = "NaN"
                    n_val = calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - Node_List[SOURCENODE].location[0]),
                                                     (Node_List[DESTNODE].location[1] - Node_List[SOURCENODE].location[1]))

                    for s_vt_data in obj_t:
                        if obj_and_nearest[s_vt_data] < n_val:
                            tempid = s_vt_data.id
                            n_val = obj_and_nearest[s_vt_data]

                    if tempid != "NaN":
                        datalist[1] += "-" + tempid
                        adddata = ";".join(datalist)
                        PacketData += ";" + adddata

                        self.packet_broadcast(PacketData, Node_List, Config_List[RADIUS])
                        self.reach_flag[REACHEGF] = 1

                        # else:
                            # if Node_List[DESTNODE].reach_flag[REACHEGF] == 0:
                                # print "EGF failed by Relay Node"

    def packet_broadcast(self, PacketData, Node_List, radius):
        self.packet_sr_times[0] += 1
        self.packet_sr_bites[0] += len(PacketData)

        for i in Node_List:
            if i != self:
                temp = calc_pythagorean_theorem((self.location[0] - i.location[0]),  (self.location[1] - i.location[1]))

                if temp < radius:
                    i.packet_queue.append(PacketData)

    def search_nodes_around(self, Node_List, radius):
        # todo:2016-05-12:テストが書けるか検討
        nodes_around_list = []

        for i in Node_List:
            if i != self:
                temp = calc_pythagorean_theorem((self.location[0] - i.location[0]), (self.location[1] - i.location[1]))

                if temp < radius:
                    nodes_around_list.append(i)
        return nodes_around_list

# ---------------------------------------------------------------------------------------------------------
# Functions


# TODO:2016-04-13 ConfigはConfigParserを使うことにしてる。
def open_config(config_list):
    file = open("config.conf", 'r')

    for line in file:
        line = line.replace("\n", "")
        print line
        line = line.split(":")

        if line[1].find("-") != -1:
            temp = line[1].split("-")
            temp[0] = int(temp[0])
            temp[1] = int(temp[1])
            config_list.append(temp)

        else:
            config_list.append(int(line[1]))

    file.close()


def config_checker(config_list):
    """
    読み込んだ設定が利用できる範囲にあるかを調べる。
    :param config_list:
    :return:
    """
    if config_list[ARTIFICIAL] == 1 and config_list[VZ_COUNT] == 0:
        print "Attention: VZ = 0, but ARTIFICIAL = 1."
        exit()

    if config_list[ARTIFICIAL] == 1 and config_list[CELL_DIV] == 0:
        print "Attention: CELLDIV = 0, but ARTIFICIAL = 1."
        exit()

    if config_list[ARTIFICIAL] == 2 and config_list[NODE_COUNT][0] != config_list[NODE_COUNT][1]:
        print "Error: ARTIFICIAL = 2, but NODECOUNT is NOT the same."
        exit()

    if config_list[ARTIFICIAL] == 2:
        print "Attention: Use egf_finalB."
        exit()

    if config_list[CELL_DIV] == 1:
        print "Attention: CELLDIV must be grater than 1."
        exit()

    if config_list[CELL_DIV]**2 < config_list[VZ_COUNT]:
        print "Error: VZ must be less than CELLDIV^2"
        exit()

    if config_list[ARTIFICIAL] == 1 and \
           (config_list[MAP_SIZE_X] % config_list[CELL_DIV] != 0 or
            config_list[MAP_SIZE_Y] % config_list[CELL_DIV] != 0):
        print "Attention: MAPSIZE must be disivle by CELLDIV."
        exit()


def output_hello_result(node_list):
    data_log = open("HELLO_Result.txt", 'w')
    data_log.write("-------------------------------------\n")
    data_log.write("   Hello Result\n")
    data_log.write("-------------------------------------\n\n")

    for i in node_list:
        data_log.write("ID : " + i.id + "\n")
        data_log.write("send_bite, recv_bite = [" + str(
            i.packet_sr_bites[0]) + ", " + str(i.packet_sr_bites[1]) + "]\n")

        data_log.write("hello_buffer = [")
        if len(i.hello_buffer) == 0:
            data_log.write("]\n")

        for j in range(len(i.hello_buffer)):
            data_log.write(i.hello_buffer[j])
            if j != len(i.hello_buffer) - 1:
                data_log.write(", ")
            else:
                data_log.write("]\n")

        data_log.write("hello_list = [")
        if len(i.hello_list) == 0:
            data_log.write("]\n")

        for j in range(len(i.hello_list)):
            data_log.write(i.hello_list[j])
            if j != len(i.hello_list) - 1:
                data_log.write(", ")
            else:
                data_log.write("]\n")

        data_log.write("\n")
    data_log.close()


def output_source_plot(node_list):
    data_log = open("Source_Plot.csv", 'w')

    for i in node_list:
        data_log.write(
            i.id + "," + str(i.location[0] / 1000) + "," + str(i.location[1] / 1000) + "\n")

    data_log.write("\n")

    for hello_list_data in node_list[0].hello_list:
        data = hello_list_data.split("@")
        data = data[0].split(":")
        data_log.write(data[0] + "," + str(int(data[1]) / 1000) +
                       "," + str(int(data[2]) / 1000) + "," + str(data[3]) + "\n")

    data_log.close()


def generate_node_id(length):
    """
    ノードのIDをランダムに生成する
    lengthはIDの長さを示す
    """
    choice_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    return "".join(random.choice(choice_chars) for i in range(length))


def generate_unique_id(id, ids):
    """
    ノードのIDがかぶっていないかチェックしてIDを振り直す

    :param id:
    :param ids:
    :return:
    """
    pass


def create_node(node_list, config_list):
    """
    tempA:cellのX軸座標リスト?
    tempB:cellのY軸座標リスト?
    tempC:マップ全体の分割数?
    tempD:void zoneの配置cell位置?
    """

    # todo:2016-05-25:ノードの生成結果はreturnで返すよう変更する（引数側のリストに入れる必要性があまりないので）
    for i in range(0, config_list[TOTAL_NODE]):
        node_list.append(Node())

    # TODO:2016-04-13 tempA~Dは必要な値なのに無い時の考慮がないので、考慮する
    if config_list[ARTIFICIAL] == 1:
        tempA = []
        tempB = []
        tempC = []

        tempX = 0
        tempY = 0
        x_d = config_list[MAP_SIZE_X] / config_list[CELL_DIV]
        y_d = config_list[MAP_SIZE_Y] / config_list[CELL_DIV]

        for countA in range(config_list[CELL_DIV]):
            tempA.append(tempX)
            tempB.append(tempY)

            tempX += x_d
            tempY += y_d

        for countB in range(config_list[CELL_DIV]**2):
            tempC.append(countB)

        tempD = random.sample(tempC, config_list[VZ_COUNT])

    for i in node_list:

        i.id = generate_node_id(ID_LENGTH)

        # 既存のidとかぶらないかチェックしてる

        unique_id_check = 1
        # Todo:2016-05-19: ここは重複しているかしていないかのチェックが１回のみで、重複する可能性がある。（ノードIDの重複が重要なのかは知らないけど）

        while unique_id_check:
            unique_id_check = 0
            for k in node_list:
                if k != i and k.id == i.id:
                    i.id = generate_node_id(ID_LENGTH)
                    unique_id_check = 1
                    break

        if config_list[ARTIFICIAL] == 0:
            i.location.append(random.randint(0, config_list[MAP_SIZE_X]))
            i.location.append(random.randint(0, config_list[MAP_SIZE_Y]))

        elif config_list[ARTIFICIAL] == 1:

            flagA = 1
            while flagA:
                flagA = 0
                tempXA = random.randint(0, config_list[MAP_SIZE_X])
                tempYA = random.randint(0, config_list[MAP_SIZE_Y])

                for check_in in tempD:
                    amari = check_in % config_list[CELL_DIV]
                    sho = check_in / config_list[CELL_DIV]

                    if ((tempA[amari] <= tempXA) and (tempXA <= tempA[amari] + x_d)) and \
                        ((tempB[sho] <= tempYA) and (tempYA <= tempB[sho] + y_d)):
                        flagA = 1

            i.location.append(tempXA)
            i.location.append(tempYA)

        i.dest_location.append(random.randint(0, config_list[MAP_SIZE_X]))
        i.dest_location.append(random.randint(0, config_list[MAP_SIZE_X]))

        i.speed = random.randint(0, config_list[MAX_SPEED])

        i.direction = math.atan2((i.dest_location[1] - i.location[1]),
                                 (i.dest_location[0] - i.location[0]))

        i.wait = random.randint(0, config_list[MAX_WAIT])

        i.hello_timing = random.randint(0, config_list[HELLO_PERIOD])


def init_sd_node(Node_List, Config_List):

    "ソースノードとディスティネーションノードの初期化"

    Node_List[SOURCENODE].location[0] = 0
    Node_List[SOURCENODE].location[1] = 0
    Node_List[SOURCENODE].dest_location[0] = Config_List[MAP_SIZE_X]
    Node_List[SOURCENODE].dest_location[1] = Config_List[MAP_SIZE_Y]
    Node_List[SOURCENODE].wait = Config_List[MAX_KHRONOS] + 1
    Node_List[DESTNODE].location[0] = Config_List[MAP_SIZE_X]
    Node_List[DESTNODE].location[1] = Config_List[MAP_SIZE_Y]
    Node_List[DESTNODE].dest_location[0] = 0
    Node_List[DESTNODE].dest_location[1] = 0
    Node_List[DESTNODE].wait = Config_List[MAX_KHRONOS] + 1


# def NodeInformation(Node_List):
#     for i in Node_List:
#         print i.id, i.location

# 2円の交点算出 ----------------------------------------
def calc_common_points(point_loc_1, point_loc_2, radius):


    # todo:2016-04-13: これは計算だけど変数名をちゃんとわかりやすくする（したいけどできるかな・・？）
    # todo:2016-05-12: ここのテストがかければテストを書く
    # todo:2016-05-12: point_loc_1, point_loc_2の中身をわかるように書く（x,yの座標だけどデータ構造を正したほうがいい, nametupleかノードのインスタンスを直接呼ぶとか？）

    point_loc_1_x = point_loc_1[0]
    point_loc_1_y = point_loc_1[1]
    point_loc_2_x = point_loc_2[0]
    point_loc_2_y = point_loc_2[1]

    # 円完全一致
    if point_loc_1_x == point_loc_2_x and point_loc_1_y == point_loc_2_y:
        return [[-1, -1], [-1, -1]]

    # X座標で一致
    if point_loc_1_x == point_loc_2_x:
        y = float(point_loc_2_y ** 2 - point_loc_1_y ** 2) / (-2 * point_loc_1_y + 2 * point_loc_2_y)

        l = 1
        m = -2 * point_loc_1_x
        n = point_loc_1_x ** 2 + y ** 2 - 2 * point_loc_1_y * y + point_loc_1_y ** 2 - radius ** 2

        # 一つ目の交点(左側)
        q = float(-m - math.sqrt(m ** 2 - 4 * l * n)) / (2 * l)
        s = y

        # 二つ目の交点(右側)
        r = float(-m + math.sqrt(m ** 2 - 4 * l * n)) / (2 * l)
        t = y

        return [[int(q), int(s)], [int(r), int(t)]]

    # Y座標で一致
    elif point_loc_1_y == point_loc_2_y:
        x = float(point_loc_2_x ** 2 - point_loc_1_x ** 2) / (-2 * point_loc_1_x + 2 * point_loc_2_x)

        l = 1
        m = -2 * point_loc_1_y
        n = point_loc_1_y ** 2 + x ** 2 - 2 * point_loc_1_x * x + point_loc_1_x ** 2 - radius ** 2

        # 一つ目の交点(下側)
        q = x
        s = float(-m - math.sqrt(m ** 2 - 4 * l * n)) / (2 * l)

        # 二つ目の交点(上側)
        r = x
        t = float(-m + math.sqrt(m ** 2 - 4 * l * n)) / (2 * l)

        return [[int(q), int(s)], [int(r), int(t)]]

    # 通常処理
    else:
        alpha = (-2 * point_loc_1_x) + 2 * point_loc_2_x
        beta = (-2 * point_loc_1_y) + 2 * point_loc_2_y
        gamma = (-point_loc_1_x**2) + point_loc_2_x ** 2 - point_loc_1_y ** 2 + point_loc_2_y ** 2

        e = float(-alpha) / beta
        f = float(gamma) / beta

        l = 1 + e ** 2
        m = (-2 * point_loc_2_x) + 2 * e * f - 2 * point_loc_2_y * e
        n = point_loc_2_x ** 2 + f ** 2 - 2 * point_loc_2_y * f + point_loc_2_y ** 2 - radius ** 2

        # 一つ目の交点(左側)
        q = float(-m - math.sqrt(m ** 2 - 4 * l * n)) / (2 * l)
        s = e * q + f

        # 二つ目の交点(右側)
        r = float(-m + math.sqrt(m ** 2 - 4 * l * n)) / (2 * l)
        t = e * r + f

        return [[int(q), int(s)], [int(r), int(t)]]


# ------------------------------------------------------
# Void_Edge内に目的ノードまでの進行方向を持たないノードの距離をn_dリストに挿入
def nearest_distance(egf_depth, node_p, n_d, Node_List, Config_List):
    nodes_around = node_p.search_nodes_around(Node_List, Config_List[RADIUS])

    if egf_depth == 0:
        for i in nodes_around:
            if i.id == Node_List[DESTNODE].id:
                Node_List[DESTNODE].reach_flag[REACHEGF] = 1

        r_v_x = {}
        for nodes_around_data in nodes_around:
            logger.debug("calc common point {} {} {}".format(node_p.location,
                                                             nodes_around_data.location,
                                                             Config_List[RADIUS]))
            temp = calc_common_points(node_p.location,
                                      nodes_around_data.location,
                                      Config_List[RADIUS])
            r_v_x[nodes_around_data] = temp

        r_x = []
        for nodes_around_data in nodes_around:
            for point in r_v_x[nodes_around_data]:
                inside_flag = 0

                for nodes_around_data_t in nodes_around:
                    if nodes_around_data != nodes_around_data_t:

                        temp = calc_pythagorean_theorem((point[0] - nodes_around_data_t.location[0]),
                                                        (point[1] - nodes_around_data_t.location[1]))

                        if temp <= Config_List[RADIUS]:
                            inside_flag = 1

                if inside_flag == 0:
                    r_x.append(point)

        void_edge = []
        while len(r_x) != 0:
            comp = Config_List[RADIUS] + 1
            which_i = 1
            for i in range(1, len(r_x)):
                temp = calc_pythagorean_theorem((r_x[0][0] - r_x[i][0]), (r_x[0][1] - r_x[i][1]))

                if temp < comp:
                    which_i = i

            void_edge.append([r_x[0], r_x[which_i]])
            del r_x[which_i]
            del r_x[0]

        # 180度以上の差があるとき場合わけ
        void_edge_rad = []
        for void_to_rad in void_edge:
            pretemp = []

            pretemp.append(math.atan2((void_to_rad[0][1] - node_p.location[1]),
                                      (void_to_rad[0][0] - node_p.location[0])))

            pretemp.append(math.atan2((void_to_rad[1][1] - node_p.location[1]),
                                      (void_to_rad[1][0] - node_p.location[0])))

            void_edge_rad.append(pretemp)

        self_rad = math.atan2((Node_List[DESTNODE].location[1] - node_p.location[1]),
                              (Node_List[DESTNODE].location[0] - node_p.location[0]))

        for i in void_edge_rad:
            i.sort()

        for two_point in void_edge_rad:
            if (two_point[1] - two_point[0]) < math.pi:
                if self_rad < two_point[0] or two_point[1] < self_rad:
                    n_d.append(calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - node_p.location[0]),
                                                        (Node_List[DESTNODE].location[1] - node_p.location[1])))

#                else:
#                    print "----- Void_Edge In !!! -----"

            else:
                if two_point[0] < self_rad < two_point[1]:
                    n_d.append(calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - node_p.location[0]),
                                                        (Node_List[DESTNODE].location[1] - node_p.location[1])))

#                else:
#                    print "----- Void_Edge In !!! -----"

        if len(void_edge_rad) == 0:
            n_d.append(calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - node_p.location[0]),
                                                (Node_List[DESTNODE].location[1] - node_p.location[1])))

    else:
        egf_depth -= 1

        r_vt = []
        self_distance = calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - node_p.location[0]),
                                                 (Node_List[DESTNODE].location[1] - node_p.location[1]))

        for nodes_around_data in nodes_around:
            datalist = [nodes_around_data.id,
                        nodes_around_data.location[0],
                        nodes_around_data.location[1]]

            temp = calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - int(datalist[1])),
                                            (Node_List[DESTNODE].location[1] - int(datalist[2])))

            if temp < self_distance:
                r_vt.append(nodes_around_data)

        for r_vt_data in r_vt:
            nearest_distance(egf_depth, r_vt_data, n_d, Node_List, Config_List)

def main():
    print "\n-------------------------------------"
    print "           Configuration"
    print "-------------------------------------"

    # 設定を読み込んでチェックする
    config_list = []
    open_config(config_list)
    config_checker(config_list)

    print "\n-------------------------------------"
    print "   Configration check is complete!"
    print "-------------------------------------"
    # print "Start? (y/n)\n"
    # print "(EGF-SNS) >",
    #
    # temp = raw_input()
    #
    # if temp != "y":
    #     print "bye!"
    #     exit()

    logger.debug("set config. and run simurator.")

    print ""

    global gf_hop_log
    global egf_hop_log

    # todo:2016-04-13: csvファイルなので、csvモジュールを使おう
    # todo:2016-04-13: logファイルを書き出すときは一番下でやろう。
    log_csv = open("log_sns.csv", 'a')

    # todo:2016-04-13: ファイルを開くときはwith節を使おう
    file = open("config.conf", 'r')

    # todo:2016-04-13: これはリストで定義するで良くない？
    logdataA = ""
    for line in file:
        line = line.split(":")
        line = line[0].replace(" ", "")
        logdataA += line
        logdataA += ","

    file.close()
    logdataA += "Reachability_SF,Reachability_GF,Reachability_EGF,H_AVE_GF,H_AVE_EGF,R/H_GF,R/H_EGF"
    logdataA += "\n"
    log_csv.write(logdataA)
    log_csv.close()

    for node_inc in range(config_list[NODE_COUNT][0], config_list[NODE_COUNT][1] + 1):
        config_list[TOTAL_NODE] = node_inc

        # todo:2016-04-13 ijkとは一体・・・？
        ijk = 1

        sf_log = 0
        gf_log = 0
        egf_log = 0
        gf_hop_log = 0
        egf_hop_log = 0

        while ijk <= config_list[TRIALS]:

            # シミュレーションの処理時間の可視化（の試みらしい）
            # todo:2016-04-13 シミュレーション処理状況の可視化部分 このモジュールで実装しなおしてみよう。
            # [tqdm](https://github.com/tqdm/tqdm)
            sys.stdout.write("\r")
            sys.stdout.write("Processing... [")

            count_process = 40
            p_count = int((ijk / float(config_list[TRIALS])) * count_process)

            for i in range(p_count):
                sys.stdout.write("*")

            for i in range(count_process - p_count):
                sys.stdout.write(" ")

            sys.stdout.write("]")

            # シミュレーションの試行回数毎にノードを作成する
            Node_List = []
            create_node(Node_List, config_list)
            init_sd_node(Node_List, config_list)

            global EGF_HOP_FLAG
            EGF_HOP_FLAG = 0

    #        total_process = float(Config_List[MAXKHRONOS]) / Config_List[ONEFRAME]
    #        now_process = 0
    #        count_process = 40
    #        print ""
            Kronos = 0
            while Kronos <= config_list[MAX_KHRONOS]:
                # logger.debug("while area: Kronos <= config_list[MAX_KHRONOS]: count{}".format(Kronos))
                #            sys.stdout.write("\r")
                #            sys.stdout.write("Hello-Process ... [")
                #            p_count = int((now_process / total_process) * count_process)

                #            for i in range(p_count):
                #                sys.stdout.write("*")

                #            for i in range(count_process - p_count - int(math.ceil((1 / total_process) * count_process))):
                #            for i in range(count_process - p_count):
                #                sys.stdout.write(" ")

                #            sys.stdout.write("]")


                # Node Movingまでのこのプロセスは、

                # ------------------------------------------------------------------------------------------------
                # [Packet Processing]

                # logger.debug("start packet process")

                # TODO:2016-04-27:ここは何をしているのか？Hello Packet Process?

                # pq_flagとは？-> パケットキュー?の長さ？
                pq_flag = 0

                while pq_flag != 1:

                    for i in Node_List:
                        i.packet_processing(Node_List, config_list, Kronos)

                    # todo:2016-05-12: この部分、もしかして意味が無い？→ ここ自体は意味が無いが、その先は意味があるっぽい）
                    pq_temp = 0
                    for i in Node_List:

                        if len(i.packet_queue) != 0:
                            logger.debug("see hello packet_queue: id:{} length:{} val={}".format(i.id, len(i.packet_queue), i.packet_queue))

                        pq_temp += len(i.packet_queue)

                    if pq_temp == 0:
                        pq_flag = 1

                # ------------------------------------------------------------------------------------------------
                # [Hello end]
    #            if Kronos == Config_List[EXECEGF]:
    #                print "\n-*-OK!-*-\n"
                # ------------------------------------------------------------------------------------------------
                # [SF Process]

                # EXEC_EGF(confi.,conf内 Exec_EGF|どのタイミングで試行を始めるか)より、SF, GF, EGFと切り替えてるらしい

                if Kronos == config_list[EXEC_EGF]:

                    #  print "SF-Process ..."

                    logger.debug("run SF Process")

                    # パケットデータを生成(へっだー?
                    PacketData = str(TYPE_SF)
                    PacketData += ":"
                    PacketData += "SFdata"

                    # スタートノード(source_node)の設定とブロードキャストを開始。
                    Node_List[SOURCENODE].reach_flag[REACHSF] = 1
                    Node_List[SOURCENODE].packet_broadcast(PacketData,
                                                           Node_List,
                                                           config_list[RADIUS])

                    # pq_flagとは？-> パケットキュー?の長さ？
                    pq_flag = 0
                    while pq_flag != 1:

                        # Nodeごとにパケットプロセスの実行
                        for i in Node_List:
                            i.packet_processing(Node_List, config_list, Kronos)

                        #
                        pq_temp = 0
                        for i in Node_List:
                            if len(i.packet_queue) != 0:
                                logger.debug("see sf packet_queue: id:{} length:{} val={}".format(i.id, len(i.packet_queue), i.packet_queue))
                            pq_temp += len(i.packet_queue)

                        if pq_temp == 0:
                            pq_flag = 1

    #                if Node_List[DESTNODE].reach_flag[REACHSF] == 1:
    #                    print "-*-OK!-*-\n"

    #                else:
    #                    print "Impossible Communicating!\n"

                # ----------
                # [GF Process]
                #if Kronos == config_list[EXEC_EGF]:

                    logger.debug("run GF Process")

                    if config_list[SF_CHECK] == 0 or \
                            (config_list[SF_CHECK] == 1 and
                             Node_List[DESTNODE].reach_flag[REACHSF] == 1):
                        PacketData = str(TYPE_GF)

                        self_distance = calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - Node_List[SOURCENODE].location[0]),
                                                                 (Node_List[DESTNODE].location[1] - Node_List[SOURCENODE].location[1]))

                        nodes_around_list = Node_List[SOURCENODE].search_nodes_around(Node_List,
                                                                                      config_list[RADIUS])

                        temp_id = ""
                        temp_distance = self_distance + 1
                        for nodes_around_list_data in nodes_around_list:
                            datalist = [nodes_around_list_data.id,
                                        nodes_around_list_data.location[0],
                                        nodes_around_list_data.location[1]]

                            temp = calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - int(datalist[1])),
                                                            (Node_List[DESTNODE].location[1] - int(datalist[2])))

                            if temp < temp_distance:
                                temp_id = datalist[0]
                                temp_distance = temp

                        if temp_distance < self_distance:
                            PacketData += ";" + Node_List[SOURCENODE].id + ":" + \
                                          str(Node_List[SOURCENODE].location[0]) + ":" + \
                                          str(Node_List[SOURCENODE].location[1])

                            PacketData += ";" + temp_id
                            PacketData += ";" + Node_List[DESTNODE].id + ":" + \
                                          str(Node_List[DESTNODE].location[0]) + ":" + \
                                          str(Node_List[DESTNODE].location[1])
                            PacketData += ";" + "GFdata"

                            Node_List[SOURCENODE].packet_broadcast(PacketData,
                                                                   Node_List,
                                                                   config_list[RADIUS])
                            Node_List[SOURCENODE].reach_flag[REACHGF] = 1

                            pq_flag = 0
                            while pq_flag != 1:

                                for i in Node_List:
                                    i.packet_processing(Node_List,
                                                        config_list,
                                                        Kronos)

                                pq_temp = 0
                                for i in Node_List:
                                    if len(i.packet_queue) != 0:
                                        logger.debug("see gf packet_queue: id:{} length:{} val={}".format(i.id, len(i.packet_queue), i.packet_queue))
                                    pq_temp += len(i.packet_queue)

                                if pq_temp == 0:
                                    pq_flag = 1

    #                        if Node_List[DESTNODE].reach_flag[REACHGF] == 1:
    #                            print "-*-OK!-*-\n"

    #                        else:
    #                            print "Packet Lost!\n"

    #                    else:
    #                        print "No Next Hops!"

    #                else:
    #                    print "Not reacable with SF\n"

                # ------------------------------------------------------------------------------------------------
                # [EGF Process]
                #if Kronos == config_list[EXEC_EGF]:

                    logger.debug("run EGF Process")
                    if config_list[SF_CHECK] == 0 or \
                            (config_list[SF_CHECK] == 1 and
                             Node_List[DESTNODE].reach_flag[REACHSF] == 1):

                        PacketData = str(TYPE_EGF)

                        self_distance = calc_pythagorean_theorem(
                                                (Node_List[DESTNODE].location[0] - Node_List[SOURCENODE].location[0]),
                                                (Node_List[DESTNODE].location[1] - Node_List[SOURCENODE].location[1]))

                        s_v = Node_List[SOURCENODE].search_nodes_around(Node_List,
                                                                        config_list[RADIUS])

                        s_vt = []

                        for s_v_data in s_v:
                            datalist = [s_v_data.id,
                                        s_v_data.location[0],
                                        s_v_data.location[1]]

                            temp = calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - int(datalist[1])),
                                                            (Node_List[DESTNODE].location[1] - int(datalist[2])))

                            if temp < self_distance:
                                s_vt.append(s_v_data)

                        # void_edgeの検出を含みかつ距離によるネクストホップ選択まで全部ここ
                        # 辞書を用意しといてあるs_vt_dataの時の最短距離を入れて最終的にどいつが最短距離もつか
                        # 同じループ回してもいいや
                        # 定数渡しは再帰処理内というか関数内では利用不能なのでリストにして利用
                        obj_and_nearest = {}
                        obj_t = []
                        for s_vt_data in s_vt:
                            egf_depth = config_list[EGF_DEPTH]
                            egf_depth -= 1

                            n_d = []
                            nearest_distance(egf_depth,
                                             s_vt_data,
                                             n_d,
                                             Node_List,
                                             config_list)

                            if len(n_d) != 0:
                                n_d.sort()
                                obj_and_nearest[s_vt_data] = n_d[0]
                                obj_t.append(s_vt_data)

                        tempid = "NaN"

                        n_val = calc_pythagorean_theorem((Node_List[DESTNODE].location[0] - Node_List[SOURCENODE].location[0]),
                                                         (Node_List[DESTNODE].location[1] - Node_List[SOURCENODE].location[1]))

                        for s_vt_data in obj_t:
                            if obj_and_nearest[s_vt_data] < n_val:
                                tempid = s_vt_data.id
                                n_val = obj_and_nearest[s_vt_data]

                        if tempid != "NaN":
                            PacketData += ";" + Node_List[SOURCENODE].id + ":" + \
                                          str(Node_List[SOURCENODE].location[0]) + ":" + \
                                          str(Node_List[SOURCENODE].location[1])
                            PacketData += ";" + tempid
                            PacketData += ";" + Node_List[DESTNODE].id + ":" + \
                                          str(Node_List[DESTNODE].location[0]) + ":" + \
                                          str(Node_List[DESTNODE].location[1])
                            PacketData += ";" + "EGFdata"

                            Node_List[SOURCENODE].packet_broadcast(PacketData,
                                                                   Node_List,
                                                                   config_list[RADIUS])
                            Node_List[SOURCENODE].reach_flag[REACHEGF] = 1

                            pq_flag = 0
                            while pq_flag != 1:

                                for i in Node_List:
                                    i.packet_processing(Node_List,
                                                        config_list,
                                                        Kronos)

                                pq_temp = 0
                                for i in Node_List:
                                    pq_temp += len(i.packet_queue)
                                    logger.debug("see egf packet_queue: id:{} length:{} val={}".format(i.id, len(i.packet_queue), i.packet_queue))

                                if pq_temp == 0:
                                    pq_flag = 1

    #                        if Node_List[DESTNODE].reach_flag[REACHEGF] == 1:
    #                            print "-*-OK!-*-\n"

    #                        else:
    #                            print "Packet Lost!\n"

    #                    else:
    #                        print "EGF failed by Source Node"

    #                else:
    #                    print "Not reacable with SF\n"

                # ------------------------------------------------------------------------------------------------
                # [Node Moving]
                for i in Node_List:
                    if i.wait < Kronos:
                        i.move(config_list[ONE_FRAME])

                    temp = i.speed * config_list[ONE_FRAME]

                    if math.fabs(i.dest_location[0] - i.location[0]) < temp and \
                                    math.fabs(i.dest_location[1] - i.location[1]) < temp:
                        i.dest_location[0] = random.randint(0, config_list[MAP_SIZE_X])
                        i.dest_location[1] = random.randint(0, config_list[MAP_SIZE_Y])
                        i.direction = math.atan2((i.dest_location[1] - i.location[1]),
                                                 (i.dest_location[0] - i.location[0]))
                        i.speed = random.randint(0, config_list[MAX_SPEED])
                        i.wait = Kronos + \
                            random.randint(0, config_list[MAX_WAIT])

                # ------------------------------------------------------------------------------------------------
                # [One Frame Ending]
                Kronos += config_list[ONE_FRAME]
    #            now_process += 1


            # 次のループへ
            # 到達できたら+1してる。
            if config_list[SF_CHECK] == 0:
                ijk += 1
                sf_log += Node_List[DESTNODE].reach_flag[REACHSF]
                gf_log += Node_List[DESTNODE].reach_flag[REACHGF]
                egf_log += Node_List[DESTNODE].reach_flag[REACHEGF]

            else:
                if Node_List[DESTNODE].reach_flag[REACHSF] == 1:
                    ijk += 1
                    sf_log += Node_List[DESTNODE].reach_flag[REACHSF]
                    gf_log += Node_List[DESTNODE].reach_flag[REACHGF]
                    egf_log += Node_List[DESTNODE].reach_flag[REACHEGF]

            logger.debug("while area end: Kronos <= config_list[MAX_KHRONOS]:")
            logger.debug("while now stat... ijk:{}, sf_log:{}, gf_log:{}, egf_log:{}".format(ijk,
                                                                                             sf_log,
                                                                                             gf_log,
                                                                                             egf_log))

        # logger EGF, id, loc, packet quere
        for node in Node_List:
            logger.debug("NodeID:{} loc:{} packet:{}".format(node.id,
                                                             str(node.location),
                                                             node.packet_queue))

        # 結果の出力
        print "\n-*-Complete!-*-\n"

        # print "TRIALS =", str(Config_List[TRIALS])
        print "Total Nodes =", str(config_list[TOTAL_NODE])

        print "SF  :", sf_log

        print "GF  :", gf_log, \
              "--- h_ave_GF  =", float(gf_hop_log) / gf_log, \
              "--- R/H_GF =", str((gf_log) / (float(gf_hop_log) / gf_log))

        print "EGF :", egf_log, \
              "--- h_ave_EGF =", float(egf_hop_log) / egf_log, \
              "--- R/H_GF =", str((egf_log) / (float(egf_hop_log) / egf_log))

        print ""

        log_csv = open("log_sns.csv", 'a')

        logdataB = ""

        for cl in range(len(config_list) - 1):
            logdataB += str(config_list[cl])
            logdataB += ","

        logdataB += str(config_list[NODE_COUNT][0]) + "-" + \
                    str(config_list[NODE_COUNT][1]) + ","

        logdataB += str(sf_log) + "," + \
                    str(gf_log) + "," + \
                    str(egf_log) + "," + \
                    str(float(gf_hop_log) / gf_log) + "," + \
                    str(float(egf_hop_log) /egf_log) + "," + \
                    str((gf_log) / (float(gf_hop_log) / gf_log)) + "," + \
                    str((egf_log) / (float(egf_hop_log) / egf_log)) + "\n"

        log_csv.write(logdataB)
        log_csv.close()

#    NodeInformation(Node_List)
#    print "Config_List :", Config_List
#    output_hello_result(Node_List)
#    output_source_plot(Node_List)

if __name__ == "__main__":
    main()
