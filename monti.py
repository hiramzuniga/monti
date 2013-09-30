# -*- coding: utf-8 -*-
#!/usr/bin/env/python
import wx
import wx.animate
import os
import glob
import time

#------------------------------------------------------------------------------
# Aplication developed in python the function is to burn iso images
# into external device storage, for example it works perfectly with Raspbian
# and others SO available for Raspberry, works to with any iso file and any
# device.
#------------------------------------------------------------------------------

wildcard = "Imágen (*.img)|*.img| Iso (*.iso)|*.iso|All files (*.*)|*.*"

class Monti(wx.Frame):

#-------------------------Constructor Principal--------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY | wx.TAB_TRAVERSAL,
                          "Monti v0.3.2b", size=(400, 400),
                          style=wx.WANTS_CHARS | wx.TAB_TRAVERSAL |
                          wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        self.image = wx.Image('data/logo.png')
        self.image.Rescale(250, 150)
        self.image = wx.BitmapFromImage(self.image)
        wx.SplashScreen(self.image, wx.SPLASH_CENTRE_ON_SCREEN |
            wx.SPLASH_TIMEOUT, 2000, None, -1)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        #os.system("gksudo '' ")
        self.meSystem()
        self.InitUI()
        self.Centre()
        self.Show()

#--------------------Construcción de la GUI principal--------------------------
    def InitUI(self):
        panel = wx.Panel(self, style=wx.TAB_TRAVERSAL)
        panel.SetBackgroundColour(wx.Colour(255, 255, 255))

        ico = wx.Icon('data/linux.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        sis = "Monti: Quemar imágen en medio extraible"
        sis = wx.StaticText(panel, -1, sis, (20, 100))
        sis.SetBackgroundColour(wx.Colour(255, 255, 255))
        sis.SetForegroundColour(wx.Colour(0, 0, 0))
        sis.SetFont(wx.Font(11, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        hbox.Add(sis, proportion=1, flag=wx.LEFT, border=25)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        sis = "1.- Seleccionar imagen a quemar: "
        sis = wx.StaticText(panel, -1, sis, (20, 100))
        sis.SetBackgroundColour(wx.Colour(255, 255, 255))
        sis.SetForegroundColour(wx.Colour(0, 0, 0))
        sis.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        start_image = wx.Image('data/iso1.png')
        start_image.Rescale(50, 50)
        image = wx.BitmapFromImage(start_image)
        self.btnShow = wx.BitmapButton(panel, -1, image)
        self.Bind(wx.EVT_BUTTON, self.onOpenFile, self.btnShow)
        self.btnShow.SetToolTipString("Seleccionar imágen iso a quemar")
        hbox1.Add(sis, proportion=1, flag=wx.TOP | wx.LEFT, border=15)
        hbox1.Add(self.btnShow, flag=wx.LEFT, border=5)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        sis = "2.- Seleccionar medio extraible:"
        sis = wx.StaticText(panel, -1, sis, (20, 100))
        sis.SetBackgroundColour(wx.Colour(255, 255, 255))
        sis.SetForegroundColour(wx.Colour(0, 0, 0))
        sis.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        cb = wx.ComboBox(panel, pos=(50, 30), size=(100, -1),
            choices=self.drive, style=wx.CB_READONLY)
        cb.Bind(wx.EVT_COMBOBOX, self.onSelect)
        hbox2.Add(sis, proportion=1, flag=wx.TOP | wx.LEFT, border=15)
        hbox2.Add(cb, flag=wx.TOP | wx.LEFT, border=15)

        desmontar = wx.BoxSizer(wx.HORIZONTAL)
        sis = "3.- Desmontar unidad seleccionada: "
        sis = wx.StaticText(panel, -1, sis, (20, 100))
        sis.SetBackgroundColour(wx.Colour(255, 255, 255))
        sis.SetForegroundColour(wx.Colour(0, 0, 0))
        sis.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        start_image = wx.Image('data/usb.png')
        start_image.Rescale(50, 50)
        image = wx.BitmapFromImage(start_image)
        self.btnShow = wx.BitmapButton(panel, -1, image)
        self.Bind(wx.EVT_BUTTON, self.OnFormat, self.btnShow)
        self.btnShow.SetToolTipString("Desmontar imagen")
        desmontar.Add(sis, proportion=1, flag=wx.TOP | wx.LEFT, border=15)
        desmontar.Add(self.btnShow, flag=wx.LEFT, border=5)

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        quemar = "4.- Quemar imágen:"
        quemar = wx.StaticText(panel, -1, quemar, (20, 100))
        quemar.SetBackgroundColour(wx.Colour(255, 255, 255))
        quemar.SetForegroundColour(wx.Colour(0, 0, 0))
        quemar.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        start_image = wx.Image('data/burn.png')
        start_image.Rescale(50, 50)
        image = wx.BitmapFromImage(start_image)
        self.btnBurn = wx.BitmapButton(panel, -1, image)
        self.Bind(wx.EVT_BUTTON, self.onOk, self.btnBurn)
        self.btnBurn.SetToolTipString("Quemar imágen")

        ani = wx.animate.Animation('data/cargando.gif')
        self.ctrl = wx.animate.AnimationCtrl(panel, -1, ani)
        self.ctrl.SetUseWindowBackgroundColour()
        self.ctrl.Play()
        self.ctrl.Hide()

        hbox3.Add(quemar, flag=wx.TOP | wx.LEFT, border=15)
        hbox3.Add(self.btnBurn, flag=wx.LEFT, border=5)
        hbox3.Add(self.ctrl, flag=wx.LEFT, border=10)

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        salir = "5.- Salir:"
        salir = wx.StaticText(panel, -1, salir, (20, 100))
        salir.SetBackgroundColour(wx.Colour(255, 255, 255))
        salir.SetForegroundColour(wx.Colour(0, 0, 0))
        salir.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.BOLD, 0, ""))
        start_image = wx.Image('data/exit2.png')
        start_image.Rescale(50, 50)
        image = wx.BitmapFromImage(start_image)
        self.btnBurn = wx.BitmapButton(panel, -1, image)
        self.Bind(wx.EVT_BUTTON, self.onQuit, self.btnBurn)
        self.btnBurn.SetToolTipString("Salir")
        start_image = wx.Image('data/about.png')
        start_image.Rescale(40, 40)
        image = wx.BitmapFromImage(start_image)
        self.btnAcerca = wx.BitmapButton(panel, -1, image)
        self.Bind(wx.EVT_BUTTON, self.OnAboutBox, self.btnAcerca)
        self.btnAcerca.SetToolTipString("Acerca de...")

        hbox4.Add(salir, flag=wx.TOP | wx.LEFT, border=15)
        hbox4.Add(self.btnBurn, flag=wx.LEFT, border=5)
        hbox4.Add(self.btnAcerca, flag=wx.LEFT, border=170)

        vbox.Add(hbox, flag=wx.TOP, border=10)
        vbox.Add(hbox1, flag=wx.TOP, border=20)
        vbox.Add(hbox2, flag=wx.TOP, border=10)
        vbox.Add(desmontar, flag=wx.TOP, border=20)
        vbox.Add(hbox3, flag=wx.TOP, border=10)
        vbox.Add(hbox4, flag=wx.TOP, border=20)

        panel.SetSizer(vbox)

    def OnFormat(self, event):
        n = self.drive.encode('ascii', 'ignore')
        primerMontaje = list(n)
        segundoMontaje = list(n)
        for i in [0]:
            primerMontaje.pop()
        primero = ''.join(primerMontaje)
        segundoMontaje = primerMontaje
        for i in [0]:
            segundoMontaje.pop()
        for i in [0]:
            segundoMontaje.append('2')
        segundo = ''.join(segundoMontaje)
        os.system("umount %s" % primero)
        os.system("umount %s" % segundo)

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
        dlg.Destroy()

    def onSelect(self, e):
        self.drive = e.GetString()
        print "Ha seleccionado el dispositivo montado en:\n" + self.drive

    def onOk(self, e):
        n = self.path.encode('ascii', 'ignore')
        path = list(n)
        pathF = ''.join(path)
        print pathF
        s = self.drive.encode('ascii', 'ignore')
        primerMontaje = list(s)
        for i in [0, 1]:
            primerMontaje.pop()
        montaje = ''.join(primerMontaje)
        print 'Empezando a quemar'
        time.sleep(2)
        os.system("dd bs=1M if=%s of=%s" % (pathF, montaje))
        print 'me esperare 2 segundos'
        time.sleep(2)
        os.system("sync")
        print 'Termine'
        dlg1 = wx.MessageDialog(self, "Imagen Montada Correctamente",
            u"Monti0.3.2b", wx.OK | wx.ICON_INFORMATION | wx.CENTRE,
            pos=wx.DefaultPosition)
        ret = dlg1.ShowModal()
        if ret == wx.ID_OK:
            self.Show()
        print 'Path', pathF
        print 'Montaje', montaje

    def onQuit(self, e):
        dial = wx.MessageDialog(None, 'Realmente quieres salir?', 'Pregunta',
        wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = dial.ShowModal()
        if ret == wx.ID_YES:
            #filelist = glob.glob("*.monti")
            #for f in filelist:
            os.system("rm hd.monti")
            #os.remove(f)
            print "Erase files..."
            self.Destroy()
        else:
            self.Show()

    def meSystem(self):
        os.system("""find /dev/ -name 'sd[b-Z][0-9]' > hd.monti &&
            find /dev/ -name 'mmcblk[0-9]' >> hd.monti""")
        f = open("hd.monti")
        self.drive = []
        for line in f:
            self.drive.append(line)

    def OnAboutBox(self, e):
        op = os.open("data/desc", os.O_RDWR)
        self.f = os.read(op, 280)
        description = self.f
        li = os.open("data/lice", os.O_RDWR)
        self.l = os.read(li, 200)
        licence = self.l
        info = wx.AboutDialogInfo()
        info.SetIcon(wx.Icon('data/logo.png', wx.BITMAP_TYPE_PNG))
        info.SetName('Monti')
        info.SetVersion('0.3.1b')
        info.SetDescription(description)
        info.SetCopyright('Hiram Zúñiga')
        info.SetWebSite('http://hiramzuniga.com')
        info.SetLicence(licence)
        info.AddDeveloper('Hiram Zúñiga')
        info.AddDocWriter('Hiram Zúñiga')
        info.AddArtist('Hiram')
        info.AddTranslator('-')
        wx.AboutBox(info)

    def OnClose(self, event):
        filelist = glob.glob("*.monti")
        for f in filelist:
            os.remove(f)
            print 'Erase files...'
            self.Destroy()
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = Monti()
    app.MainLoop()