""" Pretty Table Wrapper """
from prettytable import PrettyTable, FRAME

def text_table_from_sqlalchemy_query(data, **tableargs):

    if len(data) == 0:
        return None
    else:

        # SQLalchemy returns the results as what appears to be a list, however
        # as depicted by msw @ http://stackoverflow.com/questions/2828248/sqlalchemy-returns-tuple-not-dictionary
        # ... SQLalchemey uses ResultProxy's which appear as lists
        #
        # Your can run specific methods to access information, i.e. keys to extract the
        # actual column headings as per the orm
        columns = data[0].keys()

        # Create a new PrettyTable with the columns as headers
        table = PrettyTable(data[0].keys(), **tableargs)

        # Process each result
        for entry in data:

            # Create a list of items according to the column entries
            row_data = [getattr(entry, column) for column in columns]

            # Add the row to the table
            table.add_row(row_data)

        # Return a table object
        return table


def text_table_from_array_dict(data, **table_args):

    if len(data) == 0:
        return None
    else:

        # SQLalchemy returns the results as what appears to be a list, however
        # as depicted by msw @ http://stackoverflow.com/questions/2828248/sqlalchemy-returns-tuple-not-dictionary
        # ... SQLalchemey uses ResultProxy's which appear as lists
        #
        # Your can run specific methods to access information, i.e. keys to extract the
        # actual column headings as per the orm
        columns = table_args['column_order']

        # Create a new PrettyTable with the columns as headers
        table = PrettyTable(columns, **table_args)

        # Process each result
        for result in data:

            # Create a list of items according to the column entries
            row_data = [result[column] for column in columns]

            # Add the row to the table
            table.add_row(row_data)

        # Return a table object
        return table
