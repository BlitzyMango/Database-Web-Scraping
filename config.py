import cx_Oracle

username = 'example_username'
password = 'example_password'

# When the database uses am old-style Oracle SID “system identifier”, 
# and doesn't have a service name:
dsn = cx_Oracle.makedsn(hostname = 'dbhost.example.com',    # Host which Oracle Database service (SID) runs on
                        port = 1521,                        # Oracle Database port (default is port 1521)
                        service_name = 'orclpdb1')          # Name of the SID
encoding = 'UTF-8'