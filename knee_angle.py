import matplotlib.pyplot as plt
from stability import Body

if __name__ == "__main__":

	body_mass = 62 					# [kilograms]
	head_neck_length = 0.2286 		# [metres]
	torso_length = 0.5715 			# [metres]
	leg_length = 0.381 				# [metres]
	measured_femur_length = 0.4191	# [metres]
	arm_length = 0.7366 			# [metres]
	ankle_height = 0.08				# [metres]
	foot_length = 0.142				# [metres]

	## JOINT ANGLES
	## Note: Positive angles are toward the anterior part of the body from the vertical
	theta_leg = 38	 			# angle between vertical and leg at ankle [degrees]
	theta_femur = -95			# angle between vertical femur at knee [degrees]
	theta_torso = 30 			# angle between vertical and torso at hip [degrees]
	theta_arm = 0 				# angle between vertical and arm at shoulder [degrees]

	# X COM CHANGES WITH FEMUR LENGTH AND KNEE ANGLE
	fig = plt.figure()
	fig.suptitle('Change in X CoM with Femur Length and Knee Angle')

	while theta_femur > -180 + theta_leg:
		xcom_arr = []
		femur_length_arr = []
		femur_length = leg_length/2

		while femur_length < torso_length:
			model = Body(body_mass, head_neck_length, torso_length, femur_length, leg_length, arm_length, foot_length, ankle_height)
			__, body_com = model.body_com(theta_leg, theta_femur, theta_torso, theta_arm)

			xcom = body_com[0]
			xcom_arr.append(xcom)
			femur_length_arr.append(femur_length)

			femur_length += 0.01

			print('Femur length: {}'.format(femur_length))
			print('\txCom = {}'.format(xcom))

		plt.plot(femur_length_arr, xcom_arr, label='Knee angle: {} deg'.format(theta_femur))

		inc = 10
		theta_femur -= inc
		# To keep other joint angles constant
		theta_torso += inc

	plt.ylim(-0.4, 0.3)
	# plt.xlim(0, 90)
	plt.plot([measured_femur_length, measured_femur_length], [-0.4, 0.4], linestyle=':', color='black')
	plt.xlabel('Femur length (metres)')
	plt.ylabel('X CoM (metres)')
	plt.grid(b=True, which='both', axis='both', linestyle='--')
	plt.legend()
	plt.show()

	# X COM CHANGE WITH KNEE ANGLE
	fig = plt.figure()
	fig.suptitle('Change in X CoM With Knee Angle')
	theta_torso = 30
	theta_femur = 0
	theta_leg = 38
	xcom_arr = []
	theta_femur_arr = []

	while theta_femur > -180 + theta_leg:
		theta_femur_arr.append(theta_femur)
		model = Body(body_mass, head_neck_length, torso_length, measured_femur_length, leg_length, arm_length, foot_length, ankle_height)
		__, body_com = model.body_com(theta_leg, theta_femur, theta_torso, theta_arm)

		xcom = body_com[0]
		xcom_arr.append(xcom)
		inc = 1
		theta_femur -= inc
		# To keep other joint angles constant
		theta_torso += inc

	plt.plot(theta_femur_arr, xcom_arr, color='orange')
	plt.xlim(-180 + theta_leg,0)
	plt.xlabel('Knee angle (deg)')
	plt.ylabel('X CoM (metres)')
	plt.grid(b=True, which='both', axis='both', linestyle='--')
	plt.legend()
	plt.show()