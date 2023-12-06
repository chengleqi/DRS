import matplotlib.pyplot as plt

def read_rewards_from_file(file_path):
    rewards = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2 and parts[0].startswith("Action:"):
                _, reward = parts[1].split(':')
                rewards.append(float(reward.strip()))
    return rewards

# 将这里的文件路径替换为您的 'reward.log' 文件的实际路径
file_path = "reward.log"  
rewards = read_rewards_from_file(file_path)

# 绘制奖励值的可视化
plt.plot(rewards, marker='o')
plt.xlabel('Step')
plt.ylabel('Reward')
plt.title('Rewards Over Steps')
plt.grid(True)
plt.savefig('reward.png')