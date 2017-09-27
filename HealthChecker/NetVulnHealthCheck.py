import securitycenter, getpass
from tests import *

# log in
HOST = "netvuln.wvu.edu"
session = securitycenter.SecurityCenter5( HOST )

while True:
	try:
		session.login( raw_input("username: "), getpass.getpass() )
		break
	except Exception as e:
		print "API Error: " + str( e.msg )

# now, execute the following tests
print "\nBeginning Health check...\n"

data = SCTools.get_all( session, verbose = True )

#CheckForAssetsInMultipleScans.run( session, data = data )

CheckForBadScans.run( session, data=data )

CompareAvailableAndAccessible.run( session, data=data)

CheckForAssetsWithoutGroups.run( session, data=data)

CheckForAssetsNotInScans.run( session, data=data )

ScanResultCheck.run( session, data=data )

raw_input(" [ Hit enter to kill ]")
