import logging
import sys
import argparse as ap

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet, overwrite=False):
    """Store a snippet with an associated name.
    
    If successful, returns the name and the snippet
    If collision with existing name, returns False
    Overwrite value is optional boolean
    Overwrite = True will overwrite any existing collision
    """
    
    logging.error("FIXME: Unimplemented - put({!r}, {!r})".format(name, snippet))
    return False

def get(name):
    """Retrieve the snippet with a given name.

    If there is no such snippet, returns False; otherwise, returns the snippet.
    """
    logging.error("FIXME: Unimplemented - get({!r})".format(name))
    return False

def dir(mask="?"):
    """Get a list of snippet tags, filtered by any given mask
    
    If no mask is provided, all stored snippets are returned.
    """
    logging.error("FIXME: Unimplemented - dir({!r})".format(mask))
    return False

def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = ap.ArgumentParser(description="Store and retrieve snippets of text")
    arguments = parser.parse_args(sys.argv[1:])

    
if __name__ == "__main__":
    main()
    
