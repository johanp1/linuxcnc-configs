#!/usr/bin/ python

import gtk
import gobject
import linuxcnc
import hal
import hal_glib
import xml.etree.ElementTree as ET

debug = 0

class XmlParser:
   def __init__(self, f):
      self.tree = []
      self.list = gtk.ListStore(int, str, str)

      self._parse_file(f)
      
   def get_parsed_data(self):
      return self.list
   
   def _parse_file(self, f):
      self.tree = ET.parse(f)
      root = self.tree.getroot()
            
      i = 0
      for func in root.iter('function'):
         gcode = func.find('gcode')
      
         # create the LinuxCNC hal pin and create mapping dictionary binding incomming events with data and the hal pins
         if gcode is not None:
            self.list.append([i, func.text, gcode.text])
            i = i+1

class HandlerClass:

    def on_destroy(self,obj,data=None):
        print "on_destroy, combobox active=%d" %(self.combo.get_active())
        self.halcomp.exit() # avoid lingering HAL component
        gtk.main_quit()

    def on_changed(self, combobox, data=None):
        print "on_changed %f %d" % (combobox.hal_pin_f.get(), combobox.hal_pin_s.get())

    def __init__(self, halcomp, builder, useropts):
        self.linuxcnc_status = linuxcnc.stat()
        self.linuxcnc_cmd = linuxcnc.command()
        self.halcomp = halcomp
        self.builder = builder
        self.useropts = useropts
        self.trigger = hal_glib.GPin(halcomp.newpin('trigger_pin', hal.HAL_BIT, hal.HAL_IN))
        self.trigger.connect('value-changed', self._trigger_change)
        
        self.combo = self.builder.get_object('hal_combobox1')
                
        func_list = XmlParser('func-btn.xml').get_parsed_data()

        self.combo.set_model(func_list)
        self.combo.set_entry_text_column(1)
        self.combo.set_active(0)
        
        renderer_text = gtk.CellRendererText()      
        self.combo.pack_start(renderer_text, True)
       
    def _trigger_change(self, pin, userdata = None):
        #setp gladevcp.trigger_pin 1
        #print "pin value changed to: " + str(pin.get())
        #print "pin name= " + pin.get_name()
        #print "pin type= " + str(pin.get_type())
        #print "active " + str(self.combo.get_active())
        if pin.get() is True:
            model = self.combo.get_model()
            self._send_mdi(model[self.combo.get_active()][2])

    def _ok_for_mdi(self):
        self.linuxcnc_status.poll()
        return not self.linuxcnc_status.estop and self.linuxcnc_status.enabled and (self.linuxcnc_status.homed.count(1) == self.linuxcnc_status.joints) and (self.linuxcnc_status.interp_state == linuxcnc.INTERP_IDLE)

    def _send_mdi(self, mdi_cmd_str):
        if self._ok_for_mdi():
            self.linuxcnc_cmd.mode(linuxcnc.MODE_MDI)
            self.linuxcnc_cmd.wait_complete() # wait until mode switch executed
            self.linuxcnc_cmd.mdi(mdi_cmd_str)
		
def get_handlers(halcomp, builder, useropts):

    global debug
    for cmd in useropts:
        exec cmd in globals()

    return [HandlerClass(halcomp, builder, useropts)]

