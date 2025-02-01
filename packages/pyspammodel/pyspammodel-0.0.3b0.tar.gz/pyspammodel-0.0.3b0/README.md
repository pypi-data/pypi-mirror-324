# pyspammodel
<!--Basic information-->
pyspammodel is a Python3 implementation of models of the X-ray, extreme and far ultraviolet radiation spectra of the Sun 
described by V.D. Nikolaeva. Solar-SPAM is an independent sub-model of the SPAM model and is intended for a wide range 
of uses. This model calculates the spectrum of extreme ultraviolet radiation in the wavelength range of 0-190 nm in 
intervals with a step of 1 nm.
Aero-SPAM is an independent sub-model of the SPAM model and is designed for astronomical calculations. This model 
calculates the spectrum of extreme ultraviolet radiation in the wavelength range of 5-105 nm. The spectrum 
is calculated for 20 intervals with a width of 5 nm and 17 separate lines (including the line Ly-alpha with 
λ = 121.6). The input parameter for both models is daily index F<sub>10.7</sub> (in s.f.u.). Using this parameter allows you 
to calculate solar radiation fluxes for any period of time.

If you use pyspammodel or SPAM model directly or indirectly, please, cite in your research the following paper:

1.  Nikolaeva, V.; Gordeev, E.  SPAM: Solar Spectrum Prediction for Applications and Modeling. Atmosphere 2023, 14, 226.
https://doi.org/10.3390/atmos14020226

## User's guide

<!--Users guide-->

### Installation

The following command is used to install the package:

```
python -m pip install pyspammodel
```

pyspammodel is the name of the package.

The package contains two classes: SolarSpam and AeroSpam.

### SolarSpam

This class is a implementation of the Solar-SPAM model of the photon energy flux spectrum for the wavelength range of 
0-190 nm in spectral bands of 1 nm each.

Input parameters:
- single value of the daily index F<sub>10.7</sub> (in s.f.u.). You can set one or more F<sub>10.7</sub> values.
Use a list to pass multiple values.

Output parameters:
- xarray dataset

```
<xarray.Dataset> Size: 8kB
Dimensions:           (band_center: 190, F107: 3, band_number: 190)
Coordinates:
  * band_center       (band_center) float64 2kB 0.5 1.5 2.5 ... 188.5 189.5
  * F107              (F107) float64 24B <F10.7 input values>
  * band_number       (band_number) int32 760B 0 1 2 3 4 ... 185 186 187 188 189
Data variables:
    euv_flux_spectra  (band_center, F107) float64 5kB <output spectrum values>
    line_lambda       (band_number) float64 2kB 0.5 1.5 2.5 ... 188.5 189.5
```

### SolarSpam usage example

- import the pyspammodel package;
- create an instance of the SolarSpam class;
- perform calculations with the created instance.

This class contains two methods for calculating the spectrum:
- get_spectral_bands() for calculating the spectrum in a wavelength interval;
- get_spectra() a method for unifying the use of a class with the AeroSpam class.


1. get_spectral_bands()
```
# importing a package with the alias spam
import pyspammodel as spam
# creating an instance of the SolarSpam class
example = spam.SolarSpam()
# calculate the spectrum values at F10.7 = 155.0 s.f.u. using get_spectral_bands()
spectrum = example.get_spectral_bands(155.)
# output the resulting spectrum
print(spectrum['euv_flux_spectra'])


<xarray.DataArray 'euv_flux_spectra' (band_center: 190, F107: 1)> Size: 2kB
array([[1.38379787e-05],
       [2.00129689e-04],
...
       [3.34889779e-03],
       [2.53368184e-03]])
Coordinates:
  * band_center  (band_center) float64 2kB 0.5 1.5 2.5 3.5 ... 187.5 188.5 189.5
  * F107         (F107) float64 8B 155.0
```

If you need to calculate the spectrum for several F<sub>10.7</sub> values, pass them using a list:

```
# calculate the spectrum values at F10.7 = 155.0 s.f.u. and F10.7 = 200.0 s.f.u. using get_spectral_bands()
spectra = example.get_spectral_bands([155., 200.])
# output the resulting spectra
print(spectra['euv_flux_spectra'])


<xarray.DataArray 'euv_flux_spectra' (band_center: 190, F107: 2)> Size: 3kB
array([[1.38379787e-05, 1.91147693e-05],
       [2.00129689e-04, 2.66188391e-04],
...
       [3.34889779e-03, 3.41110956e-03],
       [2.53368184e-03, 2.63010161e-03]])
Coordinates:
  * band_center  (band_center) float64 2kB 0.5 1.5 2.5 3.5 ... 187.5 188.5 189.5
  * F107         (F107) float64 16B 155.0 200.0
```

2. get_spectra()
This method is used to unify the use of the pyspammodel package classes. get_spectra() internally calls the 
get_spectral_bands() method with the parameters passed to get_spectra().

### AeroSpam

This class is a implementation of the Aero-SPAM model which is designed specifically for aeronomic research 
and provides a photon flux for 37 specific wavelength intervals (20 wave bands and 16 separate spectral lines 
within the range of 5–105 nm, and an additional 121.5 nm Lyman-alpha line).

Input parameters:
- single value of the daily index F<sub>10.7</sub> (in s.f.u.). You can set one or more F<sub>10.7</sub> values.
Use a list to pass multiple values.

Output parameters:
- xarray dataset

For calculations of the model by interval wavelength and by wavelength interval xarray is different:

```
# wavelength interval
<xarray.Dataset> Size: 888B
Dimensions:           (band_center: 20, F107: 1, band_number: 20)
Coordinates:
  * band_center       (band_center) float64 160B 7.5 12.5 17.5 ... 97.5 102.5
  * F107              (F107) float64 8B <F10.7 input values>
  * band_number       (band_number) int32 80B 0 1 2 3 4 5 ... 14 15 16 17 18 19
Data variables:
    euv_flux_spectra  (band_center, F107) float64 160B <output spectrum values>
    lband             (band_number) float64 160B 5.0 10.0 15.0 ... 95.0 100.0
    uband             (band_number) float64 160B 10.0 15.0 20.0 ... 100.0 105.0
    center            (band_number) float64 160B 7.5 12.5 17.5 ... 97.5 102.5


# wavelength line
<xarray.Dataset> Size: 484B
Dimensions:           (lambda: 17, F107: 1, line_number: 17)
Coordinates:
  * line_number       (line_number) int32 68B 0 1 2 3 4 5 ... 11 12 13 14 15 16
  * lambda            (lambda) float64 136B 25.6 28.4 30.3 ... 102.6 103.2 121.6
  * F107              (F107) float64 8B <F10.7 input values>
Data variables:
    euv_flux_spectra  (lambda, F107) float64 136B <output spectrum values>
    line_lambda       (line_number) float64 136B 25.6 28.4 30.3 ... 103.2 121.6
```

### AeroSpam usage example

This class contains three methods for calculating the spectrum:
- get_spectral_bands() for calculating the spectrum in a wavelength interval;
- get_spectral_lines() for calculating the spectrum for an individual wavelength;
- get_spectra() for calculating the spectrum in a wavelength interval and in an individual wavelength.

The steps of work are similar to the steps described for the SolarSpam class. 

Below is an example of working with the AeroSpam class:

1. get_spectral_bands()
```
# importing a package with the alias spam
import pyspammodel as spam
# creating an instance of the AeroSpam class
example = spam.AeroSpam()
# calculate the spectrum values at F10.7 = 155.0 s.f.u. using get_spectral_bands()
spectrum = example.get_spectral_bands(155.)
# output the resulting spectrum
print(spectrum['euv_flux_spectra'])


<xarray.DataArray 'euv_flux_spectra' (band_center: 20, F107: 1)> Size: 160B
array([[3.37198588e+11],
       [9.52514320e+12],
...
       [3.39380556e+13],
       [2.75864363e+13]])
Coordinates:
  * band_center  (band_center) float64 160B 7.5 12.5 17.5 ... 92.5 97.5 102.5
  * F107         (F107) float64 8B 155.0
```

If you need to calculate the spectrum for several F<sub>10.7</sub> values, pass them using a list:

```
# calculate the spectrum values at F10.7 = 155.0 s.f.u. and F10.7 = 200.0 s.f.u. using get_spectral_bands()
spectra = example.get_spectral_bands([155., 200.])
# output the resulting spectra
print(spectra['euv_flux_spectra'])


<xarray.DataArray 'euv_flux_spectra' (band_center: 20, F107: 2)> Size: 320B
array([[3.37198588e+11, 4.17408996e+11],
       [9.52514320e+12, 1.15589974e+13],
...
       [3.39380556e+13, 3.66626002e+13],
       [2.75864363e+13, 3.01543655e+13]])
Coordinates:
  * band_center  (band_center) float64 160B 7.5 12.5 17.5 ... 92.5 97.5 102.5
  * F107         (F107) float64 16B 155.0 200.0
```

2. get_spectral_lines()
```
# importing a package with the alias spam
import pyspammodel as spam
# creating an instance of the AeroSpam class
example = spam.AeroSpam()
# calculate the spectrum values at F10.7 = 155.0 s.f.u. using get_spectral_lines()
spectrum = example.get_spectral_lines(155.)
# output the resulting spectrum
print(spectrum['euv_flux_spectra'])


<xarray.DataArray 'euv_flux_spectra' (lambda: 17, F107: 1)> Size: 136B
array([[9.33579829e+12],
       [1.23749924e+13],
       [9.23118140e+13],
...
       [6.54897084e+13],
       [5.44081490e+15]])
Coordinates:
  * lambda   (lambda) float64 136B 25.6 28.4 30.3 36.8 ... 102.6 103.2 121.6
  * F107     (F107) float64 8B 155.0
```

If you need to calculate the spectrum for several Na values, pass them using a list:

```
# calculate the spectrum values at F10.7 = 155.0 s.f.u. and F10.7 = 200.0 s.f.u. using get_spectral_lines()
spectra = example.get_spectral_lines([155., 200.])
# output the resulting spectra
print(spectra['euv_flux_spectra'])


<xarray.DataArray 'euv_flux_spectra' (lambda: 17, F107: 2)> Size: 272B
array([[9.33579829e+12, 1.19780897e+13],
       [1.23749924e+13, 1.55517822e+13],
       [9.23118140e+13, 1.03186884e+14],
...
       [6.54897084e+13, 7.24188015e+13],
       [5.44081490e+15, 6.00590180e+15]])
Coordinates:
  * lambda   (lambda) float64 136B 25.6 28.4 30.3 36.8 ... 102.6 103.2 121.6
  * F107     (F107) float64 16B 155.0 200.0
```

3. get_spectra()

This method is used to unify the use of the pyspammodel package classes. get_spectra() internally calls the 
get_spectral_bands() and get_spectral_lines() method with the parameters passed to get_spectra(). The method returns 
a tuple of two datasets, the first element is a dataset from the get_spectral_bands() method, 
the second is a dataset from the get_spectral_lines() method. get_spectra() can accept either one or 
several values of F<sub>10.7</sub>.

```
# importing a package with the alias spam
import pyspammodel as spam
# creating an instance of the AeroSpam class
example = spam.AeroSpam()
# calculate the spectrum values at F10.7 = 155.0 s.f.u. using get_spectra()
spectrum = example.get_spectra(155.)
# output the resulting spectrum
print(spectrum)


(<xarray.Dataset> Size: 888B
Dimensions:           (band_center: 20, F107: 1, band_number: 20)
Coordinates:
  * band_center       (band_center) float64 160B 7.5 12.5 17.5 ... 97.5 102.5
  * F107              (F107) float64 8B 155.0
  * band_number       (band_number) int32 80B 0 1 2 3 4 5 ... 14 15 16 17 18 19
Data variables:
    euv_flux_spectra  (band_center, F107) float64 160B 3.372e+11 ... 2.759e+13
    lband             (band_number) float64 160B 5.0 10.0 15.0 ... 95.0 100.0
    uband             (band_number) float64 160B 10.0 15.0 20.0 ... 100.0 105.0
    center            (band_number) float64 160B 7.5 12.5 17.5 ... 97.5 102.5, <xarray.Dataset> Size: 484B

Dimensions:           (lambda: 17, F107: 1, line_number: 17)
Coordinates:
  * line_number       (line_number) int32 68B 0 1 2 3 4 5 ... 11 12 13 14 15 16
  * lambda            (lambda) float64 136B 25.6 28.4 30.3 ... 102.6 103.2 121.6
  * F107              (F107) float64 8B 155.0
Data variables:
    euv_flux_spectra  (lambda, F107) float64 136B 9.336e+12 ... 5.441e+15
    line_lambda       (line_number) float64 136B 25.6 28.4 30.3 ... 103.2 121.6)
```

Use tuple indexing using square brackets [] to get a specific dataset:

```
# calculate the spectrum values at F10.7 = 155.0 s.f.u. using get_spectra()
spectrum = example.get_spectra(155.)
# getting a dataset for the spectrum in the wavelength intervals
print(spectrum[0])


<xarray.Dataset> Size: 888B
Dimensions:           (band_center: 20, F107: 1, band_number: 20)
Coordinates:
  * band_center       (band_center) float64 160B 7.5 12.5 17.5 ... 97.5 102.5
  * F107              (F107) float64 8B 155.0
  * band_number       (band_number) int32 80B 0 1 2 3 4 5 ... 14 15 16 17 18 19
Data variables:
    euv_flux_spectra  (band_center, F107) float64 160B 3.372e+11 ... 2.759e+13
    lband             (band_number) float64 160B 5.0 10.0 15.0 ... 95.0 100.0
    uband             (band_number) float64 160B 10.0 15.0 20.0 ... 100.0 105.0
    center            (band_number) float64 160B 7.5 12.5 17.5 ... 97.5 102.5
```

4. predict()

This method calculates EUV spectrum from mixed dataset (containing intervals and lines together).

```
# importing a package with the alias spam
import pyspammodel as spam
# creating an instance of the AeroSpam class
example = spam.AeroSpam()
# calculate the spectrum values at F10.7 = 155.0 s.f.u. using predict()
spectrum = example.predict(155.)
# output the resulting spectrum
print(spectrum['euv_flux_spectra'])


<xarray.DataArray 'euv_flux_spectra' (band_center: 37, F107: 1)> Size: 296B
array([[3.37198588e+11],
       [9.52514320e+12],
       [9.32119976e+13],
...
       [6.54897084e+13],
       [2.75864363e+13],
       [5.44081490e+15]])
Coordinates:
  * band_center  (band_center) float64 296B 7.5 12.5 17.5 ... 103.2 102.5 121.6
  * F107         (F107) float64 8B 155.0
```

Just like the get_spectral_bands() and get_spectral_lines() methods, the predict() method supports passing the 
F<sub>10.7</sub> parameter as a list.


