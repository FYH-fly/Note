#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2016-4-1

@author: zWX279959
'''
import os
import re
import time
import sys
import wx
import shutil
import conf_xml
import ver_down
import datetime
import svn_update
from apscheduler.scheduler import Scheduler 
import xml.dom.minidom
import subprocess
import copy
cmd_1 = 'start A7.xsh'
cmd_2 = 'start AP.xsh'

rpmsg = 'RPMSG'
gtest = 'GTEST'
apk   = 'APK'
move_txt = 'move.txt'
gt_cmd = 'gt_cmd.txt'
kill_adb_cmd = "TASKKILL /F /IM adb.exe /T"

fastboot_cmd = 'fastboot reboot'
wait_dev_cmd = 'adb wait-for-device'
adb_pull_pass_cmd = 'adb pull /data/Rpmsg_Result_PASS.txt'
adb_pull_fail_cmd = 'adb pull /data/Rpmsg_Result_FAIL.txt' 
adb_rm_pass_cmd = 'adb shell rm -rf /data/Rpmsg_Result_PASS.txt'
adb_rm_fail_cmd = 'adb shell rm -rf /data/Rpmsg_Result_FAIL.txt'

adb_pull_android_log = 'adb pull /data/log/android_logs'
adb_pull_isp_log = 'adb pull /data/log/isp-log'
adb_rm_android_log = 'adb shell rm -rf /data/log/android_logs'
adb_rm_isp_log = 'adb shell rm -rf /data/log/isp-log'

gt_resu_path = 'D:\\Auto_Project\\gtest\\'
apk_resul_path = 'D:\\Auto_Project\\apk\\result\\'
# tomorrow_cmp_time = int(time.strftime("%m%d",time.localtime(time.time())))+1
# today_cmp_time = int(time.strftime("%m%d",time.localtime(time.time())))
class bat_txt(object):
    '''
    @summary: 
    '''
    name      = 'name.txt'
    dirs      = 'dirs.txt'
    re_dirs   = 're_dirs.txt'
    exec_file = 'exec_file.txt'
    cfg_xml   = 'config.xml'    
    
class mail_txt(object):
    '''
    @summary: 
    '''
    rp_sce   = 'Rpmsg_TestScene.txt'
    rp_tes   = 'Rpmsg_TestCase.txt'
    rp_resul = 'Rpmsg_Result.txt'
    gt_sce   = 'Gtest_TestScene.txt'
    gt_tes   = 'Gtest_TestCase.txt'
    apk_sce  = 'Apk_TestScene.txt'
    apk_tes  = 'Apk_TestCase.txt'
    
    gt_resul_pass = 'Gtest_Result_PASS.txt'
    gt_resul_fail = 'Gtest_Result_FAIL.txt'
    rp_resul_pass = 'Rpmsg_Result_PASS.txt'
    rp_resul_fail = 'Rpmsg_Result_FAIL.txt'
    apk_resul_pass = 'Apk_Result_PASS.txt'
    apk_resul_fail = 'Apk_Result_FAIL.txt'
    
    rp_star_tim =  'Rpmsg_StartTime.txt'
    rp_end_tim  = 'Rpmsg_EndTime.txt'
    gt_star_tim =  'Gtest_StartTime.txt'
    gt_end_tim  = 'Gtest_EndTime.txt'
    apk_star_tim = 'Apk_StartTime.txt'
    apk_end_tim = 'Apk_EndTime.txt'
#     gt_total_tim = 'Gtest_Total_Time.txt'
#     rp_total_tim = 'Rpmsg_Total_Time.txt'
        
    
def dict_list():
    
    main_work_path = os.getcwd()
    cp_path_dict = {"hi3650":("Austin", main_work_path + '\\Automation_Result\\Austin\\Result_TXT\\' +'Austin_'),\
                    "hi6250":("Dallas", main_work_path + '\\Automation_Result\\Dallas\\Result_TXT\\' +'Dallas_'),\
                    "hi3660":("Chicago",main_work_path + '\\Automation_Result\\Chicago\\Result_TXT\\'+'Chicago_')}
    return cp_path_dict
    
    
def creat_object(cfg_value):
    '''
    @summary: Create project files
    '''
    disk = 'D:\\'
    at_folder = 'Auto_Project'
    sav_pic = 'save_picture'
    rp_folder = 'rpmsg'
    gt_folder = 'gtest'
    os.chdir(disk)
    exists_(at_folder)
    exists_(disk+at_folder+'\\'+sav_pic)
    exists_(cfg_value.Disk)
    exists_(cfg_value.rp_picture_save_path)
    exists_(cfg_value.gt_picture_save_path)
    exists_(disk+at_folder+'\\'+rp_folder)
    exists_(disk+at_folder+'\\'+gt_folder)
    
def work_path():
    '''
    @summary: Get the current working path
    '''
    ABS_PATH = os.path.abspath(sys.argv[0])
    ABS_PATH = os.path.dirname(ABS_PATH)
    os.chdir(ABS_PATH)    
    return ABS_PATH
    
def get_filesname(cfg_value,text_mode):
    '''
    @summary:
    1.Get the path to the test case folder in the config.xml
    2.Gets the contents of the subfolder and writes it to the dir.txt
    '''
    print '---------------get_filesname---------------'
    work_path()
    
    if rpmsg == text_mode:
        ABSPATH = cfg_value.rpmsg_file_path + '\\' + cfg_value.version_name + '\\' + cfg_value.rp_file_name[fi_node_nu]
    elif gtest == text_mode:
        ABSPATH = conf_xml.get_str(cfg_value,10) 
    elif apk == text_mode:
        ABSPATH = conf_xml.get_str(cfg_value,9) 

    try:
        aaa = os.listdir(ABSPATH)
    except WindowsError:
        wx.MessageBox(u"请检查配置文件中file_name节点中内容是否在version下拉框所选中的文件路径下")
        return
    with open(bat_txt.dirs,'w') as dirs_w_fd:
        dirs_w_fd.write(str(aaa))

    print '------------get_filesname  end---------------'

    
def re_dirs_file(cfg_value):
    '''
    @summary: 
    1.Filter invalid files in dirs.txt(config and bin)
    2.Write the subfolder name to re_dirs.txt(eg:'D_Cam02_058_ResolutionTiny')
    '''
    print '------------re_dirs_file-----------------'
    work_path()
    with open(bat_txt.dirs,'r') as dirs_r_fd:
        dirs_content = dirs_r_fd.read()
    with open(bat_txt.re_dirs,"w") as re_dirs_w_fd:
        dirs_content = eval(dirs_content)
        for name in dirs_content:
            if 'bin' != name and 'config' != name: 
                re_dirs_w_fd.write(name+'\n')
    print '------------re_dirs_file end-----------------'


def copy_file(cfg_value,camera,text_mode):
    '''
    @summary: Rename the re_dirs.txt file to version name + Rpmsg/Gtest_TestScene.txt 
    '''
    work_path()
#     for i in range(3):
#         hw = ver_down.get_hardware()
    with open('hw_info.txt','r') as fp:
        hw = fp.read()
    cp_path_dict = dict_list()
    
    if hw not in cp_path_dict:
        print 'cp_path_dict not found hardware'
        hw = ver_down.get_hardware()
        
    hw_na, path = cp_path_dict[hw]
    
    if rpmsg == text_mode:
        if 0 == camera:
            shutil.copyfile(bat_txt.re_dirs,path + mail_txt.rp_sce)
        else:
            with open(path+mail_txt.rp_sce,'a') as h:
                with open(bat_txt.re_dirs,'r') as s:
                    h.write(s.read())
                    
    if gtest == text_mode:
        shutil.copyfile(bat_txt.re_dirs,path + mail_txt.gt_sce)
    
    if apk == text_mode:
        shutil.copyfile(bat_txt.re_dirs,path + mail_txt.apk_sce)
    work_path()
    
# def get_ext_name(filename):
#     '''
#     @summary: get file extend name
#     @param filename: target filename
#     @return: if success return extend name of file with point(e.g) '.doc'\
#     else return None
#     '''
#     ext = ""
#     if type(filename) != str:
#         return ext
#     fn_ext = os.path.splitext(filename)
#     return fn_ext[1]
    
def bat_exec(cfg_value,text_mode):
    '''
    @summary: Execute all the test cases in a use-case folder
    '''
    print '------------------bat_exec---------------------'
    work_path()
    global xml_exec_file_flag
    xml_exec_file_flag = text_mode
    with open(bat_txt.re_dirs,'r') as re_dirs_r_fd:
        re_dirs_content = re_dirs_r_fd.readlines()
    print re_dirs_content
#     star_log = time.time()
    for idx in range(0,len(re_dirs_content),1):
        dirs_file = re_dirs_content[idx][:-1]
        print 'dirs_file is:[%s]'%(dirs_file)
        
        if rpmsg == text_mode:
            ABSPATH = cfg_value.rpmsg_file_path + '\\' + cfg_value.version_name + '\\' + cfg_value.rp_file_name[fi_node_nu]
        elif gtest == text_mode:
            ABSPATH = conf_xml.get_str(cfg_value,10) 
        elif apk == text_mode:
            ABSPATH = conf_xml.get_str(cfg_value,9)
            
        ABSPATH = ABSPATH +'\\' + dirs_file
        print '[%s]' %ABSPATH
        bat_list = os.listdir(ABSPATH)
        bat_list = str(bat_list)
        with open(bat_txt.exec_file,'w') as fp:
            fp.write(bat_list)
            
            
            
        print '----------------------------'
        print 'listdir[%s]'%bat_list
        print '----------------------------'
        
        with open(bat_txt.exec_file,'r') as exec_file_r_fd:
            exec_file_content = exec_file_r_fd.read()
            
        with open(bat_txt.name,"w") as bat_name_w_fd:
            exec_file_content = eval(exec_file_content)
            for name in exec_file_content:
                if not name.endswith(('.bat','.py')):
                    print name
                    print 'no .bat or no .py'
                    continue
                print name
                bat_name_w_fd.write(name+'\n')
                
        with open(bat_txt.name,'r') as bat_name_r_fd:
            bat_name_content = bat_name_r_fd.readlines()
        
#         os.chdir(ABSPATH)
        print '---------------------'
        print bat_name_content
        print '---------------------'
        log_folder_na = get_date()
        file_result = log(cfg_value,text_mode)
        schedudler = Scheduler(daemonic = False)
        schedudler.add_interval_job(job,seconds=20, start_date=datetime.datetime.now()+datetime.timedelta(seconds=1))
        schedudler.start()
        for idx in range(0,len(bat_name_content),1):
              
#             if int(time.strftime("%m%d%H%M",time.localtime(time.time())))  >= int(str(cmp_time)+time_up.split(':')[0]+time_up.split(':')[1]):
#                 print '''
#                        #############################
#                        #time up and function return#
#                        #############################
#                       '''
#                 schedudler.shutdown(True)
#                 return
#             now_log = time.time()
#             if int(now_log)-int(star_log)>3600:
#                 os.system('android_logs_all.bat')
#                 star_log = now_log-1
            print 'bat or py:[%s]'%(bat_name_content[idx][:-1])
            bat_fi = bat_name_content[idx][:-1]
            PATH = os.path.abspath(sys.argv[0])
            PATH = os.path.dirname(PATH)
            bat_na = PATH + '\\' + file_result + '\\' + log_folder_na + '\\' + bat_fi.split('.')[0]
            cmd_log = PATH + '\\' + file_result + '\\' + log_folder_na + '\\' + bat_fi.split('.')[0] + '\\' + 'cmd.txt'
            print 'bat_path:[%s]'%bat_na            
            if False == os.path.exists(bat_na):
                os.mkdir(bat_na)                           
            print 'bat_fi :[%s]'%bat_fi
            print 'cmd_log :[%s]'%cmd_log
#             exec_bat = 'echo.|call ' + bat_fi + '>' + cmd_log
            exec_bat = ABSPATH+'\\'+bat_fi
            bat_adb_pull_android_log = adb_pull_android_log+ ' ' + bat_na
            bat_adb_pull_isp_log = adb_pull_isp_log+ ' '+bat_na
            
            print 'exec_bat_cmd [%s]'%exec_bat
            
#             star_tim_str=str(time.time()) 
#             star_tim= star_tim_str.split(".")[0]
            
            get_start_t = get_bigdata_time()
            print 'start_time:[%s]'%get_start_t  
            
            work_path()   
            if rpmsg == text_mode:
                sta_data = open(mail_txt.rp_star_tim,'a')
            elif gtest == text_mode:
                sta_data = open(mail_txt.gt_star_tim,'a')
            elif apk == text_mode:
                sta_data = open(mail_txt.apk_star_tim,'a')
            sta_data.write(get_start_t + '\n') 
            sta_data.close()
            
            os.chdir(ABSPATH)
            global nowtime
            nowtime_str=str(time.time())
            nowtime= nowtime_str.split(".")[0]
            
            
            hw = ver_down.get_hardware()
            print 'hardware:'
            print hw
            count = 1
            if '' == hw:
                while True:
                    hw = ver_down.get_hardware()
                    print 'hardware:[%s]'%hw
                    if '' == hw or -1 == hw.find('hi'):
                        print '------[hardware_info not found]------'
                        print 'try to connect....'
                        count = count + 1
                        if count > 10:
                            print "adb reboot ing..."
                            os.system('adb kill-server')
                            os.system('adb start-server')
                            time.sleep(4)
                        time.sleep(1)
                    else:
                        print 'connect success hw_info is [%s]'%hw
                        break
            print '**********'
            print 'work_path is %s'%ABSPATH  
            print '**********'
            os.system(adb_rm_android_log)
            print 'adb_rm_android_log'
            os.system(adb_rm_isp_log)
            print 'adb_rm_isp_log'
#             os.system('echo.|call 'ABSPATH+'\\'+exec_bat)

            if bat_fi.endswith('.py'):
                execfile(exec_bat)
            else:
                exec_bat = 'echo.|call ' + bat_fi + '>' + cmd_log
                os.system(exec_bat)
            print exec_bat
            os.system(bat_adb_pull_android_log)
            print 'bat_adb_pull_android_log'
            os.system(bat_adb_pull_isp_log)
            print 'bat_adb_pull_isp_log'
            work_path()
            
#             end_tim_str=str(time.time())
#             end_tim=end_tim_str.split(".")[0]
            
            get_end_t = get_bigdata_time()  
            print 'end_time:[%s]'%get_end_t
            
            if rpmsg == text_mode:
                end_data = open(mail_txt.rp_end_tim,'a')
            elif gtest == text_mode:
                end_data = open(mail_txt.gt_end_tim,'a')
            elif apk == text_mode:
                end_data = open(mail_txt.apk_end_tim,'a')
            end_data.write(get_end_t+'\n')
            end_data.close()      
            if rpmsg == text_mode:
                fp = open(mail_txt.rp_tes,'a')
            elif gtest == text_mode:
                fp = open(mail_txt.gt_tes,'a')
            elif apk == text_mode:
                fp = open(mail_txt.apk_tes,'a')
                
            fp.write(bat_fi.split('.')[0]+'\n')
            fp.close()
            
        schedudler.shutdown(True)
        
    print '------------------bat_exec end---------------------'
    
def job():
    '''
    @summary: 
    '''
    print "============jobrun==================="
    str_eachtime=str(time.time())
    eachtime=str_eachtime.split(".")[0]
#     cfg_value = conf_xml.conf()
    
    print 'eachtime:%s'%eachtime
    print 'nowtime:%s'%nowtime
    print 'usetime:%s'%(int(eachtime)-int(nowtime))
    print 'rp:%s'%rpmsg
    print 'xml_exec_file_flag:%s'%xml_exec_file_flag
    if rpmsg == xml_exec_file_flag and ((int(eachtime)-int(nowtime))>250):
        print '[RPMSG]:kill_adb_cmd'
        os.system(kill_adb_cmd)
        os.system('power_down.bat')
    elif gtest == xml_exec_file_flag and ((int(eachtime)-int(nowtime))>354):
        print '[GTEST]:kill_adb_cmd'
        os.system(kill_adb_cmd)
    return 
    
def move_test(cfg_value,text_mode):
    '''
    @summary: Copy the two test results files to the version of the Automation_Restult folder
    '''
    print '-------------------move_test_file-----------------'
    work_path()
    with open('hw_info.txt','r') as fp:
        hw = fp.read()
    
#     main_work_path = os.getcwd()
    os.system(kill_adb_cmd)
    cp_path_dict = dict_list()
    if hw not in cp_path_dict:
        print 'not found'
    hw_na, path = cp_path_dict[hw]
    gt_resul_pass_src = gt_resu_path + cfg_value.version_name + '\\' + mail_txt.gt_resul_pass
    gt_resul_fail_src = gt_resu_path + cfg_value.version_name + '\\' + mail_txt.gt_resul_fail
    rp_pass = path[:-(len(hw_na)+1)]+mail_txt.rp_resul_pass
    rp_fail = path[:-(len(hw_na)+1)]+mail_txt.rp_resul_fail
    apk_resul_pass_src = apk_resul_path + mail_txt.apk_resul_pass
    apk_resul_fail_src = apk_resul_path + mail_txt.apk_resul_fail
    
    
    
    if rpmsg == text_mode:
        if os.path.exists(mail_txt.rp_star_tim and mail_txt.rp_end_tim):
            shutil.move(mail_txt.rp_star_tim,path+mail_txt.rp_star_tim)
            shutil.move(mail_txt.rp_end_tim,path+mail_txt.rp_end_tim)
        if os.path.exists(mail_txt.rp_tes):
            shutil.move(mail_txt.rp_tes,path+mail_txt.rp_tes)
            os.system(adb_pull_pass_cmd+' '+ rp_pass)
            os.system(adb_pull_fail_cmd+' '+ rp_fail)  
            
            while True:          
                print 'check pass/fail file'
                if os.path.exists(rp_pass) and os.path.exists(rp_fail):    
                    if os.path.getsize(rp_pass)==0 and os.path.getsize(rp_fail)==0:
                        print 'check pass/fail file getsize == 0'
                        os.system(adb_pull_pass_cmd+' '+ rp_pass)
                        os.system(adb_pull_fail_cmd+' '+ rp_fail)
                        time.sleep(3)
                    else:
                        break
                else:
                    os.system(adb_pull_pass_cmd+' '+ rp_pass)
                    os.system(adb_pull_fail_cmd+' '+ rp_fail)
                    
                    
    if gtest == text_mode:
        if os.path.exists(mail_txt.gt_star_tim) and os.path.exists(mail_txt.gt_end_tim):
            shutil.move(mail_txt.gt_star_tim,path+mail_txt.gt_star_tim)
            shutil.move(mail_txt.gt_end_tim,path+mail_txt.gt_end_tim)
        if os.path.exists(gt_resul_pass_src):
            shutil.move(gt_resul_pass_src,path[:-(len(hw_na)+1)]+mail_txt.gt_resul_pass)
        if os.path.exists(gt_resul_fail_src):
            shutil.move(gt_resul_fail_src,path[:-(len(hw_na)+1)]+mail_txt.gt_resul_fail)
        if os.path.exists(mail_txt.gt_tes):
            shutil.move(mail_txt.gt_tes,path + mail_txt.gt_tes)
            
    if apk == text_mode:
        if os.path.exists(mail_txt.apk_tes):
            shutil.move(mail_txt.apk_tes,path + mail_txt.apk_tes)
        if os.path.exists(mail_txt.apk_sce):
            shutil.move(mail_txt.apk_sce,path + mail_txt.apk_sce)
        if os.path.exists(apk_resul_pass_src):
            shutil.move(apk_resul_pass_src,path[:-(len(hw_na)+1)]+mail_txt.apk_resul_pass)
        if os.path.exists(apk_resul_fail_src):
            shutil.move(apk_resul_fail_src,path[:-(len(hw_na)+1)]+mail_txt.apk_resul_fail)
            
            
#     if apk == text_mode:
#         if os.path.exists(mail_txt.apk_star_tim) and os.path.exists(mail_txt.apk_star_tim):
#             shutil.move(mail_txt.apk_star_tim, path+mail_txt.apk_star_tim)
#             shutil.move(mail_txt.apk_star_tim, path+mail_txt.apk_star_tim)
            
    work_path() 
    print '-------------------move_test_file end-----------------'            
    
    
def get_new_dir(f_list):
    '''
    @summary:
    '''
    print '-------------------get_new_dir-------------------'
    for f_name in f_list[::-1]:
        if os.path.isfile(f_name):
            continue
        return f_name
    print '-------------------get_new_dir end-------------------'
    
def get_endwith_type_fi(fi_path,fi_type,save_fi):
        os.chdir(fi_path)
        h = open(save_fi,'a')
        dirnames = [name for name in os.listdir(fi_path)
            if name.endswith(fi_type)]
        aa = len(dirnames)
        print dirnames
        print aa
        
        for i in range(0,len(dirnames),1):
            tt = dirnames[i]
            h.write(tt+'\n')
        h.close()
        
        b = open(save_fi,'r')
        c = b.readlines()
        b.close()
        print 'save_fi is :[%s]'%c
        for nu in range(0,len(c),1):
            re_move_file = c[nu][:-1]
            print 're_move_file is [%s]'%re_move_file
   
def del_any_type_fi(fi_path,fi_type,data_fi):
    h = open(data_fi,'r')
    aa = h.readlines()
    h.close()    
    print aa
    for i in range(0,len(aa),1):
        bb = aa[i][:-1]
        cc = fi_path+'\\'+bb
        if os.path.exists(cc):
            if '' == fi_type:
                if '' == os.path.splitext(bb)[1][1:]:
                    shutil.rmtree(bb)
                    os.remove(data_fi)
            else:
                os.remove(bb) 
                
def exists_(file_t):
    '''
    @summary: 
    '''
    if True != os.path.exists(file_t):
        os.mkdir(file_t)

def pic_save(pic_type):
    '''
    @summary: 
    '''
    with open(ver_down.ver_nu,'r') as fp:
        v_num = fp.readline()
    save_folder = pic_type +'\\'+ str(v_num)
    exists_(save_folder)
    return save_folder
    
def move_next(cfg_value,dw_stat,text_mode):
    '''
    @summary: 
    '''
    print '------------------move_folder----------------'
    work_path() 
    
    pic_time = get_pic_file_time()
    with open(bat_txt.re_dirs,'r') as fp:
        subfolders= fp.readlines()
    print subfolders
    
    if 1 == dw_stat:
        if rpmsg == text_mode:
            pic_folder = pic_save(cfg_value.rp_picture_save_path)
        elif gtest == text_mode:
            pic_folder = pic_save(cfg_value.gt_picture_save_path)
            
    if 0 == dw_stat:
        if rpmsg == text_mode:
            pic_folder = cfg_value.rp_picture_save_path +'\\'+ str(pic_time)
            exists_(pic_folder)
        elif gtest == text_mode and 0 == dw_stat:
            pic_folder = cfg_value.gt_picture_save_path +'\\'+ str(pic_time)
            exists_(pic_folder)
            
    for idx in range(0,len(subfolders),1):
        dirs_file = subfolders[idx][:-1]
        print 'dirs_file is:[%s]'%(dirs_file)
            
        if rpmsg == text_mode:
            ABSPATH = cfg_value.rpmsg_file_path + '\\' + cfg_value.version_name + '\\' + cfg_value.rp_file_name[fi_node_nu]
        elif gtest == text_mode:
            ABSPATH = conf_xml.get_str(cfg_value,10) 
        elif apk == text_mode:
            ABSPATH = conf_xml.get_str(cfg_value,9) 
            
        ABSPATH = ABSPATH +'\\' + dirs_file
        os.chdir(ABSPATH)
        hp = open(move_txt,'a')
        dirnames = [name for name in os.listdir(ABSPATH)
            if name.endswith('')]
        len_dirnames = len(dirnames)
        print dirnames
        print len_dirnames
        
        for i in range(0,len_dirnames,1):
            pic_dir = dirnames[i]
            matchobject = re.match(r'^(\w+).*?(\d+)$',str(pic_dir))
            if matchobject:
                print "match:" + matchobject.group(0)
                hp.write(matchobject.group(0)+'\n')
        hp.close()
        
        with open(move_txt,'r') as move_fp:
            move_content = move_fp.readlines()
#         move_fp = open(move_txt,'r')
#         c = move_fp.readlines()
#         move_fp.close()
        print 'move_txt is :[%s]'%move_content
        
        for nu in range(0,len(move_content),1):
            re_move_file = move_content[nu][:-1]
            print 're_move_file is [%s]'%re_move_file
            try:
                shutil.move(re_move_file, pic_folder)
            except Exception,e:
                print 'shutil.move: '+str(e)
                
        os.remove(move_txt)
        
        if gtest == text_mode:
            hp = open(gt_cmd,'a')
            dirnames = [name for name in os.listdir(ABSPATH)
                 if name.endswith('txt')]
            len_dirnames = len(dirnames)
            print '------------------------------'
            print 'dirnames is [%s]'%dirnames
            print 'len_dirnames is [%s]'%len_dirnames
            print '------------------------------'
            
            for i in range(0,len_dirnames,1):
                pic_dir = dirnames[i]
                matchobject = re.match(r'^(\w+).*?(\w+)$',str(pic_dir))
                if matchobject:
                    print "match:" + matchobject.group(0)
                    if matchobject.group(0) != 'gt_cmd.txt':
                        hp.write(matchobject.group(0)+'\n')
            hp.close()
            
            with open(gt_cmd,'r') as gtcmd_fp:
                gtcmd_content = gtcmd_fp.readlines()
#             b = open(gt_cmd,'r')
#             c = b.readlines()
#             b.close()
            print 'gt_cmd is :[%s]'%gtcmd_content
            
            for nu in range(0,len(gtcmd_content),1):
                re_move_file = gtcmd_content[nu][:-1]
                print 're_move_file is [%s]'%re_move_file
                if not os.path.exists(pic_folder):
                    shutil.move(re_move_file, pic_folder)
            os.remove(gt_cmd)
            
def get_date():
    '''
    @summary: 
    '''
    return time.strftime("%Y_%m_%d",time.localtime(time.time()))
    
def get_pic_file_time():
    '''
    @summary: 
    '''
    return time.strftime("%Y_%m_%d_%H_%M",time.localtime(time.time()))    
    
def get_bigdata_time():
    '''
    @summary: 
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    
def log(cfg_value,text_mode):
    '''
    @summary: create a test results folder
    '''
    print '---------------log----------------------'
    log_folder_na = get_date()    
    PATH = os.path.abspath(sys.argv[0])
    PATH = os.path.dirname(PATH)
    if rpmsg == text_mode:
        result_path = PATH + '\\' +'rpmsg_result'
        file_result = rpmsg + '_result'
    elif gtest == text_mode:
        result_path = PATH + '\\' +'gtest_result'      
        file_result = gtest + '_result'  
    elif apk == text_mode:
        result_path = PATH + '\\' + 'apk_result'
        file_result = apk + '_result'
    ABSPATH = result_path + '\\' + log_folder_na
    exists_(result_path)
    print 'log_ABSPATH:[%s]'%ABSPATH
    exists_(ABSPATH)
    print '---------------log end----------------------'
    return file_result
    
def start_shell():
    '''
    @summary: 
    '''
    print '------------start_shell--------------------'
    os.system(cmd_1)
    os.system(cmd_2)
    print '------------start_shell end--------------------'

def clean_Result_TXT_folder():
    for i in range(3):
        hw = ver_down.get_hardware()
    cp_path_dict = dict_list()
    hw_na,__null = cp_path_dict[hw]
    current_path = os.getcwd()
    path = current_path +'\\Automation_Result\\'+hw_na+'\\Result_TXT\\'
    print 'mail_path:%s'%path
    file_list = os.listdir(path)
    del_list = [file for file in file_list if file.endswith(('.txt','.html'))]
    print 'del_list: %s'%del_list
    list_len = len(del_list)
    for i in range(list_len):
        os.remove(path+del_list[i])

def ba_func_init(cfg_value,svn_update_flag):
    '''
    @summary: 
    '''
    print '--------------ba_func_init---------------'
    if '1' == svn_update_flag:
        svn_update.update_svn()
    os.system(kill_adb_cmd)
    if os.path.exists(gt_resu_path + cfg_value.version_name + '\\' + mail_txt.gt_resul_pass):
        os.remove(gt_resu_path + cfg_value.version_name + '\\' + mail_txt.gt_resul_pass)
    if os.path.exists(gt_resu_path + cfg_value.version_name + '\\' + mail_txt.gt_resul_fail):
        os.remove(gt_resu_path + cfg_value.version_name + '\\' + mail_txt.gt_resul_fail)
    os.system(adb_rm_pass_cmd)
    os.system(adb_rm_fail_cmd)

    print '-------------ba_func_init end-------------'
def batch_function(cfg_value,dw_stat,text_mode):
    '''
    @summary: 
    '''
    work_path()
    dom = xml.dom.minidom.parse('config.xml')
    root = dom.documentElement
    
    svn_update_flag = root.getElementsByTagName('svn_update_flag')[0].childNodes[0].data
    print 'svn_update_flag is [%s]'%svn_update_flag,type(svn_update_flag)
    print 'text_mode : %s'%text_mode
    global fi_node_nu
    fi_node_nu = 0
#     global node_range
    node_range = 0
    print '-----------------batch_function-----------------'
#     start_shell()
#     for mode in mode_list:
#         
    ba_func_init(cfg_value,svn_update_flag)
#     for text_mode in cfg_value.exec_file:
        
    if rpmsg == text_mode:
        exec_folder = cfg_value.rp_file_name
        node_range = len(exec_folder)
        print 'rpmsg node_range is %s'%node_range
    elif gtest == text_mode:
        exec_folder = cfg_value.gt_file_name
        print 'exec_folder is :%s'%exec_folder
        node_range = 1
        print 'gtest node_range is %s'%node_range
    elif apk == text_mode:
        exec_folder = cfg_value.apk_file_name
        node_range = 1
        print 'apk node_range is %s'%node_range
            
    print 'node_range is [%s]'%node_range
            
    for i in range(0,node_range):
        print 'exec_folder:[%s]'%exec_folder[fi_node_nu]
        get_filesname(cfg_value,text_mode)
        re_dirs_file(cfg_value)
        
        bat_exec(cfg_value,text_mode)
        
        copy_file(cfg_value,2,text_mode)
        move_next(cfg_value,dw_stat,text_mode)
        
        fi_node_nu += 1
            
    move_test(cfg_value,text_mode)
    work_path()
    print '-----------------batch_function end-----------------'
