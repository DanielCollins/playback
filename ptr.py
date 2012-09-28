#!/usr/bin/env python

import wx
import cv2.cv as cv

class WebcamPlayback(wx.Panel):

    TIMER_PLAY_ID = 101

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.parent = parent

        self.capture = cv.CaptureFromCAM(0)
        frame = cv.QueryFrame(self.capture)

        self.SetSize((frame.width, frame.height))

        self.Bind(wx.EVT_PAINT, self.onPaint)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.frame_timer = wx.Timer(self, self.TIMER_PLAY_ID)
        wx.EVT_TIMER(self, self.TIMER_PLAY_ID, self.onNextFrame)
        self.frame_timer.Start(25)
        self.SetBackgroundColour(wx.BLUE)
        self.Show(True)

    def onPaint(self, evt):
        frame = cv.QueryFrame(self.capture)
        if frame:
            cv.CvtColor(frame, frame, cv.CV_BGR2RGB)
            img = wx.EmptyImage(frame.width , frame.height)
            img.SetData(frame.tostring())
            bmp = wx.BitmapFromImage(img)
            wx.BufferedPaintDC(self, bmp)

    def OnSize(self, event):
        self.Refresh()

    def onNextFrame(self, evt):
        self.Refresh()
        evt.Skip()

class MainWindow(wx.Frame):

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL, )
        wp = WebcamPlayback(self, -1)
        wp.SetSizer(vbox)
        self.Centre()
        self.Show(True)

if __name__=="__main__":
    app = wx.App()
    app.SetTopWindow(MainWindow(None, -1, 'ptr'))
    app.RestoreStdio()
    app.MainLoop()

