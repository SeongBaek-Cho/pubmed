import os


file_list = os.listdir(path)
count = 1
for i in file_list :
    if (i.__contains__(".")) :
        print (i,"is files")
    else :
        
        lines = f.readlines()
        

        cnt = 0
        init = None
        for line in lines :
            sw = open(fp+"pySwitch7.txt", 'a', encoding='utf-8')
            line = line.replace("\n","")
            if (cnt == 0) :
                init = line
                sps = line.split(",")
                sw.write('"%s":[\n' % str(count))
                sw.write("{lat:"+sps[1]+", lng:"+sps[0]+"},\n")
                sw.flush()
                cnt = cnt +1
                count = count +1
            else:
                if(init == line) :
                    sps = line.split(",")
                    sw.write("{lat:"+sps[1]+", lng:"+sps[0]+"},\n")
                    sw.write("],\n")
                    sw.flush()
                    cnt=0
                else :
                    sps = line.split(",")
                    sw.write("{lat:"+sps[1]+", lng:"+sps[0]+"},\n")
                    sw.flush()
                    cnt = cnt +1

            sw.close()
        f.close()

