#! /usr/bin/python
"""changes all words for controlling filament advancment 'E' to 
more appropriet LinuxCNC join 'U' words
also changes argument names for the user defined M-codes"""
import sys

def main(argv):

  openfile = open(argv, 'r')
  file_in = openfile.readlines()
  openfile.close()

  file_out = []
  for l in file_in:
    line = l.rstrip('\n')
    #print line
    #if line[0] == ';':
    #  print 'hej'
    if line.find('E') != -1:
      words = line.split(' ')

      newArray = []
      for i in words:
        if i != '':          
            if i[0] == 'E':
               i = i.replace('E', 'U', 1)
          
        if len(i) > 0:
            newArray.append(i)
            
      line = ' '.join(newArray)
       
    elif line.find('M104 S') != -1:
        line = line.replace('M104 S', 'M104 P', 1)
        
    elif line.find('M106 S') != -1:
        line = line.replace('M106 S', 'M106 P', 1)
    
    elif line.find('M109 S') != -1:
        line = line.replace('M109 S', 'M109 P', 1)
        
    elif line.find('M140 S') != -1:
        line = line.replace('M140 S', 'M140 P', 1)
    
    # Cura seems to forget to divide the wait-value (Pxyz) with 1000
    # giving really long dwell-times
    elif line.find('G4') != -1:
        words = line.split('P')
        words[1] = str(float(words[1])/1000)
        line = 'P'.join(words)
        
    file_out.append(line)
      
  for item in file_out:
    print item

if __name__ == '__main__':
   main(sys.argv[1])
