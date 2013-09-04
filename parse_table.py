from string import split

class Table:
    def __init__(self):
        self.labels = []
        self.data = []

    def populate(self, file_name, col_delim="\t", row_delim="\n", data_start=None):
        with open(file_name, 'r') as f:
            if data_start:
                while True:
                    a = f.readline()
                    if a == data_start:
                        break
            raw_data = f.read()
        rows = [split(raw_row, col_delim) for raw_row in split(raw_data, row_delim)]
        self.data = [map(float, row) for row in rows[1:]]
        self.labels = {label: index for index, label in enumerate(rows[0])}

    def get_label_ind(self, label):
        if label not in self.labels:
            raise KeyError('No column with label : "' + label + '".')
        return self.labels[label]

    def get_column(self, data_label):
        col_ind = self.get_label_ind(data_label)
        return [data_row[col_ind] for data_row in self.data]

    # returns dict of format {class_id : { label : data_column}}
    def get_classified_columns(self, classifier, class_label, *labels):
        if len(labels) is 0:
            labels = [class_label]
        classes = {}
        c_ind = self.get_label_ind(class_label)
        for row in self.data:
            class_id = row[c_ind] if classifier is None else classifier(row[c_ind])
            for label in labels:
                d_ind = self.get_label_ind(label)
                if class_id not in classes:
                    classes[class_id] = {}
                if label not in classes[class_id]:
                    classes[class_id][label] = []
                classes[class_id][label].append(row[d_ind])
        return classes

    def map_columns(self, fn, *labels):
        columns = [self.get_column(l) for l in labels]
        return map(fn, *columns)
