# -*- coding: sjis -*-

# ---------------------------------------------------------------------------------------------------------
# Import

import sys
import math
import random

# ---------------------------------------------------------------------------------------------------------
# Define

TOTALNODE    = 0
MAPSIZEX     = 1
MAPSIZEY     = 2
RADIUS       = 3
MAXSPEED     = 4
MAXWAIT      = 5
MAXKHRONOS   = 6
ONEFRAME     = 7
HELLOPERIOD  = 8
TRIALS       = 9
SFCHECK      = 10
EXECEGF      = 11
EGFDEPTH     = 12
ARTIFICIAL   = 13
CELLDIV      = 14
VZCOUNT      = 15
NODECOUNT    = 16

PACKET_SEND_TIME = 0
PACKET_RECV_TIME = 1
PACKET_SEND_BITE = 0
PACKET_RECV_BITE = 1

REACHSF  = 0
REACHGF  = 1
REACHEGF = 2

ID_LENGTH = 4

TYPE_HELLO = 0
TYPE_SF    = 1
TYPE_GF    = 2
TYPE_EGF   = 3

SOURCENODE = 0
DESTNODE   = 1

EGF_HOP_FLAG = 0
gf_hop_log = 0
egf_hop_log = 0

# ---------------------------------------------------------------------------------------------------------
# Class

class node_class:

	def __init__(self):
		self.id = "NaN"
		self.location = []
		self.dest_location = []
		self.speed = -1
		self.direction = -1
		self.wait = -1
		self.hello_buffer = []
		self.packet_sr_times = [0, 0]
		self.packet_sr_bites = [0, 0]
		self.hello_timing = -1
		self.packet_quere = []
		self.hello_list = []
		self.reach_flag = [0, 0, 0]

	def move(self, one_frame):
		self.location[0] = int(self.location[0] + (one_frame * self.speed * math.cos(self.direction)))
		self.location[1] = int(self.location[1] + (one_frame * self.speed * math.sin(self.direction)))
		self.direction = math.atan2((self.dest_location[1] - self.location[1]), (self.dest_location[0] - self.location[0]))

	def packet_processing(self, Node_List, Config_List, Kronos):
		if self.hello_timing < Kronos:
			HelloPacket = []
			PacketData = []
			# はじめから文字列で扱ってもおｋ、現状利用してるのは分岐みやすくするためのみ
			HelloPacket.append(str(TYPE_HELLO))
			HelloPacket.append(self.id)
			HelloPacket.append(str(self.location[0]))
			HelloPacket.append(str(self.location[1]))
			HelloPacket.append(str(Kronos))
			PacketData.append(":".join(HelloPacket))

			# この辺全体一纏めすることが可能
			if len(self.hello_buffer) == 0:
				PacketData = ";".join(PacketData)

			else:
				if len(self.hello_list) == 0:
					PacketData = ";".join(PacketData)
					PacketData += "@"

					for hello_buffer_data in self.hello_buffer:
						PacketData += hello_buffer_data
						PacketData += "="

					PacketData = PacketData[:len(PacketData)-1]

				else:
					PacketData = ";".join(PacketData)
					PacketData += "@"

					for hello_buffer_data in self.hello_buffer:
						PacketData += hello_buffer_data
						PacketData += "="

					PacketData = PacketData[:len(PacketData)-1]

					for hello_list_data in self.hello_list:
						PacketData += ";"
						PacketData += hello_list_data

#			self.packet_broadcast(PacketData, Node_List, Config_List[RADIUS])
			self.hello_timing += Config_List[HELLOPERIOD]

		if len(self.packet_quere) != 0:
			rawdata = self.packet_quere.pop()
			self.packet_sr_times[1] += 1
			self.packet_sr_bites[1] += len(rawdata)

			# ------------------------------------------------------------------------------------------------
			# [Hello Packet Process]
			if rawdata[0] == str(TYPE_HELLO):
				rawdata_h = rawdata[2:]

				if rawdata_h.find("@") == -1:
					datalist = rawdata_h.split(":")

					idsearchflag = 0
					for i in range(len(self.hello_buffer)):
						if self.hello_buffer[i].find(datalist[0]) != -1:
							self.hello_buffer[i] = rawdata_h
							idsearchflag = 1
							break

					if idsearchflag == 0:
						self.hello_buffer.append(rawdata_h)

				else:
					if rawdata_h.find(";") == -1:
						data = rawdata_h.split("@")
						datalist = data[0].split(":")
						idsearchflag = 0
						for i in range(len(self.hello_buffer)):
							if self.hello_buffer[i].find(datalist[0]) != -1:
								self.hello_buffer[i] = data[0]
								idsearchflag = 1
								break

						if idsearchflag == 0:
							self.hello_buffer.append(data[0])

						idsearchflag = 0
						for i in range(len(self.hello_list)):
							if self.hello_list[i].startswith(datalist[0]):
								timecomp = self.hello_list[i].split("@")
								timecomp = timecomp[0].split(":")
								if timecomp[3] < datalist[3]:
									self.hello_list[i] = rawdata_h

								idsearchflag = 1
								break

						if idsearchflag == 0:
							self.hello_list.append(rawdata_h)

					else:
						alldatalist = rawdata_h.split(";")
						data = alldatalist[0].split("@")
						datalist = data[0].split(":")

						idsearchflag = 0
						for i in range(len(self.hello_buffer)):
							if self.hello_buffer[i].find(datalist[0]) != -1:
								self.hello_buffer[i] = data[0]
								idsearchflag = 1
								break

						if idsearchflag == 0:
							self.hello_buffer.append(data[0])

						idsearchflag = 0
						for i in range(len(self.hello_list)):
							if self.hello_list[i].startswith(datalist[0]):
								timecomp = self.hello_list[i].split("@")
								timecomp = timecomp[0].split(":")
								if timecomp[3] < datalist[3]:
									self.hello_list[i] = alldatalist[0]

								idsearchflag = 1
								break

						if idsearchflag == 0:
							self.hello_list.append(alldatalist[0])

						for i in range(1, len(alldatalist)):
							data = alldatalist[i].split("@")
							datalist = data[0].split(":")

							idsearchflag = 0
							for j in range(len(self.hello_list)):
								if self.hello_list[j].startswith(datalist[0]):
									timecomp = self.hello_list[j].split("@")
									timecomp = timecomp[0].split(":")
									if timecomp[3] < datalist[3]:
										self.hello_list[j] = alldatalist[i]

									idsearchflag = 1
									break

							if idsearchflag == 0:
								self.hello_list.append(alldatalist[i])

			# ------------------------------------------------------------------------------------------------
			# [SF Packet Process]
			elif rawdata[0] == str(TYPE_SF):
				if self.reach_flag[REACHSF] == 0:
					self.reach_flag[REACHSF] = 1
					self.packet_broadcast(rawdata, Node_List, Config_List[RADIUS])

			# ------------------------------------------------------------------------------------------------
			# [GF Packet Process]
			elif rawdata[0] == str(TYPE_GF):
				temprawdata = rawdata[2:]
				datalist = temprawdata.split(";")
				destlist = datalist[2].split(":")
				relaylist = datalist[1].split("-")

				if self.id == destlist[0]:
					self.reach_flag[REACHGF] = 1
#					print "\ndata =", temprawdata
					t1 = temprawdata.split(";")
					t2 = t1[1].split("-")
#					print "hops =", len(t2)-1

					global gf_hop_log
					gf_hop_log += len(t2) - 1

				elif self.id == relaylist[len(relaylist)-1] and self.reach_flag[REACHGF] != 1:
					PacketData = str(TYPE_GF)
#					print "data1 =", temprawdata
#					print "Chec :", Node_List[DESTNODE].reach_flag

					self_distance = math.sqrt((int(destlist[1]) - self.location[0])**2 + (int(destlist[2]) - self.location[1])**2)
					nodes_around_list = self.search_nodes_around(Node_List, Config_List[RADIUS])

					temp_id = ""
					temp_distance = self_distance + 1

					for nodes_around_list_data in nodes_around_list:
						datalist_t = [nodes_around_list_data.id, nodes_around_list_data.location[0], nodes_around_list_data.location[1]]

						temp = math.sqrt((int(destlist[1]) - int(datalist_t[1]))**2 + (int(destlist[2]) - int(datalist_t[2]))**2)
						if temp < temp_distance:
							temp_id = datalist_t[0]
							temp_distance = temp

					if temp_distance < self_distance:
						datalist[1] += "-" + temp_id
						adddata = ";".join(datalist)
						PacketData += ";" + adddata

						self.packet_broadcast(PacketData, Node_List, Config_List[RADIUS])
						self.reach_flag[REACHGF] = 1

#						if Node_List[DESTNODE].reach_flag[1] == 1:
#							print "data2 =", temprawdata

			# ------------------------------------------------------------------------------------------------
			# [EGF Packet Process]
			elif rawdata[0] == str(TYPE_EGF):
				temprawdata = rawdata[2:]
				datalist = temprawdata.split(";")
				destlist = datalist[2].split(":")
				relaylist = datalist[1].split("-")

				if self.id == destlist[0]:
					self.reach_flag[REACHEGF] = 1

				elif self.id == relaylist[len(relaylist)-1] and self.reach_flag[REACHEGF] != 1:
					PacketData = str(TYPE_EGF)

					global EGF_HOP_FLAG
					if Node_List[DESTNODE].reach_flag[2] == 1 and EGF_HOP_FLAG == 0:
#						print "data =", temprawdata
						EGF_HOP_FLAG = 1
						t1 = temprawdata.split(";")
						t2 = t1[1].split("-")
#						print "hops =", len(t2)+Config_List[EGFDEPTH]

						global egf_hop_log
						egf_hop_log += len(t2) + Config_List[EGFDEPTH]

					self_distance = math.sqrt((int(destlist[1]) - self.location[0])**2 + (int(destlist[2]) - self.location[1])**2)
					s_v = self.search_nodes_around(Node_List, Config_List[RADIUS])

					s_vt = []
					for s_v_data in s_v:
						datalist_t = [s_v_data.id, s_v_data.location[0], s_v_data.location[1]]

						temp = math.sqrt((int(destlist[1]) - int(datalist_t[1]))**2 + (int(destlist[2]) - int(datalist_t[2]))**2)
						if temp < self_distance:
							s_vt.append(s_v_data)

					obj_and_nearest = {}
					obj_t = []
					for s_vt_data in s_vt:
						egf_depth = Config_List[EGFDEPTH]
						egf_depth -= 1

						n_d = []
						nearest_distance(egf_depth, s_vt_data, n_d, Node_List, Config_List)

						if len(n_d) != 0:
							n_d.sort()
							obj_and_nearest[s_vt_data] = n_d[0]
							obj_t.append(s_vt_data)

					tempid = "NaN"
					n_val = math.sqrt((Node_List[DESTNODE].location[0] - Node_List[SOURCENODE].location[0])**2 + (Node_List[DESTNODE].location[1] - Node_List[SOURCENODE].location[1])**2)

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

#					else:
#						if Node_List[DESTNODE].reach_flag[REACHEGF] == 0:
#							print "EGF failed by Relay Node"


	def packet_broadcast(self, PacketData, Node_List, radius):
		self.packet_sr_times[0] += 1
		self.packet_sr_bites[0] += len(PacketData)

		for i in Node_List:
			if i != self:
				temp = math.sqrt((self.location[0] - i.location[0])**2 + (self.location[1] - i.location[1])**2)

				if temp < radius:
					i.packet_quere.append(PacketData)

	def search_nodes_around(self, Node_List, radius):
		nodes_around_list = []

		for i in Node_List:
			if i != self:
				temp = math.sqrt((self.location[0] - i.location[0])**2 + (self.location[1] - i.location[1])**2)

				if temp < radius:
					nodes_around_list.append(i)

		return nodes_around_list

# ---------------------------------------------------------------------------------------------------------
# Functions

def ConfigOpen(Config_List):
	file = open("config.conf", 'r')

	for line in file:
		line = line.replace("\n", "")
		print line
		line = line.split(":")

		if line[1].find("-") != -1:
			temp = line[1].split("-")
			temp[0] = int(temp[0])
			temp[1] = int(temp[1])
			Config_List.append(temp)

		else:
			Config_List.append(int(line[1]))

	file.close()

def ConfigCheck(Config_List):
	if Config_List[ARTIFICIAL] == 1 and Config_List[VZCOUNT] == 0:
		print "Attention: VZ = 0, but ARTIFICIAL = 1."
		exit()

	if Config_List[ARTIFICIAL] == 1 and Config_List[CELLDIV] == 0:
		print "Attention: CELLDIV = 0, but ARTIFICIAL = 1."
		exit()

	if Config_List[ARTIFICIAL] == 2 and Config_List[NODECOUNT][0] != Config_List[NODECOUNT][1]:
		print "Error: ARTIFICIAL = 2, but NODECOUNT is NOT the same."
		exit()

	if Config_List[ARTIFICIAL] == 2:
		print "Attention: Use egf_finalB."
		exit()

	if Config_List[CELLDIV] == 1:
		print "Attention: CELLDIV must be grater than 1."
		exit()

	if Config_List[CELLDIV]**2 < Config_List[VZCOUNT]:
		print "Error: VZ must be less than CELLDIV^2"
		exit()

	if Config_List[ARTIFICIAL] == 1 and (Config_List[MAPSIZEX] % Config_List[CELLDIV] != 0 or Config_List[MAPSIZEY] % Config_List[CELLDIV] != 0):
		print "Attention: MAPSIZE must be disivle by CELLDIV."
		exit()

def Output_HELLO_Result(Node_List):
	data_log = open("HELLO_Result.txt", 'w')
	data_log.write("-------------------------------------\n")
	data_log.write("   Hello Result\n")
	data_log.write("-------------------------------------\n\n")

	for i in Node_List:
		data_log.write("ID : " + i.id + "\n")
		data_log.write("send_bite, recv_bite = [" + str(i.packet_sr_bites[0]) + ", " + str(i.packet_sr_bites[1]) + "]\n")

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

def Output_Source_Plot(Node_List):
	data_log = open("Source_Plot.csv", 'w')

	for i in Node_List:
		data_log.write(i.id + "," + str(i.location[0] / 1000) + "," + str(i.location[1] / 1000) + "\n")

	data_log.write("\n")

	for hello_list_data in Node_List[0].hello_list:
		data = hello_list_data.split("@")
		data = data[0].split(":")
		data_log.write(data[0] + "," + str(int(data[1]) / 1000) + "," + str(int(data[2]) / 1000) + "," + str(data[3]) + "\n")

	data_log.close()

def NodeCreate(Node_List, Config_List):

	for i in range(0, Config_List[TOTALNODE]):
		Node_List.append(node_class())

	if Config_List[ARTIFICIAL] == 1:
		tempA = []
		tempB = []
		tempC = []

		tempX = 0
		tempY = 0
		x_d = Config_List[MAPSIZEX] / Config_List[CELLDIV]
		y_d = Config_List[MAPSIZEY] / Config_List[CELLDIV]

		for countA in range(Config_List[CELLDIV]):
			tempA.append(tempX)
			tempB.append(tempY)

			tempX += x_d
			tempY += y_d

		for countB in range(Config_List[CELLDIV]**2):
			tempC.append(countB)

		tempD = random.sample(tempC, Config_List[VZCOUNT])

	for i in Node_List:
		i.id = "".join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for j in range(ID_LENGTH))

		unique_id_check = 1
		while unique_id_check:
			unique_id_check = 0
			for k in Node_List:
				if k != i and k.id == i.id:
					i.id = "".join(random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for j in range(ID_LENGTH))
					unique_id_check = 1
					break

		if Config_List[ARTIFICIAL] == 0:
			i.location.append(random.randint(0, Config_List[MAPSIZEX]))
			i.location.append(random.randint(0, Config_List[MAPSIZEY]))

		elif Config_List[ARTIFICIAL] == 1:

			flagA = 1
			while flagA:
				flagA = 0
				tempXA = random.randint(0, Config_List[MAPSIZEX])
				tempYA = random.randint(0, Config_List[MAPSIZEY])

				for check_in in tempD:
					amari = check_in % Config_List[CELLDIV]
					sho = check_in / Config_List[CELLDIV]

					if ((tempA[amari] <= tempXA) and (tempXA <= tempA[amari] + x_d)) and ((tempB[sho] <= tempYA) and (tempYA <= tempB[sho] + y_d)):
						flagA = 1

			i.location.append(tempXA)
			i.location.append(tempYA)

		i.dest_location.append(random.randint(0, Config_List[MAPSIZEX]))
		i.dest_location.append(random.randint(0, Config_List[MAPSIZEX]))

		i.speed = random.randint(0, Config_List[MAXSPEED])

		i.direction = math.atan2((i.dest_location[1] - i.location[1]), (i.dest_location[0] - i.location[0]))

		i.wait = random.randint(0, Config_List[MAXWAIT])

		i.hello_timing = random.randint(0, Config_List[HELLOPERIOD])

def SD_node_init(Node_List, Config_List):
	Node_List[SOURCENODE].location[0] = 0
	Node_List[SOURCENODE].location[1] = 0
	Node_List[SOURCENODE].dest_location[0] = Config_List[MAPSIZEX]
	Node_List[SOURCENODE].dest_location[1] = Config_List[MAPSIZEY]
	Node_List[SOURCENODE].wait = Config_List[MAXKHRONOS] + 1
	Node_List[DESTNODE].location[0] = Config_List[MAPSIZEX]
	Node_List[DESTNODE].location[1] = Config_List[MAPSIZEY]
	Node_List[DESTNODE].dest_location[0] = 0
	Node_List[DESTNODE].dest_location[1] = 0
	Node_List[DESTNODE].wait = Config_List[MAXKHRONOS] + 1

def NodeInformation(Node_List):
	for i in Node_List:
		print i.id, i.location

# 2円の交点算出 ----------------------------------------
def CalcCommonPoints(p1, p2, radius):
	a = p1[0]
	b = p1[1]
	c = p2[0]
	d = p2[1]

	# 円完全一致
	if a == c and b == d:
		return [[-1, -1], [-1, -1]]

	# X座標で一致
	if a == c:
		y = float(d**2 - b**2) / (-2*b + 2*d)

		l = 1
		m = -2 * a
		n = a**2 + y**2 - 2 * b * y + b**2 - radius**2

		# 一つ目の交点(左側)
		q = float(-m - math.sqrt(m**2 - 4 * l * n)) / (2 * l)
		s = y

		# 二つ目の交点(右側)
		r = float(-m + math.sqrt(m**2 - 4 * l * n)) / (2 * l)
		t = y

		return [[int(q), int(s)], [int(r), int(t)]]

	# Y座標で一致
	elif b == d:
		x = float(c**2 - a**2) / (-2*a + 2*c)

		l = 1
		m = -2 * b
		n = b**2 + x**2 - 2 * a * x + a**2 - radius**2

		# 一つ目の交点(下側)
		q = x
		s = float(-m - math.sqrt(m**2 - 4 * l * n)) / (2 * l)

		# 二つ目の交点(上側)
		r = x
		t = float(-m + math.sqrt(m**2 - 4 * l * n)) / (2 * l)

		return [[int(q), int(s)], [int(r), int(t)]]

	# 通常処理
	else:
		alpha = (-2 * a) + 2 * c
		beta = (-2 * b) + 2 * d
		gamma = (-a**2) + c**2 - b**2 + d**2

		e = float(-alpha) / beta
		f = float(gamma) / beta

		l = 1 + e**2
		m = (-2 * c) + 2*e*f - 2*d*e
		n = c**2 + f**2 - 2*d*f + d**2 - radius**2

		# 一つ目の交点(左側)
		q = float(-m - math.sqrt(m**2 - 4 * l * n)) / (2 * l)
		s = e * q + f

		# 二つ目の交点(右側)
		r = float(-m + math.sqrt(m**2 - 4 * l * n)) / (2 * l)
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
			temp = CalcCommonPoints(node_p.location, nodes_around_data.location, Config_List[RADIUS])
			r_v_x[nodes_around_data] = temp

		r_x = []
		for nodes_around_data in nodes_around:
			for point in r_v_x[nodes_around_data]:
				inside_flag = 0

				for nodes_around_data_t in nodes_around:
					if nodes_around_data != nodes_around_data_t:
						temp = math.sqrt((point[0] - nodes_around_data_t.location[0])**2 + (point[1] - nodes_around_data_t.location[1])**2)
						if temp <= Config_List[RADIUS]:
							inside_flag = 1

				if inside_flag == 0:
					r_x.append(point)

		void_edge = []
		while len(r_x) != 0:
			comp = Config_List[RADIUS] + 1
			which_i = 1
			for i in range(1, len(r_x)):
				temp = math.sqrt((r_x[0][0] - r_x[i][0])**2 + (r_x[0][1] - r_x[i][1])**2)

				if temp < comp:
					which_i = i

			void_edge.append([r_x[0], r_x[which_i]])
			del r_x[which_i]
			del r_x[0]

		# 180度以上の差があるとき場合わけ
		void_edge_rad = []
		for void_to_rad in void_edge:
			pretemp = []

			pretemp.append(math.atan2((void_to_rad[0][1] - node_p.location[1]), (void_to_rad[0][0] - node_p.location[0])))
			pretemp.append(math.atan2((void_to_rad[1][1] - node_p.location[1]), (void_to_rad[1][0] - node_p.location[0])))

			void_edge_rad.append(pretemp)

		self_rad = math.atan2((Node_List[DESTNODE].location[1] - node_p.location[1]), (Node_List[DESTNODE].location[0] - node_p.location[0]))

		for i in void_edge_rad:
			i.sort()

		for two_point in void_edge_rad:
			if (two_point[1] - two_point[0]) < math.pi:
				if self_rad < two_point[0] or two_point[1] < self_rad:
					n_d.append(math.sqrt((Node_List[DESTNODE].location[0] - node_p.location[0])**2 + (Node_List[DESTNODE].location[1] - node_p.location[1])**2))

#				else:
#					print "----- Void_Edge In !!! -----"

			else:
				if two_point[0] < self_rad and self_rad < two_point[1]:
					n_d.append(math.sqrt((Node_List[DESTNODE].location[0] - node_p.location[0])**2 + (Node_List[DESTNODE].location[1] - node_p.location[1])**2))

#				else:
#					print "----- Void_Edge In !!! -----"

		if len(void_edge_rad) == 0:
			n_d.append(math.sqrt((Node_List[DESTNODE].location[0] - node_p.location[0])**2 + (Node_List[DESTNODE].location[1] - node_p.location[1])**2))

	else:
		egf_depth -= 1

		r_vt = []
		self_distance = math.sqrt((Node_List[DESTNODE].location[0] - node_p.location[0])**2 + (Node_List[DESTNODE].location[1] - node_p.location[1])**2)

		for nodes_around_data in nodes_around:
			datalist = [nodes_around_data.id, nodes_around_data.location[0], nodes_around_data.location[1]]

			temp = math.sqrt((Node_List[DESTNODE].location[0] - int(datalist[1]))**2 + (Node_List[DESTNODE].location[1] - int(datalist[2]))**2)
			if temp < self_distance:
				r_vt.append(nodes_around_data)

		for r_vt_data in r_vt:
			nearest_distance(egf_depth, r_vt_data, n_d, Node_List, Config_List)

def main():
	print "\n-------------------------------------"
	print "           Configuration"
	print "-------------------------------------"

	Config_List = []
	ConfigOpen(Config_List)
	ConfigCheck(Config_List)

	print "\n-------------------------------------"
	print "   Configration check is complete!"
	print "-------------------------------------"
	print "Start? (y/n)\n"
	print "(EGF-SNS) >",

	temp = raw_input()

	if temp != "y":
		print "bye!"
		exit()

	print ""

	global gf_hop_log
	global egf_hop_log

	log_csv = open("log_sns.csv", 'a')
	file = open("config.conf", 'r')
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

	for node_inc in range(Config_List[NODECOUNT][0], Config_List[NODECOUNT][1]+1):
		Config_List[TOTALNODE] = node_inc

		ijk = 1
		sf_log = 0
		gf_log = 0
		egf_log = 0
		gf_hop_log = 0
		egf_hop_log = 0
		while ijk <= Config_List[TRIALS]:

			sys.stdout.write("\r")
			sys.stdout.write("Processing... [")

			count_process = 40
			p_count = int((ijk / float(Config_List[TRIALS])) * count_process)

			for i in range(p_count):
				sys.stdout.write("*")

			for i in range(count_process - p_count):
				sys.stdout.write(" ")

			sys.stdout.write("]")


			Node_List = []
			NodeCreate(Node_List, Config_List)
			SD_node_init(Node_List, Config_List)

			global EGF_HOP_FLAG
			EGF_HOP_FLAG = 0

	#		total_process = float(Config_List[MAXKHRONOS]) / Config_List[ONEFRAME]
	#		now_process = 0
	#		count_process = 40
	#		print ""
			Kronos = 0
			while Kronos <= Config_List[MAXKHRONOS]:

	#			sys.stdout.write("\r")
	#			sys.stdout.write("Hello-Process ... [")
	#			p_count = int((now_process / total_process) * count_process)

	#			for i in range(p_count):
	#				sys.stdout.write("*")

	#			for i in range(count_process - p_count - int(math.ceil((1 / total_process) * count_process))):
	#			for i in range(count_process - p_count):
	#				sys.stdout.write(" ")

	#			sys.stdout.write("]")

				# ------------------------------------------------------------------------------------------------
				# [Packet Processing]
				pq_flag = 0
				while pq_flag != 1:

					for i in Node_List:
						i.packet_processing(Node_List, Config_List, Kronos)

					pq_temp = 0
					for i in Node_List:
						pq_temp += len(i.packet_quere)

					if pq_temp == 0:
						pq_flag = 1

				# ------------------------------------------------------------------------------------------------
				# [Hello end]
	#			if Kronos == Config_List[EXECEGF]:
	#				print "\n-*-OK!-*-\n"

				# ------------------------------------------------------------------------------------------------
				# [SF Process]
				if Kronos == Config_List[EXECEGF]:
	#				print "SF-Process ..."

					PacketData = str(TYPE_SF)
					PacketData += ":"
					PacketData += "SFdata"

					Node_List[SOURCENODE].reach_flag[REACHSF] = 1
					Node_List[SOURCENODE].packet_broadcast(PacketData, Node_List, Config_List[RADIUS])

					pq_flag = 0
					while pq_flag != 1:

						for i in Node_List:
							i.packet_processing(Node_List, Config_List, Kronos)

						pq_temp = 0
						for i in Node_List:
							pq_temp += len(i.packet_quere)

						if pq_temp == 0:
							pq_flag = 1

	#				if Node_List[DESTNODE].reach_flag[REACHSF] == 1:
	#					print "-*-OK!-*-\n"

	#				else:
	#					print "Impossible Communicating!\n"

				# ------------------------------------------------------------------------------------------------
				# [GF Process]
				if Kronos == Config_List[EXECEGF]:
	#				print "GF-Process ..."

					if Config_List[SFCHECK] == 0 or (Config_List[SFCHECK] == 1 and Node_List[DESTNODE].reach_flag[REACHSF] == 1):
						PacketData = str(TYPE_GF)

						self_distance = math.sqrt((Node_List[DESTNODE].location[0] - Node_List[SOURCENODE].location[0])**2 + (Node_List[DESTNODE].location[1] - Node_List[SOURCENODE].location[1])**2)
						nodes_around_list = Node_List[SOURCENODE].search_nodes_around(Node_List, Config_List[RADIUS])

						temp_id = ""
						temp_distance = self_distance + 1
						for nodes_around_list_data in nodes_around_list:
							datalist = [nodes_around_list_data.id, nodes_around_list_data.location[0], nodes_around_list_data.location[1]]

							temp = math.sqrt((Node_List[DESTNODE].location[0] - int(datalist[1]))**2 + (Node_List[DESTNODE].location[1] - int(datalist[2]))**2)
							if temp < temp_distance:
								temp_id = datalist[0]
								temp_distance = temp

						if temp_distance < self_distance:
							PacketData += ";" + Node_List[SOURCENODE].id + ":"+ str(Node_List[SOURCENODE].location[0]) + ":" + str(Node_List[SOURCENODE].location[1])
							PacketData += ";" + temp_id
							PacketData += ";" + Node_List[DESTNODE].id + ":"+ str(Node_List[DESTNODE].location[0]) + ":" + str(Node_List[DESTNODE].location[1])
							PacketData += ";" + "GFdata"

							Node_List[SOURCENODE].packet_broadcast(PacketData, Node_List, Config_List[RADIUS])
							Node_List[SOURCENODE].reach_flag[REACHGF] = 1

							pq_flag = 0
							while pq_flag != 1:

								for i in Node_List:
									i.packet_processing(Node_List, Config_List, Kronos)

								pq_temp = 0
								for i in Node_List:
									pq_temp += len(i.packet_quere)

								if pq_temp == 0:
									pq_flag = 1

	#						if Node_List[DESTNODE].reach_flag[REACHGF] == 1:
	#							print "-*-OK!-*-\n"

	#						else:
	#							print "Packet Lost!\n"

	#					else:
	#						print "No Next Hops!"

	#				else:
	#					print "Not reacable with SF\n"


				# ------------------------------------------------------------------------------------------------
				# [EGF Process]
				if Kronos == Config_List[EXECEGF]:
	#				print "EGF-Process ..."

					if Config_List[SFCHECK] == 0 or (Config_List[SFCHECK] == 1 and Node_List[DESTNODE].reach_flag[REACHSF] == 1):
						PacketData = str(TYPE_EGF)

						self_distance = math.sqrt((Node_List[DESTNODE].location[0] - Node_List[SOURCENODE].location[0])**2 + (Node_List[DESTNODE].location[1] - Node_List[SOURCENODE].location[1])**2)
						s_v = Node_List[SOURCENODE].search_nodes_around(Node_List, Config_List[RADIUS])

						s_vt = []

						for s_v_data in s_v:
							datalist = [s_v_data.id, s_v_data.location[0], s_v_data.location[1]]

							temp = math.sqrt((Node_List[DESTNODE].location[0] - int(datalist[1]))**2 + (Node_List[DESTNODE].location[1] - int(datalist[2]))**2)
							if temp < self_distance:
								s_vt.append(s_v_data)

						# void_edgeの検出を含みかつ距離によるネクストホップ選択まで全部ここ
						# 辞書を用意しといてあるs_vt_dataの時の最短距離を入れて最終的にどいつが最短距離もつか
						# 同じループ回してもいいや
						# 定数渡しは再帰処理内というか関数内では利用不能なのでリストにして利用
						obj_and_nearest = {}
						obj_t = []
						for s_vt_data in s_vt:
							egf_depth = Config_List[EGFDEPTH]
							egf_depth -= 1

							n_d = []
							nearest_distance(egf_depth, s_vt_data, n_d, Node_List, Config_List)

							if len(n_d) != 0:
								n_d.sort()
								obj_and_nearest[s_vt_data] = n_d[0]
								obj_t.append(s_vt_data)

						tempid = "NaN"
						n_val = math.sqrt((Node_List[DESTNODE].location[0] - Node_List[SOURCENODE].location[0])**2 + (Node_List[DESTNODE].location[1] - Node_List[SOURCENODE].location[1])**2)

						for s_vt_data in obj_t:
							if obj_and_nearest[s_vt_data] < n_val:
								tempid = s_vt_data.id
								n_val = obj_and_nearest[s_vt_data]

						if tempid != "NaN":
							PacketData += ";" + Node_List[SOURCENODE].id + ":"+ str(Node_List[SOURCENODE].location[0]) + ":" + str(Node_List[SOURCENODE].location[1])
							PacketData += ";" + tempid
							PacketData += ";" + Node_List[DESTNODE].id + ":"+ str(Node_List[DESTNODE].location[0]) + ":" + str(Node_List[DESTNODE].location[1])
							PacketData += ";" + "EGFdata"

							Node_List[SOURCENODE].packet_broadcast(PacketData, Node_List, Config_List[RADIUS])
							Node_List[SOURCENODE].reach_flag[REACHEGF] = 1

							pq_flag = 0
							while pq_flag != 1:

								for i in Node_List:
									i.packet_processing(Node_List, Config_List, Kronos)

								pq_temp = 0
								for i in Node_List:
									pq_temp += len(i.packet_quere)

								if pq_temp == 0:
									pq_flag = 1

	#						if Node_List[DESTNODE].reach_flag[REACHEGF] == 1:
	#							print "-*-OK!-*-\n"

	#						else:
	#							print "Packet Lost!\n"

	#					else:
	#						print "EGF failed by Source Node"

	#				else:
	#					print "Not reacable with SF\n"


				# ------------------------------------------------------------------------------------------------
				# [Node Moving]
				for i in Node_List:
					if i.wait < Kronos:
						i.move(Config_List[ONEFRAME])

					temp = i.speed * Config_List[ONEFRAME]

					if math.fabs(i.dest_location[0] - i.location[0]) < temp and math.fabs(i.dest_location[1] - i.location[1]) < temp:
						i.dest_location[0] = random.randint(0, Config_List[MAPSIZEX])
						i.dest_location[1] = random.randint(0, Config_List[MAPSIZEY])
						i.direction = math.atan2((i.dest_location[1] - i.location[1]), (i.dest_location[0] - i.location[0]))
						i.speed = random.randint(0, Config_List[MAXSPEED])
						i.wait = Kronos + random.randint(0, Config_List[MAXWAIT])

				# ------------------------------------------------------------------------------------------------
				# [One Frame Ending]
				Kronos += Config_List[ONEFRAME]
	#			now_process += 1

			if Config_List[SFCHECK] == 0:
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

		print "\n-*-Complete!-*-\n"
#		print "TRIALS =", str(Config_List[TRIALS])
		print "Total Nodes =", str(Config_List[TOTALNODE])
		print "SF  :", sf_log
		print "GF  :", gf_log, "--- h_ave_GF  =", float(gf_hop_log)/gf_log, "--- R/H_GF =", str((gf_log)/(float(gf_hop_log)/gf_log))
		print "EGF :", egf_log, "--- h_ave_EGF =", float(egf_hop_log)/egf_log, "--- R/H_GF =", str((egf_log)/(float(egf_hop_log)/egf_log))
		print ""

		log_csv = open("log_sns.csv", 'a')
		logdataB = ""
		for cl in range(len(Config_List)-1):
			logdataB += str(Config_List[cl])
			logdataB += ","

		logdataB += str(Config_List[NODECOUNT][0]) + "-" + str(Config_List[NODECOUNT][1]) + ","
		logdataB += str(sf_log) + "," + str(gf_log) + "," + str(egf_log) + "," + str(float(gf_hop_log)/gf_log) + "," + str(float(egf_hop_log)/egf_log) + "," + str((gf_log)/(float(gf_hop_log)/gf_log)) + "," + str((egf_log)/(float(egf_hop_log)/egf_log)) + "\n"
		log_csv.write(logdataB)
		log_csv.close()

#	NodeInformation(Node_List)
#	print "Config_List :", Config_List
#	Output_HELLO_Result(Node_List)
#	Output_Source_Plot(Node_List)

# ---------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

	main()


