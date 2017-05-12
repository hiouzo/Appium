from .result import BbtResult


class BbtRunner(object):
    def run(self, test):
        result = BbtResult()
        result.startTestRun()
        try:
            test(result)
        finally:
            result.stopTestRun()
        result.printErrors()
        return result
