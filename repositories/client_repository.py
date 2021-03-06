from db.run_sql import run_sql

from models.client import Client
from models.consultant import Consultant
import repositories.consultant_repository as consultant_repository
import repositories.client_repository as client_repository
import repositories.assignment_repository as assignment_repository

def save(client):
    sql = "INSERT INTO clients(name,type_of_business,contact_details) VALUES (%s,%s,%s) RETURNING id"
    values = [client.name,client.type_of_business,client.contact_details]
    results = run_sql(sql,values)
    client.id = results[0]['id']
    return client

def select_all():
    clients = []
    sql = "SELECT * FROM clients"
    results = run_sql(sql)

    for row in results:
        client = Client(row['name'],row['type_of_business'],row['contact_details'],row['id'])
        clients.append(client)
    return clients

def select(id):
    client = None
    sql = "SELECT * FROM clients WHERE id = %s"
    values = [id]
    result = run_sql(sql,values)[0]

    if result is not None:
        client = Client(result['name'],result['type_of_business'],result['contact_details'],result['id'])
    return client

def delete_all():
    sql = "DELETE  FROM clients"
    run_sql(sql)

def delete(id):
    sql = "DELETE FROM clients WHERE id = %s"
    values = [id]
    run_sql(sql,values)

# Find the clients by the consultant
def clients(consultant):
    values = [consultant.id]
    sql = f"""
            SELECT clients.* FROM clients
            INNER JOIN assignments
            ON clients.id = assignments.client_id
            WHERE consultant_id = %s
            """
    results = run_sql(sql,values)
    clients = []
    for row in results:
        client = Client(row['name'],row['type_of_business'],row['contact_details'], row['id'])
        clients.append(client)
    return clients

def update(client):
    sql = "UPDATE clients SET (name,type_of_business,contact_details) = (%s,%s,%s) WHERE id = %s"
    values = [client.name,client.type_of_business,client.contact_details,client.id]
    run_sql(sql,values)

def total_client_spend():
    sql = f"""
            SELECT client_id, SUM(total_cost) FROM clients
            INNER JOIN assignments ON clients.id = assignments.client_id
            GROUP BY client_id
            """
    total_client_spend =run_sql(sql)
    return total_client_spend