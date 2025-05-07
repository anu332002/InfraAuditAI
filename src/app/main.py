# Importing the `get_message` function from the `utils` module.
# This function will be used to retrieve a message for the application.
from utils import get_message

# The main function serves as the entry point of the application.
# It retrieves a message using the `get_message` function and prints it.
def main():
    # Call the `get_message` function to get a message.
    message = get_message()
    
    # Print the message to the console, prefixed with "[InfraAuditAI]".
    print(f"[InfraAuditAI] {message}")

# This block ensures that the `main` function is executed only when
# this script is run directly (not when imported as a module).
if __name__ == "__main__":
    main()
