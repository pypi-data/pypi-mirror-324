# src/local_lambda/runtime.py
import json
import time
import traceback

class LocalLambda:
    def __init__(self, function, timeout=3, memory=128):
        """
        Simulates an AWS Lambda execution environment.
        :param function: Lambda function to execute
        :param timeout: Maximum execution time in seconds
        :param memory: Simulated memory allocation (not enforced)
        """
        self.function = function
        self.timeout = timeout
        self.memory = memory

    def invoke(self, event, context=None):
        """
        Executes the Lambda function with a given event.
        """
        try:
            start_time = time.time()
            response = self.function(event, context)
            end_time = time.time()
            
            if end_time - start_time > self.timeout:
                raise TimeoutError("Function execution timed out!")

            return {
                "statusCode": 200,
                "executionTime": round(end_time - start_time, 3),
                "response": response
            }
        except Exception as e:
            return {
                "statusCode": 500,
                "error": str(e),
                "traceback": traceback.format_exc()
            }
