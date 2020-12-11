import http.client

conn = http.client.HTTPSConnection("dad-jokes.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "49cd45596amsh3d92318f8322e5cp17fd76jsn0b8e815b14ea",
    'x-rapidapi-host': "dad-jokes.p.rapidapi.com"
    }

conn.request("GET", "/random/joke", headers=headers)

res = conn.getresponse()
data = res.read()
data_str = data.decode("utf-8")

# change 'true' -> 'True' for python dictionary
s_dict = data_str.replace('true', 'True', 1)
# convert to dictionary
d_dict = eval(s_dict)

def get_setup():
    return d_dict["body"][0].get("setup")

def get_punchline():
    return d_dict["body"][0].get("punchline")
