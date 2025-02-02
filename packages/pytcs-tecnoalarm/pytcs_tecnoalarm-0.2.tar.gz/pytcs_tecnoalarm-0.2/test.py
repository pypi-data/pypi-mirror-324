from pytcs_tecnoalarm import TCSSession

s = TCSSession("58f1071670745115bbba74b802259510c8491763c38da5af1ef687072bb3f75d250ce44d509f4bb71958eaebcb9bab61", 1668500101155)

s.get_centrali()
elementari = s.centrali["24680"]
comune = s.centrali["99887"]

s.select_centrale(elementari.tp)
ciao = s.get_logs()


body = {
    "background_syncing": False,
    "code": "99887",
    "codes": [],
    "description": "Comune",
    "icon": "ta-home",
    "idx": 0,
    "ip": None,
    "keys": [],
    "passphTCS": "+121+127+53+40-70-98+49+11-87-78+41-47+51+113-51+100",
    "port": 0,
    "programs": [    {
      "description": "SCUOLA",
      "icon": "ta-program",
      "idx": 0,
      "id": 1736369608141,
      "zones": [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 49, 50, 51, 52, 53, 54, 55
      ]
    },],
    "rcmds": [],
    "remotes": [],
    "sn": "003088963",
    "syncCRC": None,
    "type": 38,
    "use_fingerprint": False,
    "valid_data": True,
    "zones": []
}

r = s.post("/tcs/tp", json=body)

print(ciao)
