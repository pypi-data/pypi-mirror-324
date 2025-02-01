import astronify

def z():
    astronify.simulated_lc("flare", lc_ofile="outputs/flare_nonoise.fits",
                           visualize=True)

if __name__ == "__main__":
    z()
