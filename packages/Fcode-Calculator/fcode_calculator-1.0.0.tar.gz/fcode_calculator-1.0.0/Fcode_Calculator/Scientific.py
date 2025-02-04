import math

def speed(distance, time):
    """Calculate speed (distance/time)."""
    return distance / time

def time(distance, speed):
    """Calculate time (distance/speed)."""
    return distance / speed

def distance(speed, time):
    """Calculate distance (speed * time)."""
    return speed * time

def escape_velocity(planet):
    """Return escape velocity of a planet (in km/s)."""
    velocities = {'Mercury': 4.25, 'Venus': 10.36, 'Earth': 11.19, 'Mars': 5.03,
                  'Jupiter': 59.5, 'Saturn': 35.5, 'Uranus': 21.3, 'Neptune': 23.5}
    return velocities.get(planet, "Invalid planet name")

def newton_2nd_law(mass, acceleration):
    """Calculate force using Newton's Second Law (F = m * a)."""
    return mass * acceleration

def gravitational_force(G, m1, m2, r):
    """Calculate gravitational force (F = G * m1 * m2 / r²)."""
    return G * m1 * m2 / r**2

def einstein_mass_energy(mass):
    """Calculate energy using Einstein’s E = mc²."""
    c = 3 * 10**8
    return mass * c**2
