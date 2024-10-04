# from PrivateSign.signer.cms import sign
# from PrivateSign.signer.validate import validate

# __all__ = ['sign', 'validate']

from .signer import cms, validate

def sign_document():
    return cms.sign()

def validate_signature():
    return validate.validate()
