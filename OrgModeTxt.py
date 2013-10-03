from texttable import *
import re



class OrgTable(object):
    """
    """
    
    def __init__(self, numberOfClumn,):
        """
        """
        self._table = Texttable()
        self._table.set_deco(Texttable.BORDER|Texttable.HEADER|Texttable.VLINES)
        self._table.set_cols_align(["l"]+["r"]*(numberOfClumn-1))
        self._headerData = None
        self._rowData = []

    def setHeaderData(self, headerData):
        self._headerData = headerData
#        self._table.set_cols_dtype(['t'])
    def addRowData(self, rowData):
        self._rowData.append(rowData)
    def printTable(self,):
        self._table.add_rows([self._headerData]+self._rowData)
        tableData = self._table.draw().split("\n")
        firstCol = True
        for item in tableData[1].split("|"):
            if len(item)==0:
                continue
            length = len(item) - 2
            if firstCol:
                item = item.strip().ljust(length)
                firstCol = False
            else:
                item = item.strip().rjust(length)
            print "|",item,
        print "|"
        border = re.compile("\+[-+\+]+")
        header = re.compile("\+[=+\+]+")
        for line in tableData[2:]:
            if border.match(line) is not None:
                continue
            if header.match(line) is not None:
                line = line.replace("=","-")
                line = re.sub(re.compile("^\+|\+$"),"|",line)
            print line
#        print tableData

def fileLink(filename):
    return "[["+filename+"]]"
            
if __name__ == '__main__':
    orgtable = OrgTable(3)
    orgtable.setHeaderData(["c1","c2","c3"])
    orgtable.addRowData([1,222222222,3])
    orgtable.addRowData([1,2,3])
    orgtable.printTable()
