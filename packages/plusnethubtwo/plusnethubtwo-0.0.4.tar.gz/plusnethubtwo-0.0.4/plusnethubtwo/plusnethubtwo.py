from requests import get, post
from hashlib import md5
from urllib.parse import unquote

class PlusnetHubTwo:
    def __init__(self, ip="192.168.1.254", password=None):
        if password:
            self.password = md5(password.encode()).hexdigest()
        self.ip = ip
        router_test = get(f"http://{self.ip}")
        if router_test.status_code != 200:
            raise ConnectionError("Router not found, check IP address")


    def light_on(self):
        """Turns Hub Light On"""
        response = post(f"http://{self.ip}/HubLightControl.cgi", data={"CMD": "", "brightness_enable": "0","led_brightness": "2", "led_schedule": "0", "led_schedule_start":"07:30", "led_schedule_end": "22:15", "pi": ""})
        if response.status_code != 200:
            raise ConnectionError("Failed to turn on the light")
    def light_off(self):
        """Turns Hub Light Off"""
        response = post(f"http://{self.ip}/HubLightControl.cgi", data={"CMD": "", "brightness_enable": "1","led_brightness": "0", "led_schedule": "0", "led_schedule_start":"07:30", "led_schedule_end": "22:15", "pi": ""})
        if response.status_code != 200:
            raise ConnectionError("Failed to turn off the light")
        
    def light_status(self):
        """ Returns the status of the Hub Light"""
        response = get(f"http://{self.ip}/cgi/cgi_home.js", headers={"Referer": f"http://{self.ip}/basic_-_my_devices.htm"})
        if response.status_code != 200:
            raise ConnectionError("Failed to get light status")
        response = response.text
        if "cgi_brightness_enable = unescape(\"0\")" in response:
            return True
        else:
            return False

    def get_devices(self):
        """Returns a dictionary of devices connected to the router"""
        response = get(f"http://{self.ip}/cgi/cgi_owl.js", headers={"Referer": f"http://{self.ip}/basic_-_my_devices.htm"})
        if response.status_code != 200:
            raise ConnectionError("Failed to get device list")
        response = response.text
        response = response.split("\n")
        device_dict = {}
        for i in range(len(response)):
            device_dict[i] = {}
            response[i] = unquote(response[i])
            temp_index = response[i].find("{") + 1
            response[i] = response[i][temp_index:len(response[i])-2]
            response[i] = response[i].split(",")
            for item in response[i]:
                split_index = item.find(":")
                device_dict[i][item[0:split_index-1]] = item[split_index+1::]
        return device_dict
    
    def get_online_devices(self):
        """Returns a list of devices connected to the router that are currently online"""
        devices = self.get_devices()
        online_devices = []
        for item in devices:
            if "station_nam" in devices[item] and devices[item]["onlin"] == "'1'":
                online_devices.append(devices[item]["station_nam"][1:-1])
        return online_devices

if __name__ == "__main__":
    # user_password = input("(Not Used) Enter router password: ")
    hub = PlusnetHubTwo()
    
    while True:
        user_input = input("Enter command: ")
        if user_input == "on":
            hub.light_on()
        elif user_input == "off":
            hub.light_off()
        elif user_input == "status":
            print(hub.light_status())
        elif user_input == "devices":
            print(hub.get_devices())
        elif user_input == "online":
            print(hub.get_online_devices())
        elif user_input == "exit":
            break
        else:
            print("Invalid command")