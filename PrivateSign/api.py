from .signer import cms, validate

def sign_document():
    return cms.sign()

def validate_signature():
    return validate.validate()
