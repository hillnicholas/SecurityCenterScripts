#!/usr/bin/env python
import SCTools, securitycenter, getpass


HOST = "netvuln.wvu.edu"

# returns true if the exception exists
def exception( asset ):
    return (asset["type"] != "static")# or \
           #( "zzzz" in asset["name"].lower() )

def run( session, data = None ):
    # create the variables based on whether they were given as a parameter
    if not data:
        asset_data = SCTools.get_assets( session , usable=False )
    else:
        asset_data = data["assets"]

    for asset in asset_data:
        if not exception( asset) and asset["tags"] == "":
            print asset["name"]
            

        
if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST )
    session.login(raw_input("username: "), getpass.getpass("password: ") )
    #data = SCTools.get_all( session, verbose = True )
    run( session )#, data = data )
    raw_input(" [ Hit enter to kill ] ")
    
