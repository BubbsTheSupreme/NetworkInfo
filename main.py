import psycopg2
import argparse
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

			with self.conn.cursor() as cur:
				cur.execute('''
					CREATE TABLE IF NOT EXISTS "virtual_machines" (
						id INTEGER SERIAL PRIMARY KEY,
						name TEXT,
						ip TEXT,
						operating_system TEXT,
						description TEXT,
					);

					CREATE TABLE IF NOT EXISTS "servers" (
						id INTEGER SERIAL PRIMARY KEY,
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
		except Exception as e:
			logging.error(e)

	def read_all_vms(self):
		try:
			with self.conn.cursor() as cur:
				cur.execute("SELECT * FROM virtual_machines;")
				for record in cur:
					print(record)
		except Exception as e:
			logging.error(e)

	def get_vm_by_id(self, id):
		try:	
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE id = %s;"
				cur.execute(query, (id,))
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)

	def get_vm_by_ip(self, ip):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE ip = %s;"
				cur.execute(query, (ip,))
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)

	def get_vm_by_name(self, name):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE name = %s;"
				cur.execute(query, (name,))
				print(cur.fetchone())
		except Exception as e:
				logging.error(e)

	def get_vms_by_os(self, os):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE os = %s;"
				cur.execute(query, (os,))
				for record in cur:
					print(record)
		except Exception as e:
			logging.error(e)

	def insert_vm_data(self, ip, name, os, desc):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f'''INSERT INTO virtual_machines (ip, name, description) 
								VALUES ({ip}, {name}, {os}, {desc})''')
		except Exception as e:
			logging.error(e)	
	
	def delete_vm_data(self, id):
		try:
			with self.conn.cursor() as cur:
				query = "DELETE FROM virtual_machines WHERE id = %s;"
				cur.execute(query, (id,))
		except Exception as e:
			logging.error(e)

	def read_all_servers(self):
		try:
			with self.conn.cursor() as cur:
				cur.execute("SELECT * FROM servers;")
				for record in cur:
					print(record)
		except Exception as e:
			logging.error(e)
		
	def get_server_by_id(self, id):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM servers WHERE id = %s;"
				cur.execute(query, (id,))
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)

	def get_server_by_ip(self, ip):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM servers WHERE ip = %s;"
				cur.execute(query, (ip,))
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)			

	def get_server_by_name(self, name):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM servers WHERE name = %s;"
				cur.execute(query, (name,))
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)

	def get_servers_by_os(self, os):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE os = %s;"
				cur.execute(query, (os,))
				for record in cur:
					print(record)
		except Exception as e:
			logging.error(e)
	
	def get_servers_by_memory(self, memory):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE memory = %s;"
				cur.execute(query, (memory,))
				for i in cur.fetchall():
					print(i)
		except Exception as e:
			logging.error(e)
		
	def get_servers_by_cpu(self, processor):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE processor = %s;"
				cur.execute(query, (processor,))
				for i in cur.fetchall():
					print(i)
		except Exception as e:
			logging.error(e)

	def get_servers_by_video(self, video):
		try:
			with self.conn.cursor() as cur:
				query = "SELECT * FROM virtual_machines WHERE video = %s;"
				cur.execute(query, (video,))
				for record in cur:
					print(record)
		except Exception as e:
			logging.error(e)

	def insert_server_data(self, ip, name, memory, processor, storage, video, network_interface, os, desc):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f'''INSERT INTO servers (ip, name, description) 
								VALUES ({ip}, {name}, {memory}, {processor}, {storage}, {video}, {network_interface}, {os}, {desc})''')
		except Exception as e:
			logging.error(e)

	def delete_server_data(self, id):
		try:
			with self.conn.cursor() as cur:
				query = "DELETE FROM server WHERE id = %s;"
				cur.execute(query, (id,))
		except Exception as e:
			logging.error(e)


if __name__ == "__main__":
	network_info = NetworkInfo("config.toml")

	parser = argparse.ArgumentParser(
		description="Keeps track of information involving my servers and ESXi virtual machines",
		prog="NetworkInfo"
	)
	parser.add_argument("--newvm", required=False, help="Inserts new VM data into database, input is the number of entries you want to add.", type=int)
	parser.add_argument("--delvm", required=False, help="Removes VM data from database")
	parser.add_argument("--getvmip", required=False, help="Select VM by its IP")
	parser.add_argument("--getvmname", required=False, help="Select VM by its Name")
	parser.add_argument("--getvmbyos", required=False, help="Select many VM's by their OS")

	parser.add_argument("--newserver", required=False, help="Inserts new server data into database, input is the number of entries you want to add.", type=int)
	parser.add_argument("--getserverip", required=False, help="Select server by its IP")
	parser.add_argument("--getservername", required=False, help="Select server by its Name")
	parser.add_argument("--getserverbyos", required=False, help="Select servers by their OS")
	parser.add_argument("--getserverbyram", required=False, help="Select servers by their Memory")
	parser.add_argument("--getserverbycpu", required=False, help="Select servers by their CPU")
	parser.add_argument("--getserverbyvideo", required=False, help="Select servers by their Video Interface")
	parser.add_argument("--delserver", required=False, help="Removes server data from database")
	args = parser.parse_args()

	if args.newvm is not None:
		for i in range(args.newvm):
			ip = input("VM IP: ")
			name = input("VM Name: ")
			os = input("VM OS: ")
			desc = input("VM Description: ")
			network_info.insert_vm_data(ip, name, os, desc)
	if args.getvmip is not None:
		network_info.get_server_by_ip(args.getvmip)
	if args.getvmname is not None:
		network_info.get_vm_by_name(args.getvmname)
	if args.getvmbyos is not None:
		network_info.get_vms_by_os(args.getvmbyos)
	if args.delvm is not None:
		network_info.delete_vm_data(args.delvm)

	if args.newserver is not None:
		for i in range(args.newserver):
			ip = input("Server IP: ")
			name = input("Server Name: ")
			os = input("Server OS: ")
			memory = input("Server Ram: ")
			cpu = input("Server CPU: ")
			storage = input("Server Storage: ")
			video = input("Server Video: ")
			network_card = input("Server Network Interface")
			operating_system = input("Server OS: ")
			desc = input("Server Description: ")
			network_info.insert_server_data(ip, name, memory, cpu, storage, video, network_card, os, desc)
	if args.getserverip is not None:
		network_info.get_server_by_ip(args.getserverip)
	if args.getservername is not None:
		network_info.get_server_by_name(args.getservername)
	if args.getserverbyos is not None:
		network_info.get_servers_by_os(args.getserverbyos)
	if args.getserverbyram is not None:
		network_info.get_servers_by_memory(args.getserverbyram)
	if args.getserverbycpu is not None:
		network_info.get_servers_by_cpu(args.getserverbycpu)
	if args.getserverbyvideo is not None:
		network_info.get_servers_by_video(args.getserverbyvideo)
	if args.delserver is not None:
		network_info.delete_server_data(args.delserver)