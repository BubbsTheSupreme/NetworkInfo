import psycopg2
from argparse import ArgumentParser 
import tomli

class NetworkInfo:
	def __init__(self,file):
		with open(file, "r") as f:
			parsed_toml = tomli.loads(f.read())
		
		self.conn = psycopg2.connect(
			dbname = parsed_toml["dbname"],
			user = parsed_toml["user"],
			password = parsed_toml["password"],
			host = parsed_toml["host"],
			port = parsed_toml["port"]
		)

		with self.conn.cursor() as cur:
			cur.execute('''
				CREATE TABLE IF NOT EXISTS "virtual_machines" (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					name TEXT,
					ip TEXT,
					description TEXT,
				);

				CREATE TABLE IF NOT EXISTS "servers" (
					id INTEGER PRIMARY KEY AUTOINCREMENT,
					name TEXT,
					ip TEXT,
					memory TEXT,
					processor TEXT,
					storage TEXT,
					video TEXT,
					network_card TEXT,
					operating_system TEXT,
					description TEXT,
				);
			''')

	def read_all(self):
		with self.conn.cursor() as cur:
			cur.execute("SELECT * FROM virtual_machines;")
			for record in cur:
				print(record)
		

	def get_vm_by_id(self, id):
		with self.conn.cursor() as cur:
			cur.execute(f"SELECT * FROM virtual_machines WHERE id = {id};")
			return cur.fetchone()

	def get_vm_by_ip(self, ip):
		with self.conn.cursor() as cur:
			cur.execute(f"SELECT * FROM virtual_machines WHERE ip = {ip};")
			return cur.fetchone()

	def get_vm_by_name(self, name):
		with self.conn.cursor() as cur:
			cur.execute(f"SELECT * FROM virtual_machines WHERE name = {name};")
			return cur.fetchone()

	def insert_data(self, ip, name, desc):
		with self.conn.cursor() as cur:
			cur.execute(f'''INSERT INTO virtual_machines (ip, name, description) 
	       					VALUES ({ip}, {name}, {desc})''')
			
	def delete_data(self, id):
		pass


if __name__ == "__main__":
	network_info = NetworkInfo("config.toml")
	