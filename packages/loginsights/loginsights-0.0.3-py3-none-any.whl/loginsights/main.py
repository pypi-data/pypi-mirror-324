import json
from datetime import datetime, UTC
from enum import IntEnum
from typing import Optional, Self
from azure.storage.queue import QueueClient

import requests

class LogLevel(IntEnum):
    DEBUG = 0
    VERBOSE = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    FATAL = 5


class LogInsightsLogger:
    __instance = None
    __credentials : Optional[dict] = None
    __queueClient : Optional[QueueClient] = None
    
    def __init__(self):
        return

    @classmethod
    def configure(cls, creds: dict):
        print(1111, creds.keys())
        if cls.__credentials is not None:
            return

        required_keys = {"ClientApplicationId", "ConnectionString", "Secret"}
        if not creds or not required_keys.issubset(creds.keys()):
            raise ValueError("Missing required credential fields.")
        cls.__credentials = creds

    @classmethod
    def __verify_configuration__(cls):
        response = requests.post("https://log-insights-fyp-g6g5ekdpcse2eefw.uksouth-01.azurewebsites.net/verify/client-application", json={
            "ClientApplicationId": cls.__credentials["ClientApplicationId"],
            "Secret": cls.__credentials["Secret"],
            "ConnectionString": cls.__credentials["ConnectionString"]
        }, verify=False)
        if response.status_code != 200:
            print(response.reason, response.status_code, response.raw)
            raise ValueError("Configuration for LogInsightsLogger is invalid.")
        return

    @classmethod
    def __create_azure_queue__(cls):
        cls.__queueClient =  QueueClient.from_queue_url(cls.__credentials["ConnectionString"])

    @classmethod
    def get_logger(cls) -> Self:
        if cls.__instance is None:
            print('Creating the object')
            cls.__instance = super(LogInsightsLogger, cls).__new__(cls)
            cls.__verify_configuration__()
            cls.__create_azure_queue__()
        return cls.__instance
    
    def __log__(self, level:LogLevel, message, properties=Optional[dict], exception=Optional[Exception], is_metric=False):
        log_entry = {
            "Language":"Python",
            "LogEvent":{
                "Timestamp": datetime.now(UTC).isoformat(),
                "Level": level,
                "Message": message,
                "Properties": properties,
                "Exception": exception,
            }
        }

        if log_entry["LogEvent"]["Properties"] is None:
            log_entry["LogEvent"]["Properties"] = {}
        log_entry["LogEvent"]["Properties"]["ClientApplicationId"] = self.__credentials["ClientApplicationId"]
        log_entry["LogEvent"]["Properties"]["MessageType"] = 1 if is_metric else 0
        
        log_message = json.dumps(log_entry)

        self.__queueClient.send_message(log_message)
    
    def debug(self, message, **kwargs):
        self.__log__(LogLevel.DEBUG, message, **kwargs)

    def add_metric(self, metric_name:str, properties:dict):
        separator = ";!"
        message_template_property_names = properties.keys()
        metric_props = {
            **properties,
            "MetricName": metric_name,
            "MessageTemplateProperties": separator.join(message_template_property_names)
        }
        message = " ".join(map(lambda x: "{x}", message_template_property_names))
        self.__log__(LogLevel.INFO, message=message, properties=metric_props, is_metric=True)
    
    def info(self, message, **kwargs):
        self.__log__("INFO", message, **kwargs)
    
    def warning(self, message, **kwargs):
        self.__log__("WARNING", message, **kwargs)
    
    def error(self, message, **kwargs):
        self.__log__("ERROR", message, **kwargs)
    
    def fatal(self, message, **kwargs):
        self.__log__("FATAL", message, **kwargs)