from math import sin, cos, pi, sqrt, acos, atan
import pandas as pd
import numpy as np

# COM/SEGMENT LENGTH RATIOS
ARM_RATIO_COM_PROXIMAL = 0.470
THN_RATIO_COM_DISTAL = 0.34
FEMUR_RATIO_COM_DISTAL = 0.567
LEG_RATIO_COM_DISTAL = 0.567
FOOT_RATIO_COM_PROXIMAL = 0.500

# SEGMENT MASS/BODY MASS RATIOS
FOOT_MASS_RATIO = 0.0145
ARM_MASS_RATIO = 0.050
THN_MASS_RATIO = 0.578
FEMUR_MASS_RATIO = 0.100
LEG_MASS_RATIO = 0.0465

segments = ["FOOT", "LEG", "FEMUR", "THN", "ARMS"]
joints = ["METATARSAL5", "ANKLE", "KNEE", "HIP", "SHOULDER", "WRIST"]
ankle = [0,0]

class Body:

	def __init__(self, body_mass, hn_length, torso_length, femur_length, leg_length, arm_length, foot_length, ankle_height):
		self.body_mass = body_mass
		self.hn_length = hn_length
		self.torso_length = torso_length
		self.femur_length = femur_length
		self.leg_length = leg_length
		self.arm_length = arm_length
		self.foot_length = foot_length
		self.ankle_height = ankle_height

		print("Body with the following segment lengths was created:")
		print("\tBody mass: {} kg\n".format(self.body_mass))
		print("\tLength of head-neck: {} m".format(self.hn_length))
		print("\tLength of torso: {} m".format(self.torso_length))
		print("\tLength of femur: {} m".format(self.femur_length))
		print("\tLength of leg: {} m".format(self.leg_length))
		print("\tLength of arm: {} m".format(self.arm_length))
		print("\tHeight of ankle: {} m".format(self.ankle_height))
		print("\tLength of foot: {} m\n".format(self.foot_length))


	def segment_masses(self):
		"""Calculates masses of segments"""
		ratios = [FOOT_MASS_RATIO,LEG_MASS_RATIO,FEMUR_MASS_RATIO,THN_MASS_RATIO,ARM_MASS_RATIO]
		masses = [ratio * self.body_mass for ratio in ratios]
		masses_dict = dict(zip(segments, masses))
		print(masses_dict)
		return masses_dict
		

	def joint_coords(self, theta_leg, theta_femur, theta_torso, theta_arm):
		"""Calculates the joint coordinates"""
		ankle = [0,0]
		knee = [ankle[0] + self.leg_length*sin(theta_leg*pi/180), ankle[1] + self.leg_length*cos(theta_leg*pi/180)]
		hip = [knee[0] + self.femur_length*sin(theta_femur*pi/180), knee[1] + self.femur_length*cos(theta_femur*pi/180)]
		shoulder = [hip[0] + self.torso_length*sin(theta_torso*pi/180), hip[1] + self.torso_length*cos(theta_torso*pi/180)]
		wrist = [shoulder[0] + self.arm_length*sin(theta_arm*pi/180), shoulder[1] + self.arm_length*cos(theta_arm*pi/180)]
		meta5 = [ankle[0] + self.foot_length, ankle[1] - self.ankle_height]
		coords = dict(zip(joints, [meta5,ankle,knee,hip,shoulder,wrist]))
		return coords


	def body_com(self, theta_leg, theta_femur, theta_torso, theta_arm, coords=False, masses=False):
		"""Calculates the body CoM [xcom, ycom]"""
		if not coords:
			coords = self.joint_coords(theta_leg, theta_femur, theta_torso, theta_arm)

		if not masses:
			masses = self.segment_masses()

		thn_length = self.torso_length + self.hn_length

		foot_slope_angle =  atan(self.foot_length/self.ankle_height)
		ankle_meta5 = sqrt(self.foot_length**2 + self.ankle_height**2)
		com_foot = [coords['ANKLE'][0] + FOOT_RATIO_COM_PROXIMAL*ankle_meta5*sin(foot_slope_angle*pi/180), coords['ANKLE'][0] - FOOT_RATIO_COM_PROXIMAL*ankle_meta5*cos(foot_slope_angle*pi/180)]
		com_leg = [coords['ANKLE'][0] + LEG_RATIO_COM_DISTAL*self.leg_length*sin(theta_leg*pi/180), coords['ANKLE'][1] + LEG_RATIO_COM_DISTAL*self.leg_length*cos(theta_leg*pi/180)]
		com_femur = [coords['KNEE'][0] + FEMUR_RATIO_COM_DISTAL*self.femur_length*sin(theta_femur*pi/180), coords['KNEE'][1] + FEMUR_RATIO_COM_DISTAL*self.femur_length*cos(theta_femur*pi/180)]
		com_thn = [coords['HIP'][0] + THN_RATIO_COM_DISTAL*thn_length*sin(theta_torso*pi/180), coords['HIP'][1] + THN_RATIO_COM_DISTAL*thn_length*cos(theta_torso*pi/180)]
		com_arms = [coords['SHOULDER'][0] + ARM_RATIO_COM_PROXIMAL*self.arm_length*sin(theta_arm*pi/180), coords['SHOULDER'][1] + ARM_RATIO_COM_PROXIMAL*self.arm_length*cos(theta_arm*pi/180)]

		df = pd.DataFrame.from_dict(masses, orient='index', columns=["Mass [kg]"])
		df["CoMx"] = [com_foot[0], com_leg[0], com_femur[0], com_thn[0], com_arms[0]]
		df["CoMy"] = [com_foot[1], com_leg[1], com_femur[1], com_thn[1], com_arms[1]]
		df["CoMx*Mass"] = df["Mass [kg]"] * df["CoMx"]
		df["CoMy*Mass"] = df["Mass [kg]"] * df["CoMy"]

		body_com = [sum(df["CoMx*Mass"])/self.body_mass, sum(df['CoMy*Mass'])/self.body_mass]
		# print("Body CoM: {} metres".format(body_com))
		return df, body_com


	def joint_loads(self, df, body_com, coords):
		"""Calculates force and moment at joint using GRF and segment masses.
			Positive forces are upward and to the right.
			Positive moments are anti-clockwise"""

		foot_mass = df.loc["FOOT", "Mass [kg]"]
		com = [df.loc["FOOT", "CoMx"], df.loc["FOOT", "CoMy"]]
		Ax = 0
		Ay = foot_mass*9.81 - self.body_mass*9.81
		M_a = self.body_mass*9.81*(body_com[0] - coords["ANKLE"][0]) - foot_mass*9.81*(com[0] - coords["ANKLE"][0])

		leg_mass = df.loc["LEG", "Mass [kg]"]
		com = [df.loc["LEG", "CoMx"], df.loc["LEG", "Mass [kg]"]]
		Kx = Ax
		Ky = Ay + leg_mass*9.81
		M_k = M_a - Ax*(com[1] - coords["ANKLE"][1]) + Ay*(com[0] - coords["ANKLE"][0]) + leg_mass*9.81*(coords["KNEE"][0] - com[0])

		thigh_mass = df.loc["FEMUR", "Mass [kg]"]
		com = [df.loc["FEMUR", "CoMx"], df.loc["FEMUR", "CoMy"]]
		Hx = Kx
		Hy = Ky + thigh_mass*9.81
		M_h = M_k + Ky*(coords["KNEE"][0] - coords["HIP"][0]) - Kx*(coords["KNEE"][1] - coords["HIP"][1]) + thigh_mass*9.81*(com[0] - coords["HIP"][0])

		df = pd.DataFrame.from_dict(coords, orient='index', columns=["x [m]", "y [m]"])
		df["Fx [N]"] = [0, Ax, Kx, Hx, 0, 0]
		df["Fy [N]"] = [0, Ay, Ky, Hy, 0, 0]
		df["|F|/mg [%]"] = np.sqrt(df["Fx [N]"]**2 + df["Fy [N]"]**2)/(self.body_mass * 9.81) * 100
		df["M [Nm]"] = [0, M_a, M_k, M_h, 0, 0]
		df["M [Nm/kg]"] = df["M [Nm]"]/self.body_mass

		return df


if __name__ == "__main__":
	body_mass = 62					# [kilograms]
	head_neck_length = 0.2286 		# [metres]
	torso_length = 0.5715 			# [metres]
	leg_length = 0.381 				# [metres]
	femur_length = 0.4191			# [metres]
	arm_length = 0.7366 			# [metres]
	ankle_height = 0.08				# [metres]
	foot_length = 0.142				# [metres]

	theta_leg = 38	 			# angle between vertical and leg at ankle [degrees]
	theta_femur = -95			# angle between vertical femur at knee [degrees]
	theta_torso = 30 			# angle between vertical and torso at hip [degrees]
	theta_arm = 180				# angle between vertical and arm at shoulder [degrees]

	model = Body(body_mass, head_neck_length, torso_length, femur_length, leg_length, arm_length, foot_length, ankle_height)
	df, body_com = model.body_com(theta_leg, theta_femur, theta_torso, theta_arm)
	print(df)

	coords = model.joint_coords(theta_leg, theta_femur, theta_torso, theta_arm)
	print(coords)

	dfnew = model.joint_loads(df, body_com, coords)
	print(dfnew)
