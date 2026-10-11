import unittest
from modeling import train_model


class ModelTests(unittest.TestCase):
    def test_model_trains_and_has_expected_parameters(self):
        model, params, metrics = train_model()
        self.assertEqual(params["n_estimators"], 50)
        self.assertIn("accuracy", metrics)
        self.assertGreaterEqual(metrics["accuracy"], 0.0)
        self.assertLessEqual(metrics["accuracy"], 1.0)
        self.assertEqual(len(model.predict([[5.1, 3.5, 1.4, 0.2]])), 1)

    def test_model_predicts_a_valid_class(self):
        model, _, _ = train_model()
        prediction = int(model.predict([[5.1, 3.5, 1.4, 0.2]])[0])
        self.assertIn(prediction, [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
