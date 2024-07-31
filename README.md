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
from spamcheck import SpamCheck
spamcheck = SpamCheck(request)

'''Run checks'''
print(spamcheck.is_in_spam_list('mary@dirt.com'))
# >> True
print(spamcheck.is_in_spam_list('joedirt@gmail.com'))
# >> True
print(spamcheck.is_in_spam_list('joe@DIRT.com'))
# >> True
print(spamcheck.is_in_spam_list('thom@radiohead.com'))
# >> False

print(spamcheck.has_spam_keywords('Message with a spammy keyword'))
# >> True
print(spamcheck.has_spam_keywords('A legit message'))
# >> False
```