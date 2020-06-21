# Python processing script for 13C-DARR spectrum
# Outputs Covariance and FT processed spectra for comparison
# Written by D. K. Weber (Veglia Lab), June 21 2020 
# Adapted from Nmrglue docs (https://nmrglue.readthedocs.io/en/latest/jbnmr_examples/s10_covariance_processing.html)

import nmrglue as ng

# Input NMRPipe FID
pipe_fid = 'test.fid'

# Filename base for .ft.ft2 and .cov.ft2 file
basename = 'darr'

# Read NMRPipe FID
dic, data = ng.pipe.read(pipe_fid)

# Process Direct dimension
dic, data = ng.pipe_proc.ext(dic, data, x1=1, xn=3000)
dic, data = ng.pipe_proc.em(dic, data, lb=100, c=1.0)
#dic, data = ng.pipe_proc.gm(dic, data, g1=10, g2=20, g3=0, c=1.0)
#dic, data = ng.pipe_proc.sp(dic, data, off=0.5, end=1.0, pow=1.0, c=1.0)
dic, data = ng.pipe_proc.zf(dic, data, size=8912)
dic, data = ng.pipe_proc.ft(dic, data, auto=True)
dic, data = ng.pipe_proc.ps(dic, data, p0=260.0, p1=0.0)
dic, data = ng.pipe_proc.di(dic, data)
# Cut direct dimension down to PPM range
uc_direct = ng.pipe.make_uc(dic, data, dim=1)
point_1 = uc_direct('{} ppm'.format(80))
point_2 = uc_direct('{} ppm'.format(0))
dic, data = ng.pipe_proc.ext(dic, data, x1=point_1, xn=point_2, sw=True)

# Copy for FT anc Covar processing
dic_ft, data_ft = dic, data
dic_c, data_c = dic, data

# Process indirect dimension by Fourier transform
dic_ft, data_ft = ng.pipe_proc.tp(dic_ft, data_ft)
#dic_ft, data_ft = ng.pipe_proc.ext(dic_ft, data_ft, x1=1, xn=60)
dic_ft, data_ft = ng.pipe_proc.sp(dic_ft, data_ft, off=0.5, end=1.0, pow=1.0, c=0.5)
dic_ft, data_ft = ng.pipe_proc.zf(dic_ft, data_ft, size=512)
dic_ft, data_ft = ng.pipe_proc.ft(dic_ft, data_ft, auto=True)
dic_ft, data_ft = ng.pipe_proc.ps(dic_ft, data_ft, p0=180.0, p1=0.0)
dic_ft, data_ft = ng.pipe_proc.di(dic_ft, data_ft)
dic_ft, data_ft = ng.pipe_proc.tp(dic_ft, data_ft)
ng.pipe.write('{}.ft.ft2'.format(basename), dic_ft, data_ft, overwrite=True)

# Process indirect dimension by covariance
dic_c, data_c = ng.pipe_proc.tp(dic_c, data_c)
#dic, data = ng.pipe_proc.ext(dic_c, data_c, x1=1, xn=36)
#dic, data = ng.pipe_proc.sp(dic_c, data_c, off=0.33, end=1.0, pow=1.0, c=1.0)
dic_c, data_c = ng.pipe_proc.di(dic_c, data_c)
dic_c, data_c = ng.pipe_proc.tp(dic_c, data_c)
data_c = np.cov(data_c.T).astype('float32')
dic_c['FDF1FTFLAG'] = dic_c['FDF2FTFLAG']
dic_c['FDF1ORIG'] = dic_c['FDF2ORIG']
dic_c['FDF1SW'] = dic_c['FDF2SW']
dic_c["FDSPECNUM"] = data_c.shape[1]

# Write NMRPipe covaraiance spectrum
ng.pipe.write('{}.cov.ft2'.format(basename), dic_c, data_c, overwrite=True)


