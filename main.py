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
						id INTEGER PRIMARY KEY AUTOINCREMENT,
						name TEXT,
						ip TEXT,
						operating_system TEXT,
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
				cur.execute(f"SELECT * FROM virtual_machines WHERE id = {id};")
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)

	def get_vm_by_ip(self, ip):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM virtual_machines WHERE ip = {ip};")
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)

	def get_vm_by_name(self, name):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM virtual_machines WHERE name = {name};")
				print(cur.fetchone())
		except Exception as e:
				logging.error(e)

	def get_vms_by_os(self, os):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM virtual_machines WHERE os = {os};")
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
				cur.execute(f"DELETE FROM virtual_machines WHERE id = {id};")
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
				cur.execute(f"SELECT * FROM servers WHERE id = {id};")
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)

	def get_server_by_ip(self, ip):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM servers WHERE ip = {ip};")
				print(cur.fetchone())
		except Exception as e:
			logging.error(e)			

	def get_server_by_name(self, name):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM servers WHERE name = {name};")
				return cur.fetchone()
		except Exception as e:
			logging.error(e)

	def get_servers_by_os(self, os):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM virtual_machines WHERE os = {os};")
				for record in cur:
					print(record)
		except Exception as e:
			logging.error(e)
	
	def get_servers_by_memory(self, memory):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM virtual_machines WHERE memory = {memory};")
				for i in cur.fetchall():
					print(i)
		except Exception as e:
			logging.error(e)
		
	def get_servers_by_cpu(self, processor):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM virtual_machines WHERE processor = {processor};")
				for i in cur.fetchall():
					print(i)
		except Exception as e:
			logging.error(e)

	def get_servers_by_video(self, video):
		try:
			with self.conn.cursor() as cur:
				cur.execute(f"SELECT * FROM virtual_machines WHERE video = {video};")
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
				cur.execute(f"DELETE FROM server WHERE id = {id};")
		except Exception as e:
			logging.error(e)


if __name__ == "__main__":
	network_info = NetworkInfo("config.toml")

	parser = argparse.ArgumentParser(
		description="Keeps track of information involving my servers and ESXi virtual machines",
		prog="NetworkInfo"
	)
	parser.add_argument("-nvm", "--newvm", nargs="+", required=False, help="Inserts new VM data into database")
	parser.add_argument("-dvm", "--delvm", required=False, help="Removes VM data from database")
	parser.add_argument("-gvip", "--getvmip", required=False, help="Select VM by its IP")
	parser.add_argument("-gvn", "--getvmname", required=False, help="Select VM by its Name")
	parser.add_argument("-gvbo", "--getvmbyos", required=False, help="Select many VM's by their OS")

	parser.add_argument("-ns", "--newserver", nargs="+", required=False, help="Inserts new server data into database")
	parser.add_argument("-gsip", "--getserverip", required=False, help="Select server by its IP")
	parser.add_argument("-gsn", "--getservername", required=False, help="Select server by its Name")
	parser.add_argument("-gsbo", "--getserverbyos", required=False, help="Select servers by their OS")
	parser.add_argument("-gsbm", "--getserverbyram", required=False, help="Select servers by their Memory")
	parser.add_argument("-gsbp", "--getserverbycpu", required=False, help="Select servers by their CPU")
	parser.add_argument("-gsbv", "--getserverbyvideo", required=False, help="Select servers by their Video Interface")
	parser.add_argument("-ds", "--delserver", required=False, help="Removes server data from database")
	args = parser.parse_args()

	if args.newvm is not None:
		network_info.insert_vm_data(args.newvm)
	if args.getvmip is not None:
		network_info.get_server_by_ip(args.getvmip)
	if args.getvmname is not None:
		network_info.get_vm_by_name(args.getvmname)
	if args.getvmbyos is not None:
		network_info.get_vms_by_os(args.getvmbyos)
	if args.delvm is not None:
		network_info.delete_vm_data(args.delvm)

	if args.newserver is not None:
		network_info.insert_server_data(args.newserver)
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