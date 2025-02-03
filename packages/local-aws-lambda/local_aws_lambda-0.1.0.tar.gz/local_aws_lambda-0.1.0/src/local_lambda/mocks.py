# src/local_lambda/mocks.py
class MockS3:
    def __init__(self):
        self.storage = {}

    def put_object(self, Bucket, Key, Body):
        self.storage[Key] = Body
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    def get_object(self, Bucket, Key):
        if Key in self.storage:
            return {"Body": self.storage[Key]}
        return {"Error": "Object not found"}

class MockDynamoDB:
    def __init__(self):
        self.table = {}

    def put_item(self, TableName, Item):
        self.table[Item['id']] = Item
        return {"ResponseMetadata": {"HTTPStatusCode": 200}}

    def get_item(self, TableName, Key):
        return self.table.get(Key['id'], {"Error": "Item not found"})
