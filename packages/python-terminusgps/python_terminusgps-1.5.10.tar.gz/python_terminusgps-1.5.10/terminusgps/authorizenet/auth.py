from authorizenet.apicontractsv1 import merchantAuthenticationType
from authorizenet.constants import constants

from django.conf import ImproperlyConfigured, settings


def get_merchant_auth() -> merchantAuthenticationType:
    if not hasattr(settings, "MERCHANT_AUTH_LOGIN_ID"):
        raise ImproperlyConfigured("'MERCHANT_AUTH_LOGIN_ID' is required.")
    if not hasattr(settings, "MERCHANT_AUTH_TRANSACTION_KEY"):
        raise ImproperlyConfigured("'MERCHANT_AUTH_TRANSACTION_KEY' is required.")
    return merchantAuthenticationType(
        name=str(settings.MERCHANT_AUTH_LOGIN_ID),
        transactionKey=str(settings.MERCHANT_AUTH_TRANSACTION_KEY),
    )


def get_environment() -> str:
    if not hasattr(settings, "DEBUG"):
        raise ImproperlyConfigured("'DEBUG' is required.")
    return constants.SANDBOX if settings.DEBUG else constants.PRODUCTION
