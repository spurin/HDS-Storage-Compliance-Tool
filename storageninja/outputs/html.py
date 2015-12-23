from inlinestyler.utils import inline_css
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
        self.content += "<h3>%s</h3>" % heading

    def add_text(self, text):
        self.content += "<h4>%s</h4>" % text

    def add_table(self, data, data_information):

        if len(data) == 0:
            self.add_text('No results returned\n')
            return

        if data_information['type'] == 'array_dict':
            columns = data_information['order']
        elif data_information['type'] == 'sqlalchemy_query':
            columns = data[0].keys()

        # Start table
        self.content += '<table frame="box" rules="cols" class="gridtable" style="font-family: verdana, arial, sans-serif;font-size: 11px;color: #333;border-width: 1px;border-color: #666;border-collapse: collapse">\n'

        # Process column Heading
        self.content += '<tr>\n'
        for column in columns:
            self.content += '<th style="padding-left: 1em;padding-right: 1em;text-align: center;border-width: 1px;padding: 8px;border-style: solid;border-color: #666;background-color: #dedede">\n'
            self.content += column
            self.content += '</th>\n'
        self.content += '</tr>\n'

        # Process rows
        for entry in data:
            self.content += '<tr>\n'
            for column in columns:
                self.content += '<td style="padding-left: 1em;padding-right: 1em;text-align: center;vertical-align: top;border-width: 1px;padding: 8px;border-style: solid;border-color: #666;background-color: #fff">\n'
                if data_information['type'] == 'array_dict':
                    self.content += str(entry[column])
                elif data_information['type'] == 'sqlalchemy_query':
                    self.content += str(getattr(entry, column))
                self.content += '</td>\n'
            self.content += '</tr>\n'

        # Finish table
        self.content += '</table>\n'

    def add_table_backup(self, data, data_information):  # abandoned ... delete
        if data_information['type'] == 'array_dict':
            table_output = text_table_from_array_dict(data=data, column_order=data_information['order'], type='html')

        elif data_information['type'] == 'sqlalchemy_query':
            table_output = text_table_from_sqlalchemy_query(data=data, type='html')

        # If no results are returned act accordingly
        if table_output is None:
            self.add_text('No results returned')

        # Otherwise add the table output
        else:
            self.content += table_output.get_html_string(format=True, attributes={"class": "gridtable"})
            #self.content += inline_css(table_output.get_html_string(format=True, attributes = {"class": "gridtable"}))

            # Add two carriage returns for formatting
            self.content += '\n\n'

    def inline_css(self):

        # Add the CSS to the content
        self.content = """
<style type="text/css">
table.gridtable {
    font-family: verdana,arial,sans-serif;
    font-size:11px;
    color:#333333;
    border-width: 1px;
    border-color: #666666;
    border-collapse: collapse;
}
table.gridtable th {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #dedede;
}
table.gridtable td {
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #666666;
    background-color: #ffffff;
}
</style>
""" + self.content

        # Inline the CSS to the HTML
        self.content = inline_css(self.content)

    def dispatch(self):
        self.inline_css()
        print(self.content)
