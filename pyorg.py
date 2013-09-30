import sys,os 

import re
from pychartdir import *
from collections import namedtuple

        

        
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
                    return (start_end[0],start_end[1],time)
        return (None,None,0)
            
        
class TimeData(object):
    """
    """
    
    def __init__(self, ):
        """
        """
        self._timeData = {}

    def addTime(self, tag, (startTime,endTime,timeSpent)):
        """
        """
        if startTime is None:
            return
        if tag in self._timeData:
            self._timeData[tag] = self._timeData[tag] + timeSpent
        else:
            self._timeData[tag] = timeSpent


    
    def pieChart(self, fileName):
        """
        """
        # Create a PieChart object of size 360 x 300 pixels
        c = PieChart(360, 300)
        # Set the center of the pie at (180, 140) and the radius to 100 pixels
        c.setPieSize(180, 140, 100)
        # Set the pie data and the pie labels
        c.setData(self._timeData.values(), self._timeData.keys())
        # Output the chart
        c.makeChart("simplepie.png")
    
    def debug_printData(self, ):
        for tag in self._timeData:
            print tag,"\t",self._timeData[tag]
        print self._timeData.keys()
        print self._timeData.values()
        

        
        
        

            
# I only want to know the time spend for 1st level of task, do not need to know too detail information
if __name__ == '__main__':
    Row = namedtuple('Row',['first','second','third'])
    data1 = Row(1,2,3)
    data2 = Row(4,5,6)
    tab = OrgTable()
    tab.printTable([data1,data2])
    fd = open(sys.argv[1])
    timeData = TimeData()
    curTag = None
#    timeSpent = 0
    for line in fd.readlines():
        orgLine = OrgLine(line)
        if orgLine.getLevel() == 1:
#            timeData.addTime(curTag, timeSpent)
            curTag = orgLine.getTag();
        timeData.addTime(curTag,orgLine.getClockTime())
#            timeSpent = 0
###        else:
#            timeSpent = timeSpent + orgLine.getClockTime()
        # elif orgLine.getClockTime() is not None:
        #     timeSpent = timeSpent + orgLine.getClockTime()
#    timeData.addTime(curTag, timeSpent)
    fd.close()
    timeData.debug_printData()
    timeData.pieChart("mytime.png")
    
