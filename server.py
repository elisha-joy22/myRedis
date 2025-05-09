import socket
import time

# Store for key-value pairs and hashes
store = {}
expiry = {}

# Command handler mappings
command_handlers = {}

def main():
    print("🔌 Server listening on localhost:6379...")
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        client_socket, client_addr = server_socket.accept()
        print(f"✅ Client connected: {client_addr}")
        handle_client(client_socket)

def handle_client(sock):
    with sock:
        while True:
            data = sock.recv(1024)
            if not data:
                print("❌ Client disconnected")
                break

            print(f"📥 Received: {data}")
            response = check_commands(data)

            sock.sendall(f"{response}\r\n".encode())

def is_expired(key):
    if key in expiry and time.time() > expiry[key]:
        print(f"⌛ Key expired: {key}")
        del store[key]
        del expiry[key]
        return True
    return False

def check_commands(command):
    # Clean command input
    if isinstance(command, bytes):
        command = command.decode()
    command = command.strip()
    
    # Split command into components
    parts = command.split()
    if not parts:
        return "-ERR Empty command"

    cmd = parts[0].upper()

    # Call corresponding handler function
    if cmd in command_handlers:
        return command_handlers[cmd](parts)
    
    return "-ERR Unknown command"

# Command Handlers
def handle_ping(parts):
    return "+PONG"

def handle_set(parts):
    if len(parts) < 3:
        return "-ERR usage: SET key value [EX seconds]"
    
    key, value = parts[1], parts[2]
    store[key] = value

    if len(parts) == 5 and parts[3].upper() == "EX":
        try:
            ttl = int(parts[4])
            expiry[key] = time.time() + ttl
        except ValueError:
            return "-ERR Invalid TTL"
    
    return "+OK"

def handle_get(parts):
    if len(parts) != 2:
        return "-ERR usage: GET key"
    key = parts[1]
    if is_expired(key):
        return "$-1"
    return store.get(key, "$-1")

def handle_del(parts):
    if len(parts) != 2:
        return "-ERR usage: DEL key"
    key = parts[1]
    if is_expired(key):
        return ":0"
    if key in store:
        del store[key]
        expiry.pop(key, None)
        return ":1"
    else:
        return ":0"

def handle_exists(parts):
    if len(parts) != 2:
        return "-ERR usage: EXISTS key"
    key = parts[1]
    if key in store and not is_expired(key):
        return ":1"
    return ":0"

def handle_incr(parts):
    if len(parts) != 2:
        return "-ERR usage: INCR key"
    key = parts[1]
    if key not in store or is_expired(key):
        store[key] = "1"  # Initialize with 1 if key doesn't exist
    try:
        store[key] = str(int(store[key]) + 1)
        return store[key]
    except ValueError:
        return "-ERR value is not an integer or out of range"

def handle_expire(parts):
    if len(parts) != 3:
        return "-ERR usage: EXPIRE key seconds"
    key, ttl = parts[1], parts[2]
    try:
        ttl = int(ttl)
        if ttl < 0:
            return "-ERR Invalid TTL"
        expiry[key] = time.time() + ttl
        return ":1"
    except ValueError:
        return "-ERR Invalid TTL"

def handle_ttl(parts):
    if len(parts) != 2:
        return "-ERR usage: TTL key"
    key = parts[1]
    if is_expired(key):
        return "-2"
    ttl = expiry.get(key, None)
    if ttl is None:
        return "-1"
    remaining_ttl = int(ttl - time.time())
    if remaining_ttl <= 0:
        return "-2"
    return str(remaining_ttl)

# Set Commands
def handle_sadd(parts):
    if len(parts) < 3:
        return "-ERR usage: SADD key member [member ...]"
    key = parts[1]
    members = parts[2:]
    if key not in store:
        store[key] = set()
    store[key].update(members)  # Add members to the set
    return f":{len(members)}"

def handle_srem(parts):
    if len(parts) < 3:
        return "-ERR usage: SREM key member [member ...]"
    key = parts[1]
    members = parts[2:]
    if key not in store:
        return ":0"
    initial_len = len(store[key])
    store[key].difference_update(members)  # Remove members from the set
    return f":{initial_len - len(store[key])}"

def handle_smembers(parts):
    if len(parts) != 2:
        return "-ERR usage: SMEMBERS key"
    key = parts[1]
    if key not in store or is_expired(key):
        return "*0"
    members = list(store[key])
    return f"*{len(members)}\r\n" + "\r\n".join([f"${len(m)}\r\n{m}" for m in members])

def handle_sismember(parts):
    if len(parts) != 3:
        return "-ERR usage: SISMEMBER key member"
    key, member = parts[1], parts[2]
    if key not in store or is_expired(key):
        return ":0"
    return ":1" if member in store[key] else ":0"

def handle_scard(parts):
    if len(parts) != 2:
        return "-ERR usage: SCARD key"
    key = parts[1]
    if key not in store or is_expired(key):
        return ":0"
    return str(len(store[key]))

# Hash Commands

def handle_hset(parts):
    if len(parts) != 4:
        return "-ERR usage: HSET key field value"
    key, field, value = parts[1], parts[2], parts[3]
    if key not in store:
        store[key] = {}
    store[key][field] = value
    return ":1"

def handle_hget(parts):
    if len(parts) != 3:
        return "-ERR usage: HGET key field"
    key, field = parts[1], parts[2]
    if key in store and field in store[key]:
        return store[key][field]
    return "$-1"

def handle_hdel(parts):
    if len(parts) < 3:
        return "-ERR usage: HDEL key field [field ...]"
    key = parts[1]
    fields = parts[2:]
    if key not in store:
        return ":0"
    initial_len = len(store[key])
    for field in fields:
        if field in store[key]:
            del store[key][field]
    return f":{initial_len - len(store[key])}"

def handle_hgetall(parts):
    if len(parts) != 2:
        return "-ERR usage: HGETALL key"
    key = parts[1]
    if key not in store:
        return "*0"
    fields_values = store[key]
    response = f"*{len(fields_values)*2}\r\n"
    for field, value in fields_values.items():
        response += f"${len(field)}\r\n{field}\r\n"
        response += f"${len(value)}\r\n{value}\r\n"
    return response

def handle_hkeys(parts):
    if len(parts) != 2:
        return "-ERR usage: HKEYS key"
    key = parts[1]
    if key not in store:
        return "*0"
    fields = list(store[key].keys())
    return f"*{len(fields)}\r\n" + "\r\n".join([f"${len(f)}\r\n{f}" for f in fields])

def handle_hvals(parts):
    if len(parts) != 2:
        return "-ERR usage: HVALS key"
    key = parts[1]
    if key not in store:
        return "*0"
    values = list(store[key].values())
    return f"*{len(values)}\r\n" + "\r\n".join([f"${len(v)}\r\n{v}" for v in values])

def handle_hexists(parts):
    if len(parts) != 3:
        return "-ERR usage: HEXISTS key field"
    key, field = parts[1], parts[2]
    if key in store and field in store[key]:
        return ":1"
    return ":0"

# Register command handlers
command_handlers.update({
    "PING": handle_ping,
    "SET": handle_set,
    "GET": handle_get,
    "DEL": handle_del,
    "EXISTS": handle_exists,
    "INCR": handle_incr,
    "EXPIRE": handle_expire,
    "TTL": handle_ttl,
    "SADD": handle_sadd,
    "SREM": handle_srem,
    "SMEMBERS": handle_smembers,
    "SISMEMBER": handle_sismember,
    "SCARD": handle_scard,
    "HSET": handle_hset,
    "HGET": handle_hget,
    "HDEL": handle_hdel,
    "HGETALL": handle_hgetall,
    "HKEYS": handle_hkeys,
    "HVALS": handle_hvals,
    "HEXISTS": handle_hexists,
})

if __name__ == "__main__":
    main()
