## @package exceptions
#  Definition of Custom exception

class CustomException(Exception):
    
    def __init__(self, err_message):
        super(CustomException, self).__init__(self)
        self.message = err_message
               
        

        
        