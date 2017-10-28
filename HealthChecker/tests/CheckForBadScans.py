import SCTools
import securitycenter, getpass

HOST = ""

def get_scan_status( scan_status ):
    status = dict()
    status["0"] = "Active"
    status["1"] = "Disabled"
    status["2"] = "Invalid Repository"
    status["4"] = "Invalid Asset"
    status["8"] = "Invalid Policy"
    status["16"] = "Invalid Credential"
    status["32"] = "Invalid Option"
    status["64"] = "Invalid LCE"
    status["128"] = "Invalid Audit File"
    status["256"] = "Invalid Query"

    if scan_status not in status.keys():
        return "unknown"
    else:
        return status[ scan_status ]

    
# checks the scan statuses
def run( session, data=None ):
    if not data:
        scans = SCTools.get_scans( session )
    else:
        scans = data["scans"]
        
    bad_scans = list() 
    longest = 0

    ##### to be completed #####
    # filter and get table parameters
    for scan in scans:
        if scan["status"] != "0":
            bad_scans.append( scan )
            longest = max( longest, len( scan["name"] ) )
    # print the bad scans 
    print "=======================| Scans with Errors |=======================\n"
    table_out =  "{0:" + str( longest + 5 ) + "s} {1:6s}"
    print table_out.format( "Scan name", "Error code" )
    print table_out.format( "---------", "----------" )
    for scan in bad_scans: 
        print table_out.format( scan["name"], get_scan_status( scan["status"] ) )
    print "\n\n"


if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST )
    session.login( raw_input("username: "), getpass.getpass() )
    run( session )
    raw_input(" [ Hit enter to kill ] " )

    
