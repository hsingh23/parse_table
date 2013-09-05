
from string import split
from collections import OrderedDict

class Table:
    def __init__(self):
        """Initialize list"""
        self.columns = {}
        self.height = 0
        self.immutable = False

    def __getitem__(self, handle):
        if (type(handle) == str and handle in self.data):
            return self.data[handle]
        elif (type(handle) == int and handle < self.height and handle >= 0):
            return {
                label : column[handle] for label, column in self.data.items()
            }
        else:
            raise KeyError('Table does not contain handle ' + str(handle))


    def __repr__(self):
        return str(self.data)

    def populate(self, file_name, col_delim="\t", row_delim="\n", data_start=None):
        if self.immutable:
            return
        self.immutable = True
        with open(file_name, 'r') as f:
            if data_start:
                while True:
                    a = f.readline()
                    if data_start in a:
                        break
            raw_data = f.read()
        rows = [split(raw_row, col_delim) for raw_row in split(raw_data, row_delim)]
        self.height = len(rows) - 1
        parse_col = lambda index : self._parse_col(rows[1:], index, float)
        self.data = {
            label : parse_col(index) for index, label in enumerate(rows[0])
        }

    def _parse_col(self, rows, col_ind, conv=None):
        if conv is None:
            return [row[col_ind] for row in rows]
        try:
            return [conv(row[col_ind]) for row in rows]
        except ValueError:
            return self._parse_col(rows, col_ind, None)
        except IndexError:
            raise IndexError('A data element is missing.')

    # returns dict of format {class_id : { label : data_column}}
    def get_classified_columns(self, classifier):
        classes = {}
        for row_ind in range(self.height):
            class_id = classifier(self[row_ind])
            if class_id not in classes:
                classes[class_id] = {}
            for label in self.data.keys():
                if label not in classes[class_id]:
                    classes[class_id][label] = []
                col = self[label]
                classes[class_id][label].append(col[row_ind])
        return classes

    def map_columns(self, fn, *labels):
        columns = [self[l] for l in labels]
        return map(fn, *columns)