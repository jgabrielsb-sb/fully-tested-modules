import unittest
from packag.modules.string_operations import (
    StringOperationsPipeline,
    remove_all_accents,
    remove_all_spaces
)

# Dummy subclass just for instantiating the abstract class (if needed)
class ConcretePipeline(StringOperationsPipeline):
    pass

class TestStringOperationsPipeline(unittest.TestCase):

    def test_pipeline_runs_successfully(self):
        """Pipeline should apply all functions in order correctly."""

        input_text = "Olá Mundo"
        pipeline = [
            remove_all_accents,
            remove_all_spaces,
            str.upper
        ]
        expected_result = "OLAMUNDO"

        pipeline = ConcretePipeline(pipeline)
        result = pipeline.run(input_text)
        self.assertEqual(result, expected_result)

    def test_empty_pipeline_returns_same_string(self):
        """If pipeline is empty, text should remain unchanged."""

        input_text = "Test String"
        pipeline = []
        expected_result = "Test String"

        pipeline = ConcretePipeline(pipeline)
        result = pipeline.run(input_text)
        self.assertEqual(result, expected_result)

    def test_invalid_text_type_in_constructor(self):
        """Should raise TypeError if text is not a string."""

        input_text = 123  # invalid
        pipeline = []

        with self.assertRaises(TypeError) as context:
            ConcretePipeline(pipeline).run(input_text)
            
        self.assertEqual(str(context.exception), "Input 'text' must be a string")

    def test_invalid_pipeline_type(self):
        """Should raise TypeError if pipeline is not a list."""

        input_text = "text"
        pipeline = "not a list"  # invalid

        with self.assertRaises(TypeError) as context:
            ConcretePipeline(pipeline).run(input_text)
            
        self.assertEqual(str(context.exception), "Input 'pipeline' must be a list")

    def test_pipeline_with_non_callable_function(self):
        """Should raise TypeError if any pipeline element is not callable."""

        input_text = "text"
        pipeline = [remove_all_spaces, "not_a_function"]

        with self.assertRaises(TypeError) as context:
            ConcretePipeline(pipeline).run(input_text)
            
        self.assertEqual(str(context.exception), "Input 'pipeline' must be a list of Callable functions")


    def test_pipeline_with_single_function(self):
        """Should apply a single transformation function correctly."""

        input_text = "  spaced out "
        pipeline = [remove_all_spaces]
        expected_result = "spacedout"

        pipeline = ConcretePipeline(pipeline)
        result = pipeline.run(input_text)
        self.assertEqual(result, expected_result)

    def test_invalid_output(self):
        """Should raise TypeError if output is not a string"""

        input_text = "123"
        pipeline = [
            int
        ]
        with self.assertRaises(TypeError) as context:
            pipeline = ConcretePipeline(pipeline)
            result = pipeline.run(input_text)
    
        self.assertEqual(str(context.exception), "Output must be a string")
        
if __name__ == "__main__":
    unittest.main()