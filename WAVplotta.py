from Tkinter import *             # The Tkinter package
import Pmw,sys,os,struct,tkFileDialog,wave,py4cs.numpytools,FFT

root = Tk()                                     #
root.title('EEL 4834 WAV displayer')            #
my_balloon = Pmw.Balloon(root)                  #
graphState = {'fourierplot': None }

if not Pmw.Blt.haveblt(root):     # is Blt installed?
  print("You do not have BLT installed!")


#function definitions
def openF():
   global fileopen,nchannels, sampwidth, framerate,nframes, comptype, compname, x_vec, y_vec,seconds,windowlength,cursor
   fileopen = 1                                             #is a file open?
   dialog = tkFileDialog.Open(filetypes=[('wave', '*.wav')])
   filenameStr = str(dialog.show())
   l['text'] = '%s' % filenameStr                           #displays the file being viewed
   WAV = wave.open(filenameStr,'rb')                        #open the wave file sprecified by user
   (nchannels, sampwidth, framerate, nframes, comptype, compname) = WAV.getparams()
   WAVstring = WAV.readframes(WAV.getnframes())
   
   #mono 
   if      sampwidth == 1:
       y_vec = struct.unpack('%dB'%(nchannels*nframes),WAVstring)        
   #stereo 
   elif    sampwidth == 2:                           
       y_vec = struct.unpack('%dh'%(nchannels*nframes),WAVstring)
       
   ywindow = y_vec[0:framerate]          #ywindow = the first window to being viewed by user(0-->60 seconds)
   cursor = 0;seconds = 0
   windowlength = len(ywindow)
   PlotGraph(ywindow)

def Exit():
    print('Buh-Bye')
    root.destroy()
    
def PlotGraph(ywindow):
    global seconds,x,xwindow,framerate,nframes
    x.destroy()
    x = Pmw.Blt.Graph(root)
    x.pack(expand=NO,side = "left",fill='both')
    xwindow = tuple(py4cs.numpytools.arange(float(nframes))/framerate)
    xwindow = xwindow[0:len(ywindow)]
    x.line_create("Wave file", xdata=xwindow, ydata=ywindow,symbol='')
    if FFTon ==1:
        show_FFT()

def Bigger():
    global seconds,x,framerate,y_vec,fileopen,windowlength,cursor
    if not fileopen:
        print('exit')
##    print windowlength
    windowlength =int(round(.7*windowlength))
    cursor = cursor+(windowlength/4)
    if (cursor+windowlength)>nframes:
        windowlength = nframes - cursor
    ywindow=y_vec[cursor:cursor+windowlength]
    PlotGraph(ywindow)
    if FFTon ==1:
        show_FFT()
    
def Smaller():
    global seconds,x,framerate,y_vec,fileopen,windowlength,cursor
    if not fileopen:
        print('exit')
    cursor = cursor-(windowlength/9)
    if cursor < 0:
        cursor = 0
    windowlength =int(round(1.2*windowlength))
    ywindow=y_vec[cursor:cursor+windowlength]
    PlotGraph(ywindow)
    if FFTon ==1:
        show_FFT()
    
def ForwardT():
    global seconds,x,framerate,y_vec,fileopen,cursor
    if not fileopen:
        print('exit')
    cursor+=windowlength
    ywindow=y_vec[cursor:cursor+windowlength]
    PlotGraph(ywindow)
    if FFTon ==1:
        show_FFT()
    
def BackwardsT():
    global seconds,x,framerate,y_vec,fileopen,cursor
    if not fileopen:
        print('exit')
    cursor-=windowlength
    ywindow=y_vec[cursor:cursor+windowlength]
    PlotGraph(ywindow)
    if FFTon ==1:
        show_FFT()
    
def show_FFT():
   # make a new graph area for the fourier transform named 'fourier'
   global fourierplot,cursor,windowlength,y_vec,FFTon
   FFTon=1
   fourierplot.destroy()
   fft = tuple(abs(FFT.fft(y_vec[cursor:cursor+windowlength])))
   xfft = tuple(py4cs.numpytools.arange(float(len(fft)+1)))
   xfft = xfft[1:int(round(len(xfft)/8))]
   fft = fft[1:int(round(len(fft)/8))]
   #create graph for Fourrier Tranform of wav file snippet
   fourierplot = Pmw.Blt.Graph(root)
   fourierplot.pack(expand=1,side = "right", fill='both')
   fourierplot.line_create("Fourier Transform of Data", xdata=xfft, ydata=fft, symbol='')
   
def hide_FFT():
   global fourierplot,FFTon
   FFTon=0
   fourierplot.destroy()

#Create the menu bar object
menu_bar = Pmw.MenuBar(root,
   hull_relief='raised',           #styling
   hull_borderwidth = 1,
   balloon = my_balloon,
   hotkeys=True)
menu_bar.pack(fill='x')

menu_bar.addmenu('FiL3',            #Create menu bar items
   'File Selection',               #balloon help
   tearoff=False)

l = Label(root, text='Open a WAV file and it will be graphed below. \n You may choose to show the Fourrier Transform \n Choose wisely')
l.pack()

#add the 'open file'menu sub-item
menu_bar.addmenuitem('FiL3','command',label='Open File',    
command=openF)
#add the 'exit' sub-item
menu_bar.addmenuitem('FiL3','command',label='Exit',command=Exit)

#add the Options menu item
menu_bar.addmenu('Fourier', 'other stuff')

#add Filter menu sub-menu items
menu_bar.addmenuitem('Fourier', 'command',
   label='Show Fourier Transform',
   command=show_FFT)
menu_bar.addmenuitem('Fourier', 'command',
   label='Hide Fourier Transform',
   command=hide_FFT)


buttFrame = Frame(root)
buttFrame.pack()
#CREATE BUTTONS
#create button to make graph larger
BigButt = Button(buttFrame, text=' Zoom In ',command=Bigger)
BigButt.pack(fill=BOTH,expand=1,side = 'top')

#create button to make graph smaller
BigButt = Button(buttFrame, text=' Zoom Out ', command=Smaller)
BigButt.pack(fill=BOTH,expand=1,side = 'bottom')

#create button to move time forward
timeButt = Button(buttFrame, text=' t--> ', command=ForwardT)
timeButt.pack(fill=Y,expand=1,side = 'right')

#create button to move time backward
timeButt = Button(buttFrame , text=' <--t  ', command=BackwardsT)
timeButt.pack(fill=Y,expand=1,side = 'left')

#initialize a graph for the WAV data in time named 't'
x = Pmw.Blt.Graph(root)
x.pack(expand=NO,side = "left",fill='both')

FFTon = 0
fourierplot = Pmw.Blt.Graph(root)
fileopen = 0
root.mainloop()             # and wait...
