import boto3
import time

class TimeStream:

    def __init__ (self, dbName, tableName, region):
        self.dbName = dbName
        self.tableName = tableName
        self.region = region

    def write(self, temp):
        
        CURRENT_TIME = str(int(time.time() *1000))
        client = boto3.client('timestream-write', region_name=self.region)
        dimension = [{'Name': 'data_origin', 'Value': 'raspbery_pi'}]

        record = {
                    'Time': CURRENT_TIME,
                    'Dimensions': dimension,
                    'MeasureName': 'Temperature',
                    'MeasureValue': temp,
                    'MeasureValueType' : 'DOUBLE'
                 }

        records = [record]

        response = client.write_records(DatabaseName=self.dbName, TableName=self.tableName, Records=records)

        print("wrote to timestream")

