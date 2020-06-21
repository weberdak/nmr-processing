#!/bin/csh

var2pipe -in fid \
 -noaswap  \
  -xN              3000  -yN               240  \
  -xT              1500  -yT               120  \
  -xMODE        Complex  -yMODE        Complex  \
  -xSW       100000.000  -ySW        33333.333  \
  -xOBS         175.950  -yOBS         175.950  \
  -xCAR           96.00  -yCAR           96.00  \
  -xLAB            C13x  -yLAB            C13y  \
  -ndim               2  -aq2D         States  \
  -out ./test.fid -verb -ov

sleep 5
