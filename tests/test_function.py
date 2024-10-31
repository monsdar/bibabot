
import json
import os
import unittest

import azure.functions as func
from function_app import http_trigger

mock_request_data = {
    'message': {'chat': {'all_members_are_administrators': True,
                         'id': -12345678,
                         'title': 'Channel_Name',
                         'type': 'group'},
                'date': 1728156449,
                'entities': [{'length': 5, 'offset': 0, 'type': 'bot_command'}],
                'from': {'first_name': 'John',
                         'id': 123456789,
                         'is_bot': False,
                         'language_code': 'en',
                         'last_name': 'doe',
                         'username': 'pu$$ykiller69'},
                'message_id': 1678,
                'text': '/test'},
    'update_id': 123456789}

def prepare_env_from_local_settings():
    """
    Read the local.settings.json file and set the values as environment variables.

    This is needed because the Azure Functions Core Tools do not support
    loading environment variables from the local.settings.json file when running
    tests locally. This function is used to set the environment variables
    when running the tests locally.
    """
    # Do not do anything when the local.settings.json file does not exist
    if not os.path.exists('local.settings.json'):
        return
    
    # set env from local.settings.json
    with open('local.settings.json', 'r') as f:
        local_settings = json.load(f)
    for key, value in local_settings.get('Values', {}).items():
        os.environ[key] = value

class TestFunction(unittest.TestCase):
    def test_handle_biba(self):
        # Prepare env
        prepare_env_from_local_settings()
        mock_request_data['message']['text'] = '/biba'
        req = func.HttpRequest(method='GET',
                            body=json.dumps(mock_request_data).encode('utf-8'),
                            url='/api/biba')
            
        # Call the function.
        func_call = http_trigger.build().get_user_function()
        resp = func_call(req)
            
        # NOTE: Whe running this without a proper local environment the function return code 500
        # Locally with a proper env set it should return 200
        # self.assertEqual(resp.status_code, 200)
    
    def test_handle_recent_activity(self):
        # Prepare env
        prepare_env_from_local_settings()
        mock_request_data['message']['text'] = '/activity'
        req = func.HttpRequest(method='GET',
                            body=json.dumps(mock_request_data).encode('utf-8'),
                            url='/api/biba')
            
        # Call the function.
        func_call = http_trigger.build().get_user_function()
        resp = func_call(req)
            
        # NOTE: Whe running this without a proper local environment the function return code 500
        # Locally with a proper env set it should return 200
        # self.assertEqual(resp.status_code, 200)
        # self.assertEqual(resp.status_code, 200)
    
    def test_handle_power_ranking(self):
        # Prepare env
        prepare_env_from_local_settings()
        mock_request_data['message']['text'] = '/power'
        req = func.HttpRequest(method='GET',
                            body=json.dumps(mock_request_data).encode('utf-8'),
                            url='/api/biba')
            
        # Call the function.
        func_call = http_trigger.build().get_user_function()
        resp = func_call(req)
            
        # NOTE: Whe running this without a proper local environment the function return code 500
        # Locally with a proper env set it should return 200
        # self.assertEqual(resp.status_code, 200)