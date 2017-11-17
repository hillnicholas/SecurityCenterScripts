import securitycenter, getpass, sys
from tests import *

# log in
HOST = raw_input("Host: ") if len(sys.argv) < 2 else sys.argv[1]
session = securitycenter.SecurityCenter5( HOST )

session.login( raw_input("username: "), getpass.getpass() )


# now, execute the following tests
print "\nBeginning Health check...\n"

data = SCTools.get_all( session, verbose = True )

CheckForAssetsInMultipleScans.run( session, data = data )

CheckForBadScans.run( session, data=data )

CompareViewableAndAccessible.run( session, data=data)

CheckForAssetsWithoutGroups.run( session, data=data)

CheckForAssetsNotInScans.run( session, data=data )

ScanResultCheck.run( session, data=data )

raw_input(" [ Hit enter to kill ]")
