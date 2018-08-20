import unittest
import create_response


class TestCreateResponse(unittest.TestCase):
    def test_createResponsePath_NonEmptyArray(self):
        title = 'A'
        paths = ['U', 'X', 'F']
        resultDict = create_response.createResponsePath(title, paths)

        self.assertEqual(resultDict['searchTitle'], title)
        self.assertEqual(resultDict['pathTitles'], paths)
        self.assertEqual(resultDict['status'], 'data')
        if 'errors' in resultDict:
            self.fail("key 'errors' found in result")

    def test_createResponsePath_EmptyArray(self):
        title = 'B'
        paths = []
        resultDict = create_response.createResponsePath(title, paths)

        self.assertEqual(resultDict['searchTitle'], title)
        self.assertEqual(resultDict['pathTitles'], paths)
        self.assertEqual(resultDict['status'], 'data')
        if 'errors' in resultDict:
            self.fail("key 'errors' found in result")

    def test_createResponsePath_False(self):
        title = 'C'
        paths = False
        resultDict = create_response.createResponsePath(title, paths)

        self.assertEqual(resultDict['searchTitle'], title)
        self.assertEqual(resultDict['status'], 'no_data')
        if 'errors' in resultDict:
            self.fail("key 'errors' found in result")
        if 'pathTitles' in resultDict:
            self.fail("key 'pathTitles' found in result")

    def test_createResponsePath_None(self):
        title = 'D'
        paths = None
        resultDict = create_response.createResponsePath(title, paths)

        self.assertEqual(resultDict['searchTitle'], title)
        if "error_code_01_tdne" not in resultDict['errors']:
            self.fail("error code not found in result")
        self.assertTrue(resultDict['errors'], 'no_data')
        if 'status' in resultDict:
            self.fail("key 'status' found in result")
        if 'pathTitles' in resultDict:
            self.fail("key 'pathTitles' found in result")

    def test_createResponseStatus_NoData(self):
        title = 'D'
        statusMap = {}
        resultDict = create_response.createResponseStatus(title, statusMap)
        self.assertEqual(resultDict['searchTitle'], title)
        self.assertEqual(resultDict['status'], 'NO_DATA')

    def test_createResponseStatus_NotComplete(self):
        title = 'D'
        statusMap = {'x': '50', 'y': '100'}
        resultDict = create_response.createResponseStatus(title, statusMap)
        self.assertEqual(resultDict['searchTitle'], title)
        self.assertEqual(resultDict['status'], 'NOT_COMPLETE')
        self.assertEqual(resultDict['x'], '50')
        self.assertEqual(resultDict['y'], '100')

        def test_createResponseStatus_Complete(self):
            title = 'D'
            statusMap = {'x': '100', 'y': '100'}
            resultDict = create_response.createResponseStatus(title, statusMap)
            self.assertEqual(resultDict['searchTitle'], title)
            self.assertEqual(resultDict['status'], 'COMPLETE')
            self.assertEqual(resultDict['x'], '100')
            self.assertEqual(resultDict['y'], '100')
