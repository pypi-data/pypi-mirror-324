import gym
import pybullet as p
import pybullet_data
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
import cv2
from gym.wrappers import FlattenObservation

print ("You are using:")
print ("████████████████████████████████████████████████████████████████████████████████")
print ("████████████████████████████████████████████████████████████████████████████████")
print ("█████          ███████████████████████████████████     █     ███████████████████")
print ("█████ ████████   █████████████████████████████████ ███ █ ███ ███████████████████")
print ("█████ ███  █████ ██         ██           ███       ███ █     █          ████████")
print ("█████ ███   ████ █  ███████  █ ███ █████  █  █████ ███ █ ███   ████████ ████████")
print ("█████ ████████     ███   ███   ████   ███   ███   ████ █ ███  ███       ████████")
print ("█████ ███    ███  ███████████  ███  █ ███  ████ █  ███ █ ███   ███████  ████████")
print ("█████ ███    ███   ███         ███ ██ ███  ████   ████ █ ███ █      ███ ████████")
print ("█████ ██████████   █████████ █ ███ ██ ███   ██████████ █ ███ █ ████████ ████████")
print ("█████            █           █     ██     █            █     █          ████████")
print ("████████████████████████████████████████████████████████████████████████████████")
print ("████████████████████████████████████████████████████████████████████████████████")



class RoboticArmEnv(gym.Env):
    def __init__(self):
        super(RoboticArmEnv, self).__init__()
        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.setGravity(0, 0, -9.81)
        
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(7,), dtype=np.float32)
        
 
        self.observation_space = gym.spaces.Dict({
            "vector": gym.spaces.Box(low=-np.inf, high=np.inf, shape=(20,), dtype=np.float32),
            "lidar": gym.spaces.Box(low=0, high=10, shape=(10,), dtype=np.float32),
            "camera": gym.spaces.Box(low=0, high=255, shape=(64, 64, 3), dtype=np.uint8)  
        })
        
  
        self.initial_ball_pos = None
        self.previous_ball_pos = None

  
        self.lidar_range = 10  
        self.lidar_angle = np.pi / 2 
        

        self.camera_width = 64
        self.camera_height = 64
        self.camera_fov = 60
        self.camera_position = [0, -1.5, 1.0]  
        self.camera_target = [0, 0, 0.5]  
        self.camera_up = [0, 0, 1]  
        
        self.reset()

    def reset(self, seed=None, options=None):
        if seed is not None:
            np.random.seed(seed)
            
        p.resetSimulation()
        p.setGravity(0, 0, -9.81)
        
        self.planeId = p.loadURDF("plane.urdf")
        self.armId = p.loadURDF("/home/luca/Desktop/kuka_iiwa/model.urdf", [0, 0, 0])
        
        
        self.trayId = p.loadURDF("tray/traybox.urdf", [0.5, 0, 0])
        
     
        ball_pos = [0.5, 0, 0.2]  
        self.ballId = p.loadURDF("sphere_small.urdf", ball_pos, globalScaling=4.0)
        
        
        self.initial_ball_pos = ball_pos
        self.previous_ball_pos = ball_pos
        
        p.changeVisualShape(self.ballId, -1, rgbaColor=[1, 0, 0, 1])
        
        for i in range(7):
            p.resetJointState(self.armId, i, 0)
        
   
        for _ in range(10):
            p.stepSimulation()
            

        self.camera_position = [0, -1.5, 1.0] 
        self.camera_target = [0.25, 0, 0.5]  
            
        obs = self._get_obs()
        info = {}
        return obs, info

    def step(self, action):
      
        if np.ndim(action) > 1:
            action = action[0]
            
        scaled_action = np.clip(action * np.pi, -np.pi, np.pi)
        
        for i in range(7):
            p.setJointMotorControl2(
                self.armId, i,
                p.POSITION_CONTROL,
                targetPosition=scaled_action[i],
                force=500,
                maxVelocity=1
            )
        
        
        self.previous_ball_pos = p.getBasePositionAndOrientation(self.ballId)[0]
        
        for _ in range(5):
            p.stepSimulation()
            
        obs = self._get_obs()
        reward = self._get_reward(obs["vector"])  
        done = self._get_done(obs["vector"])
        truncated = False
        info = {}
        
        return obs, reward, done, truncated, info

    def _get_obs(self):
      
        joint_states = []
        for i in range(7):
            state = p.getJointState(self.armId, i)
            joint_states.extend([state[0], state[1]])
            
        end_effector_pos = p.getLinkState(self.armId, 6)[0]
        ball_pos, _ = p.getBasePositionAndOrientation(self.ballId)
        
        vector_obs = np.array(joint_states + list(end_effector_pos) + list(ball_pos), dtype=np.float32)
        
        
        lidar_obs = self._get_lidar_data()
        
       
        camera_obs = self._get_camera_image(
            self.camera_position, self.camera_target, self.camera_up,
            self.camera_width, self.camera_height, self.camera_fov
        )
        
        return {
            "vector": vector_obs,
            "lidar": lidar_obs,
            "camera": camera_obs
        }

    def _get_lidar_data(self):
        lidar_points = []

        angles = np.linspace(-self.lidar_angle / 2, self.lidar_angle / 2, 10)
        for angle in angles:
        
            dx = self.lidar_range * np.cos(angle)
            dy = self.lidar_range * np.sin(angle)
          
            ray_from = p.getLinkState(self.armId, 6)[0]
            ray_to = [ray_from[0] + dx, ray_from[1] + dy, ray_from[2]]
            ray_result = p.rayTest(ray_from, ray_to)
            if ray_result[0][0] != -1:
                hit_point = ray_result[0][3]
                distance = np.linalg.norm(np.array(hit_point) - np.array(ray_from))
                lidar_points.append(distance if distance < self.lidar_range else self.lidar_range)
            else:
                lidar_points.append(self.lidar_range)
        return np.array(lidar_points, dtype=np.float32)
    
    def _get_camera_image(self, position, target, up, width, height, fov):
     
        view_matrix = p.computeViewMatrix(position, target, up)
        aspect = width / height
        projection_matrix = p.computeProjectionMatrixFOV(fov, aspect, 0.1, 100)
     
        img_arr = p.getCameraImage(width, height, view_matrix, projection_matrix)
        rgb_array = np.array(img_arr[2], dtype=np.uint8)
        bgr_array = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)
        return bgr_array

    def _get_reward(self, vector_obs):
        end_effector_pos = vector_obs[14:17]
        current_ball_pos = vector_obs[17:20]
        
        distance = np.linalg.norm(np.array(end_effector_pos) - np.array(current_ball_pos))
        reward = -distance
        
        if distance < 0.2:
            reward += 10
            
        distance_from_start = np.linalg.norm(np.array(current_ball_pos) - np.array(self.initial_ball_pos))
        if distance_from_start > 0.5:
            reward -= 20 * distance_from_start
            
        if self.previous_ball_pos is not None:
            ball_movement = np.linalg.norm(np.array(current_ball_pos) - np.array(self.previous_ball_pos))
            if ball_movement > 0.05:
                reward -= 50 * ball_movement
                
        joint_positions = vector_obs[::2][:7]
        joint_penalty = -0.1 * np.sum(np.square(joint_positions))
        reward += joint_penalty
        
        return reward

    def _get_done(self, vector_obs):
        end_effector_pos = vector_obs[14:17]
        ball_pos = vector_obs[17:20]
        
        distance_from_start = np.linalg.norm(np.array(ball_pos) - np.array(self.initial_ball_pos))
        if distance_from_start > 1.0:
            return True
            
        distance_to_ball = np.linalg.norm(np.array(end_effector_pos) - np.array(ball_pos))
        return distance_to_ball < 0.2

    def close(self):
        p.disconnect()


