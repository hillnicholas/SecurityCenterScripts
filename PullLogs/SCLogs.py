import securitycenter, getpass
import csv, datetime, re, argparse

'''
pulls SecurityCenter logs from the specified host under the system
account and exports the response to a CSV file.
'''

host = ""

# exports the response data to a csv file
def __export_logs_to_csv( logs, file_name ):

    # check filename
    if file_name[len(file_name) - 4:] != ".csv":
        file_name += ".csv"
    
    # remove nested features 
    for log in logs:
        # change organization to name
        log["organization"] = log["organization"]["name"]
        # change the initiator to the username
        log["initiator"] = log["initiator"]["username"]
        log["severity"] = log["severity"]["description"]

    # write the data
    with open( file_name,"wb") as f:
        w = csv.DictWriter( f, fieldnames = logs[0].keys() )
        w.writeheader()
        for log in logs:
            w.writerow( log )
        f.close()


# makes the HTTP POST request for the logs and returns the JSON response
def get_logs( session, no_of_logs ):
    year = datetime.datetime.now().strftime("20%y")
    month = datetime.datetime.now().strftime("%m")
    '''
    # severity IDs:
    # 2 - critical
    # 1 - warning
    
    JSON filter definition for severity logs:

    {"id":"severityLogs",
     "filterName":"severity",
     "operator":"=",
     "type":"scLog",
     "value":{"id" }
     
    '''
    response = session.post( "analysis", json={"query":
                                                {"name":"",
                                                 "description":"",
                                                 "context":"",
                                                 "status":-1,
                                                 "createdTime":0,
                                                 "modifiedTime":0,
                                                 "groups":[],
                                                 "type":"scLog",
                                                 "tool":"scLog",
                                                 "sourceType":"",
                                                 "startOffset":0,
                                                 "endOffset": no_of_logs,
                                                 "filters":[{"id":"date",
                                                             "filterName":"date",
                                                             "operator":"=",
                                                             "type":"scLog",
                                                             "isPredefined":True,
                                                             "value":{"id":"201706"}
                                                             },
                                                            {"id":"organization",
                                                             "filterName":"organization",
                                                             "operator":"=",
                                                             "type":"scLog",
                                                             "isPredefined":True,
                                                             "value":{"id":"0"}
                                                             }],
                                                 "sortColumn":"date",
                                                 "sortDirection":"desc"
                                                 },
                                                "sourceType":"scLog",
                                                "sortField":"date",
                                                "sortDir":"desc",
                                                "columns":[],
                                                "type":"scLog",
                                                "date":int(str(year)+str(month))}
                            ).json()["response"]
    logs = response["results"]
    return logs


# collect the args in based on the command line switches
def define_vars():
    
    # defaults
    file_name = "logs-" + datetime.datetime.now().date().isoformat() + ".csv"
    no_of_logs = 500
    global host
    
    parser = argparse.ArgumentParser(description='Extract the system logs from SecurityCenter.')

    parser.add_argument('-i',"--interactive", action="store_true",
                        help='Use the interactive menu')

    parser.add_argument('-n',"--number-of-logs", metavar='number_of_logs',type=int,
                        help='define the number of logs to retrieve (default: 500)')

    parser.add_argument('-o', "--output", metavar='output_filename', type=str,
                        help='define the output file name (default: logs-[current date].csv')

    parser.add_argument('-H', "--host", metavar='hostname',
                        type=str,
                        help='define the hostname of the SecurityCenter instance')
        
    args = parser.parse_args()

    #return args, None
    # if interactive option is chosen, continue to the interactive() method
    if args.interactive:
        no_of_logs, file_name, host = interactive()

    # if included, define variables
    if args.output:
        file_name = args.o
        
    if args.number_of_logs:
        no_of_logs = args.n

    if args.host:
        host = args.host

    return interactive(no_of_logs=no_of_logs, file_name=file_name, host=host)


# uses an interactive interface to get the parameters in rather than the flags/defaults
def interactive(host="",no_of_logs="",file_name=""):
    valid = False

    if no_of_logs == "":
        while not valid:
            no_of_logs = raw_input("type the number of logs to pull (default 500): ")
            valid = re.match("[0-9]{1,5}", no_of_logs)
            # exception:
            if no_of_logs == "":
                no_of_logs = 500
                valid = True
        no_of_logs = int( no_of_logs)

    if file_name == "":
        file_name = raw_input("type the filename or full path to save to: ")
        if file_name == "":
            file_name = "logs-" + datetime.datetime.now().date().isoformat() + ".csv"
        elif file_name[:len(file_name) - 4] != ".csv":
            file_name += ".csv"

    if host == "":
        while host == "":
            host = raw_input("type the hostname/domain of the SecurityCenter instance: ")
            
    return no_of_logs, file_name, host


    
if __name__ == "__main__":

    # get params
    no_of_logs, output_file, host = define_vars()

    # log in
    session = securitycenter.SecurityCenter5( host )
    print "A system account required."
    session.login(raw_input("username: "),getpass.getpass() )

    # get the logs
    print "exporting logs..."
    r = get_logs( session, no_of_logs )

    # write to file
    print "writing csv..."
    __export_logs_to_csv( r, output_file )
                          
