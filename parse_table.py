
from string import split

class Table:
    def __init__(self):
        self.data = {}

    def populate(self, file_name, col_delim="\t", row_delim="\n", data_start=None):
        with open(file_name, 'r') as f:
            if data_start:
                while True:
                    a = f.readline()
                    if data_start in a:
                        break
            raw_data = f.read()
        rows = [split(raw_row, col_delim) for raw_row in split(raw_data, row_delim)]
        parse_col = lambda index : self._parse_col(rows[1:], index, float)
        self.data = {
            label : parse_col(index) for index, label in enumerate(rows[0])
        }

    def _parse_col(self, rows, col_ind, conv=None):
        if not conv:
            return [row[col_ind] for row in rows]
        try:
            return [conv(row[col_ind]) for row in rows]
        except ValueError:
            return self._parse_col(rows, col_ind, None)
        except IndexError:
            raise IndexError('A data element is missing.')

    def get_column(self, data_label):
        return self.data[data_label]

    # returns dict of format {class_id : { label : data_column}}
    def get_classified_columns(self, classifier, class_label, *labels):
        if len(labels) is 0:
            labels = [class_label]
        classes = {}
        class_col = self.get_column(class_label)
        for row_ind in range(len(class_col)):
            class_id = class_col[row_ind]
            if classifier is not None:
                class_id = classifier(class_id)
            for label in labels:
                col = self.data[label]
                if class_id not in classes:
                    classes[class_id] = {}
                if label not in classes[class_id]:
                    classes[class_id][label] = []
                classes[class_id][label].append(col[row_ind])
        return classes

    def map_columns(self, fn, *labels):
        columns = [self.get_column(l) for l in labels]
        return map(fn, *columns)
