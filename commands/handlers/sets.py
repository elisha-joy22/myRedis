from mem.storage import store,expiry
import time
import random


class SetHandler:
    def handle_sadd(cmd_parts):
        if len(cmd_parts) < 3:
            return "-ERR usage: SADD key member [member..]"
        
        key, members = cmd_parts[1], cmd_parts[2:]

        if key not in store:
            store[key] = set()
        
        if not isinstance(store[key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"

        added = 0

        for member in members:
            if member not in store[key]:
                store[key].add(member)
                added += 1
        return f":{added}"

    def handle_srem(cmd_parts):
        if len(cmd_parts) < 3:
            return "-ERR usage: SREM key member [member..]"
        
        key, members = cmd_parts[1], cmd_parts[2:]

        if key not in store or not isinstance(store[key], set):
            return "-ERR : Key not found or wrong type"
        
        removed = 0
        for member in members:
            if member in store[key]:
                store[key].remove(member)
                removed += 1
        return f":{removed}"


    def handle_spop(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage: SPOP key count"

        key, count_str = cmd_parts[1], cmd_parts[2]

        if key not in store:
            return "-ERR: Key not found"
        if not isinstance(store[key], set):
            return "-ERR: WRONGTYPE Operation against a key holding the wrong kind of value"

        try:
            count = int(count_str)
        except ValueError:
            return "-ERR: count must be an integer"

        current_set = store[key]
        count = min(count, len(current_set))

        popped = random.sample(current_set, count)
        for val in popped:
            current_set.remove(val)
        return popped



    def handle_srandmember(cmd_parts):
        if len(cmd_parts) not in (2, 3):
            return "-ERR usage: SRANDMEMBER key [count]"

        key = cmd_parts[1]

        if key not in store:
            return "$-1"

        if not isinstance(store[key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"
        
        values = list(store[key])

        if len(cmd_parts) == 2:
            return f"${values[random.randint(0,len(values)-1)]}"
        
        try:
            count = int(cmd_parts[2])
        except ValueError:
            return "-ERR count must be an integer"
        
        if count >= 0:
            sampled = random.sample(values, min(count, len(values)))

        else:
            sampled = [random.choice(values) for _ in range(abs(count))]
        
        return "\n".join(f"${val}" for val in sampled)

    def handle_smembers(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage: SMEMBERS key"
        key, members = cmd_parts[1], cmd_parts[2:]
        if key not in store or not isinstance(store[key], set):
            return "-ERR : Key not found or wrong type"
        return "\n".join(f"{i + 1}) {member}" for i, member in enumerate(store[key]))

    def handle_sismember(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage: SISMEMBER key member"
        key, member = cmd_parts[1], cmd_parts[2]
        if key not in store or not isinstance(store[key], set):
            return "-ERR : Key not found or wrong type"
        
        if member in store[key]:
            return ":1"
        return ":0"


    def handle_scard(cmd_parts):
        if len(cmd_parts) != 2:
            return "-ERR usage: SCARD key"
        
        key = cmd_parts[1]

        if key not in store:
            return ":0"

        if not isinstance(store[key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"
        
        return f":{len(store[key])}"
    

    def handle_sunion(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage: SUNION set1 set2"                
        set1_key, set2_key = cmd_parts[1], cmd_parts[2]
        if not set1_key in store or not set2_key in store:
            return ":0"
        if not isinstance(store[set1_key], set) or not isinstance(store[set2_key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"            
        try:
            union_set = store[set1_key].union(store[set2_key])
        except:
            return "-ERR : Operation failed"

        return union_set



    def handle_sinter(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage: SINTER set1 set2"                
        set1_key, set2_key = cmd_parts[1], cmd_parts[2]
        if not set1_key in store or not set2_key in store:
            return ":0"
        if not isinstance(store[set1_key], set) or not isinstance(store[set2_key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"            
        try:
            inter_set = store[set1_key].intersection(store[set2_key])
        except:
            return "-ERR : Operation failed"

        return inter_set



    def handle_sdiff(cmd_parts):
        if len(cmd_parts) != 3:
            return "-ERR usage: SDIFF set1 set2"                
        set1_key, set2_key = cmd_parts[1], cmd_parts[2]
        if not set1_key in store or not set2_key in store:
            return ":0"
        if not isinstance(store[set1_key], set) or not isinstance(store[set2_key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"            
        try:
            diff_set = store[set1_key].difference(store[set2_key])
        except:
            return "-ERR : Operation failed"

        return diff_set


    def handle_sunionstore(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage: SUNIONSTORE result_set set1 set2"                
        result_set_key, set1_key, set2_key = cmd_parts[1], cmd_parts[2], cmd_parts[3]
        if not set1_key in store or not set2_key in store:
            return ":0"
        if not isinstance(store[set1_key], set) or not isinstance(store[set2_key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"            
        try:
            store[result_set_key] = store[set1_key].union(store[set2_key])
        except:
            return "-ERR : Operation failed"
        
        return f":{store[result_set_key]}"


    def handle_sinterstore(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage: SINTERSTORE result_set set1 set2"                
        result_set_key, set1_key, set2_key = cmd_parts[1], cmd_parts[2], cmd_parts[3]
        if not set1_key in store or not set2_key in store:
            return ":0"
        if not isinstance(store[set1_key], set) or not isinstance(store[set2_key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"            
        try:
            store[result_set_key] = store[set1_key].intersection(store[set2_key])
        except:
            return "-ERR : Operation failed"
        
        return f":{store[result_set_key]}"


    def handle_sdiffstore(cmd_parts):
        if len(cmd_parts) != 4:
            return "-ERR usage: SDIFFSTORE result_set set1 set2"                
        result_set_key, set1_key, set2_key = cmd_parts[1], cmd_parts[2], cmd_parts[3]
        if not set1_key in store or not set2_key in store:
            return ":0"
        if not isinstance(store[set1_key], set) or not isinstance(store[set2_key], set):
            return "-ERR WRONGTYPE Operation against a key holding the wrong kind of value"            
        try:
            store[result_set_key] = store[set1_key].difference(store[set2_key])
        except:
            return "-ERR : Operation failed"
        
        return f":{store[result_set_key]}"



