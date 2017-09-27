import securitycenter, getpass
import SCTools

HOST = "netvuln.wvu.edu"

# exceptions for assets that shouldnt be in scans go here
def scan_exception( asset ):
    return ( asset["type"] == "dynamic" ) or \
           ( asset["type"] == "combination" ) or \
           ( asset["tags"] == "wireless" ) or \
           ( asset["owner"]["username"] != "WVU" ) or \
           ( "ZZZZ" in asset["name"] ) or \
           ( "HSC (Reserved) NATTED" in asset["name"] ) or \
           ( "ZZZZ" in asset["name"] ) or \
           ( "TEC - RHNet" in asset["name"] ) or \
           ( "NSX" in asset["name"] ) or \
           ( "HSCNAT" in asset["name"] ) or \
           ( "OPEN" in asset["name"] ) or \
           ( "All Defined Ranges" in asset["name"] )           



def run( session, data = None):

    if not data:
        # grab some stored information if not defined
        asset_data = SCTools.get_assets( session , usable=False )
        scan_data = SCTools.get_scans( session )
    else:
        asset_data = data["assets"]
        scan_data = data["scans"]


    # remove non-scheduled scans
    scan_data = list(filter( lambda scan: scan["schedule"]["repeatRule"], scan_data))

    scanned_assets = set()
    not_scanned_assets = list()

    # collect the scanned assets
    for scan in scan_data:
        assets = scan["assets"]
        for asset in assets:
            scanned_assets.add( asset["name"] )

    longest = 0
    # check to see if each asset in SC is a scanned asset, also check exceptions
    for asset in asset_data:
        if not scan_exception( asset ) and \
           asset["name"] not in scanned_assets:
            longest = max( len(asset["name"]) , longest )
            if asset["name"] not in list(map( lambda a: a["name"], not_scanned_assets)):
                not_scanned_assets.append( asset )


    # format a pretty output
    table_out =  "{0:" + str( ( longest + 5 ) ) + "s} {1:6s}"
    print "=====================| assets that aren't in scans |=====================\n"
    if len( not_scanned_assets ) > 0:
        print table_out.format("Asset name", "Group")
        print table_out.format("----------", "-----")
        for asset in not_scanned_assets:
            print table_out.format( asset["name"],
                                    "|".join(list(map( lambda group: group["name"], asset["groups"]))) )
    else:
        print "all assets are in scheduled scans!"
    print "\n\n"





if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST )
    session.login(raw_input("username: "), getpass.getpass("password: ") )
    run( session )
    data = SCTools.get_assets( session )
    raw_input(" [ Hit enter to kill ] ")
