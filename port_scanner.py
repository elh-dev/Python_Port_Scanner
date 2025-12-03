import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
debug = 0

#Debuging
def debug_option(x, debug):
    if debug == 1:
        print(x)

#####-Visualiser-#####
def menu_pading(z, list, input_option):
    if z != "":
        print("".center(40,'-'))
        print("")
        print(z.center(40,' '))
        print("")
        print("".center(40,'-'))
    print("".center(40,'-'))
    print(f"{list[0]}",f"{list[1]}".center(34,' '))
    if len(list) > 2:
        print(f"{list[2]}",f"{list[3]}".center(34,' '))
    if len(list) > 4:
        print(f"{list[4]}",f"{list[5]}".center(34,' '))
    print("".center(40,'-'))
    if input_option == True:
        menu_option = input()
        print("".center(40,'-'))
        return menu_option

def error_pading(message):
    print("".center(40,'-'))
    print("")
    print("ERROR".center(40,'+'))
    print("")
    print("".center(40,'-'))
    print("".center(40,'-'))
    print(message.center(40,' '))

def result_pading(message):
    print("".center(40,'-'))
    print("")
    print("Result".center(40,' '))
    print("")
    print("".center(40,'-'))
    print("".center(40,'-'))
    print(message.center(40,' '))
    
#####-.txt Manipulation-#####
def write_to_text(y, x, debug):
    try:
        with open(x, 'a') as file:
            try:
                y = f"{datetime.now()}: " + y
                file.write(y 
                           + '\n')
                
            except:
                print("file.write error")
    except Exception as e: 
        print(f"An Error occured: {e}")

    # Print veriable if debug is on
    debug_option("Text appended", debug)

#####-Input Handeling-#####
def input_port(text):
    end_loop = False
    while end_loop != True:
        print(text)
        try:
            port_number = int(input())
        except Exception as e:
            print(f"an error occured: {e}")
        else: 
            end_loop = True
            return port_number     

def input_name(text):
    confirm_input = False
    while confirm_input != True:
        print(text)
        try:
            name = input()
        except Exception as e:
            print(f"an error occured: {e}")
        else: 
            confirm_input = True
            return name

#####-IP Validation-#####
def resolve_ip(adres):
    try:
        socket.gethostbyname(adres)
    except socket.gaierror:
        error_pading(f"{adres}: Not A Valid IP")
        return False
    else:
        return adres

def input_ip_validator():
    confirm_input = False
    list = ["  ", "Enter host IP:"]
    while confirm_input != True:
        
        try:
            # Assigns IP address to veriable for verification
            adres = menu_pading("Host By IP", list, True)
            # Verifies correct formating
            socket.inet_aton(adres)
            adres = resolve_ip(adres)
        # Returns Error Type
        except socket.error as e:
            error_pading("Incorect IP")
            write_to_text(f"Error: {e}; Address Entered: {adres}", "errors.txt",debug)
        else:
            if adres != False: 
                confirm_input = True
                return adres

def ip_name():
    end_option = False
    list = ["  ", "Enter Host Name:"]
    while end_option != True:
        try:
            menu_pading("Host Name", list, False)
            name = input_name("")
            host = socket.gethostbyname(name)
        except socket.error as e:
            error_pading("Error with host name")
            write_to_text(f"Error: {str(e)}, Address Entered: {name}", "errors.txt", debug)  
        else:
            end_option = True
            result_pading(host)
            return host    

#####-Port Checks-#####
# Individual port check
def port_check(host, port, option):
    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Short timeout
    sock.settimeout(1)   
    try:
        # Attempts conection to port
        result = sock.connect_ex((host, port))
        if result == 0:
            result_pading(f"Port: {port} is open")
            # Adds open socket details to .txt
            write_to_text(f"Port: {port} is open. Host: {host}", "open_ports.txt", debug)
            return port
        # Displays open ports when required
        if option == True:
            result_pading(f"Port: {port} is closed")
    except socket.error as e:
        error_pading("an Error occured: ", e)
        # Adds error details to .txt
        write_to_text(f"Error at port: {port}: {str(e)}", "errors.txt", debug)
    finally:       
        sock.close()
    return None
# Concurent port checking
def port_check_range(host, start, stop, workers):
    open_ports = []
    # Concurency to speed up multiple port checks
    with ThreadPoolExecutor(max_workers=workers) as executor:
        try:
            futures = [executor.submit(port_check, host, port, False) for port in range(start, stop+1)]
        except: 
            error_pading("Error: ThreadPoolExecutor")
        else:  
            # Iterates over ports checking status
            for future in futures:
                port = future.result()
                if port is not None:
                    write_to_text(f"Port: {port} is open. Host: {host}", "open_ports.txt", debug)
                    # Assigns open port number no list
                    open_ports.append(port)
    # Prints open ports if found
    if len(open_ports) > 0:
        result_pading(f"{len(open_ports)}: Ports Open: {open_ports}")
    else: 
        result_pading(f"Ports in Range: {start} -> {stop} Closed")
#
def scan_port(host):
    # Scan port by number 
    confirm = False
    list = ["  ", "Enter Port"]
    # Error handels for invalid port number
    while confirm != True:
        menu_pading("Scan Port", list, False)
        port = input_port("Enter Port Number:")
        try:
            # Runs port check for port number 
            port_check(host, port, True)
            confirm = True
        except:
            debug_option("Error: No Port",1)

def scan_ports(host):
    # Scan ports in range
    confirm = False
    length = 0
    #port_start = 0
    #port_end = 0
    while confirm != True:
        while length < 1:
            z = "Scan Ports in range"
            list = ["  ", "Enter Start Point:"]
            menu_pading(z, list, False)
            port_start = input_port("")
            list = ["  ", "Enter End Point:"]
            menu_pading("", list, False)
            port_end = input_port("")
            length = port_end - port_start
            if length < 1:
                error_pading("Not Acceptable Range")
                
        # Changer workers for scan length 
        workers = 1
        if length > 10 and length <= 100:
            workers = 5
        if length > 100 and length <= 1000:
            workers = 50
        if length >  1000 and length <= 10000:
            workers = 500
        if length > 10000:
            workers = 1000
        debug_option(workers, debug)
        try:
            port_check_range(host, port_start, port_end, workers)
            confirm = True
        except:
            write_to_text(f"Error: Out of range: {port_start} to {port_end} ", "errors.txt", debug)  
            debug_option("Error: No Port",1)

#####-Option Menu-######
def host_option():
    end_host = False
    while end_host != True:
        list = ["1:", "Enter host by name", "2:", "Enter host by IP", "0:", "Exit"]
        
        host_option = menu_pading("Host", list, True)
        match host_option:
            case "1":
                host = ip_name(); end_host = True; return host
            case "2":
                host = input_ip_validator(); end_host = True; return host
            case "0":
                host = True; return host
            case _:
                error_pading("Invalid Option")       

def port_option(host):
    end_port = False
    while end_port != True:
        list = ["1:", "Scan Port", "2:", "Scan Ports", "0:", "Exit"]
        
        scan_option = menu_pading("Port", list, True)
        match scan_option:
            case "1":
                # Scan port by number 
                scan_port(host); end_port = True
            case "2":
                # Scan ports in range
                scan_ports(host); end_port = True
            case "0": 
                end_port = True
            case _:
                error_pading("Invalid Option")




#####-Main-#####
end = False
while end != True:
    z = "Menu"
    list = ["1:", "Port Scanner", "0:", "Exit"]
    quit_option = False
    menu_option = menu_pading(z, list, True)
    if menu_option == "1":
        host = host_option()
        if host != True:
            port_option(host)
    if menu_option == "0":
        end = True
    if menu_option != "1" and menu_option != "0":
        error_pading("no option")
    







