"""
Custom exceptions
"""
 
class CustomException(Exception):
    """
    Raised if the name of the element already exists in the namespace.
    """
    def __init__(self, err_message):
        super(CustomException, self).__init__(self)
        self.message = err_message
               
        

        
        