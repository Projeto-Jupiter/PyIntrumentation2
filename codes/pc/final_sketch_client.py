import socket,pickle,time
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtWidgets

#Functions
def qv1():
    """Event activated by the slection of the QV1 checkbox.
    If checked, the element referent of QV1 valve satate is set as True, else, it is set as False."""
    
    global data
    
    data[3] = not data[3]

    # if toggled: #check if it is toggled
    #     data[3] = True #set QV1 valve state element as True if toggled
    #     print ('QV1 on')
    # else:
    #     data[3] = False #set QV1 valve state element as True if not toggled
    #     print('QV1 off')

def update():

    global data,x,y,z
    
    data[0:3] = pickle.loads(s.recv(256))[0:3]

    x = x[1:]
    x.append(data[0])
    
    y = y[1:]
    y.append(data[1])

    z = z[1:]
    z.append(data[2])
    
    data_line_1.setData(x,y)
    data_line_3.setData(x,z)
    print(data)
    s.sendall(pickle.dumps(data))

HOST = '192.168.1.100'    # The remote host
PORT = 50006              # The same port as used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = [0,0,0,0]
    s.sendall(pickle.dumps(data))

    #Creating GUI
    app = pg.mkQApp() #create app variable

    mw = QtWidgets.QMainWindow() #criate main window variable
    mw.setWindowTitle('Hybrid Control GUI') #set window title
    cw = QtWidgets.QWidget() #create central widget
    mw.setCentralWidget(cw) #set central widget

    #the rows below create some layouts
    l1 = QtWidgets.QVBoxLayout() 
    cw.setLayout(l1) #set layout l2 as the central widget layout

    btn_QV1 = QtWidgets.QPushButton('Valvula')
    btn_QV1.clicked.connect(qv1) #connect qv1 button to function qv1

    pw1 = pg.PlotWidget(name='Plot1',title="Line Temperature Now",labels={'left': ('Temperature(K)'), 'bottom': ('Time(ms)')})  ## giving the plots names allows us to link their axes togethe
    pw3 = pg.PlotWidget(name='Plot3',title="Line Pressure Now",labels={'left': ('Pressure(bar)'), 'bottom': ('Time(ms)')})

    l1.addWidget(pw1)
    l1.addWidget(pw3)
    l1.addWidget(btn_QV1)

    mw.show() #open the main window in full screen

    x = list(np.zeros(200))  # 100 time points    
    y = list(np.zeros(200))  # 100 data points
    z = list(np.zeros(200))  # 100 data points
    
    pen2 = pg.mkPen(color=(0, 255, 0))
    data_line_1 = pw1.plot(x,y,pen = pen2)
    data_line_3 =  pw3.plot(x, z, pen=pen2)

    #Set timer
    timer = QtCore.QTimer()
    timer.setInterval(50)
    timer.timeout.connect(update)
    timer.start()

    pg.exec()