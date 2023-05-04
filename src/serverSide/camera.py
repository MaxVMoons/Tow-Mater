# Part 01 using opencv access webcam and transmit the video in HTML
import cv2
import  pyshine as ps #  pip3 install pyshine==0.0.9
#SERVER = '192.168.8.153'
SERVER = '192.168.6.2'
HTML="""
<html>
<head>
<title>Car Live Feed</title>
</head>

<body>
<center> <div width='640' height = '240' 
<center><h1> LIVE BEAGLEBONE REACTION </h1></center>
<center><img src="stream.mjpg" width='640' height='480' autoplay playsinline></center>
</body>
</html>
"""
def main():
    StreamProps = ps.StreamProps
    StreamProps.set_Page(StreamProps,HTML)
    address = (SERVER,9000) # Enter your IP address 
    try:
        StreamProps.set_Mode(StreamProps,'cv2')
        
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
        capture.set(cv2.CAP_PROP_BUFFERSIZE,4)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH,320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
        capture.set(cv2.CAP_PROP_FPS,24)

        StreamProps.set_Capture(StreamProps,capture)
        StreamProps.set_Quality(StreamProps,90)
        server = ps.Streamer(address,StreamProps)
        print('Server started at','http://'+address[0]+':'+str(address[1]))
        server.serve_forever()
        
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()
        
if __name__=='__main__':
    main()