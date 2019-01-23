import os
os.environ["MPLCONFIGDIR"] = "/home/vagrant/.matplotlib"
import matplotlib.pyplot as plt
import iris
import iris.quickplot as qplt


def write_plot(cube, fname):
    plt.clf()
    print("Writing plot: {}".format(fname))
    qplt.pcolormesh(cube)
    # Add coastlines to the map
    plt.gca().coastlines()
    plt.savefig(fname)


def plot_input_data():
    fout = '../output1.png' 
    fname = 'inputs/source_ncs/ukcp18-land-prob-uk-25km-all.nc'
    full_cube = iris.load(fname)[2]
    cube = full_cube[0]
    write_plot(cube, fout)


def plot_output_data(pc):
    fout = '../output-{}.png'.format(pc)
    fname = 'fakedata/ukcp18/data/land-prob/uk/25km/rcp85/percentile/tasAnom/mon/latest/tasAnom_rcp85_land-prob_uk_25km_percentile_mon_20021201-20031130.nc'
    fname = 'fakedata/ukcp18/data/land-prob/uk/25km/rcp85/percentile/tasAnom/mon/latest/tasAnom_rcp85_land-prob_uk_25km_percentile_mon_20021201-20031130.nc'
    fname = 'fakedata/ukcp18/data/land-prob/uk/25km/rcp85/percentile/tasAnom/mon/latest/tasAnom_rcp85_land-prob_uk_25km_percentile_mon_20081201-20091130.nc'
    full_cube = iris.load(fname)[1]
    # Subset to get 1st time and percentile at 90th
    cube = full_cube[0].extract(iris.Constraint(percentile=pc))
    write_plot(cube, fout)


def main():
    plot_input_data()
    plot_output_data(pc=90)
    plot_output_data(pc=91)


if __name__ == "__main__":

    main()
