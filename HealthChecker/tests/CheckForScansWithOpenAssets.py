#!/usr/bin/env python
import SCTools, securitycenter, getpass, re


HOST = "netvuln.wvu.edu"


# returns true if theres an exception and a scan shouldnt be counted if theres
# a duplicate, such as unscheduled scans
def scan_exception( scan ):
    return ( scan["schedule"]["repeatRule"] == "" ) or \
           ( "Authenticated" in scan["policy"]["name"] ) or \
           ( "discovery" in scan["name"].lower() )# or \
            #( "ITS-SUPPORT" in scan["name"] ) # temporary



def run( session, data = None ):

    # create the variables based on whether they were given as a parameter
    if not data:
        scan_data = SCTools.get_scans( session )
    else:
        scan_data = data["scans"]

    print "DEBUG: finished pulling data from SecurityCenter"

    '''
    for scan in scan_data:
        assets = scan["assets"]
        asset_list = list( map( lambda a: a["name"], assets ) )
    '''

    scans_with_opens = dict()
    for scan in scan_data:
        #scan = scan_data[47]
        assets = scan["assets"]
        #print scan["name"],"\n",map( lambda a: a["name"].encode("utf-8"), assets )
        open_assets = filter( lambda a_name: bool( re.match( "open", a_name.lower() ) ), map( lambda a: a["name"].encode("utf-8"), assets ) )
        if len(open_assets) != 0:
            scans_with_opens[ scan["name"] ] = open_assets

    print "==========| Scans with open ranges |============"
    for scan_name in scans_with_opens.keys():
        print "\n",scan_name
        for asset in scans_with_opens[ scan_name ]:
            print "\t",asset
    print "\n"
    
    '''

    for asset_name in asset_list.keys():
        scan_list_for_asset = asset_list[ asset_name ]
        if len( scan_list_for_asset ) > 1:
            if "AI" in look_up_groups( asset_name, asset_data)  and \
               "ITS - SUPPORT" in look_up_groups( asset_name, asset_data ):
                print asset_name
    # remove unnecessary junk, keep name and asset list only
    scan_list = dict()
    for scan in scan_data:
        scan_list[ scan["name" ] ] = 
    '''

    



if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST )
    session.login(raw_input("username: "), getpass.getpass("password: ") )
    #data = SCTools.get_all( session, verbose = True )
    dbug = run( session )#, data = data )
    raw_input(" [ Hit enter to kill ] ")
    
    scan_data = dbug
    '''
    scans_with_opens = dict()
    for scan in scan_data:
        #scan = scan_data[47]
        assets = scan["assets"]
        #print scan["name"],"\n",map( lambda a: a["name"].encode("utf-8"), assets )
        open_assets = filter( lambda a_name: bool( re.match( "open", a_name.lower() ) ), map( lambda a: a["name"].encode("utf-8"), assets ) )
        if len(open_assets) != 0:
            scans_with_opens[ scan["name"] ] = open_assets

    print "==========| Scans with open ranges |============"
    for scan_name in scans_with_opens.keys():
        print "\n",scan_name
        for asset in scans_with_opens[ scan_name ]:
            print "\t",asset
    '''
