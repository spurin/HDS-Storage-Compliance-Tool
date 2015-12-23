from storageninja.utilities.prettytable_wrapper import text_table_from_sqlalchemy_query, text_table_from_array_dict

class OutputClass(object):

    '''
    classdocs
    '''

    def __init__(self, **kwargs):
        '''
        Constructor
        '''
        # Store Content
        self.content = ""

    def add_entry(self, data, data_information, report_parameters):

        # If a title is defined, add accordingly
        if '__title__' in report_parameters:

            # Add a heading
            self.add_heading(report_parameters['__title__'])

            # Add table
            self.add_table(data=data, data_information=data_information)

    def add_heading(self, heading):
        self.content += "--== %s ==--\n\n" % heading

    def add_text(self, text):
        self.content += "%s\n\n" % text

    def add_table(self, data, data_information):
        if data_information['type'] == 'array_dict':
            table_output = text_table_from_array_dict(data=data, column_order=data_information['order'])

        elif data_information['type'] == 'sqlalchemy_query':
            table_output = text_table_from_sqlalchemy_query(data=data)

        # If no results are returned act accordingly
        if table_output is None:
            self.add_text('No results returned')

        # Otherwise add the table output
        else:
            self.content += table_output.get_string()

            # Add two carriage returns for formatting
            self.content += '\n\n'

    def dispatch(self):
        print(self.content)
