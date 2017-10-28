import SCTools
from datetime import datetime
import securitycenter, getpass

HOST = ""

def pull_status( status_type, data ):
    list_out = list()
    for line in data:
        if line[ "status" ] == status_type:
            list_out.append( line )
    return list_out

def pull_errors( data ):
    return pull_status( "Error", data )

def pull_partials( data ):
    return pull_status( "Partial", data )

def date( timestamp ):
    return datetime.fromtimestamp( timestamp ).strftime( "%H:%M %m-%d-%Y" )



def run( session, data=None ):

    if not data:
        # grab data if not defined
        results = SCTools.get_scan_results( session )
    else:
        results = data["scan results"]

        
    # errors
    longest = 0
    for line in pull_errors( results ):
        longest = max( longest, len( line["name"] ) )
    print "===================| Scans with Runtime Errors |===================\n"
    table_out =  "{0:" + str( longest + 5 ) + "s} {1:6s}"
    print table_out.format( "Scan name", "Time of Error" )
    print table_out.format( "---------", "-------------" )
    for line in pull_errors( results ):
        print table_out.format( line["name"], date( int( line[ "finishTime" ] ) ) )

    print "\n\n"
    # partials
    longest = 0
    for line in pull_partials( results ):
        longest = max( longest, len( line["name"] ) )
    print "=========================| Partial Scans |=========================\n"
    table_out =  "{0:" + str( longest + 5 ) + "s} {1:6s}"
    print table_out.format( "Scan name", "End Time" )
    print table_out.format( "---------", "--------" )

    for line in pull_partials( results ):
        print table_out.format( line["name"], date( int( line[ "finishTime" ] ) ) )

    print "\n\n"


if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST  )
    session.login( raw_input("username: "), getpass.getpass() )
    run( session )
    raw_input(" [ Hit enter to kill ] " )
    
