import os
import shutil

logPath = "log/"
xmlPath = "xml/"
completePath = "complete/"

log_list = os.listdir(logPath)

for log in log_list :
    filename = log.replace(".txt", "")+'.xml'
    xml_list = os.listdir(xmlPath)
    for xml in xml_list :
        if (filename == xml) :
            shutil.move(xmlPath+xml , completePath+xml)
