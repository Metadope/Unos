#!/usr/bin/python
"""
   ProcMon.py -- Script to monitor process Starts & Stops
   
"""
__title__     = 'ProcMon'
__version__   = '1.0'
__author__    = 'Metadope'
__date__      = 'October 20th 2017'
__url__       = 'http://metadope.org' 

import pythoncom
import wmi
import threading
import Queue
import sys
import msvcrt
import time

class ProcessWatcher (threading.Thread):

  def __init__ (self, q, event, name = "modification" ):
    threading.Thread.__init__ (self)
    self.q = q
    self.event = event
    self.name = name
    #self.setDaemon (True)

  def run (self):
    pythoncom.CoInitialize ()
    try:
      c = wmi.WMI()
      self.q.put(("Starting to watch for process " + self.name, None))
      watcher = c.Win32_Process.watch_for(self.name) 
      while True:
        try:
          pro = watcher(timeout_ms=5000) #this 'watcher()' call blocks
        except wmi.x_wmi_timed_out:
          if self.event.wait(0.1): #see if we've been asked to quit (Event)
            break
        else: #woke up with a winner
          self.q.put ((self.name, pro))
    finally:
      pythoncom.CoUninitialize ()
      
animacons = [ "/|\\-/|\\- ", "\\|/-\\|/- ", chr(3)+chr(4)+chr(5)+chr(6), chr(1)+" "+chr(2)   ]
animate = True
animtimes = 0

def Animacon(w = 0, twix=0.1):
  global animate, animtimes
  out.write( time.strftime("\r%H:%M:%S ", time.localtime()) ) #we always output time
  if animate == False:
    return
  animtimes += 1
  if animtimes == 8:
    animtimes = 0
  inStr = animacons[ w & 3 ] #old C style
  for c in inStr:
    out.write(c + "\b")
    time.sleep(twix)

def EnumProcesses():
  counter = 0
  try:
    c = wmi.WMI()
    processes = c.Win32_Process() 
    for pro in processes:
      pathstr = pro.ExecutablePath
      if( pathstr == None):
        pathstr = ""
      print "%02d[%04d<-%04d] %s (%s)" % (counter, pro.ProcessId, pro.ParentProcessId, pro.Caption, pathstr)
        #pro.ExecutablePath, pro.CommandLine)
      counter += 1
  except:
    sys.stderr.write("Error enumerating processes\n")
  return counter

if __name__ == '__main__':
  out = sys.stderr
  
  q = Queue.Queue()
  ev = threading.Event()
  tCreate = ProcessWatcher(q, ev, name="creation")
  tCreate.start()
  tDelete = ProcessWatcher(q, ev, name="deletion")
  tDelete.start()
  tMod = None
#  tMod = ProcessWatcher(q, ev, name="modification")
#  tMod.start()
  #pythoncom.CoInitialize ()
  counter = EnumProcesses()
  
  out.write( "\n%s v%s - by %s (%s)\n" % (__title__, __version__, __author__, __url__))
  out.write("%d running processes at startup. Press 'q' to quit ('m' for menu)...\n" % (counter))
  time.sleep(1.5)
  events = 0
  alteranim = 0
  detail = 0
  while True:
    while not msvcrt.kbhit(): # or msvcrt.getch() != "q":
      if q.empty():
        if animate:
          Animacon(alteranim)
        else:
          time.sleep(0.2)
        if animtimes == 0:
          alteranim += 1
          alteranim &= 1
        continue
      #otherwise
      name, pro = q.get()
      if pro != None:
        #ts = "%s:%s:%s" % (pro.CreationDate[8:10], pro.CreationDate[10:12], pro.CreationDate[12:14])
        if detail == 2:
          print "[%04d]%02x %s of %s <-[%04d]" % (pro.ProcessId, events+1, name, pro.ExecutablePath, pro.ParentProcessId)
        elif detail == 3:
          print "[%04d]%02x %s of %s" % (pro.ProcessId, events+1, name, pro.Caption)
          print pro
        else:
          print "[%04d]%02x %s of %s" % (pro.ProcessId, events+1, name, pro.Caption)
        events += 1
        Animacon() #this is to insure that multiple q items get timestamped
      else:
        print name
      
    c = msvcrt.getch()
    
    if c == "q":
      ev.set() #tell our thread children we want to quit
      out.write("Signalling. Waiting for worker threads...\n")
      tCreate.join(11)
      if tCreate.is_alive():
        print "Creation watcher thread failed to respond to quit-flag."
      tDelete.join(11)
      if tDelete.is_alive():
        print "Deletion watcher thread failed to respond to quit-flag."
      if tMod != None:
        tMod.join(22)
        if tMod.is_alive():
          print "Modification watcher thread failed to respond to quit-flag."
        
      while msvcrt.kbhit(): #clear the kb buff (in case the user got impatient)
        msvcrt.getch()
      
      break #from the outermost-- maybe I should throw?
    elif c == "m":
      out.write("\r'a':animate (toggle) 'q': quit 'p': process list '1': 1-liner '2':detail '3':super-detail\n")
    elif c == "a":
      if( animate ):
        animate = False
      else:
        animate = True
      out.write("\b")
    elif c == "1" or c == "2" or c == "3":
      detail = int(c)
      out.write("Detail == %d\n" % detail)
    elif c == "p":
      EnumProcesses()
 
  out.write( "You pressed 'q' so I quit. Reported %d events\n" % (events))
  #pythoncom.CoUninitialize ()

  # after a while
    