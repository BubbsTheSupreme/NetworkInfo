import argparse
from network_info import NetworkInfo 


if __name__ == "__main__":
	net_info = NetworkInfo("config.toml")

	parser = argparse.ArgumentParser(
		description="Keeps track of information involving my servers and ESXi virtual machines",
		prog="NetworkInfo"
	)
	parser.add_argument("--allvm", required=False, help="Returns all VM data", action="store_false")
	parser.add_argument("--newvm", required=False, help="Inserts new VM data into database, input is the number of entries you want to add.", type=int)
	parser.add_argument("--delvm", required=False, help="Removes VM data from database")
	parser.add_argument("--getvmip", required=False, help="Select VM by its IP")
	parser.add_argument("--getvmname", required=False, help="Select VM by its Name")
	parser.add_argument("--getvmbyos", required=False, help="Select many VM's by their OS")

	parser.add_argument("--allservers", required=False, help="Returns all server data", action="store_false")
	parser.add_argument("--newserver", required=False, help="Inserts new server data into database, input is the number of entries you want to add.", type=int)
	parser.add_argument("--getserverip", required=False, help="Select server by its IP")
	parser.add_argument("--getservername", required=False, help="Select server by its Name")
	parser.add_argument("--getserverbyos", required=False, help="Select servers by their OS")
	parser.add_argument("--getserverbyram", required=False, help="Select servers by their Memory")
	parser.add_argument("--getserverbycpu", required=False, help="Select servers by their CPU")
	parser.add_argument("--getserverbyvideo", required=False, help="Select servers by their Video Interface")
	parser.add_argument("--delserver", required=False, help="Removes server data from database")
	args = parser.parse_args()

	if args.allvm is not None:
		net_info.read_all_vms()
	if args.newvm is not None:
		for i in range(args.newvm):
			ip = input("VM IP: ")
			name = input("VM Name: ")
			os = input("VM OS: ")
			desc = input("VM Description: ")
			net_info.insert_vm_data(ip, name, os, desc)
	if args.getvmip is not None:
		net_info.get_server_by_ip(args.getvmip)
	if args.getvmname is not None:
		net_info.get_vm_by_name(args.getvmname)
	if args.getvmbyos is not None:
		net_info.get_vms_by_os(args.getvmbyos)
	if args.delvm is not None:
		net_info.delete_vm_data(args.delvm)
	
	if args.allservers is not None:
		net_info.read_all_servers()
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
			net_info.insert_server_data(ip, name, memory, cpu, storage, video, network_card, os, desc)
	if args.getserverip is not None:
		net_info.get_server_by_ip(args.getserverip)
	if args.getservername is not None:
		net_info.get_server_by_name(args.getservername)
	if args.getserverbyos is not None:
		net_info.get_servers_by_os(args.getserverbyos)
	if args.getserverbyram is not None:
		net_info.get_servers_by_memory(args.getserverbyram)
	if args.getserverbycpu is not None:
		net_info.get_servers_by_cpu(args.getserverbycpu)
	if args.getserverbyvideo is not None:
		net_info.get_servers_by_video(args.getserverbyvideo)
	if args.delserver is not None:
		net_info.delete_server_data(args.delserver)
		
	net_info.close()