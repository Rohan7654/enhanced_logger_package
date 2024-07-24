
import logging
import requests
import sqlite3
import json
import time
import functools
import tracemalloc
from xml.etree.ElementTree import Element, tostring

class EnhancedLogger:

    class TraceLogger(logging.Logger):
        def __init__(self, name, level=logging.DEBUG):
            super().__init__(name, level)

        def trace(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                self.debug(f"Entering: {func.__name__} with args: {args} and kwargs: {kwargs}")
                result = func(*args, **kwargs)
                self.debug(f"Exiting: {func.__name__} with result: {result}")
                return result
            return wrapper

    class HTTPHandler(logging.Handler):
        def __init__(self, url, method='POST', headers=None):
            super().__init__()
            self.url = url
            self.method = method
            self.headers = headers or {'Content-Type': 'application/json'}

        def emit(self, record):
            log_entry = self.format(record)
            try:
                response = requests.request(method=self.method, url=self.url, data=log_entry, headers=self.headers)
                response.raise_for_status()
            except requests.RequestException as e:
                self.handleError(record)

    class UniversalDBHandler(logging.Handler):
        def __init__(self, db_type, connection_params):
            super().__init__()
            self.db_type = db_type
            self.connection_params = connection_params
            self.conn = self.create_connection()

        def create_connection(self):
            if self.db_type == 'sqlite':
                return sqlite3.connect(self.connection_params['db_path'])
            elif self.db_type == 'mongodb':
                try:
                    import pymongo             
                except ImportError:
                    raise Exception(f'Module not found!! {pymongo}')
                return pymongo.MongoClient(self.connection_params['uri'])[self.connection_params['db_name']]
            elif self.db_type == 'postgres':
                try:
                    import psycopg2             
                except ImportError:
                    raise Exception(f'Module not found!! {psycopg2}')
                return psycopg2.connect(**self.connection_params)
            else:
                raise ValueError(f"Unsupported database type: {self.db_type}")

        def emit(self, record):
            log_entry = {
                'timestamp': self.formatTime(record, self.datefmt),
                'name': record.name,
                'level': record.levelname,
                'message': record.getMessage(),
            }
            if self.db_type == 'sqlite':
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO logs (timestamp, name, level, message) VALUES (?, ?, ?, ?)",
                            (log_entry['timestamp'], log_entry['name'], log_entry['level'], log_entry['message']))
                self.conn.commit()
            elif self.db_type == 'mongodb':
                self.conn['logs'].insert_one(log_entry)
            elif self.db_type == 'postgres':
                
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO logs (timestamp, name, level, message) VALUES (%s, %s, %s, %s)",
                            (log_entry['timestamp'], log_entry['name'], log_entry['level'], log_entry['message']))
                self.conn.commit()

    def close(self):
        if self.db_type == 'sqlite' or self.db_type == 'postgres':
            self.conn.close()
        super().close()

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                'timestamp': self.formatTime(record, self.datefmt),
                'name': record.name,
                'level': record.levelname,
                'message': record.getMessage(),
                'context': getattr(record, 'context', None),
                'function': record.funcName,
                'line_no': record.lineno,
            }
            return json.dumps(log_entry)

    class XMLFormatter(logging.Formatter):
        def format(self, record):
            log_entry = Element('log')
            for key, value in {
                'timestamp': self.formatTime(record, self.datefmt),
                'name': record.name,
                'level': record.levelname,
                'message': record.getMessage(),
                'context': getattr(record, 'context', None),
                'function': record.funcName,
                'line_no': record.lineno,
            }.items():
                element = Element(key)
                element.text = str(value)
                log_entry.append(element)
            return tostring(log_entry, encoding='unicode')

    class PerformanceLogger(logging.Logger):
        def __init__(self, name, level=logging.DEBUG):
            super().__init__(name, level)

        def log_performance(self, func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                tracemalloc.start()
                result = func(*args, **kwargs)
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                end_time = time.time()
                elapsed_time = end_time - start_time
                self.info(f"Function {func.__name__} executed in {elapsed_time:.4f} seconds. "
                          f"Current memory usage: {current / 10**6:.2f} MB; Peak: {peak / 10**6:.2f} MB")
                return result
            return wrapper

    @staticmethod
    def configure_trace_logger(name):
        logger = EnhancedLogger.TraceLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def configure_http_logger(name, url, method='POST', headers=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        http_handler = EnhancedLogger.HTTPHandler(url, method, headers)
        logger.addHandler(http_handler)
        return logger

    @staticmethod
    def configure_db_logger(name, db_type, connection_params):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        db_handler = EnhancedLogger.UniversalDBHandler(db_type, connection_params)
        logger.addHandler(db_handler)
        return logger

    @staticmethod
    def configure_json_logger(name):
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = EnhancedLogger.JsonFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def configure_xml_logger(name):
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = EnhancedLogger.XMLFormatter()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def configure_performance_logger(name):
        logger = EnhancedLogger.PerformanceLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    @staticmethod
    def configure_enhanced_performance_logger(name):
        logger = EnhancedLogger.PerformanceLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger
    
    @staticmethod
    def json_log(logger_name):
        formatter = EnhancedLogger.JsonFormatter()
        logger = EnhancedLogger.configure_logger(logger_name, formatter)
        
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                context_info = {
                    'context': {
                        'args': args,
                        'kwargs': kwargs
                    }
                }
                logger.info(f"Entering function {func.__name__}", extra=context_info)
                result = func(*args, **kwargs)
                logger.info(f"Exiting function {func.__name__} with result {result}", extra=context_info)
                return result
            return wrapper
        return decorator
    
    @staticmethod
    def configure_logger(name, formatter,):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger