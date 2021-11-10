# SpamCheck

SpamCheck is a tool to ignore emails by domain, email, or ip.

###  Django settings
```python
SPAM_DOMAINS = ['dirt.com']  # block entire domain
SPAM_EMAILS = ['joedirt@gmail.com']  # block specific email
SPAM_IPS = ['100.90.80.1']  # block from IP address
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