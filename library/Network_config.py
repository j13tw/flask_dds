import os, sys
import serial
from serial import SerialException
import datetime, time

class Reboot_system():
    def __init__(self):
       self.command = "sudo init 6"

    def reboot(self):
       os.system(self.command)

class Watchdog_config():
    def __init__(self):
        self.cpu_short_load = "24"
        self.cpu_middle_load = "20"
        self.cpu_long_load = "18"
        self.cpu_temperature = "40"

    def watchdog_status(self):
        file = open('/etc/watchdog.conf', 'r') 
        for x in range (1, 36):
            line = file.readline()
#            print(line)
            if (x == 10): 
                self.cpu_short_load = line.split(" ")[2].split("\n")[0]
            if (x == 11): 
                self.cpu_middle_load = line.split(" ")[2].split("\n")[0]
            if (x == 12): 
                self.cpu_long_load = line.split(" ")[2].split("\n")[0]
            if (x == 35): 
                self.cpu_temperature = line.split(" ")[2].split("\n")[0]
#        print(self.cpu_short_load)
#        print(self.cpu_middle_load)
#        print(self.cpu_long_load)
#        print(self.cpu_temperature)
        return self.cpu_short_load, self.cpu_middle_load , self.cpu_long_load, self.cpu_temperature

    def set_cpu_load_short(self, percent):
        command = "sudo sed -i '10c max-load-1 = " + percent + "' /etc/watchdog.conf"
        status = os.system(command)
        return status

    def set_cpu_load_middle(self, percent):
        command = "sudo sed -i '11c max-load-5 = " + percent + "' /etc/watchdog.conf"
        status = os.system(command)
        return status

    def set_cpu_load_long(self, percent):
        command = "sudo sed -i '12c max-load-15 = " + percent + "' /etc/watchdog.conf"
        status = os.system(command)
        return status

    def set_cpu_temperature(self, temperature):
        command = "sudo sed -i '35c max-temperature = " + temperature + "' /etc/watchdog.conf"
        status = os.system(command)
        return status

    def remove_cpu_load_short(self):
        command = "sudo sed -i '10c \#max-load-1 = " +  self.cpu_long_load  + "' /etc/watchdog.conf"
        status = os.system(command)
        return status

    def remove_cpu_load_middle(self):
        command = "sudo sed -i '11c \#max-load-5 = " +  self.cpu_middle_load  + "' /etc/watchdog.conf"
        status = os.system(command)
        return status

    def remove_cpu_load_long(self):
        command = "sudo sed -i '12c \#max-load-15 = " + self.cpu_long_load + "' /etc/watchdog.conf"
        status = os.system(command)
        return status

class Gps_time():
    def __init__(self):
        self.set_date = ""
        self.set_time = ""

    def get_time(self):
        try:
            self.gps = serial.Serial('/tty/USB0', 4800, timeout=1)
        except:
            return "ERROR"    
        while(1):
            response = self.gps.readline().decode('ascii')
#            print(response)
            if (response.split(',')[0] == "$GPRMC"):
                date = datetime.datetime.strptime(response.split(',')[9], '%d%m%y')
#                print("DATE : ", date.year, date.month, date.day)
                self.set_date = str(date.year) + "-" + str(date.month) + "-" + str(date.day)
#                print(set_date)
            if (response.split(',')[0] == "$GPGGA"):
                now = datetime.datetime.strptime(response.split(',')[1].split('.')[0], '%I%M%S')
#                print("Now", now.hour+ 8, now.minute, now.second)
                self.set_time = str(now.hour + 8) + ":" + str(now.minute) + ":" + str(now.second)
#                print(set_time)
            if (self.set_time != "" and self.set_date != ""):
#               print("set GPS time")
                os.system("sudo timedatectl set-ntp 0")
                command = 'sudo date -s "' + self.set_date + ' ' + self.set_time + '"'
                os.system(command)
                break
        self.gps.close()
        return "OK"

class File_search():
    def __init__(self):
        pass

    def ini_list(self):
        self.ini_table = os.listdir('/home/pi/ini/')
        return  self.ini_table

class Time_config():
    def __init__(self):
        pass

    def get_now(self):
        now = datetime.datetime.now()
        year = str(now.year)
        if (int(now.month) < 10): month = "0" + str(now.month)
        else: month = str(now.month)
        if (int(now.day) < 10): day = "0" + str(now.day)
        else: day = str(now.day)
        if (int(now.hour) < 10): hour = "0" + str(now.hour)
        else: hour = str(now.hour)
        if (int(now.minute) < 10): minute = "0" + str(now.minute)
        else: minute = str(now.minute)
        if (int(now.second) < 10): second = "0" + str(now.second)
        else: second = str(now.second)
        response = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
        return response
   
    def date_set(self, year, month, date):
        os.system("sudo timedatectl set-ntp 0")
        now = datetime.datetime.now()
        self.date_command = 'sudo date -s "' + year + '-' + month + '-' + date + " " + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second) + '"'
#        print(self.date_command)
        os.system(self.date_command)
        return "OK"
    
    def time_set(self, hour, minute, second):
        os.system("sudo timedatectl set-ntp 0")
        now = datetime.datetime.now()
        self.time_command = 'sudo date -s "' + str(now.year) + '-' + str(now.month) + '-' + str(now.day) + " " + hour + ':' + minute + ':' + second + '"'
#        print(self.time_command)
        os.system(self.time_command)
        return "OK"

class Ntp_config():
    def __init__(self):
#       need install ntpdate By 'sudo apt-get install ntpdate'
        os.system('timedatectl set-timezone "Asia/Taipei"')
#        os.system('sudo /etc/init.d/ntp stop >/dev/null 2>&1')
        try:
            f = open('/etc/network/ntp.log', 'r')
            f.close()
        except:
            os.system('cp ./library/ntp.log /etc/network/ntp.log')

    def ntp_set(self, ntp_host):
        os.system("sudo timedatectl set-ntp 0")
        self.ntp_command = 'sudo ntpdate ' + ntp_host + ' >/dev/null 2>&1'
        self.f = open('/etc/network/ntp.log', 'w')
        self.f.write(ntp_host)
        self.f.close()
        connect = os.system(self.ntp_command)
        now = datetime.datetime.now()
        year = str(now.year)
        if (int(now.month) < 10): month = "0" + str(now.month)
        else: month = str(now.month)
        if (int(now.day) < 10): day = "0" + str(now.day)
        else: day = str(now.day)
        if (int(now.hour) < 10): hour = "0" + str(now.hour)
        else: hour = str(now.hour)
        if (int(now.minute) < 10): minute = "0" + str(now.minute)
        else: minute = str(now.minute)
        if (int(now.second) < 10): second = "0" + str(now.second)
        else: second = str(now.second)
        response = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
        if (connect == 0):
            return "OK", response
        else:
            return "ERROR", response

class Net_config():
    def __init__(self):
        try:
            f = open('/etc/network/interfaces.bak')
            f.close()
        except:
            os.system('sudo cp ./library/interfaces.bak /etc/network/interfaces')
        try:
            f = open('/etc/network/Restusb.py')
            f.close()
        except:
            os.system('sudo cp ./library/Restusb.py /etc/network/Restusb.py')

    def eth0_dhcp(self):
        os.system("sudo sed -i '3c iface eth0 inet dhcp' /etc/network/interfaces")
        os.system("sudo sed -i '4c \\ ' /etc/network/interfaces")
        os.system("sudo sed -i '5c \\ ' /etc/network/interfaces")
        os.system("sudo sed -i '6c \\ ' /etc/network/interfaces")
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
        os.system('sudo cp /etc/network/interfaces ./library/interfaces.bak')

    def eth1_dhcp(self):
        os.system("sudo sed -i '12c iface eth1 inet dhcp' /etc/network/interfaces")
        os.system("sudo sed -i '13c \\ ' /etc/network/interfaces")
        os.system("sudo sed -i '14c \\ ' /etc/network/interfaces")
        os.system("sudo sed -i '15c \\ ' /etc/network/interfaces")
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()
        os.system(self.usb_reset)
        os.system('sudo cp /etc/network/interfaces /etc/network/interfaces.bak')

    def eth0_static(self, ip, netmask, gateway):
        os.system("sudo sed -i '3c iface eth0 inet static' /etc/network/interfaces")
        command = "sudo sed -i '4c address " + ip + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '5c netmask " + netmask + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '6c gateway " + gateway + "' /etc/network/interfaces"
        os.system(command)
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
        os.system('sudo cp /etc/network/interfaces /etc/network/interfaces.bak')

    def eth1_static(self, ip, netmask, gateway):
        self.f = open('/etc/network/interfaces', 'r+')
        self.f.seek(190)
        self.f.write('allow-hotplug eth1\n\n')
        os.system("sudo sed -i '12c iface eth1 inet static' /etc/network/interfaces")
        command = "sudo sed -i '13c address " + ip + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '14c netmask " + netmask + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '15c gateway " + gateway + "' /etc/network/interfaces"
        os.system(command)
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()
        os.system(self.usb_reset)
        os.system('sudo cp /etc/network/interfaces /etc/network/interfaces.bak')

    def eth0_dns(self, dns):
        command = "sudo sed -i '7c dns-nameserver " + dns + "' /etc/network/interfaces"
        os.system(command)
        os.system("sudo sed -i '8c \\ ' /etc/network/interfaces")
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
        os.system('sudo cp /etc/network/interfaces /etc/network/interfaces.bak')

    def eth1_dns(self, dns):
        command = "sudo sed -i '16c dns-nameserver " + dns + "' /etc/network/interfaces"
        os.system(command)
        os.system("sudo sed -i '17c \\ ' /etc/network/interfaces")
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()
        os.system(self.usb_reset)
    
    def eth0_dual_dns(self, dns, sub_dns):
        command = "sudo sed -i '7c dns-nameserver " + dns + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '8c dns-nameserver " + sub_dns + "' /etc/network/interfaces"
        os.system(command)
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
    
    def eth1_dual_dns(self, dns, sub_dns):
        command = "sudo sed -i '16c dns-nameserver " + dns + "' /etc/network/interfaces"
        os.system(command)
        command = "sudo sed -i '17c dns-nameserver " + sub_dns + "' /etc/network/interfaces"
        os.system(command)
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()

    def eth0_auto_dns(self):
        command = "sudo sed -i '7c dns-nameserver 8.8.8.8' /etc/network/interfaces"
        os.system(command)
        os.system("sudo sed -i '8c \\ ' /etc/network/interfaces")
        os.system('sudo ifdown eth0')
        os.system('sudo ifup eth0')
    
    def eth1_auto_dns(self):
        command = "sudo sed -i '16c dns-nameserver 8.8.8.8' /etc/network/interfaces"
        os.system(command)
        os.system("sudo sed -i '17c \\ ' /etc/network/interfaces")
        os.system('lsusb | grep "Realtek" | cut -c16,17,18 >/tmp/usb.txt')
        self.usb_id = open('/tmp/usb.txt')
        self.usb_reset = 'sudo python /etc/network/Restusb.py -d ' + self.usb_id.read()
