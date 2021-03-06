import urllib2
import sys
import re
import MySQLdb

"""Script to find names of colleges from ugc website
and print them

<tr><td valign=top ><ul><li> <font color=#006699>A. Veeriya Vendayar Memorial, Sri Pushpam College</font> POONDI. DIST.:Thanjavur TAMIL NADU-613   <b>Yr Estd.:</b> 1956 <b>Status:</b> 2(f)&12(B)
 </ul></td></tr>




<tr><td valign=top ><ul><li> <font color=#006699>A.B.M. College, SINGHBHUM.</font> DIST.:Purbi Singhbhum Jharkhand    <b>Yr Estd.:</b> 1981 <b>Status:</b> 2(f)&12(B)
 </ul></td></tr>




<tr><td valign=top ><ul><li> <font color=#006699>A.B.M. Degree College, </font> Ongole Distt.: Prakasam Andhra Pradesh   <b>Yr Estd.:</b> 1981 <b>Status:</b> 2(f)&12(B) </ul></td></tr>

"""

def find_colleges(text):
    """Given a string, reads and return a list of college names from it
    """

    colleges = []

   
    tuples =re.findall(r'<tr><td valign=top ><ul><li> <font color=#006699>([\w\s%.,(&:)\'\-]+)</font> ([\w.,:()\-\s]+)<b>Yr Estd.:</b> (\d+) <b>Status:</b> ([\w\s()&]+) </ul></td></tr>', text)

    db = MySQLdb.connect(user='root',
            db='amity',
            passwd='myarmy66',
            host='localhost')
    cursor=db.cursor()
    cursor.execute("""
    create table if not exists colleglist
    (
    id integer(5) auto_increment primary key,
    name varchar(160) not null,
    address varchar(200),
    estd year,
    section varchar(40)
    )
    """)

    q_insert = "insert into collegelist (name, address) values (%s, %s)"
    for college in tuples:
    
       #To write in a file
       """
       try:
            logfile = open('colleges.txt', 'a')
            try:
                logfile.write(','.join(map(str,college))+'\n')
            finally:
                logfile.close()
        except IOError:
            pass
        """
        #To write in a database
        cursor.execute(q_insert, (college[0], college[1]))
        db.commit()
    db.close()
    print len(tuples)  #To verify number of college names captured

def main():
    """call find_college function to get a list of colleges and then it prints them
    """

    html = ''
    for num in range(1,82):
        link = 'http://oldwebsite.ugc.ac.in/inside/reco_college_search.php?resultpage='+str(num)+'&search=%'
        response = urllib2.urlopen(link)
        html += response.read()
    find_colleges(html)  #To call find colleges function and write them in database or file



if __name__=='__main__':
    main()
