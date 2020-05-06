from numpy import sum,array,sqrt,where,ones,bool_
from numpy.ma import masked_less,masked_where,getmaskarray
from numpy.ma import array as marray
from numpy.ma import ones as mones
from numpy.ma import empty as mempty
from pyproj import Proj
try:
 try:
  from netCDF4 import default_fillvals as fv
 except:
  from netCDF4 import _default_fillvals as fv
except:
  raise ImportError('Could not import netCDF4 default fill-values')
import sys

class UTMgrid:

    """
    Attributes:

        Proj (list of pyprpoj.Proj): 61 UTM projection zones
        lonlat (float array-like): lon/lat coordinates [No of points, 2]
        xy (float array-like): lonlat projections in 61 UTM zones [61,No. of Points,2]
    """

    def __init__(self,LonLat):

        """Set-Up projections to use.

        Args:
            LonLat )float array-like): lon/lat coordinates to project
                [No of points, 2]
        """

        self.Proj=[]
        self.lonlat=LonLat
        self.xy=[]
        for i in xrange(1,61): #loop over UTM zones
            #set up projection for each UTM zone:
            self.Proj.append(Proj(proj='utm',zone=i))
            #set up grid coordinates for each UTM zone:
            x,y=self.Proj[-1](LonLat[:,0],LonLat[:,1])
            self.xy.append(array([x,y]).transpose())

    def __call__(self,p):

        """Computes distances from p=[lon,lat] to each point of
        object grid (N,2) array with lon,lat coordinates using the UTMzone of
        p.

        Args:
            p(float array-like): point in lon,lat coordinates, shape (N,2)

        Returns:
            Distance of point p to grid points using UTM projection.
        """

        zone=UTMzone(p[0]) #find UTM zone for point p
        pxy=array([self.Proj[zone](p[0],p[1])]) #get projection [x,y] of p
        dz=self.xy[zone]-pxy
        return sqrt((dz**2).sum(1))

UTMzone=lambda lon:min(int((lon+180)/6),59) #UTMzone index (0-59)
