import time
import requests
import json
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


class RestClient:
    def __init__(self, base_url, headers=None):

        self.base_url = base_url
        requests.packages.urllib3.disable_warnings()
        self.http_session = requests.Session()
        self.http_session.headers = headers
        self.http_session.verify = False
        logger.info(f"Base usrl is: {self.base_url}")
        self.success_status_code = (200, 201, 202)

    def get_request(self, end_point, data=None, headers=None, json_data_fmt=False, params=None, fmt="json",
                    retries=0, response_with_status_code=False):
        """
        This method is to send get request
        Parameters:
            end_point (str): API endpoint/url
            data (dict): Body of a request
            headers (dict): Header of a request
            params (dict): parameters for a request
            retries (int): retries
            json_data_fmt (bool): True if data should be in json else False
            fmt (str): used for return response type
            response_with_status_code (bool): True if status code required else false
        Returns: response of the request
        """
        request_url = self.base_url+end_point
        logger.info(f"Request url is : {request_url}")
        if json_data_fmt:
            data = json.dumps(data)
        try:
            logger.info(f"Initializing GET rest call from {request_url}")
            get_response = self.http_session.get(request_url, params=params, headers=headers, data=data, verify=False)
            logger.info(f"GET Request Status code : {get_response.status_code}")
            if get_response.status_code in self.success_status_code:
                logger.info("GET request is successful..!")
                if fmt == "raw":
                    return get_response
                if response_with_status_code:
                    return self.parse_response(get_response), get_response.status_code
                return self.parse_response(get_response)
            else:
                logger.info(f"GET request Failed...! ")
                logger.info(f"Response Error Message: {self.parse_response(get_response)}")
                return self.parse_response(get_response), get_response.status_code
        except Exception as exc:
            if retries > 0:
                logger.info(f"GET request failed, retrying: {str(retries)} more times...")
                time.sleep(15)
                self.get_request(end_point=end_point, params=params, headers=headers, data=data,
                                 json_data_fmt=json_data_fmt, retries=retries - 1)
            else:
                logger.info(f"GET request failed..!")
                logger.exception(f"Exception occurred: {exc}")
                raise exc

    def post_request(self, end_point, data=None, headers=None, json_data_fmt=False, params=None,
                     fmt="json", retries=1, response_with_status_code=False):
        """
        This method is to send post request
        Parameters:
            end_point (str): API endpoint/url
            data : Body of a request
            headers (dict): Header of a request
            params (dict): parameters for a request
            fmt (str):Used for response type json or raw
            retries (int): no.of retires
            json_data_fmt : True if data should be in json else False
            response_with_status_code (bool):True if status code is required else False
        Returns: response of the request
        """
        request_url = self.base_url+end_point
        logger.info(f"Request url is : {request_url}")
        if json_data_fmt:
            data = json.dumps(data)
        try:
            logger.info(f"Initializing POST rest call from {request_url}")
            post_response = self.http_session.post(request_url, params=params, headers=headers, data=data, verify=False)
            logger.info(f"POST Request Status code: {post_response.status_code}")
            if post_response.status_code in self.success_status_code:
                logger.info("POST request is successful..!")
                if fmt == "raw":
                    return post_response
                if response_with_status_code:
                    return self.parse_response(post_response), post_response.status_code
                return self.parse_response(post_response)
            else:
                logger.info(f"POST request Failed...! ")
                logger.info(f"Response Error Message: {self.parse_response(post_response)}")
                return self.parse_response(post_response), post_response.status_code
        except Exception as exc:
            if retries > 0:
                logger.info(f"POST request failed, retrying: {str(retries)} more times...")
                logger.info("Waiting for 15 Sec...")
                time.sleep(15)
                self.post_request(end_point=end_point, data=data, headers=headers,
                                  json_data_fmt=json_data_fmt, fmt=fmt, retries=retries-1)
            else:
                logger.info("POST request failed..!")
                logger.exception(f"Exception Occurred: {exc}")
                raise exc

    def put_request(self, end_point, data=None, headers=None, json_data_fmt=False, params=None,
                    fmt="json", response_with_status_code=False):
        """
        This method is to send put request
        Parameters:
            end_point (str): API endpoint/url
            data (dict): Body of a request
            headers (dict): Header of a request
            params (dict): parameters for a request
            json_data_fmt (bool): True if data should be in json else False
            fmt (str):Used for response type json or raw
            response_with_status_code (bool):True if status code is required else False
        Returns: response of the request
        """
        request_url = self.base_url + end_point
        logger.info(f"Request url is : {request_url}")
        if json_data_fmt:
            data = json.dumps(data)
        try:
            logger.info(f"Initializing PUT rest call from {request_url}")
            put_response = self.http_session.put(request_url, params=params, headers=headers, data=data, verify=False)
            logger.info(f"PUT request Status Code: {put_response.status_code}")
            if put_response.status_code in self.success_status_code:
                logger.info("PUT request is successful..!")
                if fmt == "raw":
                    return put_response
                if response_with_status_code:
                    return self.parse_response(put_response), put_response.status_code
                return self.parse_response(put_response)
            else:
                logger.info(f"PUT request Failed...! ")
                logger.info(f"Response Error Message: {self.parse_response(put_response)}")
                return self.parse_response(put_response), put_response.status_code
        except Exception as exc:
            logger.info("PUT request is failed..!")
            logger.exception(f"Exception Occurred: {exc}")

    def delete_request(self, end_point, data=None, headers=None, json_data_fmt=False, params=None,
                       fmt="json", response_with_status_code=False):
        """
        This method is to send delete request
        Parameters:
            end_point (str): API endpoint/url
            data (dict): Body of a request
            headers (dict): Header of a request
            params (dict): parameters for a request
            json_data_fmt (bool): True if data should be in json else False
            fmt (str):Used for response type json or raw
            response_with_status_code (bool):True if status code is required else False
        Returns: response of the request
        """
        request_url = self.base_url + end_point
        logger.info(f"Request url is : {request_url}")
        if json_data_fmt:
            data = json.dumps(data)
        try:
            logger.info(f"Initializing GET rest call from {request_url}")
            delete_response = self.http_session.delete(request_url, params=params, headers=headers, data=data)
            logger.info(f"DELETE request Status Code: {delete_response.status_code}")
            if delete_response.status_code in self.success_status_code:
                logger.info("DELETE request is successful..!")
                if fmt == "raw":
                    return delete_response
                if response_with_status_code:
                    return self.parse_response(delete_response), delete_response.status_code
                return self.parse_response(delete_response)
            else:
                logger.info(f"PUT request Failed...! ")
                logger.info(f"Response Error Message: {self.parse_response(delete_response)}")
                return self.parse_response(delete_response), delete_response.status_code
        except Exception as exc:
            logger.info("DELETE request is failed..!")
            logger.exception(f"Exception Occurred: {exc}")

    @staticmethod
    def parse_response(resp):
        """
        This method is to parse a response from API.
        Parameters:
                resp:request response
        Returns: Json response of the response
        """
        try:
            return resp.json()
        except Exception as exc:
            logger.exception(f"Failed to parse response as JSON: {str(exc)}")
            time.sleep(5)
            raise exc
