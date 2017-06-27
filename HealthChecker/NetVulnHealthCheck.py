import securitycenter, getpass
from tests import *

# log in
HOST = "netvuln.wvu.edu"
session = securitycenter.SecurityCenter5( HOST )
session.login( raw_input("username: "), getpass.getpass() )


# now, execute the following tests
print "\nBeginning Health check...\n"

data = SCTools.get_all( session, verbose = True )

CheckForBadScans.run( session, data=data )

CompareSharableAndViewable.run( session, data=data)

CheckForAssetsWithoutGroups.run( session, data=data)

CheckForAssetsNotInScans.run( session, data=data )

ScanResultCheck.run( session, data=data )

raw_input(" [ Hit enter to kill ]")
