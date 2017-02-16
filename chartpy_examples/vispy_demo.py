__author__ = 'saeedamen'  # Saeed Amen

#
# Copyright 2016 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#

"""
This example generates several Brownian paths with millions of time steps. It then plots these using two different backends
- VisPy (GPU accelerated) backend
- matplotlib backend

For this number of points, VisPy will tend to be much quicker when manipulating the plot and zooming. Note, the VisPy
support is very limited at this stage in chartpy, and doesn't for example yet support date labels.

"""
from chartpy import Chart, Style
import numpy
import pandas

from math import sqrt
from scipy.stats import norm
import numpy as np


## from SciPy cookbook http://scipy.github.io/old-wiki/pages/Cookbook/BrownianMotion
def brownian(x0, n, dt, delta, out=None):
    """
    Generate an instance of Brownian motion (i.e. the Wiener process):

        X(t) = X(0) + N(0, delta**2 * t; 0, t)

    where N(a,b; t0, t1) is a normally distributed random variable with mean a and
    variance b.  The parameters t0 and t1 make explicit the statistical
    independence of N on different time intervals; that is, if [t0, t1) and
    [t2, t3) are disjoint intervals, then N(a, b; t0, t1) and N(a, b; t2, t3)
    are independent.

    Written as an iteration scheme,

        X(t + dt) = X(t) + N(0, delta**2 * dt; t, t+dt)


    If `x0` is an array (or array-like), each value in `x0` is treated as
    an initial condition, and the value returned is a numpy array with one
    more dimension than `x0`.

    Arguments
    ---------
    x0 : float or numpy array (or something that can be converted to a numpy array
         using numpy.asarray(x0)).
        The initial condition(s) (i.e. position(s)) of the Brownian motion.
    n : int
        The number of steps to take.
    dt : float
        The time step.
    delta : float
        delta determines the "speed" of the Brownian motion.  The random variable
        of the position at time t, X(t), has a normal distribution whose mean is
        the position at time t=0 and whose variance is delta**2*t.
    out : numpy array or None
        If `out` is not None, it specifies the array in which to put the
        result.  If `out` is None, a new numpy array is created and returned.

    Returns
    -------
    A numpy array of floats with shape `x0.shape + (n,)`.

    Note that the initial value `x0` is not included in the returned array.
    """

    x0 = np.asarray(x0)

    # For each element of x0, generate a sample of n numbers from a
    # normal distribution.
    r = norm.rvs(size=x0.shape + (n,), scale=delta * sqrt(dt))

    # If `out` was not given, create an output array.
    if out is None:
        out = np.empty(r.shape)

    # This computes the Brownian motion by forming the cumulative sum of
    # the random samples.
    np.cumsum(r, axis=-1, out=out)

    # Add the initial condition.
    out += np.expand_dims(x0, axis=-1)

    return out

if __name__ == '__main__':

    print('Generate paths')

    delta = 2       # The Wiener process parameter.
    T = 10.0        # Total time.
    N = 10 * 1000000    # Number of steps.
    dt = T/N        # Time step size
    m = 5           # Number of realizations to generate.

    x = numpy.empty((m,N+1)) # Create an empty array to store the realizations.

    x[:, 0] = 50    # Initial values of x.

    brownian(x[:,0], N, dt, delta, out=x[:,1:])

    t = numpy.linspace(0.0, N*dt, N+1)

    df = pandas.DataFrame(index=t, data=x.T)

    style = Style(save_fig=True)

    print('About to plot vispy...')
    # try vispy, which will work (uses GPU)
    Chart().plot(df, engine='vispy', style=style)

    print('About to plot matplotlib...')
    # try matplotlib, which will likely be very slow or crash...
    Chart().plot(df, engine='matplotlib', style=style)


