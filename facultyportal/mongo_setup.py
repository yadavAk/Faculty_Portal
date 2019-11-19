import mongoengine

alias_core = 'core'
mdb = 'profile'

# data = dict(
#     username='admin',
#     password='pass',
#     host='http://127.0.0.1',
#     port='5000',
#     authentication_source='admin',
#     authentication_mechanism='SCRAM-SHA-1',
#     ssl=True,
#     ssl_cert_reqs=ssl.CERT_NONE
# )

def global_init():
    mongoengine.register_connection(alias=alias_core, name=mdb)
    