import sys, logging, argparse, psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

logging.debug("Connecting to PostgreSQL")
connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
logging.debug("Database connection established.")


def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.debug("Storing snippet {!r}: {!r}".format(name, snippet))
    
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
    logging.debug("Retrieving snippet {!r}".format(name))
    
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

def catalog():
    """Return a list of recorded snippet names."""
    logging.debug("Listing stored keywords.")
    
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets order by keyword", )
        rows = cursor.fetchall()
        names = []
        for tup in rows:
            names.append(tup[0])
    return names

def find(text):
    """Return a list of snippet names where string is found within snippet"""
    logging.debug("Finding messages containing {}".format(text))
    
    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets where message like '%{}%'".format(text), )
        rows = cursor.fetchall()
        found = []
        for tup in rows:
            found.append(tup[0])
        print "Find Function reports found: {}".format(found)
    return text, found

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
    
    #Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    cat_parser = subparsers.add_parser("catalog", help="Get a list of all snippet names")
    
    #Subparser for the find command
    logging.debug("Constructing find command")
    find_parser = subparsers.add_parser("find", help="Find snippets containing a given string")
    find_parser.add_argument("text", help="The text to find")
    
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
    elif command == "catalog":
        names = catalog()
        print("Known snippets:")
        for n in names: 
            print(n),
    elif command == "find":
        found = find(**arguments)
        print("Retrieved snippets:")
        for f in found: 
            print (f),
    
        
if __name__ == "__main__":
    main()
    
