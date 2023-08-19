# SpamCheck

SpamCheck is a tool to ignore emails by domain, email, or ip.

###  Django settings
```python
SPAMLIST_KEY_ID = ''  # S3/Spaces Key
SPAMLIST_SECRET_KEY = ''  # S3/Spaces Secret
SPAMLIST_BUCKET_NAME = ''  # S3/Spaces Bucket Name
SPAMLIST_REGION_NAME = 'sfo2'
SPAMLIST_ENDPOINT_URL = 'https://sfo2.digitaloceanspaces.com'
```

###Usage
```python
from spamcheck.util import is_in_spam_list, visitor_ip_address

'''Obtain IP address (optional)'''
ip_address = visitor_ip_address(request)

'''Run checks'''
print(is_in_spam_list('mary@dirt.com', ip_address))
# >> True
print(is_in_spam_list('joedirt@gmail.com', ip_address))
# >> True
print(is_in_spam_list('joe@DIRT.com', ip_address))
# >> True
print(is_in_spam_list('thom@radiohead.com', ip_address))
# >> False
```