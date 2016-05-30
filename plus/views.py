'''
Major references:
1. Django Google API Sample:
https://github.com/google/google-api-python-client/tree/master/samples/django_sample

2. http://engineering.hackerearth.com/2014/06/07/using-google-apis-in-django/

3. python-social-auth LIBRARY
http://stackoverflow.com/questions/29058520/how-to-sign-in-with-the-google-api-using-django

4. http://www.marinamele.com/use-the-google-analytics-api-with-django

5. Storage Class
https://developers.google.com/api-client-library/python/guide/django#storage

6. Google Python Video
https://www.youtube.com/watch?v=IVjZMIWhz3Y
'''

'''EXTRA LIBRARY FILES FROM GMAIL'''
#from __future__ import print_function
from email.mime.text import MIMEText
from apiclient import errors

'''NECESSARY LIB FILES'''
import os
import logging
import httplib2

from googleapiclient.discovery import build
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.shortcuts import render
from plus.models import *
from test_django_original_try import settings
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_orm import Storage

# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), '..', 'gmail_client_secrets.json')

FLOW = flow_from_clientsecrets(
    CLIENT_SECRETS,
    scope='https://mail.google.com/',
    redirect_uri='http://127.0.0.1:8000/oauth2callback')



def index(request):

  '''I Have created a static user as I dont have any logged in user in my app right now'''
  U = User(
      username = 'example',
      firstname= 'Bla Bla',
      lastname= 'Bla Bla',
      email = 'example@gmail.com'
  )
  U.save()

  #This is a class created by google to save the credentials automatically in the database
  storage = Storage(CredentialsModel, 'id', U, 'credential')
  credential = storage.get()
  if credential is None or credential.invalid == True:
    FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
                                                   U)
    authorize_url = FLOW.step1_get_authorize_url()
    print(authorize_url)
    return HttpResponseRedirect(authorize_url)
  else:
    http = httplib2.Http()
    http = credential.authorize(http)
    service = build("gmail", "v1", http=http)

    '''results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])'''

    #GMAIL CHECK
    '''if not labels:
        print('No labels found.')
    else:
      print('Labels:')
      for label in labels:
        print(label['name'])
    ''''activities = service.activities()'''

    #FUNCTION CALL TO FIRST CREATE MESSAGE AND THEN SEND IT
    '''message_text = "Hello How are? Khana Khake Jana Hah!!"
    sender = ""
    to = "vaibhavsawhney1511@gmail.com"
    subject = "Invitation"
    message = CreateMessage(sender, to, subject, message_text,service)
    message = SendMessage(service,"me",message)
    print(message)
    print("Successful")
    return HttpResponse("Successful")'''

    message = ListMessagesMatchingQuery(service, 'me')
    #return message


def auth_return(request):
  '''The Token generated in index() should be validated here with the same user that was used to generate the token'''
  U = User(
      username = 'example',
      firstname= 'Bla Bla',
      lastname= 'Bla Bla',
      email = 'example@gmail.com'
  )
  '''
  Reference:
  1. https://github.com/tschellenbach/Django-facebook/pull/564
  2. encode() is used here because in Django 1.6 or less we used to get the string automatically
  but in Django 1.7+ we have to use encode() to get the string
  '''
  if not xsrfutil.validate_token(settings.SECRET_KEY, (request.GET['state']).encode('utf-8'),
                                 U):
    print("Test: 1")
    return  HttpResponseBadRequest()
  print("Test: 2")
  credential = FLOW.step2_exchange(request.GET)
  storage = Storage(CredentialsModel, 'id', U, 'credential')
  storage.put(credential)
  return HttpResponseRedirect("/")



'''Functions For GMAIL'''


def CreateMessage(sender, to, subject, message_text, service):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64 encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  x = base64.b64encode(message.as_bytes())
  x = x.decode()
  body = {'raw':x}
  return body


def SendMessage(service, user_id, message):
  """Send an email message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

  Returns:
    Sent Message.
  """
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id,
                                               q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
      messages.extend(response['messages'])

    #return messages
    for i in range(10):
        print(messages[i])
    m = GetMessage(service, 'me',messages[0]['id'])
    #GetMimeMessage(service,'me',messages[0]['id'])
    return m
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    print('Message snippet: %s' % message['snippet'])

    return message
  except errors.HttpError as error:
    print('An error occurred: %s' % error)


def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    print('Message snippet: %s' % message['snippet'])

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = httplib2.email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError as error:
    print('An error occurred: %s' % error)
