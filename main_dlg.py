#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2016-4-15

@author: zWX279959
'''
import os
import wx
import time
import batch
import ver_down
import result_send
import conf_xml
import change_xml
import svn_update
import test_report
import big_data

from apscheduler.scheduler import Scheduler 

app_pa_txt = 'del.txt'

class done_tag():
    output = \
    """
    +------------------------+
    |                        |
    |                        |
    |                        |
    |          ok            |
    |                        |
    |                        |
    |                        |
    +------------------------+
    """

# class MainDlg(wx.Dialog):
#     '''
#     @summary: 
#     '''
#     def __init__(self,parent,title):
#         super(MainDlg,self).__init__(parent,title=title,size=(350,350))
#         self.InitUI()
#         self.Centre()
# #         img = wx.Icon("logo.ico", wx.BITMAP_TYPE_ANY)
# #         if img.IsOk():
# #             self.SetIcon(img)
# #         self.Show()

# import wx.lib.buttons as buttons  
  
class MainDlg(wx.Panel):  
    def __init__(self, parent, id):  
        wx.Panel.__init__(self, parent, id)  
        try:  
            image_file = '.\\logo\\17.jpg'  
            to_bmp_image = wx.Image(image_file, wx.BITMAP_TYPE_ANY).ConvertToBitmap()  
            self.bitmap = wx.StaticBitmap(self, -1, to_bmp_image, (0, 0))  
            image_width = to_bmp_image.GetWidth()  
            image_height = to_bmp_image.GetHeight()  
            set_title = "ISP Auto Factory" 
            parent.SetTitle(set_title)  
        except IOError:  
            print 'Image file %s not found' % image_file  
            raise SystemExit  
         
         
#         self.icon = wx.Icon('fly.ico', wx.BITMAP_TYPE_ICO)
#         self.SetIcon(self.icon)  

        '''-------------------创建布局 --------------------------------'''     
        stext=wx.StaticText(self, -1, "LOADING TYPE:",pos=(0,10))
        font = wx.Font(12, wx.SWISS, wx.ITALIC, wx.BOLD)
        stext.SetFont(font)
        stext.SetBackgroundColour("white")
        stext.SetForegroundColour("Navy")
        
        self.auto_butt= wx.CheckBox(self.bitmap, -1, "AUTO LOAD", (35, 50), (120, 20)) 
        
        self.udp_text = wx.StaticText(self.bitmap,-1,"UDP:",(35,90))
        self.udp_text.SetBackgroundColour("white")
        udp_typeList = ['UDP']  
        self.udp_TypeComboBox = wx.ComboBox(self.bitmap, -1, choices = udp_typeList,pos = (75, 90),  style = wx.CB_READONLY)

#         wx.Choice(self.bitmap, -1, (75, 90), choices=sampleList) 
        
        self.manual_butt = wx.CheckBox(self.bitmap, -1, "MANUL LOAD", (200, 50), (130, 20))
        
        self.ph_text = wx.StaticText(self.bitmap, -1, "PHONE:", (200, 90))  
        self.ph_text .SetBackgroundColour("white")
        self.ph_typeList = ['VENUS','NEMO','BERLIN','VICKY','VICTORIA']
        self.ph_TypeComboBox = wx.ComboBox(self.bitmap, -1, choices = self.ph_typeList, pos = (260, 90),style = wx.CB_READONLY)
#         self.ph_TypeChoice = wx.Choice(self.bitmap, -1, (260, 90), choices=sampleList) 
           
        stext=wx.StaticText(self, -1, "CASE TYPE:",pos=(0,140))
       
        font = wx.Font(12, wx.SWISS, wx.ITALIC, wx.BOLD)
        stext.SetFont(font)
        stext.SetBackgroundColour("white")
        stext.SetForegroundColour("Navy")

        self.bat_rp_butt = wx.CheckBox(self.bitmap, -1, "RPMSG", (35, 180), (60, 20))
        self.bat_gt_butt = wx.CheckBox(self.bitmap, -1, "GTEST", (135, 180), (60, 20))
        self.bat_apk_butt = wx.CheckBox(self.bitmap, -1, "APK", (235, 180), (60, 20))
        
        stext = wx.StaticText(self.bitmap, -1, "VERSION:", (35, 220)) 
        stext.SetBackgroundColour("white")
        ver_typeList = ['V100','V110','V150']
#         wx.Choice(self.bitmap, -1, (102, 220), choices=sampleList) 
        self.ver_TypeComboBox = wx.ComboBox(self.bitmap, -1, choices = ver_typeList,pos = (110, 220) ,style = wx.CB_READONLY)
        
        stext=wx.StaticText(self, -1, "SEND_EMAIL:",pos=(0,270))

        font = wx.Font(12, wx.SWISS, wx.ITALIC, wx.BOLD)
        stext.SetFont(font)
        stext.SetBackgroundColour("white")
        stext.SetForegroundColour("Navy")
        
        
        self.em_butt = wx.CheckBox(self.bitmap, -1, "SEND", (35, 310), (130, 20))
        
        
        stext=wx.StaticText(self, -1, "START NOW:",pos=(0,350))
        font = wx.Font(12, wx.SWISS, wx.ITALIC, wx.BOLD)
        stext.SetFont(font)
        stext.SetBackgroundColour("white")
        stext.SetForegroundColour("Navy")
        
        exec_butt= wx.Button(self.bitmap, -1, label='OK', pos=(35,400)) 
        svn_ch_butt = wx.Button(self.bitmap, -1, label='CHECK OUT', pos=(200,400)) 
        self.Bind(wx.EVT_BUTTON, self.exec_bat, exec_butt)
        self.Bind(wx.EVT_BUTTON, self.ch_svn_stat, svn_ch_butt)
         
        self.Bind(wx.EVT_CHECKBOX, self.auto_load_check_stat, self.auto_butt)
        self.Bind(wx.EVT_CHECKBOX, self.manual_check_stat, self.manual_butt)
        self.Bind(wx.EVT_CHECKBOX, self.batch_rpmsg_check, self.bat_rp_butt)
        self.Bind(wx.EVT_CHECKBOX, self.batch_gtest_check, self.bat_gt_butt)
        self.Bind(wx.EVT_CHECKBOX, self.batch_apk_check, self.bat_apk_butt)
        self.Bind(wx.EVT_CHECKBOX, self.butt_email_check, self.em_butt)
        self.Bind(wx.EVT_COMBOBOX, self.butt_udp_TypeComboBox_check,self.udp_TypeComboBox)
        self.Bind(wx.EVT_COMBOBOX, self.butt_ph_TypeComboBox_check,self.ph_TypeComboBox)
        self.Bind(wx.EVT_COMBOBOX, self.butt_ver_type_TyComboBo_ch, self.ver_TypeComboBox)
        self.Bind(wx.EVT_COMBOBOX, self.butt_ver_type_TyComboBo_ch, self.ver_TypeComboBox)
 
 
        self.udp_TypeComboBox.Enable(False)
        self.ph_TypeComboBox.Enable(False)
# 
    def ch_svn_stat(self,evt):
        '''
        @summary: 
        '''
        print 'clicked'
        svn_update.checkout_svn()
 
    def auto_load_check_stat(self,evt):
        '''
        @summary: 
        '''
        print 'clicked'
        if True == evt.IsChecked():
            self.manual_butt.Enable(False)
            self.ph_TypeComboBox.Enable(True)
            self.udp_TypeComboBox.Enable(True)
 
        elif False == evt.IsChecked():
            self.manual_butt.Enable(True)
            self.udp_TypeComboBox.Enable(False)   
            self.ph_TypeComboBox.Enable(False)   
 
            self.udp_TypeComboBox.Select(-1)
            self.ph_TypeComboBox.Select(-1)
 
        print 'unclicked'
         
 
    def manual_check_stat(self,evt):
        '''
        @summary: 
        '''
        print 'clicked'
        conf_name = 'config.xml'
        cfg_value = conf_xml.get_config(conf_name)
        if True == evt.IsChecked():
            self.manu_load(cfg_value) 
            self.ch_box_en()
        print 'unclicked'        
     
    def download_ver_check_stat(self,evt):
        '''
        @summary: 
        '''
        print "cliked"
        if evt.IsChecked() == True:
            print evt.IsChecked()  
        elif evt.IsChecked() == False:
            print "uncliked"
            print evt.IsChecked()     
     
    def change_type(self,get_node_val,type_val,rea_xml):
        '''
        @summary: 
        '''
        change_xml.change_node_text(get_node_val, type_val)
        change_xml.write_xml(rea_xml, "./config.xml")         
     
    def butt_ver_type_TyComboBo_ch(self,evt):
        '''
        @summary: 
        '''
        ver_idx = self.ver_TypeComboBox.GetSelection()
        ver_val = self.ver_TypeComboBox.GetValue()
        print ver_idx
        print ver_val
        tree = change_xml.read_xml("config.xml")
        text_nodes = change_xml.get_node_by_keyvalue(change_xml.find_nodes(tree, "version_name"))
        if None != ver_val:
            self.change_type(text_nodes, ver_val, tree)
         
    def butt_udp_TypeComboBox_check(self,evt):
        '''
        @summary: 
        '''
        type_idx = self.udp_TypeComboBox.GetSelection()
        udp_type_val = self.udp_TypeComboBox.GetValue()
        print type_idx
        print udp_type_val
        if '' != udp_type_val:
            self.ph_TypeComboBox.Enable(False)
        tree = change_xml.read_xml("config.xml")
        text_nodes = change_xml.get_node_by_keyvalue(change_xml.find_nodes(tree, "download_type"))
        if 'UDP' == udp_type_val:
            self.change_type(text_nodes,udp_type_val,tree)
 
 
    def butt_ph_TypeComboBox_check(self,evt):
        '''
        @summary: 
        '''
        ph_type_idx = self.ph_TypeComboBox.GetSelection()
        ph_type_val = self.ph_TypeComboBox.GetValue()
        print ph_type_idx
        print ph_type_val
        if '' != ph_type_val:
            self.udp_TypeComboBox.Enable(False)
        tree = change_xml.read_xml("config.xml")
        text_nodes = change_xml.get_node_by_keyvalue(change_xml.find_nodes(tree, "download_type"))
        if ph_type_val in self.ph_typeList:
            self.change_type(text_nodes,ph_type_val,tree)
            
#         if 'VENUS' == ph_type_val:  
#             self.change_type(text_nodes,ph_type_val,tree)
#         elif 'NEMO' == ph_type_val:
#             self.change_type(text_nodes,ph_type_val,tree)
#         elif 'EVA' == ph_type_val:
#             self.change_type(text_nodes,ph_type_val,tree)            
#         elif 'BERLIN' == ph_type_val:
#             self.change_type(text_nodes,ph_type_val,tree)   
#         elif 'KNIGHT' == ph_type_val:
#             self.change_type(text_nodes,ph_type_val,tree)
#         elif 'VICKY' == ph_type_val:
#             self.change_type(text_nodes,ph_type_val,tree)
#         elif 'VICTORIA' == ph_type_val:
#             self.change_type(text_nodes,ph_type_val,tree)
    
    def chang_xml(self,bat_type):
        '''
        @summary: 
        '''
        tree = change_xml.read_xml("config.xml")

        text_nodes = change_xml.get_node_by_keyvalue(change_xml.find_nodes(tree, "exec_file"))
        change_xml.change_node_text(text_nodes, bat_type)
        change_xml.write_xml(tree, "./config.xml")
            
    def batch_rpmsg_check(self,evt):
        '''
        @summary: 
        '''
        rpmsg = 'RPMSG'
        if evt.IsChecked() == True:
            print 'cliked'
            self.chang_xml(rpmsg)
            
        elif evt.IsChecked() == False:
            print 'unclicked'
            
    def batch_gtest_check(self,evt):
        '''
        @summary: 
        '''
        gtest = 'GTEST'
        if evt.IsChecked() == True:
            print 'cliked'
            self.chang_xml(gtest)
            
        elif evt.IsChecked() == False:
            print 'unclicked'
            
    def batch_apk_check(self,evt):
        '''
        @summary: 
        '''
        apk = 'APK'
        if evt.IsChecked() == True:
            print 'cliked'
            self.chang_xml(apk)
            
        elif evt.IsChecked() == False:
            print 'unclicked'        
            
    def butt_email_check(self,evt):
        '''
        @summary: 
        '''
        if evt.IsChecked() == True:
            print 'cliked'
        elif evt.IsChecked() == False:
            print 'unclicked'
    
    def auto_load(self,cfg_value):
        '''
        @summary: 
        '''
 
        ver_down.ver_function(cfg_value)
 
    def manu_load(self,cfg_value):
        '''
        @summary: 
        '''
        ver_down.open_url(cfg_value)
        self.manual_butt.SetValue(0)
 
    def ch_box_en(self):
        '''
        @summary: 
        '''
        self.udp_TypeComboBox.Enable(False) 
        self.ph_TypeComboBox.Enable(False)  
        self.auto_butt.Enable(True)
        self.manual_butt.Enable(True) 
 
        self.udp_TypeComboBox.Select(-1)
        self.ph_TypeComboBox.Select(-1)            
 
    def exec_bat(self,evt):
        '''
        @summary: 
        '''
 
        at_bt_stat = self.auto_butt.Get3StateValue()
#         mn_bt_stat = self.manual_butt.Get3StateValue()
 
        rp_bt_stat = self.bat_rp_butt.GetValue()
        gt_bt_stat = self.bat_gt_butt.GetValue()
        apk_bt_stat = self.bat_apk_butt.GetValue()
        
        em_bt_stat = self.em_butt.GetValue()

        udp_type_val = self.udp_TypeComboBox.GetValue()
        ph_type_val = self.ph_TypeComboBox.GetValue()         
         
        schedudler = Scheduler(daemonic = False)
        @schedudler.cron_schedule(second='*', day_of_week='1-5', hour='8-24') 
        def quote_send_sh_job(): 
            batch.batch_function(cfg_value,at_bt_stat)
        print 'udp_type_val:[%s]'%udp_type_val
        print 'ph_type_val:[%s]'%ph_type_val      
      
        if (0 == rp_bt_stat)and(0 == gt_bt_stat)and(0 == apk_bt_stat)and(0 == em_bt_stat)and(0 == at_bt_stat):
 
            wx.MessageBox(u'请选择配置项')
            return
 
        if '' == udp_type_val and '' == ph_type_val and 1 == at_bt_stat:
 
            wx.MessageBox(u'请在下拉菜单中选择下载型号')
            return

        if '' != udp_type_val and '' != ph_type_val and 1 == at_bt_stat:

            wx.MessageBox(u'只能选择一个下拉菜单选项')
            self.udp_TypeComboBox.Select(-1)
            self.ph_TypeComboBox.Select(-1)
            return            

        if (1 == rp_bt_stat)and(1 == gt_bt_stat)and(1 == apk_bt_stat):
            wx.MessageBox(u'CASE_TYPE不能同时选择两项')      
            return    
#         os.system("TASKKILL /F /IM adb.exe /T")
        path = batch.work_path()
        batch.get_endwith_type_fi(path, 'txt', app_pa_txt)
        batch.del_any_type_fi(path,'txt',app_pa_txt)
        print '--------------auto fact--------------------'
        conf_name = 'config.xml'
        cfg_value = conf_xml.get_config(conf_name)
#         time.sleep(5)
 
        count=0
        while(count<3):
            hw = ver_down.hw_info()
            print 'hw_info'
            if -1 == hw.find('hi'):
                continue
            count += 1
 
        if -1 != hw.find('not'): 
            wx.MessageBox('please check your device')
            return
         
        if 1 == at_bt_stat:
            if  '' != udp_type_val or '' != ph_type_val:
                os.system('adb wait-for-device')
                self.auto_load(cfg_value)
                if 1 == rp_bt_stat or 1 == gt_bt_stat or 1 == apk_bt_stat:
                    os.system('adb wait-for-device')
                    time.sleep(60)
                    batch.batch_function(cfg_value,at_bt_stat)
                    test_report.report(cfg_value,at_bt_stat)
                    if 1 == em_bt_stat:      
                        result_send.mail_main(cfg_value)
                        big_data.copy_to_fi(cfg_value)
                        batch.work_path()
                        if os.path.exists('collectcsv.exe'):
                            time.sleep(3)
                            os.system('collectcsv.exe')
                print done_tag.output
 
        print '--------------auto fact done---------------'
 
        print '----------------manu exec--------------------'
        if 0 == at_bt_stat:
            if (1 == rp_bt_stat)or(1 == gt_bt_stat)or(1 == apk_bt_stat):
                os.system('adb wait-for-device')
                batch.batch_function(cfg_value,at_bt_stat)
                test_report.report(cfg_value,at_bt_stat)
#                 schedudler.start()
                self.bat_gt_butt.SetValue(0)
                self.bat_rp_butt.SetValue(0)
                self.bat_apk_butt.SetValue(0)
            if 1 == em_bt_stat:
                print 'cilck evt mail'
                result_send.mail_main(cfg_value)
                self.em_butt.SetValue(0)
                big_data.copy_to_fi(cfg_value)
                batch.work_path()
                if os.path.exists('collectcsv.exe'):
                    time.sleep(3)
                    os.system('collectcsv.exe')
            print done_tag.output
        batch.work_path()
 
 
        print '----------------manu exec done--------------------'
         
