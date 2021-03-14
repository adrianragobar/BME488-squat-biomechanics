from math import sin, cos, pi, sqrt, acos
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# COM/SEGMENT LENGTH RATIOS
ARM_RATIO_COM_PROXIMAL = 0.470
THN_RATIO_COM_DISTAL = 0.34
FEMUR_RATIO_COM_DISTAL = 0.567
LEG_RATIO_COM_DISTAL = 0.567

# SEGMENT MASS/BODY MASS RATIOS
ARM_MASS_RATIO = 0.050
THN_MASS_RATIO = 0.578
FEMUR_MASS_RATIO = 0.100
LEG_MASS_RATIO = 0.0465

segments = ["LEG", "FEMUR", "THN", "ARMS"]
joints = ["ANKLE", "KNEE", "HIP", "SHOULDER", "WRIST"]
ankle = [0,0]

class Body:

	def __init__(self, body_mass, hn_length, torso_length, femur_length, leg_length, arm_length):
		self.body_mass = body_mass
		self.hn_length = hn_length
		self.torso_length = torso_length
		self.femur_length = femur_length
		self.leg_length = leg_length
		self.arm_length = arm_length

		print("Body with the following segment lengths was created:")
		print("\tBody mass: {} kg\n".format(self.body_mass))
		print("\tLength of head-neck: {} m".format(self.hn_length))
		print("\tLength of torso: {} m".format(self.torso_length))
		print("\tLength of femur: {} m".format(self.femur_length))
		print("\tLength of leg: {} m".format(self.leg_length))
		print("\tLength of arm: {} m\n".format(self.arm_length))


	def segment_masses(self):
		"""Calculates masses of segments"""
		masses = [LEG_MASS_RATIO,FEMUR_MASS_RATIO,THN_MASS_RATIO,ARM_MASS_RATIO] * self.body_mass
		masses_dict = dict(zip(segments, masses))
		return masses_dict
		

	def joint_coords(self, theta_leg, theta_femur, theta_torso, theta_arm):
		"""Calculates the joint coordinates"""
		ankle = [0,0]
		knee = [ankle[0] + self.leg_length*sin(theta_leg*pi/180), ankle[1] + self.leg_length*cos(theta_leg*pi/180)]
		hip = [knee[0] + self.femur_length*sin(theta_femur*pi/180), knee[1] + self.femur_length*cos(theta_femur*pi/180)]
		shoulder = [hip[0] + self.torso_length*sin(theta_torso*pi/180), hip[1] + self.torso_length*cos(theta_torso*pi/180)]
		wrist = [shoulder[0] + self.arm_length*sin(theta_arm*pi/180), shoulder[1] + self.arm_length*cos(theta_arm*pi/180)]
		coords = dict(zip(joints, [ankle,knee,hip,shoulder,wrist]))
		return coords


	def body_com(self, theta_leg, theta_femur, theta_torso, theta_arm, coords=False, masses=False):
		"""Calculates the body CoM"""
		if not coords:
			coords = self.joint_coords(theta_leg, theta_femur, theta_torso, theta_arm)

		if not masses:
			masses = self.segment_masses()

		thn_length = self.torso_length + self.hn_length

		com_leg = [coords['ANKLE'][0] + LEG_RATIO_COM_DISTAL*self.leg_length*sin(theta_leg), coords['ANKLE'][1] + LEG_RATIO_COM_DISTAL*self.leg_length*cos(theta_leg)]
		com_femur = [coords['KNEE'][0] + FEMUR_RATIO_COM_DISTAL*self.femur_length*sin(theta_femur), coords['KNEE'][1] + FEMUR_RATIO_COM_DISTAL*self.femur_length*cos(theta_femur)]
		com_thn = [coords['HIP'][0] + THN_RATIO_COM_DISTAL*thn_length*sin(theta_torso), coords['HIP'][1] + THN_RATIO_COM_DISTAL*thn_length*cos(theta_torso)]
		com_arms = [coords['SHOULDER'][0] + ARM_RATIO_COM_PROXIMAL*self.arm_length*sin(theta_arm), coords['SHOULDER'][1] + ARM_RATIO_COM_PROXIMAL*self.arm_length*cos(theta_arm)]

		df = pd.DataFrame.from_dict(masses, orient='index', columns=["Mass [kg]"])
		df["CoMx"] = [com_leg[0], com_femur[0], com_thn[0], com_arms[0]]
		df["CoMy"] = [com_leg[1], com_femur[1], com_thn[1], com_arms[1]]
		df["CoMx*Mass"] = df["Mass [kg]"] * df["CoMx"]
		df["CoMy*Mass"] = df["Mass [kg]"] * df["CoMy"]

		body_com = [sum(df["CoMx*Mass"])/self.body_mass, sum(df['CoMy*Mass'])/self.body_mass]
		# print("Body CoM: {} metres".format(body_com))
		return body_com


if __name__ == "__main__":

	body_mass = 62 					# [kilograms]
	head_neck_length = 0.2286 		# [metres]
	torso_length = 0.5715 			# [metres]
	leg_length = 0.381 				# [metres]
	measured_femur_length = 0.4191	# [metres]
	arm_length = 0.7366 			# [metres]

	## JOINT ANGLES
	## Note: Positive angles are toward the anterior part of the body from the vertical
	theta_leg = 38	 			# angle between vertical and leg at ankle [degrees]
	theta_femur = -95			# angle between vertical femur at knee [degrees]
	theta_torso = 30 			# angle between vertical and torso at hip [degrees]
	theta_arm = 0 				# angle between vertical and arm at shoulder [degrees]

	# X COM CHANGES WITH FEMUR LENGTH AND TORSO ANGLE
	fig = plt.figure()
	fig.suptitle('Change in X CoM with Femur Length and Torso Angle')

	while theta_torso < 90:
		xcom_arr = []
		femur_length_arr = []
		femur_length = leg_length/2

		while femur_length < torso_length:
			model = Body(body_mass, head_neck_length, torso_length, femur_length, leg_length, arm_length)
			body_com = model.body_com(theta_leg, theta_femur, theta_torso, theta_arm)

			xcom = body_com[0]
			xcom_arr.append(xcom)
			femur_length_arr.append(femur_length)

			femur_length += 0.01

			print('Femur length: {}'.format(femur_length))
			print('\txCom = {}'.format(xcom))

		plt.plot(femur_length_arr, xcom_arr, label='Torso angle: {} deg'.format(theta_torso))

		theta_torso += 10

	plt.ylim(-0.006, 0.004)
	# plt.xlim(0, 90)
	plt.plot([measured_femur_length, measured_femur_length], [-0.006, 0.004], linestyle=':', color='black')
	plt.xlabel('Femur length (metres)')
	plt.ylabel('X CoM (metres)')
	plt.grid(b=True, which='both', axis='both', linestyle='--')
	plt.legend()
	plt.show()

	# X COM CHANGE WITH TORSO ANGLE
	fig = plt.figure()
	fig.suptitle('Change in X CoM With Torso Angle')
	theta_torso = 0
	xcom_arr = []
	theta_torso_arr = []

	while theta_torso < 90:
		theta_torso_arr.append(theta_torso)
		model = Body(body_mass, head_neck_length, torso_length, measured_femur_length, leg_length, arm_length)
		body_com = model.body_com(theta_leg, theta_femur, theta_torso, theta_arm)

		xcom = body_com[0]
		xcom_arr.append(xcom)
		theta_torso += 1

	plt.plot(theta_torso_arr, xcom_arr, color='orange')
	plt.xlabel('Torso angle (deg)')
	plt.ylabel('X CoM (metres)')
	plt.grid(b=True, which='both', axis='both', linestyle='--')
	plt.legend()
	plt.show()
