from loginsights.main import LogInsightsLogger

# Configuration variables (replace with your own details)
connection_string = "http://127.0.0.1:10001/devstoreaccount1/messages?sv=2024-11-04&se=2026-02-01T16%3A23%3A21Z&sp=a&sig=OemdWUBEe2lre2iREpLQsSVQhVxVv7EUE3xCcrFirnA%3D"  # Replace with your connection string
client_application_id = 7  # Replace with the given client application id
secret = "X2oDWpC701b5bG2YxU1BujKdXB7BdsvSGKFEzJh52oHEl7sjzJN2r4kyrLpUsBdHFJyRByjox5JFbG2aTXMUe3kMjQWoeMM1L98bIbhAjjEvvfXkSOBUzInLimsub5Kk"  # Replace with the given secret

config = {
    "ConnectionString": connection_string,
    "ClientApplicationId": client_application_id,
    "Secret": secret
}

# Configure the logger
LogInsightsLogger.configure(config)
LogInsightsLogger.get_logger().debug("Debug Message")