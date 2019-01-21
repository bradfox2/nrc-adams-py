#Data Parameters fields
##Filters
##<library-type> parameter

library_types = {'public' : 'public-library:!t',
                 'legacy' : 'legacy-library:!t'}

class Library_type(object):
    '''Encapsulate library types for use in filters.
    
    Attributes:
        library_type (str): library-type parameter, public or legacy
        library_types (dict[str]): library-type: NRC API <library-type> parameter with true flag set
    
    '''

    def __init__(self, library_type, library_types = library_types):
      self.library_type = library_types[library_type]

class Filters(object):
    ''' Filters parameter
    
    Usage:
    >>> Filters().library_type(library_type='public').filters

    Attributes:
        filters (str): string filter to be added to URL.

    '''

    def __init__(self):
        self.filters = 'filters:('
    
    def library_type(self, library_type):
        '''Get a library type string. Chainable.
        Args:
            library_type (str): 'public' > 1999 or 'legacy' < 1999
        '''
        self.filters +=  Library_type(library_type, library_types).library_type + '),'
        return self    

#options fields

