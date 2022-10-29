import time
import smtplib
import os
import pika
import json
from email.message import EmailMessage
import psycopg2

gmail_user = 'mpcs.uchicago.51205@gmail.com'
gmail_password = 'donkeykong51205'

sent_from = 'mpcs.uchicago.51205@gmail.com'
to = 'mpcs.uchicago.51205@gmail.com' # user email
subject = 'test' # email subject
body = "test 51205" #email body
headers = {'User-Agent':'Mozilla/5.0'}

email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, to, subject, body)

try:
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.connect('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_password)
except:
    print("gmail server failed")
    quit()

""" Connect to the PostgreSQL database server """
conn = None
try:
  # connect to the PostgreSQL server
  print('Connecting to the PostgreSQL database...')
  conn = psycopg2.connect(host="localhost",
                database="emails",
                user="postgres",
                password="Abcd1234")

  # create a cursor
  cur = conn.cursor()

# execute a statement
  cur.execute("SELECT EXISTS ( \
   SELECT FROM information_schema.tables \
   WHERE table_name   = 'emails' \
   )")

  # display the PostgreSQL database server version
  table_exists = cur.fetchone()
  print(table_exists)
  if table_exists[0] == False:
    print("emails table does not exist, now trying to create one ...")
    sql ="""
    CREATE TABLE emails (
             email_id SERIAL PRIMARY KEY,
             to_email_addr VARCHAR(255) NOT NULL,
             subject VARCHAR(255) NOT NULL,
             body TEXT default NULL);
    """
    cur.execute(sql)
    conn.commit() #fuck this ...
  else:
    print("emails table already exists, ok to proceed ..")

except (Exception, psycopg2.DatabaseError) as error:
  print(error)
  quit()

#server.sendmail(sent_from, to, email_text)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')

def callback(ch, method, properties, body):
    email = json.loads(body)
    msg = EmailMessage()
    msg.set_content(email['body'])

    msg['Subject'] = email['subject']
    msg['From'] = sent_from
    msg['To'] = email['to']

    #TODO call insert postgress here
    sql = """
    INSERT INTO emails(to_email_addr,subject,body) VALUES(%s,%s,%s) RETURNING email_id;
    """
    server.send_message(msg)
    cur.execute(sql, (email['to'],email['subject'],email['body']))
    print("new generated email id is ---> ",cur.fetchone()[0])
    conn.commit()
    print (msg)

channel.basic_consume(queue='email_queue',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
