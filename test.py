import SmellieRS as rs

for i in range(5,-1,-1):
    for j in range(5,-1,-1):
        rs.SetRSChannel(int(i)) # sets to outer loop start point
        print "Channel " + str(i) 
        rs.Execute()
        rs.SetRSChannel(int(j))
        print "Channel " + str(j) 
        rs.Execute()

print "changed to different order"

for i in range(0,6):
    for j in range(0,6):
        rs.SetRSChannel(int(i)) # sets to outer loop start point
        print "Channel " + str(i) 
        rs.Execute()
        rs.SetRSChannel(int(j))
        print "Channel " + str(j) 
        rs.Execute()
        
        
