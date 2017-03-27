#!/usr/bin/env python
# -*- coding=utf-8 -*-
'''
Created on 2016-3-23

@author: zWX279959
'''

from selenium import webdriver
# import selenium
import time
import os
import urllib2
import re
# import chardet
import sys
import shutil
import zipfile
import conf_xml
import wx
import rarfile  # @UnusedImport
'---------------------------------------------------------------------------------------------'
'''
@summary: 
config
'''
version_download_folder = 'version_download_folder'
ver_nu = 'version_num.txt'

'''
@summary: 
command
'''

hw_cmd = 'adb shell getprop ro.hardware'
download_config_xml = 'config.xml'
'---------------------------------------------------------------------------------------------'

class ver_url(object):
    '''
    @summary: 
    austin_url
    '''
    Austin_ver_url = 'http://10.141.105.212:14000/#/compilepackage/CI_Version/austin/br_hisi_wt_kirin950_n/'
    hi3650_req_url = 'http://10.141.105.212:14000/webhdfs/v1/compilepackage/CI_Version/austin/br_hisi_wt_kirin950_n/%(data_key)s/%(ver_nu)s?op=LISTSTATUS&user.name=balong'
    '''
    
    '''
    'http://10.141.105.154:14000/#/compilepackage/CI_Version/chicago/br_hisi_wt_trunk_hione/201703/20170327_103746395_I1f83f00'
    '''
    @summary: 
    dallas_url
    '''
    Dallas_ver_url = 'http://10.141.105.153:14000/index.html#/compilepackage/CI_Version/dallas/br_dallas_v100r001c30_main/'
    hi6250_req_url = 'http://10.141.105.153:14000/webhdfs/v1/compilepackage/CI_Version/dallas/br_dallas_v100r001c30_main/%(data_key)s/%(ver_nu)s?op=LISTSTATUS&user.name=balong'        

    '''
    @summary: 
    chicago_url
    '''
    Chicago_ver_url = 'http://10.141.105.154:14000/#/compilepackage/CI_Version/chicago/br_hisi_wt_trunk_hione/'
    hi3660_req_url = 'http://10.141.105.154:14000/webhdfs/v1/compilepackage/CI_Version/chicago/br_hisi_wt_trunk_hione/%(data_key)s/%(ver_nu)s?op=LISTSTATUS&user.name=balong'
                     
class ver_type(object):
    '''
    @summary: 
    '''
    UDP = 'UDP'
    VENUS = 'VENUS'
    NEMO = 'NEMO'
    EVA = 'EVA'
    KNIGHT = 'KNIGHT'
    BERLIN  = 'BERLIN'

def download_folder(pc_disk,folder):
    version_folder =  pc_disk + folder
    check_folder = os.path.exists(version_folder)
    if check_folder == False:
        os.mkdir(version_folder)

def getnowtime():
    return time.strftime("%Y%m",time.localtime(time.time()))

def open_url(cfg_value):

    hw = get_hardware()
    global date_key
    date_key = getnowtime() 

    url_variable = {'data_key':date_key,'ver_nu':''}
    
    url_dic = {'hi3650':(ver_url.Austin_ver_url,ver_url.hi3650_req_url % url_variable),\
               'hi6250':(ver_url.Dallas_ver_url,ver_url.hi6250_req_url % url_variable),\
               'hi3660':(ver_url.Chicago_ver_url,ver_url.hi3660_req_url % url_variable)}
   
    
    version_download_url,hixxxx_request_url=url_dic[hw]
    
    print 'open_url'
    download_folder(cfg_value.Disk, version_download_folder)
    global chrome_driver
    chrome_driver = webdriver.Chrome()
    chrome_driver.get(version_download_url)

    time.sleep(1)

    first_page = '//a[@inode-path='+date_key+']'
    count_a = 5
    while (count_a !=0):
        try:
            chrome_driver.find_element_by_xpath(first_page).click()
        except Exception,error:
            time.sleep(2)
            print error
            count_a -= 1
            continue
        break
    time.sleep(1)


    global version_data_url
    version_data_url = version_download_url + date_key
        
    print 'open_url END'
    return hixxxx_request_url

def getPage(url):
    '''
    @summary:
    '''
    print 'getPage'
    request = urllib2.Request(url)
    global response
    response = urllib2.urlopen(request)
    return response.read()                      
    print 'getPage END'

def get_fullversion_code_func(get_page, cfg_value):
    print 'get_fullversion_code'
    get_fullversion_code = get_page

    request_url_txt = conf_xml.get_str(cfg_value, 2)
    with open(request_url_txt,"w") as f:
        f.write(get_fullversion_code)
    with open(request_url_txt,'r') as f:
        global total_ver_code
        total_ver_code = f.read()
    return total_ver_code
    print 'get_fullversion_code END'

# print '--------++++++++++++++++++++++++++-----------------------------------------'

def get_version_num_txt(get_page,cfg_value):
    print 'get_version_num_txt'
    total_ver_code = get_fullversion_code_func(get_page, cfg_value)
    result_1 = re.findall(u'(\d+)_(\d+)_(\w+)',total_ver_code )

    version_txt = conf_xml.get_str(cfg_value, 1)

    with open(version_txt,"w") as h:
        if result_1:
            for line in result_1:
                print line
                h.write("%s_%s_%s\n"%(line[0],line[1],line[2]))

        else :
            print "error"
    print 'get_version_num_txt END'

def rar_type(cfg_value):
    hw = get_hardware()
    
    if '' == cfg_value.download_type or '' == hw:
        wx.MessageBox('cfg_value.download_type or hw is none')
        return

    fullversion_rar_dic = {'hi3650':(hw + "_f2fs_4_1.rar", 'buildinfo_'+hw+'__f2fs_4_1.txt'),\
                           'hi6250':(hw + '_c30_f2fs_fullversion.rar', 'buildinfo_'+hw+'_c30_f2fs_fullversion.txt'),\
                           'hi3660':(hw + "_pcie.rar", 'buildinfo_'+hw+'_pcie.txt')}
    hixxxx_fullversion_rar,hixxxx_version_txt = fullversion_rar_dic[hw]

    return  hixxxx_fullversion_rar,hixxxx_version_txt

def version_download(cfg_value):
    print 'version_download'
    hw = get_hardware()  


    hixxxx_fullversion_rar,hixxxx_version_txt = rar_type(cfg_value)

    version_txt = conf_xml.get_str(cfg_value, 1)
    hixxxx_txt = conf_xml.get_str(cfg_value, 3)
    automated_factory_txt = conf_xml.get_str(cfg_value, 4)
    with open(version_txt,'r') as ver_fd:
        ver_content = ver_fd.readlines()
        print ver_content

    if ver_content:
        print "[len(version_txt) is %s]"%len(ver_content)
        for idx in range(len(ver_content),0,-1):
            version_num = ver_content[idx-1][:-1]
            
            url_variable = {'data_key':date_key,'ver_nu':version_num}
            req_url_dic = {'hi3650':ver_url.hi3650_req_url % url_variable,\
                           'hi6250':ver_url.hi6250_req_url % url_variable,\
                           'hi3660':ver_url.hi3660_req_url % url_variable}

            hixxxx_request_url=req_url_dic[hw]
            num_id = '//a[@inode-path='+'"'+version_num+'"'+']'

            while True:
                time.sleep(1)
                current_url = chrome_driver.current_url
                current_url = current_url.strip('\n')
                current_url = current_url.strip('\r')
                hw_request_url = version_data_url
                hw_request_url = hw_request_url.strip('\n')
                hw_request_url = hw_request_url.strip('\r')
                print 'dd-->%s'%current_url
                print 'aa-->%s'%hw_request_url
                if current_url == hw_request_url:
                        time.sleep(5)
                        print '###chrome_driver_click'
                        count_b = 5
                        while (count_b !=0):
                            try:
                                chrome_driver.find_element_by_xpath(num_id).click()
                            except Exception ,error:
                                time.sleep(2)
                                print error
                                count_b -= 1
                                continue
                            break                                
                        break
                else:
                    print "no match -----continue"
                    continue
            get_hixxxx_code = getPage(hixxxx_request_url)
            with open(hixxxx_txt,"w") as hixxx_w_fd:
                hixxx_w_fd.write(get_hixxxx_code)
            
            with open(hixxxx_txt,'r') as hixxx_r_fd:
                hixxxx_content = hixxx_r_fd.read()
            fail_key = hixxxx_content.find('fail')
            return_rar = hixxxx_content.find(hixxxx_fullversion_rar)
            return_txt = hixxxx_content.find(hixxxx_version_txt)

            if -1 != return_rar and -1 == fail_key and -1 != return_txt:
                global download_version_num
                download_version_num = version_num
                time.sleep(1)
                inode_path_rar ='//a[@inode-path=' + '"' + hixxxx_fullversion_rar + '"' + ']'
                count_c = 5
                while(count_c !=0):
                    try:
                        chrome_driver.find_element_by_xpath(inode_path_rar).click()
                    except Exception,error:
                        time.sleep(2)
                        print error
                        count_c -= 1
                        continue
                    break
                with open(automated_factory_txt,'w') as exec_ver_nu:
                    exec_ver_nu.write(version_num)
                
                with open(ver_nu,'w') as total_ver_nu:
                    total_ver_nu.write(download_version_num)
                print "download"
                break
            else:
                chrome_driver.back()
                print "###chrome_driver_back"
    print 'version_download END'

def rename_folder(cfg_value):
    """
    @summary: 
    """
    print 'rename_folder'
    global new_name
    hw = get_hardware()
    new_name = cfg_value.Disk + hw +'--'+download_version_num
    if os.path.exists(new_name) == True:
        del_dir(new_name)
    else:
        os.mkdir(new_name)
    print 'rename_folder END'
    print 'downloading............'    

def move_folder(cfg_value):
    print 'move_folder'
    hw = get_hardware()
    global version_path
    download_path = conf_xml.get_str(cfg_value, 5)

    hixxxx_fullversion_rar,hixxxx_version_txt = rar_type(cfg_value)
    version_path  = download_path + "\\" + hixxxx_fullversion_rar
    status_folder = os.listdir(download_path)
    if status_folder != None:
        print "-----------moved---------"
        shutil.move(version_path, new_name)
        print "-----------moved END-----------"
    else:
        print 'download_path is none��'
    print 'move_folder END'

def remove():
    print 'remove'
    delete_version_path = version_path
    os.remove(delete_version_path)
    print '-----------removed-----------'
    print 'remove END'

def del_dir(list_dir):
    '''
    @summary: 
    '''
    print '----------del_dir------------'
    if os.path.isdir(list_dir):
        paths = os.listdir(list_dir)
        for path in paths:
            filepath = os.path.join(list_dir,path)
            if os.path.isfile(filepath):
                    os.remove(filepath)
    print '--------del_dir end----------'

def unzip_file(cfg_value):
    """
    @summary: 
    """
    print 'unzip_file'
    hw = get_hardware()
    try:
        hixxxx_fullversion_rar,hixxxx_version_txt = rar_type(cfg_value)

        unzip_path = cfg_value.Disk + hw+'--'+download_version_num + "\\" + hixxxx_fullversion_rar
        global unzip_version_path
        unzip_version_path = cfg_value.Disk + hw+'--'+download_version_num
        f = zipfile.ZipFile(unzip_path,mode='r')
        for file in f.namelist():
            f.extract(file,unzip_version_path)
        print 'unzip_file END'
    except Exception,e:
        print e
        if os.path.exists(unzip_version_path):
            shutil.rmtree(unzip_version_path,True)
            print 'file is not a zip file'

def exec_(cfg_value):
    """
    @summary: 
    """
    print 'exec_'
    hw = get_hardware()
    exec_udp_bat = conf_xml.get_str(cfg_value,6)
#     exec_moblie_ph_bat = conf_xml.get_str(cfg_value,7)
    exec_bat_path = unzip_version_path + '\\image'
    os.chdir(exec_bat_path)
    if '' == cfg_value.download_type or '' == hw:
        wx.MessageBox('cfg_value.download_type or hw is none')
#     elif hw == 'hi3650' and ('EVA' == cfg_value.download_type or 'KNIGHT' == cfg_value.download_type):
#         os.system(exec_moblie_ph_bat)  
    else:
        os.system(exec_udp_bat)
    print 'exec_ END'        

def get_hardware():
    '''
    @summary: 
    '''
    r = os.popen(hw_cmd)
    info = r.readline()
    info_1 = info.strip('\n')
    info_1 = info_1.strip('\r')
    info_2 = str(info_1)

    return info_2

def hw_info():
    hw = get_hardware()
    with open('hw_info.txt','w') as hw_w_fd:
        hw_w_fd.write(hw)
    with open('hw_info.txt','r') as hw_r_fd:
        hw = hw_r_fd.read()
    return hw

def ver_function(cfg_value):
    '''
    @summary: 
    '''
    hw = get_hardware()
    print "your UDP/phone hardware is [%s]\n The tool apply to [%s]"%(hw, hw)
    print hw

    if hw != hw or hw == '':
        print "please check your hardware"
        return

    os.chdir(os.path.dirname(sys.argv[0]))

    download_path = conf_xml.get_str(cfg_value, 5)
    del_dir(download_path)
    
    count = 10
    url_re = None 
    while(count != 0):
        try:
            url_re = open_url(cfg_value)
        except Exception, error:
            print error
            time.sleep(2)
            continue
            count -= 1
        break
    if not url_re:
        return

    url_data = getPage(url_re)
    get_version_num_txt(url_data,cfg_value)
    version_download(cfg_value)

    rename_folder(cfg_value)
    time.sleep(2)

    while True:        
        hixxxx_fullversion_rar,hixxxx_version_txt = rar_type(cfg_value)

        str_rar = hixxxx_fullversion_rar

        if os.path.exists(download_path + '\\' + str_rar):
            move_folder(cfg_value)
            break

    unzip_file(cfg_value)

    time.sleep(3)
    exec_(cfg_value)
    print 'work is done'
    ABS_PATH = os.path.abspath(sys.argv[0])
    ABS_PATH = os.path.dirname(ABS_PATH)
    os.chdir(ABS_PATH)
    return
