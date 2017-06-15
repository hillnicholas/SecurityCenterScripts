import securitycenter, getpass
from tests import *

# log in
HOST = "netvuln.wvu.edu"
session = securitycenter.SecurityCenter5( HOST )
session.login( raw_input("username: "), getpass.getpass() )



# now, execute the following tests
print "\nBeginning Health check...\n"

# This is a dict that contains all of the necessary SecurityCenter data for
# each test. This is done to prevent the tests from pulling the same data twice.
# If the optional "data" variable for each run method is not defined,
# the test will retrieve it on it's own.
data = SCTools.get_all( session, verbose = True )

CheckForBadScans.run( session, data=data )

CompareSharableAndViewable.run( session, data=data)

CheckForAssetsWithoutGroups.run( session, data=data)

CheckForAssetsNotInScans.run( session, data=data )

ScanResultCheck.run( session, data=data )

# This was added to force the terminal window will stay open after the tests are
# complete, if triggered by double-clicking the script on a windows machine.
raw_input(" [ Hit enter to kill ]")
