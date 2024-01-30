import pygame
import socket
import struct

UDP_IP = "10.1.1.1"
UDP_PORT = 5005

def sendMessage(message, port:int):
    print("UDP target IP:", UDP_IP)
    print("UDP target port:", port)
    print("message:", message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(message, (UDP_IP, port))     

pygame.display.init()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()

joysticks = {}

latestForwardVal:float = 0
latestStrafeVal:float = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Close the program any way you want, or troll users who want to close your program.
            raise SystemExit

        # Handle hotplugging
        if event.type == pygame.JOYDEVICEADDED:
                # This event will be generated when the program starts for every
                # joystick, filling up the list without needing to create them manually.
                joy = pygame.joystick.Joystick(event.device_index)
                joysticks[joy.get_instance_id()] = joy
                print(f"Joystick {joy.get_instance_id()} connencted")

        if event.type == pygame.JOYDEVICEREMOVED:
                del joysticks[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")
        
        if event.type == pygame.JOYAXISMOTION:
            print(f"Joystick {event.instance_id} axis {event.axis} value {event.value}")
            print(f"latestForwardVal: {latestForwardVal} latestStrafeVal: {latestStrafeVal}")
            match event.axis:
                case 1:
                    latestForwardVal = -event.value
                    sendMessage(struct.pack('ff', latestForwardVal, latestStrafeVal), 5005)
                
                case 2:
                    latestStrafeVal = event.value
                    sendMessage(struct.pack('ff', latestForwardVal, latestStrafeVal), 5005)