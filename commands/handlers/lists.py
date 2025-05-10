from mem.storage import store,expiry
import time


class Listhandler: 
    def handle_lpush(cmd_parts: list):
        if len(cmd_parts) < 3:
            return "-ERR usage : LPUSH key value [value..]"
        key, values = cmd_parts[1], cmd_parts[2:]

        if not key in store:
            store[key] = []
        if not isinstance(store[key], list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"
 
        store[key] = values + store[key] 
        return ":1"
    


    def handle_rpush(cmd_parts):
        if len(cmd_parts)<3:
            return "-ERR usage : RPUSH key value [value..]"
        key,values = cmd_parts[1], cmd_parts[2:]

        if not key in store:
            store[key] = []
        if not isinstance(store[key], list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"

        store[key] += values
        return ":1"

    def handle_lpop(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage : LPOP key"
        key = cmd_parts[1]
        print(type(store[key]))
        if key not in store:
            return "-ERR : Key not found"
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"

        popped_item = store[key].pop(0) 
        return popped_item if popped_item else ":$-1"

    
    
    def handle_rpop(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage : RPOP key"
        key = cmd_parts[1]

        if key not in store:
            return "-ERR : Key not found"
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"

        popped_item = store[key].pop(-1) 
        return popped_item if popped_item else ":$-1"


    def handle_lrange(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage : LRANGE key start stop"

        key,start,stop = cmd_parts[1],cmd_parts[2],cmd_parts[3]
        if key not in store:
            return "-ERR : Key not found"
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"
 
        try:
            return store[key][start:stop] 
        except:
            return "-ERR : Invalid range" 
                       

    def handle_llen(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage : LLEN key"
        key = cmd_parts[1]
        if key not in store:
            return "-ERR : Key not found"  
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"
        try:
            return len(store[key]) 
        except:
            return "-ERR : Invalid list"               


    def handle_lindex(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage : LINDEX key index"
        key, index_str = cmd_parts[1], cmd_parts[2]
        if key not in store:
            return "-ERR : Key not found"  
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"       
        try:
            index = int(index_str)
            return store[key][index] 
        except:
            return "-ERR : Invalid index" 


    def handle_lset(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage : LSET key index value"
        key, index_str, value = cmd_parts[1], cmd_parts[2], cmd_parts[3]
        if key not in store:
            return "-ERR : Key not found"  
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"       
        try:
            index = int(index_str)
            store[key][index] = value
            return ":1" 
        except:
            return "-ERR : Invalid index or value"         


    def handle_ltrim(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage : LTRIM key start stop"
        key, start_str, stop_str = cmd_parts[1], cmd_parts[2], cmd_parts[3]
        if key not in store:
            return "-ERR : Key not found"  
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"       
        try:
            store[key] = store[key][int(start_str):int(stop_str)+1]
            return ":1" 
        except:
            return "-ERR : Invalid index or value"  


    def handle_lrem(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage : LREM key count value"
        key, count_str, value = cmd_parts[1], cmd_parts[2], cmd_parts[3]
        if key not in store:
            return "-ERR : Key not found"  
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"       
        try:
            stop_count = int(count_str)
        except ValueError:
            return "-ERR: count must be an integer"

        removed_count = 0
        new_list = []
        
        if stop_count == 0:
            for val in store[key]:
                if val == value:
                    removed_count += 1
                else:
                    new_list.append(val)
        
        elif stop_count > 0:
            for val in store[key]:
                if val == value and removed_count < stop_count:
                    removed_count += 1
                else:
                    new_list.append(val)
        else:
            for val in reversed(store[key]):
                if val == value and removed_count < abs(stop_count):
                    removed_count += 1
                else:
                    new_list.append(val)
            new_list.reverse()
            store[key] = new_list
            return removed_count
        
        store[key] = new_list
        return removed_count


    def handle_blpop(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage : BLPOP key [key...] timeout"
        key, timeout = cmd_parts[1], cmd_parts[2]
        if key not in store:
            return "-ERR : Key not found"  
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"          
        try: 
            time.sleep(int(timeout))
            return Listhandler.handle_lpop(['RPOP',cmd_parts[1]])
        except:
            return "-ERR : TYPERROR timeout must be an int"

    def handle_brpop(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage : BRPOP key [key...] timeout"
        key, timeout = cmd_parts[1], cmd_parts[2]
        if key not in store:
            return "-ERR : Key not found"  
        if not isinstance(store[key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"          
        try:
            time.sleep(int(timeout))
            return Listhandler.handle_rpop(['RPOP',cmd_parts[1]])
        except:
            return "-ERR : TYPERROR timeout must be an int"

    def handle_rpoplpush(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage : RPOPLPUSH source destination"
        source_key, destination_key = cmd_parts[1], cmd_parts[2]
        if source_key not in store or destination_key not in store:
            return "-ERR : Key not found"  
        if not isinstance(store[source_key],list):
            return "-ERR : WRONGTYPE Operation against a key holding the wrong kind of value"       
        try:
            popped_item = Listhandler.handle_rpop(['RPOP',source_key])
            return Listhandler.handle_lpush(['LPUSH',destination_key, popped_item])
        except ValueError:
            return "-ERR - operation failed!"