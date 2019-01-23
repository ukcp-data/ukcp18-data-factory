# example of reading   /home/h03/hadto/ukcp18/src/operational/ports/merged_ports_03.txt
# and plotting locations as a check
import iris
import matplotlib.pyplot as plt
import iris.plot as iplt

import pandas

all_ports_df=pandas.read_fwf('/home/h03/hadto/ukcp18/src/operational/ports/merged_ports_03.txt', comment='#')
# Notice that Sheerness and Southend count as the same pixel in this work (i.e. (76, 103):
print all_ports_df[[0,1,2,3,4]]

#     iport increases from west  to  east, so that for example Exmouth is 51, Dover is  80
# but jport increases from north to south, so that for example Lerwick is 25, Dover is 106 

# load some data on the CS3 grid so we can check (data is bathymetry):
b=(iris.load_cube('/net/home/h03/hadto/ukcp18/src/operational/./ports/CS3_bathymetry_2017.nc')).copy()


# overwrite bathymetry tide gauge locations with a noticeable value 
for k, site in enumerate(all_ports_df.Site):
    i=all_ports_df.iport[k]
    j=all_ports_df.jport[k]
    b.data[j,i]=-999

# confirm that the noticeable values are at coastal locations, plus Scilly Isles and Jersey and Guernsey
iplt.pcolormesh(b)
plt.show()

iplt.pcolormesh(b)
# print and plot the pixel centres of each site:
blat=b.coord('latitude').points
blon=b.coord('longitude').points
for k, site in enumerate(all_ports_df.Site):
    i=all_ports_df.iport[k]
    j=all_ports_df.jport[k]
    print all_ports_df.Site[k], blon[i], blat[j]
    plt.scatter(blon[i], blat[j])
plt.show()

# consistent with the above remarks, confirm that blon is an increasing function:
plt.plot(blon)
plt.show()
# but blat is a decreasing function:
plt.plot(blat)
plt.show()

# Increments are 1/6 degree in lon:
blon[6]-blon[0] #  1.0
# and -1/9 degree in lat:
blat[9]-blat[0] # -1.0





