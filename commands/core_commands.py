from mem.storage import store,expiry
import time

def check_commands(command):
    if isinstance(command,bytes):
        command = command.decode()
        command = command.strip()
    command_parts = command.split()
    if not command_parts:
        return "-ERR Empty command"  
    return command_parts


def is_expired(key):
    if key in expiry and time.time() > expiry[key]:
        print(f"key expired: {key}")
        del store[key]
        del expiry[key]
        return True
    return False
    

class BaseCommandHandler:
    def handle_ping(cmd_parts: list):
        return "+PONG"
    
    def handle_set(cmd_parts: list):
        if len(cmd_parts) == 3:
            key, value = cmd_parts[1], cmd_parts[2]
            store[key] = value
            return "+OK"

        elif len(cmd_parts) == 5:
            if cmd_parts[3].upper() != "EX":
                return "-ERR syntax error: expected EX for expiry"

            try:
                ttl = int(cmd_parts[4])
            except ValueError:
                return "-ERR invalid TTL value"

            key, value = cmd_parts[1], cmd_parts[2]
            store[key] = value
            expiry[key] = time.time() + ttl
            return "+OK"

        else:
            return "-ERR usage : SET key value [EX seconds]"
        
    def handle_get(cmd_parts: list):
        if len(cmd_parts)!= 2:
            return "-ERR usage : GET key"
        key = cmd_parts[1]
        if is_expired(key):
            return "$-1"
        return store.get(key, "$-1")
    
    def handle_del(cmd_parts: list):
        if len(cmd_parts) != 2:
            return "-ERR usage : DEL key"
        key = cmd_parts[1]
        if is_expired(key):
            return ":0"
        if key in store:
            del store[key]
            expiry.pop(key, None)
            return ":1" 
        else:
            return ":0"
        
    def handle_exists(cmd_parts: list):
        if len(cmd_parts) != 2:
            return "ERR usage : EXISTS key"
        key = cmd_parts[1]
        if not is_expired(key) and store.get(key, None):
            return ":1"
        return ":0"


    def handle_incr(cmd_parts: list):
        if len(cmd_parts) != 2:
            return "-ERR usage : INCR key"
        key = cmd_parts[1]
        if key not in store or is_expired(key): 
            store[key] = 1
            return "+1"
        try:
            store[key] = int(store.get(key)) + 1
            return store[key]
        except ValueError:
            return "-ERR value is not an integer or out of range"



    def handle_expire(cmd_parts: list):
        if len(cmd_parts) != 3:
            return "-ERR usage : EXPIRE key seconds"
        key, ttl = cmd_parts[1], cmd_parts[2]

        try:
            ttl = int(ttl)
            if ttl < 0:
                return "-ERR : Invalid TTL"
        except ValueError:
            return "-ERR : Invalid TTL"
        expiry[key] = time.time() + ttl
        return ":1"

    def handle_ttl(cmd_parts: list):
        if len(cmd_parts) != 2:
            return "-ERR usage : TTL key"        
        
        key = cmd_parts[1]
        if is_expired(key):
            return "-2"
        if key in expiry:
            ttl = expiry[key]
            remaining_time = int(ttl - time.time())
            if remaining_time <= 0:
                return "-2"
            return remaining_time
        return "-1"

