import sys,os 

import re
from pychartdir import *
from collections import namedtuple
from datetime import date
from OrgTable import *        

        
class OrgLine(object):
    """
    """
    
    def __init__(self, lineStr):
        """
        """
        self.line = lineStr
        # self._level = None
        # self._tag = None
        # self._timeSpent = None
        # level = self._parseLevel()
        # if level is not None:
        #     self._level = level
        #     self._tag = self._parseTag()
        # else:
        #     self._timeSpent = self._parseClockTime()

    def _parseTimeStr(self,timeStr):
        timeVal = timeStr.split("-")
        return date(int(timeVal[0]),int(timeVal[1]),int(timeVal[2]))

    def getLevel(self,):
        """
        """
        level_pattern = re.compile(r'\*+')
        match = level_pattern.match(self.line)
        if match:
            return len(match.group())
        else:
            return None

    def getTag(self,):
        """
        Only return one tag if there is multi tags
        """
        tag_pattern = re.compile('(:\w+)+:')
        tag_str = tag_pattern.search(self.line)
        if tag_str:
            curTagList = tag_str.group().strip(':').split(':')
            if len(curTagList) is not 0:
                return curTagList[0]
        return 'default'

    def getClockTime(self,):
        """
        """
        date_pattern = re.compile('\d{4}-\d{2}-\d{2}')
        clock_pattern = re.compile(' *CLOCK:')
        if clock_pattern.match(line) is not None:
            time = 0
            timeStrPattern = re.compile('\d+:\d+$')
            timeStrGroup = timeStrPattern.search(self.line)
            if timeStrGroup is not None:
                timeStr = timeStrGroup.group().split(':')
                time = int(timeStr[0])*60+int(timeStr[1])
                start_end = date_pattern.findall(self.line)
                if len(start_end) == 2:
                    return (self._parseTimeStr(start_end[0]),self._parseTimeStr(start_end[1]) ,time)
                    #return (start_end[0],start_end[1],time)
        return (None,None,0)
            

class TimeFrame_Today(object):
    """
    """
    
    def __init__(self, ):
        """
        """
        self._today = date.today() 
    def inTimeFrame(self, timeFrameDate):
        return self._today == timeFrameDate

    def getTimeFrameName(self,):
        return "Today"
        
class TimeFrame_CurWeek(object):
    """
    """
    
    def __init__(self, ):
        """
        """
        curDateISOCanendar = date.today().isocalendar()
        self._curWeek = curDateISOCanendar[1]
        self._curYear = curDateISOCanendar[0]

    def inTimeFrame(self, timeFrameDate):
        timeFrameDateCalendar = timeFrameDate.isocalendar()
        return (timeFrameDateCalendar[1] == self._curWeek) and (timeFrameDateCalendar[0] == self._curYear )

    def getTimeFrameName(self,):
        return "Current Week"


        
class TimeFrame_CurMonth(object):
    """
    """
    
    def __init__(self, ):
        """
        """
        curDay = date.today();
        self._curMonth = curDay.month
        self._curYear = curDay.year
    def inTimeFrame(self, timeFrameDate):
        return (self._curYear == timeFrameDate.year) and (self._curMonth == timeFrameDate.month)

    def getTimeFrameName(self,):
        return "Current Month"
        

    
class TimeData(object):
    """
    """
    
    def __init__(self, timeFrame, workingDir):
        """
        """
        self._timeData = {}
        self._timeFrame = timeFrame
        self._totalTime = 0
        self._workingDir = workingDir


    def addTime(self, tag, (startTime,endTime,timeSpent)):
        """
        """
        if startTime is None:
            return
        if self._timeFrame.inTimeFrame(startTime):
            self._totalTime = self._totalTime+timeSpent
            if tag in self._timeData:
                self._timeData[tag] = self._timeData[tag] + timeSpent
            else:
                self._timeData[tag] = timeSpent

    def totalTimeStr(self,):
        return "%dh %dm" % (self._totalTime/60,self._totalTime%60)

    def totalTime(self,):
        return self._totalTime

    def pieChartPath(self,):
        fileName = self._timeFrame.getTimeFrameName().replace(' ','_')+".png"
        return os.path.join(self._workingDir,fileName)

    
    def pieChart(self, ):
        """
        """
        # Create a PieChart object of size 360 x 300 pixels
        c = PieChart(360, 300)
        c.addTitle(self._timeFrame.getTimeFrameName(), "arialbd.ttf", 10)
        # Set the center of the pie at (180, 140) and the radius to 100 pixels
        c.setPieSize(180, 140, 100)
        # Set the pie data and the pie labels
        c.setData(self._timeData.values(), self._timeData.keys())
        # Output the chart
        c.makeChart(self.pieChartPath())
    
    def debug_printData(self, ):
        for tag in self._timeData:
            print tag,"\t",self._timeData[tag]
        print self._timeData.keys()
        print self._timeData.values()
        

        
        
        

            
# I only want to know the time spend for 1st level of task, do not need to know too detail information
if __name__ == '__main__':
    
    fd = open(sys.argv[1])
    timeDataToday = TimeData(TimeFrame_Today(),sys.argv[2])
    timeDataCurWeek = TimeData(TimeFrame_CurWeek(),sys.argv[2])
    timeDataCurMonth = TimeData(TimeFrame_CurMonth(),sys.argv[2])
    curTag = None
    for line in fd.readlines():
        orgLine = OrgLine(line)
        if orgLine.getLevel() == 1:
            curTag = orgLine.getTag();
        orgClockTime = orgLine.getClockTime()
        timeDataToday.addTime(curTag,orgClockTime)
        timeDataCurWeek.addTime(curTag,orgClockTime)
        timeDataCurMonth.addTime(curTag,orgClockTime)
    fd.close()

    orgTable = OrgTable(2)
    orgTable.setHeaderData(["TimeFrame","Working Time"])
    orgTable.addRowData(["Today",timeDataToday.totalTimeStr()])
    orgTable.addRowData(["This Week",timeDataCurWeek.totalTimeStr()])
    orgTable.addRowData(["This Month",timeDataCurMonth.totalTimeStr()])
    orgTable.printTable()
    for timeData in [timeDataToday,timeDataCurWeek,timeDataCurMonth]:
        if timeData.totalTime() is not 0:
            timeData.pieChart()
            print " [["+timeData.pieChartPath()+"]] ",
#    timeDataToday.pieChart("mytime_today.png")
#    timeDataCurWeek.pieChart("mytime_curweek.png")
#    timeDataCurMonth.pirChart("mytime_curmonth.png")
    
