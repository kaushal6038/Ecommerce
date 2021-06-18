# NEXTMOTION - Marketplace #

### Installation ###
In your requirements.txt
``` 
...
django-crispy-forms==1.7.2
stripe==1.42.0
...
```

In your settings.py
```python
INSTALLED_APPS = {
    ...
    'crispy_forms',
    'nm_marketplace',
    'stripe',
    ...
}

# stripe settings
STRIPE_PUBLISHABLE_KEY = 'STRIPE LIVE PUB KEY'
STRIPE_SECRET_KEY = 'STRIPE LIVE SECRET KEY'

# nextmotion marketplace server
NEXTMOTION_MARKETPLACE_API_URL = 'http://nextmotion.herokuapp.com/api'
NEXTMOTION_MARKETPLACE_API_USER = 'staff@nextmotion.com'
NEXTMOTION_MARKETPLACE_API_PASSWORD = 'staff@nextmotion.com'
```
