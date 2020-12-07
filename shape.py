import os

path = "Z:\\인포보스 부서별자료_사업개발실\\7.경상남도람사르환경재단_식물관리\\연안습지_SHP\\"
file_list = os.listdir(path)
count = 1
for i in file_list :
    if (i.__contains__(".")) :
        print (i,"is files")
    else :
        f = open("Z:\\인포보스 부서별자료_사업개발실\\7.경상남도람사르환경재단_식물관리\\연안습지_SHP\\%s\\shape.txt" % i, 'r', encoding='utf-8')
        lines = f.readlines()
        fp = "Z:\\인포보스 부서별자료_사업개발실\\7.경상남도람사르환경재단_식물관리\\연안습지_SHP\\"

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

