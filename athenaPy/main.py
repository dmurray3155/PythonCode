import os
import boto3
from athena_utility import AthenaUtility


query = 'select * from yr2223_week_fd;'
session = boto3.Session(
    aws_access_key_id=os.getenv('aws_access_key_id'),
    aws_secret_access_key=os.getenv('aws_secret_access_key'),
    region_name='us-west-2'
)

athena_utils = AthenaUtility(session=session, filename='athena_config.conf', decorator='ATHENA_UTILITY')
data = athena_utils.query_results(query=query)

print("Result Data: ")
# print(data)

s3 = session.resource('s3')
athena_utils.delete_output(s3)  # This is for cleaning up the query result once data is fetched.

# This is modeled after noble_gases.py under C:\Users\DMAdmin\python\Rich
# This is better than a simple print(data)

from rich.console import Console
from rich.table import Table

console = Console()
table = Table(title="FD of Test Admins per Week")

table.add_column("Year", style="cyan", justify="center")
table.add_column("Date Reference", style="yellow", justify="center")
table.add_column("Week Number", style="green", justify="right")
table.add_column("Tests / Week", style="blue", justify="right")

for datum in data:
    table.add_row(
        datum["year"],
        str(datum["date_ref"]),
        str(datum["week_num"]),
        datum["total_counts_per_week"],
    )

console.print(table)