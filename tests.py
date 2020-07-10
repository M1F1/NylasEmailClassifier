import unittest
from create_train_predict import preprocessing

class TestFunctions(unittest.TestCase):

    def test_preprocessing(self):
        data = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "https://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html xmlns="https://www.w3.org/1999/xhtml">
            <head>
            <title>Test           Email         Sample    </title>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <meta http-equiv="X-UA-Compatible" content="IE=edge" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0 " />
            <style>
            <!--- CSS code (if any) --->
            </style>
            </head>'''
        expected_result = 'Test Email Sample'
        output = preprocessing(data)
        self.assertEqual(expected_result, output)

if __name__ == '__main__':
    unittest.main()
