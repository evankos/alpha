

class CustomAssertions:
    def assertDictHasKey(self,dict_,key):
        if isinstance(dict_,dict):
            if not key in dict_.keys():
                raise AssertionError('Dictionary does not contain key %s' % key.__str__())
        else:
            raise AssertionError('Object is not a dictionary instance')