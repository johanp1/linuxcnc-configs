#!/usr/bin/ python
import gtk
import gobject

class ToolTableParser:
    def __init__(self, f):
        self.f = open(f, 'r')
        self.list = gtk.ListStore(int, str, str)

    def __del__(self):
        self.f.close()
    
    def parse(self):
        lines = self.f.readlines()

        i = 0
        for line in lines:
            self.list.append([i, line[0:2], line.split(';')[1])
            i = i+1


ttp = ToolTableParser('sim_mm.tbl')
ttp.parse()
  