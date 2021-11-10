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
from spamcheck.util import is_in_spam_list

print(is_in_spam_list('mary@dirt.com'))
# >> True
print(is_in_spam_list('joedirt@gmail.com'))
# >> True
print(is_in_spam_list('joe@DIRT.com'))
# >> True
print(is_in_spam_list('thom@radiohead.com'))
# >> False
```