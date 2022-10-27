#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arfedora-gnome-tweak.py
#  
#  Copyright 2016 youcef sourani <youcef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import os
import subprocess
import platform
import sys
import shutil
import zipfile
import tarfile
import time

#themes tested only on gnome shell 3.18
supported_gnome_versions=["3.18","3.16","3.14"]
home=os.getenv("HOME")

def init_check():
    
    if not os.uname()[0]=="Linux":
        sys.exit("os not supported") 
        
        
    if platform.dist()[0]!="Kali":
        if os.getuid()==0:
            sys.exit("Run Script Without Root Permissions.")
        
        
    if not sys.version.startswith("3"):
        sys.exit("Use Python 3 Try run python3 arfedora-gnome-tweak.py")        
    
   
    if os.getenv("XDG_CURRENT_DESKTOP")!="GNOME" :
        sys.exit("Your Desktop Is Not gnome shell")


    gnome_shell_version=subprocess.Popen("gnome-shell --version",stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True).communicate()[0].split()[2][0:4].decode("utf-8")
    if gnome_shell_version not in supported_gnome_versions:
        sys.exit("Your Gnome Shell Version Not Supported.")


    if not os.path.isfile("/usr/bin/wget"):
        sys.exit("Install wget And Try Again ex: sudo apt-get install wget or sudo dnf install wget")


    if not os.path.isfile("/usr/bin/git"):
        sys.exit("Install git And Try Again ex: sudo apt-get install git or sudo dnf install git")
    
    
        
        




class Mainclass(object):
    def __init__(self,links_to_Downloads=[],links_to_clone=None,files_to_extract=None,copy_from_to=None,folder_to_make=None,commands_to_run=None):
        
        self.links_to_clone=links_to_clone
        self.links_to_Downloads=links_to_Downloads
        self.files_to_extract=files_to_extract
        self.copy_from_to=copy_from_to
        self.folder_to_make=folder_to_make
        self.commands_to_run=commands_to_run
        
        
        
    def __mkdir_folder(self,folder,bool=None):
        if bool!=None:
            os.makedirs(folder,exist_ok=True)
        else:
            os.makedirs("/tmp/arfedora-gnome-tweak/%s"%folder,exist_ok=True)
    
    
    
    def _make_folder(self):
        if self.folder_to_make!=None:
            for folder in self.folder_to_make:
                self.__mkdir_folder(folder,bool=2)
    
    
    
    def _clean(self):
        if os.path.isdir("/tmp/arfedora-gnome-tweak"):
            shutil.rmtree("/tmp/arfedora-gnome-tweak")
            
            
            
            
    def _clone_git_repo(self):
        if  self.links_to_clone!=None:
            self.__mkdir_folder("downloads")
            os.chdir("/tmp/arfedora-gnome-tweak/downloads")
            for link in self.links_to_clone:
                try:
                    check=subprocess.check_call("git clone %s"%link,shell=True)
                    if check!=0:
                        sys.exit("\nDownload Faild\n")
                except :
                    sys.exit("\nDownload Faild\n")

   

                       
    def _download(self):
        if len(self.links_to_Downloads)!=0:
            self.__mkdir_folder("downloads")
            os.chdir("/tmp/arfedora-gnome-tweak/downloads")
            for link in self.links_to_Downloads:
                try:
                    check=subprocess.check_call("wget %s -P /tmp/arfedora-gnome-tweak/downloads"%link,shell=True)
                    if check!=0:
                        sys.exit("\nDownloads Fail\n")
                except:
                    sys.exit("\nDownloads Fail\n")
                
                
                                        

    def _extract_files(self):
        if self.files_to_extract!=None:
            os.chdir("/tmp/arfedora-gnome-tweak/downloads")
            for filee in self.files_to_extract:
                if os.path.splitext(filee)[1]==".zip":
                    with zipfile.ZipFile(filee, "r") as z:
                        z.extractall()
                elif os.path.splitext(filee)[1]==".tgz":
                    with tarfile.open(filee,'r:gz') as t:
                        def is_within_directory(directory, target):
                            
                            abs_directory = os.path.abspath(directory)
                            abs_target = os.path.abspath(target)
                        
                            prefix = os.path.commonprefix([abs_directory, abs_target])
                            
                            return prefix == abs_directory
                        
                        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                        
                            for member in tar.getmembers():
                                member_path = os.path.join(path, member.name)
                                if not is_within_directory(path, member_path):
                                    raise Exception("Attempted Path Traversal in Tar File")
                        
                            tar.extractall(path, members, numeric_owner=numeric_owner) 
                            
                        
                        safe_extract(t)



    def _copy_from_to(self):
        if self.copy_from_to!=None:
            for k,v in self.copy_from_to.items():
                try:
                    check=subprocess.check_call("cp -r %s %s"%(k,v),shell=True)
                    if check!=0:
                        sys.exit("\nCopy Files Fail.\n")
                except :
                    sys.exit("\nCopy Files Fail.\n")

            
            
            
            
    def _command_to_run(self):
        if self.commands_to_run!=None:
            for command in self.commands_to_run:
                subprocess.call(command,shell=True)
                time.sleep(0.2)
        
    def init_main(self):
        self._clean()
        self._make_folder()
        self._clone_git_repo()
        self._download()
        self._extract_files()
        self._copy_from_to()
        self._command_to_run()
        self._clean()
        
def main(args):
    init_check()
    
    while True:
        subprocess.call("clear")
        answer=input("Enter Number To Install Theme ||  q to quit :\n\n1-Mac os Theme\t\t2-Dark Theme\n\n-")
        print ("\n")
        if answer=="q" or answer=="Q":
            sys.exit("bye.\n")
            
        elif answer=="1":
            mainclass=Mainclass(links_to_Downloads=["http://www.socwall.com/images/wallpapers/19189-1366x768.jpg",\
                                                    "http://p1.pichost.me/i/56/1799758.jpg"],\
                                links_to_clone=["https://github.com/yucefsourani/arfedora-gnome-tweak-theme-1.git"],\
                                files_to_extract=None,\
                                copy_from_to={"/tmp/arfedora-gnome-tweak/downloads/19189-1366x768.jpg":"%s/.wallpapers"%home,\
                                              "/tmp/arfedora-gnome-tweak/downloads/1799758.jpg":"%s/.wallpapers"%home,\
                                              "/tmp/arfedora-gnome-tweak/downloads/arfedora-gnome-tweak-theme-1/El-General-Gnome/ElGeneral":"%s/.icons"%home,\
                                              "/tmp/arfedora-gnome-tweak/downloads/arfedora-gnome-tweak-theme-1/White":"%s/.themes"%home},\
                                folder_to_make=["%s/.wallpapers"%home,"%s/.themes"%home,"%s/.icons"%home],\
                                commands_to_run=["gsettings set org.gnome.desktop.background  picture-uri 'file://%s/.wallpapers/1799758.jpg' "%home,\
                                                 "gsettings set org.gnome.desktop.screensaver picture-uri 'file://%s/.wallpapers/19189-1366x768.jpg' "%home,\
                                                 "gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close' ",\
                                                 "gsettings set org.gnome.desktop.interface enable-animations true",\
                                                 "gsettings set org.gnome.desktop.background show-desktop-icons false",\
                                                 "gsettings set org.gnome.desktop.interface icon-theme 'ElGeneral' ",\
                                                 "gsettings set org.gnome.shell.extensions.user-theme name 'White' ",\
                                                 "gsettings set  org.gnome.desktop.interface gtk-theme  White",\
                                                 "gnome-shell-extension-tool -e user-theme@gnome-shell-extensions.gcampax.github.com"])
            mainclass.init_main()
            
        elif answer=="2":
            mainclass=Mainclass(links_to_Downloads=["http://www.planwallpaper.com/static/images/Desktop-Wallpaper-HD2.jpg","http://www.wallpapereast.com/static/images/tron_lamborghini_aventador-1920x1080_pXUezIm.jpg"],\
                                            links_to_clone=["https://github.com/yucefsourani/arfedora-gnome-tweak-theme-2.git","https://github.com/daniruiz/Super-Flat-Remix.git"],\
                                            files_to_extract=None,\
                                            copy_from_to={"/tmp/arfedora-gnome-tweak/downloads/Desktop-Wallpaper-HD2.jpg":"%s/.wallpapers"%home,\
                                                          "/tmp/arfedora-gnome-tweak/downloads/tron_lamborghini_aventador-1920x1080_pXUezIm.jpg":"%s/.wallpapers"%home,\
                                                          "/tmp/arfedora-gnome-tweak/downloads/Super-Flat-Remix/\"Super Flat Remix\"":"%s/.icons/Super-Flat-Remix"%home,\
                                                          "/tmp/arfedora-gnome-tweak/downloads/arfedora-gnome-tweak-theme-2/Numix-SX-Dark":"%s/.themes"%home},\
                                            folder_to_make=["%s/.wallpapers"%home,"%s/.themes"%home,"%s/.icons"%home],\
                                            commands_to_run=["gsettings set org.gnome.desktop.background  picture-uri 'file://%s/.wallpapers/tron_lamborghini_aventador-1920x1080_pXUezIm.jpg' "%home,\
                                                             "gsettings set org.gnome.desktop.screensaver picture-uri 'file://%s/.wallpapers/Desktop-Wallpaper-HD2.jpg' "%home,\
                                                             "gsettings set org.gnome.desktop.wm.preferences button-layout ':minimize,maximize,close' ",\
                                                             "gsettings set org.gnome.desktop.interface enable-animations true",\
                                                             "gsettings set org.gnome.desktop.background show-desktop-icons false",\
                                                             "gsettings set org.gnome.desktop.interface icon-theme 'Super-Flat-Remix' ",\
                                                             "gsettings set org.gnome.shell.extensions.user-theme name 'Numix-SX-Dark' ",\
                                                             "gsettings set  org.gnome.desktop.interface gtk-theme  Numix-SX-Dark",\
                                                             "gnome-shell-extension-tool -e user-theme@gnome-shell-extensions.gcampax.github.com"])
            mainclass.init_main()
               
        """elif answer=="3":
            mainclass=Mainclass(links_to_Downloads=[],\
                                            links_to_clone=None,\
                                            files_to_extract=None,\
                                            copy_from_to=None,\
                                            folder_to_make=None,\
                                            commands_to_run=None)
            mainclass.init_main()
            """   

    return 0



if __name__ == '__main__':
    sys.exit(main(sys.argv))
