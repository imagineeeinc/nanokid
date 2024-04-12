import board, busio
import adafruit_mpu6050
import busio
import time

# Global
class Mpu:
	def __init__(self, scl=board.GP5, sda=board.GP4, disable_calibrate=False):
		try:
			i2c = busio.I2C(scl=scl, sda=sda)
			global mpu
			self.mpu = adafruit_mpu6050.MPU6050(i2c)
			if disable_calibrate == False:
				self.calibrate()
		except OSError as error:
			print(error)
			return error
	def calibrate(self):
		self.offsets = self._collect_raw_data()
		return self.offsets
	def get_values(self):
		return {
			"accel_x": self.mpu.acceleration[0] - self.offsets["accel_x"],
			"accel_y": self.mpu.acceleration[1] - self.offsets["accel_y"],
			"accel_z": self.mpu.acceleration[2] - self.offsets["accel_z"],
			"gyro_x": self.mpu.gyro[0] - self.offsets["gyro_x"],
			"gyro_y": self.mpu.gyro[1] - self.offsets["gyro_x"],
			"gyro_z": self.mpu.gyro[2] - self.offsets["gyro_x"],
		}
	def get_raw(self):
		return {
			"accel_x": self.mpu.acceleration[0],
			"accel_y": self.mpu.acceleration[1],
			"accel_z": self.mpu.acceleration[2],
			"gyro_x": self.mpu.gyro[0],
			"gyro_y": self.mpu.gyro[1],
			"gyro_z": self.mpu.gyro[2],
		}
	def get_temp(self):
		return self.mpu.temperature
	def _collect_raw_data(self):
		accel_x = []
		accel_y = []
		accel_z = []
		gyro_x = []
		gyro_y = []
		gyro_z = []

		for _ in range(100):
			accel_x.append(self.mpu.acceleration[0])
			accel_y.append(self.mpu.acceleration[1])
			accel_z.append(self.mpu.acceleration[2])
			gyro_x.append(self.mpu.gyro[0])
			gyro_y.append(self.mpu.gyro[1])
			gyro_z.append(self.mpu.gyro[2])
			time.sleep(0.01)

		return {
			"accel_x": sum(accel_x) / 100,
			"accel_y": sum(accel_y) / 100,
			"accel_z": sum(accel_z) / 100,
			"gyro_x": sum(gyro_x) / 100,
			"gyro_y": sum(gyro_y) / 100,
			"gyro_z": sum(gyro_z) / 100,
		}
