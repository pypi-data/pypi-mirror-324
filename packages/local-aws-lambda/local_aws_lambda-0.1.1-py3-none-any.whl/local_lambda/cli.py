# src/local_lambda/cli.py
import argparse
import json
from local_lambda.runtime import LocalLambda

def lambda_handler(event, context):
    """
    Sample Lambda function to test local execution.
    """
    return {"message": "Hello from Local AWS Lambda!", "event": event}

def main():
    parser = argparse.ArgumentParser(description="Simulate AWS Lambda locally.")
    parser.add_argument("--event", type=str, required=True, help="Path to event JSON file")
    
    args = parser.parse_args()

    # Read event from file
    with open(args.event, "r") as f:
        event = json.load(f)

    # Simulate Lambda execution
    lambda_sim = LocalLambda(lambda_handler)
    result = lambda_sim.invoke(event)

    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
