#!/usr/bin/python

import sys,os 

import re
from pychartdir import *
from collections import namedtuple
from datetime import date
import OrgModeTxt        

def datetime_today():
    """
    Use this function to get datetime object of current date, this is used for testing
    Can set the current date to any date.
    """
    return date.today()
#    return date(2013, 10, 22)


class OrgLine(object):
    """
    """
    
    def __init__(self, lineStr):
        """
        """
        self.line = lineStr

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
        self._today = datetime_today() 
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
        curDateISOCanendar = datetime_today().isocalendar()
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
        curDay = datetime_today();
        self._curMonth = curDay.month
        self._curYear = curDay.year
    def inTimeFrame(self, timeFrameDate):
        return (self._curYear == timeFrameDate.year) and (self._curMonth == timeFrameDate.month)

    def getTimeFrameName(self,):
        return "Current Month"
        

    
class TimeData(object):
    """
    """
    
    def __init__(self, timeFrame, orgFileName, workingDir):
        """
        """
        self._colorList = [0x00CED1]
        self._timeData = {}
        self._timeFrame = timeFrame
        self._totalTime = 0
        self._workingDir = workingDir
        self._orgFileName = orgFileName

    def getTagCount(self,):
        """
        """
        return len(self._timeData)
        
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
        fileName = self._timeFrame.getTimeFrameName().replace(' ','_')+"_"+self._orgFileName+".png"
        return os.path.join(self._workingDir,fileName)

    
    def pieChart(self, maxTag ):
        """
        """

        items = self._timeData.items()
        items = [(wtime,tag) for tag,wtime in items]
        items.sort(reverse=True)
        
        c = PieChart(400, 290 + maxTag*22)
        c.addTitle(self._timeFrame.getTimeFrameName(), "arialbd.ttf", 10)
        c.setPieSize(180, 100, 60)

        tagList = [tag for wtime,tag in items]
        workTimeList = [wtime for wtime,tag in items]
        c.setData(
            workTimeList,
            tagList
            
        )
        c.setColors2(DataColor, self._colorList)
        #       c.setData(data, labels)
        c.setSectorStyle(LocalGradientShading)
        c.setLabelLayout(SideLayout, 16)
        c.setLabelFormat("{label} ({percent}%)")

        b = c.addLegend(40, 230, 1, "arialbi.ttf", 10)

        b.setBackground(Transparent, 0x444444)
        b.setRoundedCorners()
        b.setMargin(16)
        b.setKeySpacing(0, 5)
        b.setKeyBorder(SameAsMainColor)
        b.setText(
            "<*block,valign=top*>{={sector}+1}.<*advanceTo=22*><*block,width=120*>{label}" \
            "<*/*><*block,width=120,halign=right*>{percent}<*/*>%")
        
        c.makeChart(self.pieChartPath())
    
    def debug_printData(self, ):
        for tag in self._timeData:
            print tag,"\t",self._timeData[tag]
        print self._timeData.keys()
        print self._timeData.values()
        

        
        
        

            
# I only want to know the time spend for 1st level of task, do not need to know too detail information
if __name__ == '__main__':
    
    fd = open(sys.argv[1])
    orgName = sys.argv[1].split("/")[-1].split(".")[0]
    timeDataToday = TimeData(TimeFrame_Today(),orgName,sys.argv[2])
    timeDataCurWeek = TimeData(TimeFrame_CurWeek(),orgName,sys.argv[2])
    timeDataCurMonth = TimeData(TimeFrame_CurMonth(),orgName,sys.argv[2])
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

    maxTag = max( timeDataToday.getTagCount(), timeDataCurWeek.getTagCount(), timeDataCurMonth.getTagCount() )
    
    
    
    orgTable = OrgModeTxt.OrgTable(2)
    orgTable.setHeaderData(["TimeFrame","Working Time"])
    orgTable.addRowData(["Today",timeDataToday.totalTimeStr()])
    orgTable.addRowData(["This Week",timeDataCurWeek.totalTimeStr()])
    orgTable.addRowData(["This Month",timeDataCurMonth.totalTimeStr()])
    orgTable.printTable()
    for timeData in [timeDataToday,timeDataCurWeek,timeDataCurMonth]:
        if timeData.totalTime() is not 0:
            timeData.pieChart(maxTag)
            print OrgModeTxt.fileLink(timeData.pieChartPath()) + " ",
    
