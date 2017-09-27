#!/usr/bin/env python
import SCTools, securitycenter, getpass


HOST = "netvuln.wvu.edu"


def run( session, data= None ):


    # create the variables based on whether they were given as a parameter
    if not data:
        asset_data = SCTools.get_assets( session , usable=False )
        group_data = SCTools.get_groups( session )
    else:
        asset_data = data["assets"]
        group_data = data["scans"]

    non_static_assets = list()
    
    for asset in asset_data:
        if asset["type"] != "static":
            non_static_assets.append( asset["name"] )

    for i in non_static_assets: print i
    groups_with_dynamic_assets = dict()
    for group in group_data:
        for asset in group["assets"]:
            if asset["name"] in non_static_assets:
                print "non-static asset shared: " + asset["name"]
                if group["name"] not in groups_with_dynamic_assets.keys():
                    groups_with_dynamic_assets[ group["name"] ] = list()
                groups_with_dynamic_assets.append( asset["name"] )


    return groups_with_dynamic_assets
        



if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST )
    session.login(raw_input("username: "), getpass.getpass("password: ") )
    #data = SCTools.get_all( session, verbose = True )
    dbug = run( session )#, data = data )
    raw_input(" [ Hit enter to kill ] ")
    
