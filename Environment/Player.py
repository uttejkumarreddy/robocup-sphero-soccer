import mujoco as mj
import numpy as np
import math

from AI.DDPG.Agent import Agent
from Configurations import Environment as envProps
from Configurations import DDPGHyperparameters as ddpgHP
from Utilities.Logger import Logger

class Player:
		def __init__(self, model, team, name, observation_space, action_space):
				self.team = team
				self.name = name

				self.id_body = mj.mj_name2id(model, mj.mjtObj.mjOBJ_BODY, self.name)
				self.id_geom = mj.mj_name2id(model, mj.mjtObj.mjOBJ_GEOM, self.name)
				self.id_joint = mj.mj_name2id(model, mj.mjtObj.mjOBJ_JOINT, self.name)

				self.ai = Agent(
						alpha = ddpgHP.ALPHA,
						beta = ddpgHP.BETA,
						input_dims = [observation_space.shape[0]],
						tau = ddpgHP.TAU,
						gamma = ddpgHP.GAMMA,
						n_actions=action_space.shape[0],
						max_size = ddpgHP.BUFFER_SIZE,
						layer1_size = ddpgHP.LAYER_1_SIZE,
						layer2_size = ddpgHP.LAYER_2_SIZE,
						batch_size = ddpgHP.BATCH_SIZE,
				)
				self.ai.load_models()

				self.heading = 0

				logger = Logger()
				logger.write("Player {0} initialized. id_body {1} id_geom {2} id_joint {3}".format(self.name, self.id_body, self.id_geom, self.id_joint))

		def get_position(self, data):
				return data.qpos[self.id_joint * 7 : self.id_joint * 7 + 3]

		def set_position(self, data, position):
				data.qpos[self.id_joint * 7 : self.id_joint * 7 + 3] = position

		def get_velocity(self, data):
				return data.qvel[self.id_joint * 6 : self.id_joint * 6 + 6]

		def set_velocity(self, data, vel):  # vel: [x, y, z]
				data.qvel[self.id_joint * 6 : self.id_joint * 6 + 3] = vel

		def set_heading_and_velocity(self, data, rotation, speed):
				self.heading += rotation
				direction = np.array([math.cos(self.heading), math.sin(self.heading), 0])
				velocity = speed * direction
				self.set_velocity(data, velocity)

		def get_reward(self, data, ball):
			player_position = self.get_position(data)[:2]
			player_velocity = self.get_velocity(data)[:2]
			player_velocity_norm = player_velocity / np.linalg.norm(player_velocity)

			ball_position = ball.get_position(data)[:2]
			ball_velocity = ball.get_velocity(data)[:2]

			goal_position = np.array(envProps.GOAL_HOME)

			# vel-to-ball: player's linear velocity projected onto its unit direction vector towards the ball, thresholded at zero
			player_to_ball_unit_vector = (ball_position - player_position) / np.linalg.norm(ball_position - player_position)
			reward_vel_to_ball = -np.dot(player_velocity_norm, player_to_ball_unit_vector)

			# vel-ball-to-goal: ball's linear velocity projected onto its unit direction vector towards the center of the opponent's goal
			# ball_to_goal_unit_vector = (goal_position - ball_position) / np.linalg.norm(goal_position - ball_position)
			# reward_vel_ball_to_goal = np.dot(ball_velocity, ball_to_goal_unit_vector) * 10

			# return reward_vel_to_ball # + reward_vel_ball_to_goal

			contacts = data.contact
			reward_ball_kicked = 0
			for c in contacts:
				if c.geom1 == ball.id_geom and c.geom2 == self.id_geom:
					reward_ball_kicked = 100

			return reward_vel_to_ball + reward_ball_kicked
