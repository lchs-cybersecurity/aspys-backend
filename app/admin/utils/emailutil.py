import smtplib

def send_assessment(org_id:str, assessment_id:str, login_server:str, email:str, password:str, recipients:list, contents:str):
    """
    Sends email assessments.
    """

    # Authenticate user
    server = smtplib.SMTP_SSL(login_server, 465)
    server.login(email, password)

    # Send emails, return all failed addresses
    failed = []
    for recipient in recipients:
        try:
            # Append email-open tracking element to contents
            contents_new = """ 
            <img src="https://veritas.computer/api/opentrack?org_id={0}&assessment_id={1}&address={2}">
            """.format(org_id, assessment_id, recipient)
            server.sendmail(email, recipient, contents_new)
        except:
            failed.append(email)

    server.close()
    return failed
