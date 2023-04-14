import psycopg2
import tomli
import logging

class NetworkInfo:
	def __init__(self, file):
		with open(file, "r") as f:
			parsed_toml = tomli.loads(f.read())

		logging.basicConfig(filename=parsed_toml["logfile"])

		try:	
			self.conn = psycopg2.connect(
				dbname = parsed_toml["dbname"],
				user = parsed_toml["user"],
				password = parsed_toml["password"],
				host = parsed_toml["host"],
				port = parsed_toml["port"]
			)

			self.conn.autocommit = True

			with self.conn.cursor() as cur:
				cur.execute('''
					CREATE TABLE IF NOT EXISTS "virtual_machines" (
						id SERIAL PRIMARY KEY,
						name TEXT,
						ip INET,
						operating_system TEXT,
						description TEXT
					);
					
					CREATE TABLE IF NOT EXISTS "servers" (
						id SERIAL PRIMARY KEY,
						name TEXT,
						ip INET,
						memory TEXT,
						processor TEXT,
						storage TEXT,
						video TEXT,
						network_card TEXT,
						operating_system TEXT,
						description TEXT
					);
				''')

		except Exception as e:
			print(e)
			logging.error(e)

	def read_all_vms(self):
		try:
			with self.conn.cursor() as cur:
				cur.execute("SELECT * FROM virtual_machines;")
				for record in cur:
					print(record)
		except Exception as e:
			print(e)
			logging.error(e)

	def get_vm_by_id(self, id):
		try:	
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE id = %s;"
				cur.execute(query, (id,))
				print(cur.fetchone())
		except Exception as e:
			print(e)
			logging.error(e)

	def get_vm_by_ip(self, ip):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE ip = %s;"
				cur.execute(query, (ip,))
				print(cur.fetchone())
		except Exception as e:
			print(e)
			logging.error(e)

	def get_vm_by_name(self, name):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE name = %s;"
				cur.execute(query, (name,))
				print(cur.fetchone())
		except Exception as e:
				print(e)
				logging.error(e)

	def get_vms_by_os(self, os):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE operating_system = %s;"
				cur.execute(query, (os,))
				for record in cur:
					print(record)
		except Exception as e:
			print(e)
			logging.error(e)

	def insert_vm_data(self, ip, name, os, desc):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f'''INSERT INTO virtual_machines (ip, name, operating_system, description) 
								VALUES ('{ip}', '{name}', '{os}', '{desc}');''')
		except Exception as e:
			print(e)
			logging.error(e)	
	
	def delete_vm_data(self, id):
		try:
			with self.conn.cursor() as cur:
				query = "DELETE FROM virtual_machines WHERE id = %s;"
				cur.execute(query, (id,))
		except Exception as e:
			print(e)
			logging.error(e)

	def read_all_servers(self):
		try:
			with self.conn.cursor() as cur:
				cur.execute("SELECT * FROM servers;")
				for record in cur:
					print(record)
		except Exception as e:
			print(e)
			logging.error(e)
		
	def get_server_by_id(self, id):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM servers WHERE id = %s;"
				cur.execute(query, (id,))
				print(cur.fetchone())
		except Exception as e:
			print(e)
			logging.error(e)

	def get_server_by_ip(self, ip):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM servers WHERE ip = %s;"
				cur.execute(query, (ip,))
				print(cur.fetchone())
		except Exception as e:
			print(e)
			logging.error(e)			

	def get_server_by_name(self, name):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM servers WHERE name = %s;"
				cur.execute(query, (name,))
				print(cur.fetchone())
		except Exception as e:
			print(e)
			logging.error(e)

	def get_servers_by_os(self, os):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE operating_system = %s;"
				cur.execute(query, (os,))
				for record in cur:
					print(record)
		except Exception as e:
			print(e)
			logging.error(e)
	
	def get_servers_by_memory(self, memory):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE memory = %s;"
				cur.execute(query, (memory,))
				for i in cur.fetchall():
					print(i)
		except Exception as e:
			print(e)
			logging.error(e)
		
	def get_servers_by_cpu(self, processor):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE processor = %s;"
				cur.execute(query, (processor,))
				for i in cur.fetchall():
					print(i)
		except Exception as e:
			print(e)
			logging.error(e)

	def get_servers_by_video(self, video):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE video = %s;"
				cur.execute(query, (video,))
				for record in cur:
					print(record)
		except Exception as e:
			print(e)
			logging.error(e)

	def insert_server_data(self, ip, name, memory, processor, storage, video, network_interface, os, desc):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f'''INSERT INTO servers (ip, name, memory, processor, storage, video, network_card, operating_system, description, ) 
								VALUES ({ip}, {name}, {memory}, {processor}, {storage}, {video}, {network_interface}, {os}, {desc});''')
		except Exception as e:
			print(e)
			logging.error(e)

	def delete_server_data(self, id):
		try:
			with self.conn.cursor() as cur:
				query = "DELETE FROM server WHERE id = %s;"
				cur.execute(query, (id,))
		except Exception as e:
			print(e)
			logging.error(e)
	

	def close(self):
		self.conn.close()