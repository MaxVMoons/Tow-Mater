import socketio
import socket
import time
import subprocess


# IMPORTANT:
# ENSURE YOU HAVE INSTALLED SOCKETIO. pip install "python-socketio[client]" is the command to do so.
# READ THROUGH THIS CODE TO UNDERSTAND HOW YOU WILL RECEIVE THE UDP LINK WHERE THE BBB SHOULD STREAM TO!

class RaceConnection:
    # Globals
    sio = socketio.Client()
    sendFeed = ""
    global_RM_ip = ""

    def __init__(self, hostname):
        try:  # We will try and install socketio if you don't already have it.
            subprocess.check_call(
                ["pip", "install", "python-socketio[client]"]
            )
        except subprocess.CalledProcessError as e:
            print("Error installing python-socketio:", e)
            exit(-1)

        # Race Management's IP Address. Determined by hostname,
        self.ip_address = socket.gethostbyname(hostname)
        RaceConnection.global_RM_ip = self.ip_address
        # which will be "G17". Be sure to load that value
        self.RM = "http://" + self.ip_address + ":3000"
        # into hostname when creating an instance of this class.
        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.connected = False
        self.race_number = 0
        self.name = ""
        self.sendFeed = ""

    @sio.on("server-msg")
    # On sio events, self actually refers to the message sent by the server, not the object.
    def on_server_mg(self):
        print("Server message:", self)

    # Retrieve which UDP link to stream to, store it in sendFeed.
    @sio.on("get-rtsp-server")
    def on_get_rtsp(self):
        print("Server to connect to:", self)
        if len(RaceConnection.sendFeed) == 0 and len(RaceConnection.global_RM_ip) != 0:
            if self == 1:
                RaceConnection.sendFeed = "udp://" + RaceConnection.global_RM_ip + ":33113"
                print(
                    f"Stream BBB camera to this endpoint: {RaceConnection.sendFeed}")
            elif self == 2:
                RaceConnection.sendFeed = "udp://" + RaceConnection.global_RM_ip + ":44775"
                print(
                    f"Stream BBB camera to this endpoint: {RaceConnection.sendFeed}")
            print("The UDP link where you should stream your camera has been loaded into RaceConnection.sendFeed. "
                  "Feel free to use this variable, you can send this to your BBB.")
        else:
            print("Could not retrieve UDP link. Please stop execution and run again.")
            exit(-1)

    def on_connect(self):
        print("Connected\n")
        self.connected = True

    def on_disconnect(self):
        print("Disconnected")
        self.connected = False

    def racer_setup(self):
        self.name = input("Racer name? ")
        self.race_number = input("Team number? ")
        self.sio.emit(
            "setup-racer", {"name": self.name, "number": self.race_number})

    def connect_to_RM(self):
        while not self.connected:
            try:
                self.sio.connect(self.RM)
            except socketio.exceptions.ConnectionError as e:
                print("Failed to connect. Retrying...")
                if str(e) == "Already connected":
                    break
                else:
                    time.sleep(1)

    def send_throttle(self, throttle):
        self.sio.emit(
            "send-throttle", {"teamNum": self.race_number,
                              "throttle": throttle}
        )

    def stop(self):
        self.sio.disconnect()

    def start(self):
        self.connect_to_RM()
        while True:
            command = input(
                "To enter a new car, type n, else type q to quit. ")
            if command.lower() == "n":
                self.racer_setup()
                break
            elif command.lower() == "q":
                print("No connection established.")
                break
            else:
                print("Invalid command, try again!")
