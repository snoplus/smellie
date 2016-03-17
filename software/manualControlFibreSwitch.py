import fibreSwitch as fs

def setFibreSwitch(fs_input_channel,fs_output_channel):
    channel_number = ((fs_input_channel - 1) * 14) + fs_output_channel      # pick the correct channel number
    print(channel_number)
    fs.SetFSChannel(channel_number)

#Click F5 to run this script
#setFibreSwitch(input_channel,output_channel)
#input_channel is from 1 to 5 (inclusive)
#output_channel is from 1 to 15 (inclusive)
if __name__ == "__main__":
    setFibreSwitch(xx,yy)

