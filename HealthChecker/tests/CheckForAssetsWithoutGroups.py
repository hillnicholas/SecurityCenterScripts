import SCTools
import securitycenter, getpass

HOST = "netvuln.wvu.edu" 

# define exceptions here 
def exception( asset ):
    return ( "zzzz" in asset["name"].lower() ) or \
           ( asset["type"] != "static" )


def run( session, data = None ):

    if not data:
        # pull SC data, remove usable due to duplicates
        asset_list = SCTools.get_assets( session, usable=False )
    else:
        asset_list = data["assets"]
        
    # variables
    longest = 0
    assets_without_groups = list()

    # remove any exceptions
    data = list( filter( lambda asset: not exception( asset ), asset_list ) )

    for asset in data:
        if asset["name"] == "test delete": print asset["name"]
        
        # pull list of group names for each asset
        groups = list( map( lambda group: group["name"], asset["groups"] ) )
        # check the length of the shared groups
        if len( groups ) == 0:
            longest = max( longest, len( asset["name"] ) )
            assets_without_groups.append( asset )

    # format a pretty output
    table_out =  "{0:" + str( ( longest + 5 ) ) + "s} {1:6s}"
    print "=====================| assets without groups |=====================\n"
    if len( assets_without_groups ) > 0:
        print table_out.format("Asset name", "Tag")
        print table_out.format("----------", "---")
        for asset in assets_without_groups:
            print table_out.format( asset["name"], asset["tags"] )
    else:
        print "all assets have groups!"
    print "\n\n"        


if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST )
    session.login( raw_input("username: "), getpass.getpass() )
    run( session )
    raw_input(" [ Hit enter to kill ] " )
