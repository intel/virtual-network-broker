import logging

logging.basicConfig(filename="/var/log/cred-service-prov.log", 
    filemode="w", level=logging.INFO)

logging.error("Permission denied: Token expired. Please check with the admin")
