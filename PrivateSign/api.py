from .signer import sign, sign_no_timestamp, timestamp

def sign_document(input_file, output_file, api_token, tenant_id, cert_type = 0):
    return sign(input_file, output_file, api_token, tenant_id, cert_type = 0)

def sign_document_no_timestamp(input_file, output_file, api_token, tenant_id, cert_type = 0):
    return sign_no_timestamp(input_file, output_file, api_token, tenant_id, cert_type = 0)

def timestamp_document(input_file, output_file, api_token, tenant_id):
    return timestamp(input_file, output_file, api_token, tenant_id)