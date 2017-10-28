#!/usr/bin/env python
import SCTools, securitycenter, getpass


HOST = ""


# returns true if theres an exception and a scan shouldnt be counted if theres
# a duplicate, such as unscheduled scans
def scan_exception( scan ):
    return ( scan["schedule"]["repeatRule"] == "" ) or \
           ( "Authenticated" in scan["policy"]["name"] ) or \
           ( "discovery" in scan["name"].lower() )# or \



def look_up_groups( asset_name, asset_data ):
    for asset in asset_data:
        if asset["name"] == asset_name:
            return list( map( lambda group: str( group["name"] ), asset["groups"] ) )
        
def run( session, data = None ):

    # create the variables based on whether they were given as a parameter
    if not data:
        asset_data = SCTools.get_assets( session , usable=False )
        scan_data = SCTools.get_scans( session )
    else:
        asset_data = data["assets"]
        scan_data = data["scans"]

    print "DEBUG: finished pulling data from SecurityCenter"
    
    # start with 0 for each asset
    asset_list = dict()
    for asset in asset_data:
        asset_list[ asset["name"] ] = list()


    for scan in scan_data:
        if not scan_exception( scan ):
            for asset in scan["assets"]:
                name = asset["name"]
                asset_list[name].append( scan["name"] )

    for asset_name in asset_list.keys():
        scan_list_for_asset = asset_list[ asset_name ]
        if len( scan_list_for_asset ) > 1:
            print asset_name, str( look_up_groups( asset_name, asset_data ) ) 
            for scan_name in scan_list_for_asset:
                print "\t",scan_name
            print

    print "======== tmp ============"
    for asset_name in asset_list.keys():
        scan_list_for_asset = asset_list[ asset_name ]
        if len( scan_list_for_asset ) > 1:
            if "AI" in look_up_groups( asset_name, asset_data)  and \
               "ITS - SUPPORT" in look_up_groups( asset_name, asset_data ):
                print asset_name

if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST )
    session.login(raw_input("username: "), getpass.getpass("password: ") )
    #data = SCTools.get_all( session, verbose = True )
    dbug = run( session )#, data = data )
    raw_input(" [ Hit enter to kill ] ")
    
