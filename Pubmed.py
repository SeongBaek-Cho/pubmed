
from bs4 import BeautifulSoup
import pymysql
import tqdm
from os import listdir
import os
import shutil
from time import strptime





# get Month name to number
def getMonthNumber(date) :
    if (date.isalpha()) :
        return str(strptime(date,'%b').tm_mon)
    else :
        return date

# get rows count
def getColumnCount(cursor, table, column, value) :
    try :
        sql = "SELECT COUNT(*) AS CNT FROM %s WHERE %s = %s ;" % (table, column, value)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result[0][0])
        return result[0][0]

    except Exception as ex :
        print('Exception [getColumnCount] as %s' %ex)
        return '0'

# get row value
def getColumnValue(cursor, table, column, wcolumn, value) :
    try :
        sql = "SELECT %s FROM %s WHERE %s = %s ;" % (column, table,wcolumn,value)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result[0][0])
        return result[0][0]
    except Exception as ex :
        print('Exception [getColumnValue] as %s' %ex)
        return 'null'

# get Author Id, Count from tuple type
def getAuthorCount (cursor, surname, givenname) :
    try :
        sql = "SELECT AUTHOR_ID,COUNT(*) FROM PubMedAuthorInfo WHERE SURNAME = '%s' AND GIVENNAME = '%s' GROUP BY AUTHOR_ID ;" % (surname, givenname)
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        return result
    except Exception as ex :
        print('Exception [getAuthorCount] as %s' %ex)
        return 'null'
def setDatabase(cursor, sql) :
    try :
        print(sql)
        cursor.execute(sql)
    except Exception as ex :
        print('Excpetion [setDatabase] as %s' % ex )


files = listdir(base)



#xml data parsing

def parser(i) :

    # MySQL access data
    

    prettyfile = files[i].split('.')[0]
    filebase = base+files[i]
    log = open(logbase+prettyfile+'.txt', 'a', encoding='utf-8')


    fp = open(filebase, 'r' , encoding='cp949')
    soup=BeautifulSoup(fp, 'html.parser')

    xml_content  = soup

    articleRoot = soup.findAll('pubmedarticle')


    for x in articleRoot :
        type = "PubMed"

        root = x.find('medlinecitation')
        pmid = root.pmid.string
        article = root.find('article')

        # Journal information
        journal = article.find('journal')
        try :
            abstract = article.abstract.abstracttext.string.replace("'","''")
        except Exception as ex :
            abstract = None

        issnlist = journal.findAll('issn')
        issnPrintValue = ""
        issnOnlineValue = ""
        for z in issnlist :
            issntype = z.get('issntype')
            issnvalue = z.string
            if (issntype == 'Print') :
                issnPrintType = issntype
                issnPrintValue = issnvalue
            elif (issntype == 'Electronic') :
                issnOnlineType = issntype
                issnOnlineValue = issnvalue
            else :
                issnPrintValue = 'null'
                issnOnlineValue = 'null'
        try :
            volume = journal.journalissue.volume.string
        except Exception as ex:
            print('volume exception return null')
            volume = None
        try :
            issue = journal.journalissue.issue.string
        except Exception as ex :
            print('volume exception return null')
            issue = None
        journalname = journal.title.string
        try :
            pubyear = journal.journalissue.pubdate.year.string
        except Exception as ex :
            print('pubyear exception return 1000')
            pubyear = '1000'
        try :
            pubmonth = getMonthNumber(journal.journalissue.pubdate.month.string)
        except Exception as ex :
            print('pubmonth exception return 01')
            pubmonth = "01"
        try :
            pubday = journal.journalissue.pubdate.day.string
        except Exception as ex :
            print('pubday exception return 01')
            pubday = "01"
        pubdate = pubyear+"-"+pubmonth+"-"+pubday
        try :
            abbreviation = journal.isoabbreviation.string
        except Exception as ex :
            print('abbreviation exception return null')
            abbreviation = None



        # Create log file for Journal information
        # Register journal information
        try :
            journalcnt = getColumnCount(refdb.connect(),'PubMedJournalInfo','NAME',"'%s'" %journalname)
        except Exception as jEX :
            journalCnt = 0
        if (int(journalcnt) < 1) :
            sql = "INSERT INTO PubMedJournalInfo (JOURNAL_ID,NAME,ABBREVIATION,PRINT_ISSN,ONLINE_ISSN,COMMENT,CREATE_DATE,LASTUPDATE_DATE,CREATE_USER_ID)  VALUES (0,'%s','%s','%s','%s',null,now(),null,1) ;"
            setDatabase(refdb.connect(),sql % (journalname,abbreviation,issnPrintValue,issnOnlineValue))
            refdb.commit()
        else :
            print('JOURNAL : %s is alreay exist' % journalname)

        # Journal information end

        articletitle = article.articletitle.string
        try :
            pagination = article.pagination.medlinepgn.string
            startpage = pagination.split('-')[0]
            endpage = pagination.split('-')[1]
        except Exception as ex :
            print('pagination excepetion return null')
            startpage = None
            endpage = None



        # Create log file for pubmed Publication information
        log.write('PMID : %s \t PublicationDate : %s \n' % (pmid, pubdate))


        # Register Publication information
        pmidct = getColumnCount(refdb.connect(),'PubMedPublicationInfo', 'PMID', pmid)
        try :
            journal_id = getColumnValue(refdb.connect(),'PubMedJournalInfo','JOURNAL_ID','NAME',"'%s'" %journalname)
        except Exception as jex :
            journal_id = 0

        if (int (pmidct) < 1) :
            sql = "INSERT INTO PubMedPublicationInfo (PUBLICATION_ID, PMID, JOURNAL_ID, TYPE, TITLE, ABSTRACT, PUBLICATION_DATE,PUBLICATION_YEAR, VOLUME, ISSUE, START_PAGE, END_PAGE,  CREATE_DATE, CREATE_USER_ID )  VALUES (0,%s,%s,'PubMed','%s','%s' ,'%s','%s','%s','%s','%s','%s',now(),1 );"
            setDatabase(refdb.connect(),sql  % (pmid,journal_id,articletitle,abstract,pubdate,pubyear,volume,issue,startpage,endpage))
            refdb.commit()
        else :
            print("PMID : %s is already exist." %pmid)

        # Author information
        try :
            authorlist = article.authorlist.findAll('author')
            for x in authorlist :
                lastname = x.lastname.string.replace("'","''") # equal surname
                forename = x.forename.string.replace("'","''") # equal givenname
                authorname = forename+" "+lastname

                # Register Author information
                try :
                    try :
                        authorct = getAuthorCount(refdb.connect(),lastname, forename)[0][1]
                    except Exception as fx :
                        authorct = 0

                    if (authorct < 1 ) :
                        try :
                            sql = "INSERT INTO PubMedAuthorInfo (AUTHOR_ID, SURNAME, GIVENNAME, CREATE_DATE, CREATE_USER_ID) VALUES (0,'%s','%s',now(),1) ;"
                            setDatabase(refdb.connect(),sql % (lastname, forename))
                            pubid = getColumnValue(refdb.connect(),'PubMedPublicationInfo', 'PUBLICATION_ID', 'PMID', pmid)
                            authorid = getAuthorCount(refdb.connect(),lastname,forename)[0][0]
                            sql = "INSERT INTO PubMedPublicationAuthorInfo (PUBLICATION_ID, AUTHOR_ID, CORRESPONDING_FLAG, CREATE_DATE) VALUES (%s,%s,'N',now()); "
                            setDatabase(refdb.connect(),sql %(pubid, authorid))
                        except Exception as dx :
                            print('Error occurred Insert Author Information as [ %s ]' %dx)
                    else :
                        pubid = getColumnValue(refdb.connect(),'PubMedPublicationInfo', 'PUBLICATION_ID', 'PMID', pmid)
                        authorid = getAuthorCount(refdb.connect(),lastname,forename)[0][0]
                        sql = "INSERT INTO PubMedPublicationAuthorInfo (PUBLICATION_ID, AUTHOR_ID, CORRESPONDING_FLAG, CREATE_DATE)  VALUES (%s,%s,'N',now()); "
                        setDatabase(refdb.connect(),sql %(pubid, authorid))
                        refdb.commit()
                except Exception as ex :
                    print ('Error occurred Register Author Information as [ %s ]' % ex)
        except Exception as EX :
            print('No search AuthorList')



        log.write('----------------------------------------------------------------------- \n')
    log.flush()
    log.close()
    fp.close()
    refdb.close()


if __name__ == '__main__' :
    from multiprocessing import Pool, Manager

    index = 0
    file_size = len(files)
    pool = Pool(processes = 2)
    pool.map(parser, range(1, file_size, 1))
    pool.close()
    pool.join()




