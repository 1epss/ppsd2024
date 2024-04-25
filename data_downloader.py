import obspy
import numpy as np
from obspy import read, read_inventory, UTCDateTime
from obspy.clients.fdsn import Client

client = Client()


def data_downloader(network, station, location, channel, starttime, endtime, number):

    for i in range(number):

        print(starttime, endtime)
        
        st = client.get_waveforms(network, station, location, channel, starttime, endtime)
        chan = []
        
        if network == 'XA':
            for tr in st:
                chan.append(tr.stats.channel)
    
            if chan.count('MH1') >= 2:
                for tr in st.select(component = '1'):
                    st.merge(tr, fill_value = 'interpolate')
            
            if chan.count('MH2') >= 2:
                for tr in st.select(component = '2'):
                    st.merge(tr, fill_value = 'interpolate')
            
            if chan.count('MHZ') >= 2:
                for tr in st.select(component = 'Z'):
                    st.merge(tr, fill_value = 'interpolate')
            print(st)

            timeformat = starttime.strftime('%Y%m%d%H%M')
            st.write(network + "." + station + "." + str(location) + ".MH." + timeformat + ".mseed", format = "MSEED")
            
        if network == 'XB':
            for tr in st:
                chan.append(tr.stats.channel)
    
            if chan.count('BHU') >= 2:
                for tr in st.select(component = 'U'):
                    st.merge(tr, fill_value = 'interpolate')
            
            if chan.count('BHV') >= 2:
                for tr in st.select(component = 'V'):
                    st.merge(tr, fill_value = 'interpolate')
            
            if chan.count('BHW') >= 2:
                for tr in st.select(component = 'W'):
                    st.merge(tr, fill_value = 'interpolate')
        
            print(st)

            timeformat = starttime.strftime('%Y%m%d%H%M')
            st.write(network + "." + station + "." + str(location) + ".BH." + timeformat + ".mseed", format = "MSEED")

        starttime = starttime + (60 * 60 * 24)
        endtime = endtime + (60 * 60 * 24)
        
