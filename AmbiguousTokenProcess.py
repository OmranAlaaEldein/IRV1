import re
from dateutil.parser import parse


class AmbiguousToken:

    def __init__(self):
        self.dateAndTimePatterns = [
            # MM/DD/YYYY or MM\DD\YYYY  MM-DD-YYYY
            "(([0][1-9])|([1][0-2]))[\\\/-](([0][1-9])|([1-2][0-9])|([3][0-1]))[\\\/-](([2][0-1])|([1][6-9]))[0-9][0-9]",
            # DD/MM/YYYY or DD\MM\YYYY or DD-MM-YYYY
            "([0-2][0-9]|[3][0-1])[\\\/-]([0]\d|[1][0-2])[\\\/-](([2][01])|([1][6-9]))\d{2}",
            # YYYY-MM-DD or YYYY\MM\DD or YYYY\MM\DD
            "((([2][01])|([1][6-9]))\d{2})[\\\/-]((0[1-9])|(1[0-2]))[\\\/-](0[1-9]|[12][0-9]|3[01])",
            # YYYY-DD-MM or YYYY\DD\MM or YYYY\DD\MM
            "((([2][01])|([1][6-9]))\d{2})[\\\/-](0[1-9]|[12][0-9]|3[01])[\\\/-]((0[1-9])|(1[0-2]))",
            # 00:00:00 to 12:00:00 or 00:00:00 AM to 12:00:00 PM
            "((0[0-9])|(1[0-2]))(\:)((0[0-9])|(1[0-9])|(2[0-9])|(3[0-9])|(4[0-9])|(5[0-9]))((\:)((0[0-9])|(1[0-9])|(2[0-9])|(3[0-9])|(4[0-9])|(5[0-9])))?([ ]?[ap]m)?",
            # 00:00:00 to 23:59:59
            "((1[3-9])|(2[0-3]))(\:)((0[0-9])|(1[0-9])|(2[0-9])|(3[0-9])|(4[0-9])|(5[0-9]))((\:)((0[0-9])|(1[0-9])|(2[0-9])|(3[0-9])|(4[0-9])|(5[0-9])))?",
            # dd (st,nd,th) MM ( yyyy or yy )
            "(((3[0-1])|(2[0-9])|(1[0-9])|([1-9]))(st|nd|th)?[ ])(((jan(uary)?)|(feb(ruary)?)|(mar(ch)?)|(may)|(apr(il)?)|(june?)|(july?)|(aug(ust)?)|(sep(tember)?)|((nov|dec)(ember)?)|(oct(ober)?))[ ]?)((([2][01])|([1][6-9]))?([0-9][0-9]))",
            # MM dd,yyyy  --> Jul 30,2015
            "(((jan(uary)?)|(feb(ruary)?)|(mar(ch)?)|(may)|(apr(il)?)|(june?)|(july?)|(aug(ust)?)|(sep(tember)?)|((nov|dec)(ember)?)|(oct(ober)?))[ ])(((3[0-1])|(2[0-9])|(1[0-9])|(0?[1-9]))),((([2][01])|([1][6-9]))([0-9][0-9]))",
            # CAP date time --> 2016-04-07T12:29:00-04:00
            "(?:[2-9]\d\d\d)-(?:1[012]|0?[1-9])?-(?:31(?!.(?:0?[2469]|11))|(?:30|29)(?!.0?2)|29(?=.0?2.(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))(?:T))|(?:2[0-8]|1\d|0?[1-9]))T(2[01234]|[01]\d):[0-5]\d:[0-5]\d[+-][01]\d:[0-5]\d"
        ]
        self.months = {
            "january" : 1 , "jan": 1,
            "february" : 2 ,"feb": 2,
            "march" : 3 ,"mar": 3,
            "april" : 4 ,"apr": 4,
            "may" : 5 ,
            "june" : 6 ,"jun": 6,
            "july" : 7 ,"jul": 7,
            "august" : 8 ,"aug": 8,
            "september" : 9 ,"sep": 9 ,
            "october" : 10 ,"oct": 10,
            "november" : 11 ,"nov": 11,
            "december" : 12 ,"dec" : 12
        }

    def dealWithDateTime(self , line):
        words = []
        rest = ""
        pattern_id = 0
        for pattern in self.dateAndTimePatterns:
            rest = ""
            # pr"\n new Pattern ({})\n".format(len(line)))
            while (re.search(pattern, line)):
                result = re.search(pattern, line)
                #print ("round ({})".format(pattern_id))
                first = result.span()[0]
                second = result.span()[1]
                prefix = line[0:first]
                inner = line[first:second]
                suffix = line[second:len(line)]
                # prfirst)
                # prsecond)
                # pr"prefix :" + prefix)
                #print("inner :" + inner)
                # pr"suffix :" + suffix)
                rest += prefix
                line = suffix
                normalFrm = self.normalizing(pattern_id,inner)
                words.append(normalFrm)
                #print(f"As key : {normalFrm}")

            pattern_id+=1
            line = rest + line
            #print("--> " + line)

        return (words , line)



    def normalizing(self , pattern_id , date ):
        # formal format  [DD-MM-YYYY]

        if(pattern_id == 0) :
            # MM/DD/YYYY or MM\DD\YYYY  MM-DD-YYYY
            MM = date[0:2]
            DD = date[3:5]
            YY = date[6:]

        elif(pattern_id == 1) :
            # DD/MM/YYYY or DD\MM\YYYY or DD-MM-YYYY
            DD = date[0:2]
            MM = date[3:5]
            YY = date[6:]


        elif (pattern_id == 2):
            # YYYY-MM-DD or YYYY\MM\DD or YYYY/MM/DD
            YY = date[0:4]
            MM = date[5:7]
            DD = date[8:]

        elif (pattern_id == 3):
            # YYYY-DD-MM or YYYY\DD\MM or YYYY\DD\MM
            YY = date[0:4]
            DD = date[5:7]
            MM = date[8:]

        elif (pattern_id == 7):
            #MM dd,yyyy  --> Jul 30,2015
            YY = date[-4:]
            DD = date[-7:-5]
            MM = date[:-7].strip()
            MM = str(self.months[MM])
            #print(f"{DD} {MM} {YY}")

        elif (pattern_id == 6):
            # dd (st,nd,th) MM ( yyyy or yy )
            i = 0
            while i < len(date) and date[i].isdigit(): i+=1
            DD = date[0:i]

            j = len(date) -1
            while j >= 0 and date[j].isdigit(): j -= 1
            YY = date[j:].strip()

            if len(YY)==2:
                YY = "19" + YY
            YY = YY

            MM = date[i:j]
            if( MM[0] == " " ) :
                MM = MM.strip()
            else:
                MM = MM[3:]

            MM = str(self.months[MM])

        date = DD + "-" + MM + "-" + YY
        #print(f"date per seconds : {date}")
        return date



#am = AmbiguousToken()
#with open("dataset/query.txt",encoding="utf8") as file:
 #   for line in file:
  #      am.dealWithDateTime(line)