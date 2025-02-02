class LabelEncoder:
    def __init__(self):
        self.mapping = {}
        self.inverse_mapping = {}
    
    def fit(self, labels):
        unique_labels = set(labels)

        for i, label in enumerate(unique_labels):
            self.mapping[label] = i
            self.inverse_mapping[i] = label

    def transform(self, labels):
        for i, label in enumerate(labels):
            labels[i] = self.mapping[label]
        return labels

    def inverse_transform(self, labels):
        for i, label in enumerate(labels):
            labels[i] = self.inverse_mapping[label]
        return labels

    def fit_transform(self, labels):
        self.fit(labels)
        return self.transform(labels)