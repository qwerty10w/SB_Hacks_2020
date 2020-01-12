#Lawrence Su
#CrashMaps
#sends crash data to Firebase live database



#enable I2C commands before u compile
#settings idr which ones
#create a firebase live database and download the credentials as an admin
import smbus	
import time 
from time import sleep
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('/home/pi/Downloads/crash-maps-firebase-adminsdk-mc1oh-3d46644415.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://crash-maps.firebaseio.com'
    })

#ref = db.reference('crashes')
#users_ref = ref.child('users')
#users_ref.set({
#         "Device1": {
#             'crashed':False,
#             'severity':'1'
#                },
#
 #       })


 #if u wanna start off with an object in the database
#print(ref.get())
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
        bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

        bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

        bus.write_byte_data(Device_Address, CONFIG, 0)

        bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

        bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
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

print (" Gyroscope x y z data followed by accelerometer x y z data")
#theres also temperature but we dont need it for this purpose
#doc_ref = db.collection(u'crashDetection').document(u'ligma')
#doc_ref.set({
#    u'crashed': true
#    })
avgx=[0,0,0,0,0]
avgy=[0,0,0,0,0]
avgz=[0,0,0,0,0]
while True:

    #Read Accelerometer
        acc_x = read_raw_data(ACCEL_XOUT_H)
        acc_y = read_raw_data(ACCEL_YOUT_H)
        acc_z = read_raw_data(ACCEL_ZOUT_H)

        #Read Gyroscope
        gyro_x = read_raw_data(GYRO_XOUT_H)
        gyro_y = read_raw_data(GYRO_YOUT_H)
        gyro_z = read_raw_data(GYRO_ZOUT_H)

        #Full scale range +/- 250 degree/C as per sensitivity scale factor
        Ax = acc_x/16384.0
        Ay = acc_y/16384.0
        Az = acc_z/16384.0
        avgax=(sum(avgx))/5

        avgay=(sum(avgy))/5
        avgaz=(sum(avgz))/5
        dx=Ax-avgax
        dy=Ax=avgay
        dz=Ax-avgaz

        if (dx<5 and dx>3) or (dy<5 and dy>3) or (dz<5 and dz>3):
            print ("u crashed slow lmao")

        elif (dx>5 and dx<8) or (dy>5 and dy<8) or (dz>5 and dz<8):
            print ("u crashed speedy lmao")
        else:
            x=5

        Gx = gyro_x/75
        Gy = gyro_y/75
        Gz = gyro_z/75
        if abs(Gx)>20 or abs(Gy)>20 or abs(Gz)>20 or dx>4 or dy>4 or dz>4:
            print ("u crashed lmao")
            ref = db.reference('crashes')
            users_ref = ref.child('users')
            users_ref.update({
                "Devce 1": {
                    'Device ID':'001',
                    'severity':'1'} ,

                 })
            users_ref.push({
                "Device1": {
                    'Device ID':'001',
                    'severity':'1'
                    } ,

                }) 
            print(ref.get())
           # users_ref = ref.child('users')
           # users_ref.update({
            #    "Device1": {
             #       'Device ID':'000',
              #      'severity':'1'
               #     },

                #})
            #    users_ref.update({
         #       "Device 1": {
          #          'crashed':True,
           #         'severity':'sev'
            #    },
#
 #       })
        for i in range(1,4):
            avgx[i]=avgx[i-1]
            avgy[i]=avgy[i-1]
            avgz[i]=avgz[i-1]
        avgx[0]=Ax
        avgy[0]=Ay
        avgz[0]=Az
        print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
        sleep(1)
