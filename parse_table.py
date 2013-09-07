import string
from re import split
from pprint import pprint as pp
class Table:
    def __init__(self, labels, rows):
        self.labels = labels
        self.rows = rows
        self.inverted = {label: index for index, label in enumerate(labels)}

    @classmethod
    def from_file(cls, file_name, col_delim="\s+", row_delim="\n", data_start=None):
        with open(file_name, 'r') as f:
            if data_start:
                while True:
                    a = f.readline()
                    if data_start in a:
                        break
            raw_data = f.read()
        return cls.from_raw_data(raw_data, col_delim, row_delim)

    @classmethod
    def from_raw_data(cls, raw_data, col_delim="\s+", row_delim="\n"):
        rows = [split(col_delim, raw_row) for raw_row in split(row_delim, raw_data) if raw_row]
        data_rows = rows[1:]
        for col_ind in range(len(rows[0])):
            new_rows = []
            for row_ind, row in enumerate(data_rows):
                new_row = list(row)
                try:
                    new_row[col_ind] = float(row[col_ind])
                except ValueError:
                    new_rows = data_rows
                    break
                except IndexError:
                    raise IndexError('A data element is missing at column %s row_ind %s.' %(col_ind, row_ind))
                new_rows.append(new_row)
            data_rows = new_rows
        return cls(rows[0], data_rows)

    def __getitem__(self, handle):
        if (type(handle) == str and handle in self.inverted):
            col_ind = self.inverted[handle]
            return [row[col_ind] for row in self.rows]
        elif (type(handle) == int and handle < len(self.rows) and handle >= 0):
            return self.rows[handle]
        else:
            raise KeyError('Table does not contain handle ' + str(handle))

    def __repr__(self):
        return "\n %s \n\n %s \n\n" %(self.labels, string.join(map(str, self.rows)))

    # returns dict of format {class_id : table}
    def get_classified_columns(self, classifier):
        classes = {}
        for row in self.rows:
            class_id = classifier(dict(zip(self.labels, row)))
            if class_id not in classes:
                classes[class_id] = []
            classes[class_id].append(row)
        return {k : Table(self.labels, v) for k, v in classes.items()}

    def map_columns(self, fn, *labels):
        columns = [self[l] for l in labels]
        return map(fn, *columns)
