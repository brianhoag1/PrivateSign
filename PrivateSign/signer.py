import requests
from requests.auth import HTTPBasicAuth
import base64
import json
import os

from AuroraSign.aurora_signature.sign import signers, timestamps
from AuroraSign.aurora_signature.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from AuroraSign.aurora_certvalidator import ValidationContext
from AuroraSign.aurora_signature.keys import decrypt_data
from AuroraSign.aurora_signature.pdf_utils.format import format_date

def pplg_request(api_token, tenant_id, cert_type):
    url = 'http://127.0.0.1:5000/api/openapi/sdk-sign-info.json'
    params = {
        'tenant_id': tenant_id,
        'cert_type': cert_type
    }
    headers = {
        'X-Paperlogic-Authorization': api_token,
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return True, data['result']
    else:
        print("Error:", response.status_code, response.text)
        return False, response.text


def sign(input_file, output_file, api_token, tenant_id, cert_type = 0):
    print('Start signing...')
    
    try:
        res_check, res_data = pplg_request(api_token, tenant_id, cert_type)

        cert_bytes = base64.b64decode(res_data['_c'])
        private_key_bytes = decrypt_data(res_data['_k'], api_token)
        
        cms_signer = signers.SimpleSigner.load_bytes(private_key_bytes, cert_bytes)



        timestamp_info = json.loads(decrypt_data(res_data['_t'], api_token).decode('utf-8'))
        tst_client = timestamps.HTTPTimeStamper(
            timestamp_info['ts_url'], auth=HTTPBasicAuth(timestamp_info['ts_username'], timestamp_info['ts_password'])
        )

        vc = ValidationContext(
            allow_fetching=True
        )

        pdf_buffer = open(input_file, 'rb')
        w = IncrementalPdfFileWriter(pdf_buffer)

        sig_field_name = 'Signature1'
        user_info = res_data['user_info']
        formatted_datetime_str = format_date()
        reason = [
            'Date Time: %s' % formatted_datetime_str,
            'Signer Name: %s' % user_info['user_full_name'],
            'Company Name: %s' % user_info['user_company_name'],
            'Division: %s' % (user_info['division'] if user_info['division'] is not None else ''),
            'Email: %s' % user_info['user_email'],
        ]
        reason_text = ', '.join(reason)
        signature_metadata = signers.PdfSignatureMetadata(
            field_name=sig_field_name,
            reason=reason_text,
            embed_validation_info=True,
            validation_context=vc
        )

        with open(output_file, 'wb') as outf:
            signers.sign_pdf(
                w, 
                signature_metadata,
                signer=cms_signer, 
                timestamper=tst_client,
                output=outf
            )
    except Exception as ex:
        print('Exception', ex)

    finally:
        print('done')

def sign_no_timestamp(input_file, output_file, api_token, tenant_id, cert_type = 0):
    print('Start signing...')
    
    try:
        res_check, res_data = pplg_request(api_token, tenant_id, cert_type)

        print("==> 1")

        cert_bytes = base64.b64decode(res_data['_c'])
        private_key_bytes = decrypt_data(res_data['_k'], api_token)

        print("==> 2")
        
        cms_signer = signers.SimpleSigner.load_bytes(private_key_bytes, cert_bytes)

        print("==> 3")

        vc = ValidationContext(
            allow_fetching=True
        )

        print("==> 3.1")

        pdf_buffer = open(input_file, 'rb')
        w = IncrementalPdfFileWriter(pdf_buffer)

        print("==> 4")

        sig_field_name = 'Signature1'
        user_info = res_data['user_info']
        formatted_datetime_str = format_date()
        reason = [
            'Date Time: %s' % formatted_datetime_str,
            'Signer Name: %s' % user_info['user_full_name'],
            'Company Name: %s' % user_info['user_company_name'],
            'Division: %s' % (user_info['division'] if user_info['division'] is not None else ''),
            'Email: %s' % user_info['user_email'],
        ]
        reason_text = ', '.join(reason)

        print("==> 5")
        signature_metadata = signers.PdfSignatureMetadata(
            field_name=sig_field_name,
            reason=reason_text,
            embed_validation_info=True,
            validation_context=vc
        )

        print("==> 6")

        with open(output_file, 'wb') as outf:
            signers.sign_pdf(
                w, 
                signature_metadata,
                signer=cms_signer, 
                output=outf
            )

        print("==> 7")
    except Exception as ex:
        print('Exception', ex)

    finally:
        print('done')

def test(text = None):
    print('==> Test', text)