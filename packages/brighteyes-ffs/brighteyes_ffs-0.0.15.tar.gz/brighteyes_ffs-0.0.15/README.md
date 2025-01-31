# BrightEyes-FFS

A toolbox for analysing Fluorescence Correlation Spectroscopy (FCS) and Fluorescence Fluctuation Spectroscopy (FFS) data with array detectors.
The fcs module contains libraries for:

* Calculating autocorrelations and cross-correlations of raw FCS/FFS data (i.e. photon counts vs. time)
* Fitting correlations to various 2D and 3D diffusion models
* Calibration-free FCS/FFS analysis such as circular-scanning FCS and iMSD analysis
* Miscellaneous tools

The fcs_gui module contains libraries for:

* Storing and loading FCS/FFS analysis sessions, as used in the GUI

The dataio module contains libraries for:

* Fitting various models to data (polynomial, Gaussian, power law, etc.)
* Stokes-Einstein relation
* Save/load 2D arrays to/from .csv files
* Save data to .tiff file
* Miscellaneous tools

----------------------------------

## Installation

You can install `brighteyes-ffs` via [pip] directly from [PyPI]:

    pip install brighteyes-ffs

or using the version on GitHub:

    pip install git+https://github.com/VicidominiLab/BrightEyes-FFS
	
or:
	
	pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple brighteyes-ffs

It requires the following Python packages

    h5py
	joblib
	matplotlib>=3.3.2
	multipletau>=0.3.3
	numpy>=1.19.4
	pandas>=1.1.4
	scipy
	tifffile>=2020.9.29
	seaborn
	imutils
	PyQt5
	qdarkstyle
	nbformat
	ome_types
	czifile
	brighteyes_ism

## Getting started 

### Calculating correlations

The variable *file* contains the data file (.h5 or .czi). The variable *accuracy* defines the number of points for which the correlation is calculated. The higher this number, the more points G contains. Note that accuracy does not (always) equal the number of points. The variable *split* contains the duration of a single chunk of data for which the correlation is calculated. E.g. for a 100 s time trace, split=20 will result in 5 correlations from a 20 s time trace each. The boolean *time_trace* defines whether or not the time trace should be returned. The variable *algorithm* defines the algorithm used to calculate the correlation. Valid options are 'multipletau' (time-based) and 'wiener-khinchin' (fft based).

The variable *list_of_g* contains the various correlations to be calculated. Acceptable entries are (i) integer numbers for calculating the autocorrelation of a given channel, (ii) a pre-defined string (such as 'central', 'sum3', and 'sum5') or (iii) a custom-made string with the following syntax 'Ca+b+...+cxd+...+e': starting with C (for Custom), then a list of channels to sum over (a+b+c), then x, then a second list of channels to sum over. E.g. 'C0+1x2+3' calculates tha cross-correlation between the sum of the channels 0 and 1 and the sum of channels 2 and 3. To calculate the autocorrelation, use simply 'Ca+b+c' (which is equivalent to 'Ca+b+cxa+b+c'). For cross-correlations of single channels, use 'xaabb' with aa and bb the two channel numbers (e.g. 'x0123' for the cross-correlation between channels 1 and 23).


	from brighteyes_ffs.fcs.fcs2corr import fcs_load_and_corr_split as correlate
	list_of_g = ['central', 'sum3', 'sum5']
	G, time_trace = correlate(file, list_of_g=list_of_g, accuracy=16, split=10, time_trace=True, algorithm='multipletau')

G is an object with 2D arrays (tau, G) for each correlation in list_of_g and each chunk of data, e.g. G.central_chunk0 contains the autocorrelation for the central detector element for the first chunk of data. G.central_average contains the average correlation for the central element over the whole data set.

### Fitting correlations

	from brighteyes_ffs.fcs.fcs_fit import fcs_fit
	fitresults = []
	for corr in list_of_g:
		Gsingle = getattr(G, corr + '_average')
		Gexp = Gsingle[1:,1]
		tau = Gsingle[1:,0]
		fitfun = 'fitfun_2c'
		fit_info = np.asarray([1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0]) # fit N, tauD, and offset (we fit with one component)
		param = np.asarray([1, 1, 1, 1, 1, 0, 0, 3, 0, 0, 0]) # starting values for all parameters
		lBounds = np.asarray([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])*(-1e6) # lower bounds for all parameters
		uBounds = np.asarray([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])*(1e6) # upper bounds for all parameters
		fitresult = fcs_fit(Gexp, tau, fitfun, fit_info, param, lBounds, uBounds, plotInfo=-1)
		fitresults.append(fitresult)

## License

Distributed under the terms of the [GNU GPL v3.0] license,
"BrightEyes-FFS" is free and open source software

## Contributing

You want to contribute? Great!
Contributing works best if you creat a pull request with your changes.

1. Fork the project.
2. Create a branch for your feature: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'My new feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request!
