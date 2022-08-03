# conn_scripts

This repo is a collection of scripts for converting configuration files from SecureCRT to MremotenG. 

Other programs may be added in the future


### mremote_xml.py
Script to take a CSV file and convert into a folder of sessions to be imported into mRemote 

Example format (HOST, IP, PROTOCOL, PORT):

```
93180yc-ex-1,100.64.43.25,Telnet,2035
93180yc-ex-2,100.64.43.25,Telnet,2036
93180yc-fx3-1,100.64.43.25,Telnet,2037
```

```ps
PS Z:\> python3 .\mremote_xml.py .\input.csv foldername.xml
```

### experimental
Folder of scripts to directly convert secureCRT into mRemote. 