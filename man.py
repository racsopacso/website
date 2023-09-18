manpage = {
    "ls": "Lists all commands. This implementation doesn't have any arguments",
    "man": "This function you're using right now!",
    "cv": "Outputs my CV",
    "pathitem": """Searchable list of pathfinder items that are actually useful. \n
example: pathitem --price >3 --name * boots \n
Format is similar to the bash find command. Search terms are passed by flag. Flags are:
     --name: Searches for items by name. Accepts * as a wildcard - *boots returns all items that end with 'boots'.
     --price: Searches by price. Accepts >, < and = as operators. Also allows you to append k to handle gold in thousands. --price >3k <8k returns all items between 3,000 and 8,000 gold
     --tag: Searches for items by tag.
     --description: Searches for text in description. Also uses wildcard syntax
     """
}
