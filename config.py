import os

mysql = {
    'host': 'localhost',
    'user': os.environ.get('SQL_USER'),
    'password': os.environ.get('SQL_PWD')
}

sender_email = os.environ.get('EMAIL_ADDRESS')
sender_email_pwd = os.environ.get('EMAIL_PWD')


email_body = '''\
<!DOCTYPE html>
<html>
    <body>
        <p>Dear applicant,</p>
        <p>We acknowledge the receipt of your Expression of Interest to work with us.</p>
        <p>
            To apply formally, you are required to send online application, filling all relevant details, through our
            website.
            We
            are sending you an <b>Application Code</b> “{code}” required to be entered through our website, valid for a
            period
            of
            one week, excluding the date of creation of code. In case the application is not made within the stipulated time
            frame,
            fresh Expression of Interest is required to be made.
        </p>
        <p>
            You are required to fill online application form by visiting our website at the following link:
            <a href="google.com">localhost:5000/signup</a>.
            In case of any anomaly observed between the information provided at the time of Expression of Interest and
            application,
            the application is liable to rejected/disallowed for submission. However, this should not be construed as
            rejection;
            rather, the candidates are encouraged to apply afresh.
        </p>
        <p>Good Luck.</p>
        <p>
            Regards <br>
            Aabhas Kumar Jha <br>
            Proprietor (Flask Blog-Lib) <br>
        </p>
    </body>
</html>
'''
