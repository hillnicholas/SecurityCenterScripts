import SCTools
import securitycenter, getpass

HOST = ""

def get_scan_status( scan_status ):
    status = {
        0:"Active",
        1:"Disabled",
        2:"Invalid Repository",
        4:"Invalid Asset",
        8:"Invalid Policy",
        16:"Invalid Credential",
        32:"Invalid Option",
        64:"Invalid LCE",
        128:"Invalid Audit File",
        256:"Invalid Query",
        512:"Invalid User",
        1024:"Invalid Zone",
        2048:"Invalid Scan",
        4096:"Invalid Role",
        8192:"Invalid Attribute Set",
        16384:"Invalid Group",
        32768:"Never Run",
        65536:"Invalid ARC",
        131072:"Warning: Object is Calculating",
        262144:"Invalid Agent Scanner",
    }
    if int(scan_status) not in status.keys():
        return "unknown"
    else:
        return status[ int(scan_status) ]

    
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

    
