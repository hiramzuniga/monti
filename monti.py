# -*- coding: utf-8 -*-
import wx
import os
import glob

#--------------------------------------------------------------------------------
# Aplication developed in python the unique function is to burn iso images 
# into external device storage, for example it works perfectly with Raspbian 
# and others SO available for Raspberry, works to with any iso file and any 
# device.
#--------------------------------------------------------------------------------

wildcard = "*.iso"
TASK_RANGE = 100
status = 'trabajando...'
 
class monti(wx.Frame):
 
#--------------------------------------------------------------------------------
#Constructor principal
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Monti: Burn image in the external storage", size=(450, 360))
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.meSystem()
        self.InitUI()
        self.Centre()
        self.Show()
#----------------------------------------------------------------------..........
# Construcción de la GUI
    def InitUI(self):
        
        self.timer = wx.Timer(self, 1)
        self.count = 0
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)       
#---------------------------Create a menu bar------------------------------------
        menubar = wx.MenuBar()
        
        fileMenu = wx.Menu()
        fitem = fileMenu.Append(wx.ID_EXIT, 'Salir', 'Salir de la aplicación')
        menubar.Append(fileMenu, '&Archivo')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
        
        help = wx.Menu()
        fitemdos = help.Append(-1, '&Monti')
        menubar.Append(help, '&Acerca de')
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, fitemdos)        
#--------------------Create a Panel and others components-------------------------        
        panel = wx.Panel(self)
        
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        st1 = wx.StaticText(self,-1,label='1.- Seleccionar imagen: ')  
        hbox.Add(st1)        
        self.etiqueta = wx.StaticText(self,-1,label=u'')
        hbox.Add(self.etiqueta,wx.RIGHT,border=15)         
        vbox.Add(hbox, flag=wx.LEFT|wx.TOP , border=15)    	
        vbox.Add((-1, 10))
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, label="Seleccionar...")
        btn.Bind(wx.EVT_BUTTON, self.onOpenFile)      
        hbox2.Add(btn,wx.RIGHT,border=10)                     
        vbox.Add(hbox2, flag=wx.LEFT, border=32)   
        vbox.Add((-1, 10))
        
        hbox3= wx.BoxSizer(wx.HORIZONTAL)
        st2 = wx.StaticText(self,-1,label='2.- Seleccionar dispositivo: ')  
        hbox3.Add(st2)        
        self.etiquetas = wx.StaticText(self,-1,label=u'')
        hbox3.Add(self.etiquetas,border=10)              
        
        vbox.Add(hbox3, flag=wx.LEFT | wx.TOP, border=15)   
        panel.SetSizer(vbox)
        vbox.Add((-1, 15))    
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        cb = wx.ComboBox(self, pos=(50, 30), choices=self.drive, 
            style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.OnSelect)
        hbox4.Add(cb,border=10)
        vbox.Add(hbox4, flag=wx.LEFT, border=35) 
        vbox.Add((-1, 10))
        
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        self.pro = wx.StaticText(self, label='')
        self.text = wx.StaticText(self, label='')
        self.btn1 = wx.Button(self, label="Quemar")
        self.Bind(wx.EVT_BUTTON, self.OnOk, self.btn1)
        st3 = wx.StaticText(self,-1,label='3.- Quemar imagen: ')  
        hbox6.Add(st3)  
        hbox6.Add(self.btn1, proportion=1, flag=wx.RIGHT, border=10)
        hbox6.Add(self.text, proportion=1)
        hbox6.Add(self.pro, proportion=1)
        vbox.Add(hbox6, flag=wx.LEFT | wx.TOP, border=15)   
        vbox.Add((-1, 10))
        
        self.gauge = wx.Gauge(self, range=TASK_RANGE, size=(250, 25))
        hbox5 = wx.BoxSizer(wx.HORIZONTAL)
        hbox5.Add(self.gauge, proportion=1)
        vbox.Add(hbox5, flag=wx.LEFT, border=10)   
        vbox.Add((-1, 10))
        
        hbox7 = wx.BoxSizer(wx.HORIZONTAL)
        self.btnS = wx.Button(self, label="Salir")
        self.Bind(wx.EVT_BUTTON, self.OnQuit, self.btnS)
        st4 = wx.StaticText(self,-1,label='4.- : ')  
        hbox7.Add(st4)  
        hbox7.Add(self.btnS, proportion=1, flag=wx.RIGHT, border=10)
        vbox.Add(hbox7, flag=wx.LEFT | wx.TOP, border=15)   
        vbox.Add((-1, 10))       
#----------------------------------------------------------------------
# Buscar imagen iso
    def onOpenFile(self, event):
        dlg = wx.FileDialog(
            self, message="Selecciona archivo",
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            self.paths = dlg.GetPaths()
            print "Has seleccionado el siguiente iso"
            for self.path in self.paths:
                print self.path
        if self.path != '':
        	  self.etiqueta.SetLabel(self.path)
        dlg.Destroy()
#----------------------------------------------------------------------
    def OnSelect(self, e):
        self.drive = e.GetString()
        print "Ha seleccionado el dispositivo montado en:\n" + self.drive
        self.etiquetas.SetLabel(self.drive)
#----------------------------------------------------------------------
#identificar que dispositivos tenemos conectados    
    def OnQuit(self, e):
      dial = wx.MessageDialog(None, 'Realmente quieres salir?', 'Pregunta',
      wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
      ret = dial.ShowModal()
      if ret == wx.ID_YES:
          filelist = glob.glob("*.monti")
          for f in filelist:
              os.remove(f)
              print "Erase files..."
          self.Destroy()
      else:
          self.Show()
#----------------------------------------------------------------------
#About de la aplicación        
    def OnAboutBox(self, e):
        op = os.open("stuff/desc", os.O_RDWR) 
        self.f  = os.read(op,280) 
        description = self.f 
        li = os.open("stuff/lice", os.O_RDWR) 
        self.l  = os.read(li,200) 
        licence = self.l
        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('stuff/logo.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Monti')
        info.SetVersion('0.1b')
        info.SetDescription(description)
        info.SetCopyright('(C) 2013 Hiram')
        info.SetWebSite('http://valles.servehttp.com')
        info.SetLicence(licence)
        info.AddDeveloper('Hiram Zúñiga')
        info.AddDocWriter('Hiram Zúñiga')
        info.AddArtist('Hiram')
        info.AddTranslator('-')
        wx.AboutBox(info)
#----------------------------------------------------------------------
# Método antes de cerrar     
    def OnClose(self, event):
        dial = wx.MessageDialog(None, 'Realmente quieres salir?', 'Pregunta',
        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            filelist = glob.glob("*.monti")
            for f in filelist:
                os.remove(f)
                print "Erase files..."
            self.Destroy()
        else:
            self.Show()
#----------------------------------------------------------------------
# OnOk          
    def OnOk(self, e):
        if self.count >= TASK_RANGE:
            return
        os.system("dd if=%s of=%s" % (self.path, self.drive))
        self.timer.Start(50)
        self.text.SetLabel('Verificando...')
#----------------------------------------------------------------------
# OnTimer       
    def OnTimer(self, e):
        self.count = self.count + 1
        self.gauge.SetValue(self.count)
        if self.count == TASK_RANGE:
            self.timer.Stop()
            self.text.SetLabel('Correcto')
#--------------------------------------------------------------------------------
#Averiguar que usb tengo conectadas y almaceno en un archivo temporal hd.monti
    def meSystem(self):
        os.system("find /dev/ -name 'sd[b-Z][0-9]' > hd.monti && find /dev/ -name 'mmcblk[0-9]' >> hd.monti")
        f = open("hd.monti")
        self.drive = []
        for line in f:
            self.drive.append(line)                                  
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = monti()
    app.MainLoop()