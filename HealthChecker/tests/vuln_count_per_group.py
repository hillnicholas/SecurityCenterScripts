import securitycenter, SCTools, getpass


if __name__ == "__main__":
	session = securitycenter.SecurityCenter5("netvuln.wvu.edu")
	session.login( raw_input("username: " ), getpass.getpass() )

	data = SCTools.get_groups( session)

	query = {"query":{"name":"","description":"","context":"","status":-1,"createdTime":0,"modifiedTime":0,"group":{"id":0,"name":"Administrator"},"groups":[],"type":"vuln","tool":"sumasset","sourceType":"cumulative","startOffset":0,"endOffset":5000,"filters":[],"sortColumn":"score","sortDirection":"desc","vulnTool":"sumasset"},"sourceType":"cumulative","sortField":"score","sortDir":"desc","columns":[],"type":"vuln"}


	response = session.post("analysis", json=query).json()["response"]

	vulncount_db = dict()

	for asset in response["results"]:
	    asset_name = asset["asset"]["name"]
	    vulncount = None





