from gym import spaces, core
import socket
import numpy as np
import time

def getNodeState(sock, node):
	sock.send("getState".encode("utf-8"))
	msg = sock.recv(2048)
	msg = str(msg, encoding="utf-8")[1:-1].split(",")
	msg = [float(item) for item in msg]
	# print("[INFO] Get state of {} : {}".format(node, msg))
	return msg

class K8sEnv(core.Env):
	def __init__(self):
		self.count = 0
		self.maxCount = 300

		# env parameter
		self.viewer = None
		self.action_space = spaces.Discrete(4)
		low = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], dtype = np.float32) 
		high = np.array([100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100], dtype = np.float32)
		self.observation_space =  spaces.Box(low, high, dtype=np.float32)
		self.state = [None] * 35
		self.isDone = False

		# TCP connections
		self.sock2Node1 = None
		self.sock2Node2 = None
		self.sock2Node3 = None
		self.sock2Node4 = None

	def setsocks(self, sock2Node1, sock2Node2, sock2Node3, sock2Node4):
		self.sock2Node1 = sock2Node1
		self.sock2Node2 = sock2Node2
		self.sock2Node3 = sock2Node3
		self.sock2Node4 = sock2Node4

	def getState(self):
		# print('[INFO] First State: {}'.format(self.state))
		# state: [cpu, mem, recv, tran, read, write]
		node1_state = getNodeState(self.sock2Node1, "Node1")
		node2_state = getNodeState(self.sock2Node2, "Node2")
		node3_state = getNodeState(self.sock2Node3, "Node3")
		node4_state = getNodeState(self.sock2Node4, "Node4")
		# cpu  50% => 100%
		node1_state[0] = float('%.2f' % min(node1_state[0], 100))
		node2_state[0] = float('%.2f' % min(node2_state[0], 100))
		node3_state[0] = float('%.2f' % min(node3_state[0], 100))
		node4_state[0] = float('%.2f' % min(node4_state[0], 100))
		# recv tran  120KB/s => 100%
		node1_state[2] = float('%.2f' % min(node1_state[2] / 4 * 100, 100))
		node2_state[2] = float('%.2f' % min(node2_state[2] / 4 * 100, 100))
		node3_state[2] = float('%.2f' % min(node3_state[2] / 4 * 100, 100))
		node4_state[2] = float('%.2f' % min(node4_state[2] / 4 * 100, 100))
		node1_state[3] = float('%.2f' % min(node1_state[3] / 4 * 100, 100))
		node2_state[3] = float('%.2f' % min(node2_state[3] / 4 * 100, 100))
		node3_state[3] = float('%.2f' % min(node3_state[3] / 4 * 100, 100))
		node4_state[3] = float('%.2f' % min(node4_state[3] / 4 * 100, 100))
		# read write 20480KB/s => 100%
		node1_state[4] = float('%.2f' % min(node1_state[4] / 10240 * 100, 100))
		node2_state[4] = float('%.2f' % min(node2_state[4] / 10240 * 100, 100))
		node3_state[4] = float('%.2f' % min(node3_state[4] / 10240 * 100, 100))
		node4_state[4] = float('%.2f' % min(node4_state[4] / 10240 * 100, 100))
		node1_state[5] = float('%.2f' % min(node1_state[5] / 10240 * 100, 100))
		node2_state[5] = float('%.2f' % min(node2_state[5] / 10240 * 100, 100))
		node3_state[5] = float('%.2f' % min(node3_state[5] / 10240 * 100, 100))
		node4_state[5] = float('%.2f' % min(node4_state[5] / 10240 * 100, 100))
		# print('[INFO] Node1 State: {}'.format(node1_state))
		# print('[INFO] Node2 State: {}'.format(node2_state))
		# print('[INFO] Node3 State: {}'.format(node3_state))
		# print('[INFO] Node4 State: {}'.format(node4_state))

		# VRAM
		node1_state[6] = float('%.2f' % min(node1_state[6] * 100, 100))
		node2_state[6] = float('%.2f' % min(node2_state[6] * 100, 100))
		node3_state[6] = float('%.2f' % min(node3_state[6] * 100, 100))
		node4_state[6] = float('%.2f' % min(node4_state[6] * 100, 100))

		# state: [cpu, mem, recv, tran, read, write, vram]
		self.state[0:7] = node1_state
		self.state[7:14] = node2_state
		self.state[14:21] = node3_state
		self.state[21:28] = node4_state
		# print('[INFO] Processed State: {}'.format(self.state))

	def reset(self):
		if self.state == [None] * 35:
			self.getState()
		self.isDone = False
		self.count = 0
		return np.array(self.state, dtype = np.float32)

	def step(self, action):
		self.count = self.count + 1
		print('[INFO] Start dql step {}/{}'.format(self.count, self.maxCount))

		print('[INFO] Wait for pod execution...')
		time.sleep(5)

		self.getState()
		print('[INFO] State after action: {}'.format(self.state))
		
		avg_cpu_util = np.mean([self.state[0], self.state[7], self.state[14], self.state[21]])
		avg_mem_util = np.mean([self.state[1], self.state[8], self.state[15], self.state[22]])
		avg_net_util = np.mean([self.state[2], self.state[3], self.state[9], self.state[10], self.state[16], self.state[17], self.state[23], self.state[24]])
		avg_io_util = np.mean([self.state[4], self.state[5], self.state[11], self.state[12], self.state[18], self.state[19], self.state[25], self.state[26]])
		avg_vram_util = np.mean([self.state[6], self.state[13], self.state[20], self.state[27]])
		avg_util = (avg_cpu_util + avg_mem_util + avg_net_util + avg_io_util + avg_vram_util) / 5
		#avg_cpu_util = np.mean([self.state[0], self.state[6], self.state[12], self.state[18]])
		# avg_mem_util = np.mean([self.state[1], self.state[7], self.state[13], self.state[19]])
		# avg_net_util = np.mean([self.state[2], self.state[3], self.state[8], self.state[9], self.state[14], self.state[15], self.state[20], self.state[21]])
		# avg_io_util = np.mean([self.state[4], self.state[5], self.state[10], self.state[11], self.state[16], self.state[17], self.state[22], self.state[23]])
		# avg_util = (avg_cpu_util + avg_mem_util + avg_net_util + avg_io_util) / 4

		std_cpu = np.std(np.array([self.state[0], self.state[7], self.state[14], self.state[21]],dtype=np.float32))
		std_mem = np.std(np.array([self.state[1], self.state[8], self.state[15], self.state[22]],dtype=np.float32))
		std_net = np.std(np.array([self.state[2], self.state[9], self.state[16], self.state[23]],dtype=np.float32))
		std_net = std_net + np.std(np.array([self.state[3], self.state[10], self.state[17], self.state[24]],dtype=np.float32))
		std_io = np.std(np.array([self.state[4], self.state[11], self.state[18], self.state[25]],dtype=np.float32))
		std_io = std_io + np.std(np.array([self.state[5], self.state[12], self.state[19], self.state[26]],dtype=np.float32))
		std_vram = np.std(np.array([self.state[6], self.state[13], self.state[20], self.state[27]],dtype=np.float32))
		reward = avg_util - (std_cpu + std_mem + std_net + std_io + std_vram)

		# std_cpu = np.std(np.array([self.state[0], self.state[6], self.state[12], self.state[18]],dtype=np.float32))
		# std_mem = np.std(np.array([self.state[1], self.state[7], self.state[13], self.state[19]],dtype=np.float32))
		# std_net = np.std(np.array([self.state[2], self.state[8], self.state[14], self.state[20]],dtype=np.float32))
		# std_net = std_net + np.std(np.array([self.state[3], self.state[9], self.state[15], self.state[21]],dtype=np.float32))
		# std_io = np.std(np.array([self.state[4], self.state[10], self.state[16], self.state[22]],dtype=np.float32))
		# std_io = std_io + np.std(np.array([self.state[5], self.state[11], self.state[17], self.state[23]],dtype=np.float32))

		# reward = avg_util - (std_cpu + std_mem + std_net + std_io)
		print('[INFO] Reward of this step: {}'.format(reward))
		with open("reward.log", 'a') as f:
			f.write('Action: {}, Reward: {}\n'.format(action, str(reward)))

		if self.count >= self.maxCount:
			self.isDone = True

		print('[INFO] End dql step {}/{}'.format(self.count, self.maxCount))

		return np.array(self.state, dtype = np.float32), reward, self.isDone, {}

	def render(self, mode="human"):
		pass

	def close(self):
		if self.viewer:
			self.viewer.close()

		self.sock2Node1.close()
		self.sock2Node2.close()
		self.sock2Node3.close()
		self.sock2Node4.close()