from skyfield.api import load, wgs84
import turtle
import time


# stations_url = 'http://celestrak.org/NORAD/elements/stations.txt'
stations_url = 'stations.txt'
satellites = load.tle_file(stations_url)
by_name = {sat.name: sat for sat in satellites}


class Satellite:
    
    def __init__(self, name):
        self.satellite = by_name[name]
        self.sat_draw = turtle.Turtle()
        
        self.sat_draw.shape("iss.gif")
        self.sat_draw.penup()
    
    def latitude_longtitude(self, t):
        """ 
            input:  t current time
            return: satellite's latitude, longitude
        """
        geocentric = self.satellite.at(t)
        self.lat, self.lon = wgs84.latlon_of(geocentric)
        return float(self.lat.degrees), float(self.lon.degrees)

    def draw_satellite(self, t):
        self.lat, self.lon = self.latitude_longtitude(t)
        # Update the location of Satellite image on the map
        self.sat_draw.goto(self.lon, self.lat)


class Simulation:
    
    def __init__(self):
        """ 
            Setup the world map in turtle module
        """
        self.screen = turtle.Screen()
        self.screen.setup(1280, 720)
        self.screen.setworldcoordinates(-180, -90, 180, 90)     # Mark the boundaries of the screen
        self.screen.register_shape("iss.gif")
        # Load the world map image
        self.screen.bgpic("map.gif")
        self.ts = load.timescale()


    def run_simulation(self, *args):        
        while True:
            t_now = self.ts.now()
            for satellite in args:
                satellite.draw_satellite(t_now)

            time.sleep(5)


# Example of Satelites

simulation = Simulation()

sat_ISS =      Satellite('ISS (ZARYA)')
sat_AEROCUBE = Satellite('AEROCUBE 12B')
sat_NAUKA =    Satellite('ISS (NAUKA)')

simulation.run_simulation(sat_ISS, sat_AEROCUBE, sat_NAUKA)