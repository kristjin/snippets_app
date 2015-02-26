import sys, logging, argparse, psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")


def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    
    try:
        with connection, connection.cursor() as cursor:  
            cursor.execute("insert into snippets values (%s, %s)", (name, snippet))
            logging.info("Insert successful.")
    except psycopg2.IntegrityError as e:
        logging.info("DUPLICATE: {!r}".format(e))
        with connection, connection.cursor() as cursor:
            cursor.execute("update snippets set message=%s where keyword=%s", (snippet, name))
            logging.info("Update successful.")
    return name, snippet

def get(name):
    """Retrieve the snippet with a given name, False if not found."""
    logging.info("Retrieving snippet {!r}".format(name))
    
    with connection, connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()

    if not row:
        # No snippet was found with that name. 
        logging.error("No Snippet found with name {!r}".format(name))
        return False
    else: 
        message = row[0]
        logging.info("Snippet retrieved successfully.")
        return message


def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
    #Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve a snippet")
    get_parser.add_argument("name", help="The name of the snippet")
    
    arguments = parser.parse_args(sys.argv[1:])
    
    # Convert parsed arguments from Namespace to dictionary
    # Doing so allows command(**arguments) later
    arguments = vars(arguments)
    
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
        
if __name__ == "__main__":
    main()
    
