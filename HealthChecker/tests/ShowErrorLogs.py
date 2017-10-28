import SCTools, getpass
import securitycenter

HOST = ""



def run( session ):
    logs = SCTools.get_logs( session )


    return logs
    












if __name__ == "__main__":
    
    session = securitycenter.SecurityCenter5(HOST)
    session.login(raw_input("username: "), getpass.getpass() )
    logs = run(session)
