import time
from configparser import ConfigParser


class AthenaUtility:

    def __init__(self, session, filename, decorator):
        self.session = session
        self.params = self.read_config(filename=filename, decorator=decorator)

    @staticmethod
    def get_varchar_values(d):
        return [obj['VarCharValue'] for obj in d['Data']]

    # This function returns the output of the query and its location where the result is saved
    def query_results(self, query):
        client = self.session.client('athena')

        # Below code executes the query and returns the execution id for the running query
        resp_query_execution_id = client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={
                'Database': self.params['database']
            },
            ResultConfiguration={
                'OutputLocation': 's3://' + self.params['bucket'] + '/' + self.params['path']
            }
            # print(ResultConfiguration)
        )
        response_get_query_details = client.get_query_execution(
            QueryExecutionId=resp_query_execution_id['QueryExecutionId']
        )
        status = 'RUNNING'
        iterations = 180  # 15 mins
        while iterations > 0:
            iterations = iterations - 1
            response_get_query_details = client.get_query_execution(
                QueryExecutionId=resp_query_execution_id['QueryExecutionId']
            )
            status = response_get_query_details['QueryExecution']['Status']['State']
            if (status == 'FAILED') or (status == 'CANCELLED'):
                failure_reason = response_get_query_details['QueryExecution']['Status']['StateChangeReason']
                print(failure_reason)
                return False

            elif status == 'SUCCEEDED':

                # Below function is to get the output results
                resp_query_result = client.get_query_results(
                    QueryExecutionId=resp_query_execution_id['QueryExecutionId']
                )
                result_data = resp_query_result['ResultSet']
                if len(result_data['Rows']) > 1:
                    header = result_data['Rows'][0]
                    rows = result_data['Rows'][1:]

                    header = [obj['VarCharValue'] for obj in header['Data']]
                    result = [dict(zip(header, self.get_varchar_values(row))) for row in rows]
                    return result
                else:
                    return None
            else:
                time.sleep(5)

        return False

    @staticmethod
    def read_config(filename, decorator):
        parser = ConfigParser()
        parser.read(filename)
        confdict = {section: dict(parser.items(section)) for section in parser.sections()}
        return confdict[decorator]

    def delete_output(self, s3r):
        bucket = s3r.Bucket(self.params['bucket'])
        for obj in bucket.objects.filter(Prefix=self.params['path']):
            s3r.Object(bucket.name, obj.key).delete()
        print('****Output file deleted****')