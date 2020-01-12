import smbus			#import SMBus module of I2C
from time import sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/Downloads/crash-maps-firebase-adminsdk-mc1oh-3d46644415.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crash-maps.firebaseio.com'
})

ref = db.reference('crash-maps')
users_ref = ref.child('users')
users_ref.set({
         "Lawrence": {
             "crashed":False,
                },

        })
print(ref.get())
#default.app = firebase_admin.initalize.app()
#firebase=firebase.FirebaseApplication('https://crash-map.firebaseio.com')
#result=firebase.post('https://crash-map.firebaseio.com', {'crashed' : True})
#cred = credentials.ApplicationDefault()
#firebase_admin.initialize_app(cred, {
#    'projectId':'crash-maps',
#    })
#db = firestore.client()

PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


def MPU_Init():
    #write to sample rate register
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

        #Write to power management register
        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

        #Write to Configuration register
        bus.write_byte_data(Device_Address, CONFIG, 0)

        #Write to Gyro configuration register
        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

        #Write to interrupt enable register
        bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)

        #concatenate higher and lower value
        value = ((high << 8) | low)

        #to get signed value from mpu6050
        if(value > 32768):
            value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address

MPU_Init()

print (" Reading Data of Gyroscope and Accelerometer")
#doc_ref = db.collection(u'crashDetection').document(u'ligma')
#doc_ref.set({
#    u'crashed': true
#    })
avgx=[0,0,0,0,0]
avgy=[0,0,0,0,0]
avgz=[0,0,0,0,0]
while True:

    #Read Accelerometer raw value
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)

        #Read Gyroscope raw value
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)

        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0

        Gx = gyro_x/75
        Gy = gyro_y/75
        Gz = gyro_z/75
        if Gx>15 or Gy>15 or Gz>15:
            print ("u crashed lmao")
            users_ref.set({
                "Lawrence": {
                    "crashed":True,
                },

        })
            print(ref.get())
        
        print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
        sleep(1)
