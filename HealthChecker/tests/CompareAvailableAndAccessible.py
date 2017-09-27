import SCTools
import securitycenter, getpass


# compares sharable and viewable IPs of all assets within a logged in group.


HOST = "netvuln.wvu.edu"
# compares 2 pipe separated lists.
def compare( group_name, list1, list2): 
    # split the lists
    not_in_list1 = list()
    not_in_list2 = list()
    # list the assets
    for i in list1:
        if i not in list2:
            not_in_list2.append(i)
    for i in list2:
        if i not in list1:
            not_in_list1.append(i)

    data_dict = dict()
    data_dict["name"] = group_name
    not_in_list1.sort()
    not_in_list2.sort()
    data_dict["not in available"] = not_in_list1
    data_dict["not in accessible"] = not_in_list2
    return data_dict 


def pull_names( json_dict ):
    return list( map( lambda asset : asset["name"], json_dict ) )


def run( session, data=None ):

    if not data:
        groups = SCTools.get_groups( session )
    else:
        groups = data["groups"]
    data_list = list()
    for group in groups:
        if group["name"] != "Full Access" or \
           group["name"] != "WVU":
            # compare each row
            
            comparison = compare( str(group["name"]), pull_names( group["assets"] ), pull_names( group["definingAssets"] ) )
            if len( comparison["not in available"]) + len(comparison["not in accessible"]) != 0:
                data_list.append( comparison )

    # print the data to the console
    print "================| Compare Available and Accessible |================\n"
    if len( data_list ) == 0:
        print "\nall assets match!\n"
    for row in data_list:
        print "[" + row.pop( "name") + " ]"
        
        for key in row.keys():
            print key + ":"
            for item in row[key]:
                print "\t- " + item
    print "\n\n"


if __name__ == "__main__":
    session = securitycenter.SecurityCenter5( HOST )
    session.login( raw_input("username: "), getpass.getpass() )
    run( session )
    raw_input(" [ Hit enter to kill ] " )
