from loginsights.main import LogInsightsLogger

# Configuration variables (replace with your own details)
connection_string = ""  # Replace with your connection string
client_application_id = -1  # Replace with the given client application id
secret = ""  # Replace with the given secret

config = {
    "ConnectionString": connection_string,
    "ClientApplicationId": client_application_id,
    "Secret": secret
}

# Configure the logger
LogInsightsLogger.configure(config)