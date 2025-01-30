import logging
import logging.config
import os
import sys
import tempfile
from datetime import datetime, timedelta

class LoggerConfig:
    def __init__(self, level='INFO', log_file_path=None):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.log_file_path = log_file_path
        
        # Clear existing handlers
        self.logger.handlers = []
        
        # Create formatter
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)-8s  %(message)s')
        
        # Always add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
        
        # Replace all logging methods with custom ones
        self._setup_custom_methods()
    
    def _log_with_capture(self, level, msg, *args, **kwargs):
        """Generic method to handle logging with capture parameter"""
        caller_frame = sys._getframe(2)
        msg = f"[{os.path.basename(caller_frame.f_code.co_filename)}:{caller_frame.f_lineno}] {msg}"
        
        # Check for capture flag in either args or kwargs
        should_capture = False
        actual_args = list(args)  # Convert to list for modification
        
        # Check if capture is in kwargs
        if 'capture' in kwargs:
            should_capture = kwargs.pop('capture')
        # Check if first arg is 1
        elif args and args[0] == 1:
            should_capture = True
            actual_args = actual_args[1:]  # Remove the capture flag
            
        # Log to console
        self.logger._log(level, msg, actual_args, **kwargs)
        
        # Additionally write to file if should_capture
        if should_capture and self.log_file_path:
            try:
                formatted_msg = msg % tuple(actual_args) if actual_args else msg
                with open(self.log_file_path, 'a') as f:
                    # Use the same formatter as the console handler
                    log_entry = self.formatter.format(logging.LogRecord(
                        name=self.logger.name,
                        level=level,
                        pathname='',
                        lineno=0,
                        msg=formatted_msg,
                        args=(),
                        exc_info=None
                    ))
                    f.write(f"{log_entry}\n")
            except Exception as e:
                self.logger.error(f"Failed to write to log file: {str(e)}")

    def _setup_custom_methods(self):
        """Setup custom methods for all logging levels"""
        def custom_debug(msg, *args, **kwargs):
            self._log_with_capture(logging.DEBUG, msg, *args, **kwargs)
        
        def custom_info(msg, *args, **kwargs):
            self._log_with_capture(logging.INFO, msg, *args, **kwargs)
        
        def custom_warning(msg, *args, **kwargs):
            self._log_with_capture(logging.WARNING, msg, *args, **kwargs)
        
        def custom_error(msg, *args, **kwargs):
            self._log_with_capture(logging.ERROR, msg, *args, **kwargs)
        
        def custom_critical(msg, *args, **kwargs):
            self._log_with_capture(logging.CRITICAL, msg, *args, **kwargs)
        
        def custom_traceback(exc_info=None):
            """Log exception details with file, line number and function name"""
            if exc_info is None:
                exc_info = sys.exc_info()

            try:
                if isinstance(exc_info, Exception):
                    tb = exc_info.__traceback__
                    exc_type = type(exc_info)
                    exc_value = exc_info
                else:
                    exc_type, exc_value, tb = exc_info
                
                import traceback
                tb_list = traceback.extract_tb(tb)
                
                error_msg = "======= TRACEBACK =======\n"
                error_msg += "Traceback (most recent call last):\n"
                
                for filename, line_no, function, text in tb_list:
                    error_msg += f"  File \"{filename}\", line {line_no}, in {function}\n"
                    if text:
                        error_msg += f"    {text}\n"
                
                error_msg += f"{exc_type.__name__}: {str(exc_value)}"
                self._log_with_capture(logging.ERROR, error_msg, capture=True)
                    
            except Exception as e:
                self.logger.error(f"Failed to log traceback: {str(e)}")
        
        def custom_config(log_file_path=None):
            """Configure or update logger settings"""
            if log_file_path:
                self.log_file_path = log_file_path                
            return self.log_file_path

        # Attach all custom methods to logger
        self.logger.debug = custom_debug
        self.logger.info = custom_info
        self.logger.warning = custom_warning
        self.logger.error = custom_error
        self.logger.critical = custom_critical
        self.logger.traceback = custom_traceback
        self.logger.config = custom_config

# Create log file
log_file = os.path.join(tempfile.gettempdir(), f'arlog_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
logger_config = LoggerConfig(level='DEBUG', log_file_path=log_file)
log = logger_config.logger


