import logging
import json
import xml.etree.ElementTree as ET
import functools
import time
import psutil
import requests
import sqlite3

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
        formatted_log = json.dumps(log_entry, indent=4)
        return formatted_log

class XmlFormatter(logging.Formatter):
    def format(self, record):
        log_entry = ET.Element('log_entry')
        timestamp = ET.SubElement(log_entry, 'timestamp')
        timestamp.text = self.formatTime(record, self.datefmt)
        name = ET.SubElement(log_entry, 'name')
        name.text = record.name
        level = ET.SubElement(log_entry, 'level')
        level.text = record.levelname
        message = ET.SubElement(log_entry, 'message')
        message.text = record.getMessage()
        context = ET.SubElement(log_entry, 'context')
        context.text = json.dumps(getattr(record, 'context', None))
        function = ET.SubElement(log_entry, 'function')
        function.text = record.funcName
        line_no = ET.SubElement(log_entry, 'line_no')
        line_no.text = str(record.lineno)
        formatted_log = ET.tostring(log_entry, encoding='unicode')
        return formatted_log

class PerformanceLogger(logging.Logger):
    def __init__(self, name, level=logging.NOTSET):
        super().__init__(name, level)

    def log_performance(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            process = psutil.Process()
            start_memory = process.memory_info().rss
            result = func(*args, **kwargs)
            end_time = time.time()
            end_memory = process.memory_info().rss
            execution_time = end_time - start_time
            memory_usage = end_memory - start_memory
            self.info(f"Execution time: {execution_time} seconds")
            self.info(f"Memory usage: {memory_usage} bytes")
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

class EnhancedLogger:
    @staticmethod
    def configure_logger(name, formatter, log_to_file=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        if log_to_file:
            fh = logging.FileHandler(log_to_file)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        return logger

    @staticmethod
    def json_log(logger_name, log_to_file=None):
        formatter = JsonFormatter()
        logger = EnhancedLogger.configure_logger(logger_name, formatter, log_to_file)

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
    def configure_performance_logger(name, log_to_file=None):
        logger = PerformanceLogger(name)
        if log_to_file:
            fh = logging.FileHandler(log_to_file)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)
        return logger

    @staticmethod
    def configure_http_logger(name, url, method='POST', headers=None, log_to_file=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        http_handler = HTTPHandler(url, method, headers)
        logger.addHandler(http_handler)

        if log_to_file:
            fh = logging.FileHandler(log_to_file)
            fh.setLevel(logging.DEBUG)
            logger.addHandler(fh)

        return logger

    @staticmethod
    def configure_db_logger(name, db_type, connection_params):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        db_handler = UniversalDBHandler(db_type, connection_params)
        logger.addHandler(db_handler)
        return logger
