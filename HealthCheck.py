import securitycenter, getpass, sys
import tests
from tests import *
import SCTools


def main():
    # log in
    HOST = raw_input("Host: ") if len(sys.argv) < 2 else sys.argv[1]
    session = securitycenter.SecurityCenter5( HOST )
    session.login( raw_input("username: "), getpass.getpass() )

    # now, execute the following tests
    print "\nBeginning Health check...\n"

    # grap data from SecurityCenter
    data = SCTools.get_all( session, verbose = True )

    # You can also disable checks here 
    dont_run = [ '__all__',
        '__builtins__',
        '__doc__',
        '__file__',
        '__name__',
        '__package__',
        '__path__',
        'files',
        'os',
        're']


    # run all modules added into tests/ directory
    map( 
        lambda test: getattr( getattr( tests, test), "run" )( session, data=data ),
        filter( 
            lambda test_name: test_name not in dont_run, dir(tests) 
        )
    )


if __name__ == "__main__":
    main()