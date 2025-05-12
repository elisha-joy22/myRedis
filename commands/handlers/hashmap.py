from mem.storage import store,expiry
import time


class HashmapHandler:

    def handle_hset(cmd_parts):
        if len(cmd_parts) < 4 or len(cmd_parts) % 2 != 0:
            return "-ERR usage: HSET key field value [field value ...]"
        
        key = cmd_parts[1]
        if key not in store or not isinstance(store[key], dict):
            store[key] = {}

        field_value_pairs = cmd_parts[2:]
        for i in range(0,len(field_value_pairs),2):
            field = field_value_pairs[i]
            value = field_value_pairs[i+1]
            store[key][field] = value
        return f":{len(field_value_pairs) // 2}"


    def handle_hget(cmd_parts):
        if len(cmd_parts) < 3:
            return "-ERR usage : HGET key field [field..]"
        key, fields = cmd_parts[1], cmd_parts[2:]
        if key not in store or not isinstance(store[key], dict):
            return "$-1"
        result_dict = {}
        for field in fields:
            if field in store[key]:
                result_dict[field] = store[key][field]
        return f"{result_dict}"

    def handle_hmset(cmd_parts):
        return HashmapHandler.handle_hset(cmd_parts)

    def handle_hmget(cmd_parts):
        return HashmapHandler.handle_hget(cmd_parts)

    def handle_hgetall(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage: HGETALL key"

        key = cmd_parts[1]
        if key not in store or not isinstance(store[key], dict):
            return "*0"
        return str(store[key])


    def handle_hdel(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage: HDEL key field"
        key, fields = cmd_parts[1], cmd_parts[2:]

        if key not in store or not isinstance(store[key], dict):
            return ":0"

        deleted_count = 0
        for field in fields:
            if field in store[key]:
                del store[key][field]
                deleted_count += 1
        return f":{deleted_count}"



    def handle_hexists(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage: HGETALL key field"
        key, field = cmd_parts[1], cmd_parts[2]

        if key not in store or not isinstance(store[key], dict):
            return ":0"
        
        return ":1" if field in store[key] else ":0"
        

    def handle_hkeys(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage: HKEYS key"
        
        key = cmd_parts[1]

        if key not in store or not isinstance(store[key], dict):
            return ":0"
        
        keys = store[key].keys()
        response = f"*{len(keys)}"
        for key in keys:
            response += f"\r\n${key}"
        return response


    def handle_hvals(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage: HVALUES key"
        
        key = cmd_parts[1]

        if key not in store or not isinstance(store[key], dict):
            return ":0"
        
        values = store[key].values()
        response = f"*{len(values)}"
        for value in values:
            response += f"\r\n${value}"
        return response

    def handle_hlen(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage: HLEN key"
        
        key = cmd_parts[1]

        if key not in store or not isinstance(store[key], dict):
            return ":0"
        
        keys = store[key].keys()
        return f"*{len(keys)}"

    def handle_hincrby(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage: HINCRBY key field increment"
        
        key, field, increment_str = cmd_parts[1], cmd_parts[2], cmd_parts[3]

        try:
            increment = int(increment_str)
        except ValueError:
            return "-ERR increment is not an integer"
        if key not in store:
            store[key] = {}
        if not isinstance(store[key], dict):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"
        
        current = store[key].get(field, 0)
        try:
            current = int(current)
        except ValueError:
            return "-ERR hash value is not an integer"
        store[key][field] = current + increment
        return f":{store[key][field]}"


    def handle_hincrbyfloat(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage: HINCRBY key field increment"
        
        key, field, increment_str = cmd_parts[1], cmd_parts[2], cmd_parts[3]

        try:
            increment = float(increment_str)
        except ValueError:
            return "-ERR increment is not an float"
        if key not in store:
            store[key] = {}
        if not isinstance(store[key], dict):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"
        
        current = store[key].get(field, 0)
        try:
            current = float(current)
        except ValueError:
            return "-ERR hash value is not an float"
        store[key][field] = current + increment
        return f":{store[key][field]}"