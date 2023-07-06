"""
Check that the installation worked correctly and that everything is ready for running
"""

# import hpvsim as hpv
# sim = hpv.Sim()
# sim.run()
# sim.plot()
#
import covasim as cv
sim = cv.Sim()
sim.run()
sim.plot()
