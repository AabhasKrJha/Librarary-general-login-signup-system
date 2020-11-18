create_table_sql = '''CREATE TABLE IF NOT EXISTS {tablename}(
                            id INT(11) NOT NULL AUTO_INCREMENT UNIQUE KEY,
                            name varchar(225) NOT NULL,
                            libraryID varchar(225) PRIMARY KEY NOT NULL,
                            email varchar(225) UNIQUE KEY NOT NULL,
                            phone_number varchar(10) UNIQUE KEY NOT NULL,
                            password varchar(32) NOT  NULL
                        )'''

insert_table_data_sql = 'INSERT INTO {tablename}(name, libraryID, email, phone_number, password) VALUES(%s,%s,%s,%s,%s)'

create_authCode_table_sql = '''CREATE TABLE IF NOT EXISTS {tablename}(
                                    email varchar(225) UNIQUE KEY NOT NULL,
                                    code varchar(10) UNIQUE KEY NOT NULL,
                                    desination varchar(225) NOT  NULL
                                )'''

job_applicant_table_sql = '''CREATE TABLE IF NOT EXISTS {tablename}(
                                id INT(11) NOT NULL AUTO_INCREMENT UNIQUE KEY,
                                name varchar(225) NOT NULL,
                                email varchar(225) PRIMARY KEY NOT NULL,
                                phone_number varchar(10) UNIQUE KEY NOT NULL,
                                desination varchar(225) NOT  NULL
                        )'''

insert_job_applications_sql = 'INSERT INTO job_applicants(name, email, phone_number, desination) VALUES(%s,%s,%s,%s)'
