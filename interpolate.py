def interpolate_data(x,y,n=10,k=3):
    import numpy as np
    from scipy.interpolate import make_interp_spline, BSpline
    xnew=[np.linspace(x[i],x[i+1],n) for i in range(len(x)-1)]
    xnew=np.reshape(xnew,(-1))
    spl = make_interp_spline(x, y, k=k) #BSpline object
    ynew = spl(xnew)
    return xnew,ynew