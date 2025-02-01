from astropy.io import fits
from astropy.table import Table
import astronify
from .sim_lc import simulated_lc

def make_wavs_flat():
    # Flat versions.
    output_file = "outputs/flat_nonoise.fits"
    simulated_lc("flat", output_file, lc_length=500, lc_noise=0.1,
                     visualize=False, lc_yoffset=100.)
    output_file_noise_1 = "outputs/flat_nonoise-1.fits"
    simulated_lc("flat", output_file_noise_1, lc_length=500, lc_noise=1.,
           visualize=False, lc_yoffset=100.)
    output_file_noise_10 = "outputs/flat_nonoise-10.fits"
    simulated_lc("flat", output_file_noise_10, lc_length=500, lc_noise=10.,
           visualize=False, lc_yoffset=100.)

    with fits.open(output_file, mode="readonly") as hdulist:
        data = Table(hdulist[1].data)
    with fits.open(output_file_noise_1, mode="readonly") as hdulist:
        data_noise_1 = Table(hdulist[1].data)
    with fits.open(output_file_noise_10, mode="readonly") as hdulist:
        data_noise_10 = Table(hdulist[1].data)
    soni_obj = astronify.SoniSeries(data)
    soni_obj.sonify()
    soni_obj.play()
    soni_obj_noise_1 = astronify.SoniSeries(data_noise_1)
    soni_obj_noise_1.sonify()
    soni_obj_noise_10 = astronify.SoniSeries(data_noise_10)
    soni_obj_noise_10.sonify()
#    soni_obj.write("outputs/data_noise_0.wav")
#    soni_obj_noise_1.write("outputs/data_noise_1.wav")
#    soni_obj_noise_10.write("outputs/data_noise_10.wav")

if __name__ == "__main__":
    make_wavs_flat()
