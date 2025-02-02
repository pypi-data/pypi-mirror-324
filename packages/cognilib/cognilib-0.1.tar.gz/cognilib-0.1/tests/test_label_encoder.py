import unittest
from cognilib.preprocessing import LabelEncoder

class TestLabelEncoder(unittest.TestCase):

    def test_label_encoder(self):
        labels = ['cat', 'dog', 'fish', 'cat', 'dog', 'cat']
        encoder = LabelEncoder()
        encoder.fit(labels)
        encoded_labels = encoder.transform(labels)
        decoded_labels = encoder.inverse_transform(encoded_labels)

        self.assertEqual(labels, decoded_labels, "Decoded labels do not match original labels")

        print("TestLabelEncoder: Test passed!")

if __name__ == '__main__':
    unittest.main()