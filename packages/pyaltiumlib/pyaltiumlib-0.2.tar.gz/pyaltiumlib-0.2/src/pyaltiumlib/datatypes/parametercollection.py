class ParameterCollection:
    
    def __init__(self, data = None):

        self.num_blocks = 0
        self.collection = []
        
        if data:
            self._parse( data )
        else:
            self.data = None

        
    @classmethod
    def from_block(cls, olestream, sizelength=4):
        """
        Alternate constructor to create a ParameterCollection from a block.
        Parses an ole stream block containing a parameter collection
        """ 
        length = int.from_bytes( olestream.read( sizelength ), "little" )
        
        data = olestream.read( length )
        
        if len(data) != length:
            raise ValueError("Stream does not match the declared block length.") 
                
        return cls( data )


    def __call__(self):
        """
          Returns:
                dict: The parameters stored in the collection.
        """
        return  self.collection[0] if self.num_blocks == 1 else self.collection
 
    
    def get_record(self):
        """
          Returns:
                int | None: The record id stored in the collection.
        """
        if self.num_blocks == 1:
            return self.get("record", None)
            
        return None

       
    def get(self, keys, default=None):
        """
        Retrieves all values corresponding to the given keys.
    
        Args:
            keys (str | list): A key or a list of keys to search for in the collection.
            default (any, optional): The value to return if a key is not found. Defaults to None.
    
        Returns:
            dict | list | str: A dictionary where the key is the requested key and the value
                               is either a single value or a list of values if the key exists
                               in multiple records. If a single key is provided, returns its
                               corresponding values directly or the `default` value if not found.
        """
        if isinstance(keys, str):
            keys = [keys]
        
        if not isinstance(keys, list):
            raise TypeError("The `keys` argument must be a string or a list of strings.")

        keys = [key.lower() for key in keys]
        result = {}
        
        for key in keys:
            values = []
            
            for record in self.collection:
                lower_record = {k.lower(): v for k, v in record.items()}
                if key in lower_record:
                    values.append(lower_record[key])
                    
            if values:
                result[key] = values if len(values) > 1 else values[0]
            else:
                result[key] = default
                
        return result if len(keys) > 1 else result.get(keys[0], default)   


    def get_bool(self, key, default=False):
        """
        Retrieves value corresponding to the given key as boolean
        
        Args:
            key (str): A key to search for in the collection.
    
        Returns:
            bool: The corresponding boolean value.
        """
        
        value = self.get( key, None)
        
        if isinstance(value, list):
            raise TypeError("The `keys` argument must be a string.")
                
        if isinstance(value, str):
            value = value.strip().upper()
            if value == "T":
                return True
            else:
                return default
            
        else:
            return default
            
            
            
    def _parse(self, data):
        """
        Parses a block containing separated parameters as data, each 0x00 terminated.
        The encoding used is mostly Windows-1252 / ANSI.
    
        Each parameter in the collection is separated using '|'.
        The key and value of each parameter are separated by '='.
        """       
                
        if len( data ) == 0:
            return 
        
        try:
           decoded_data = data.decode('windows-1252')
           
        except UnicodeDecodeError as e:
               raise ValueError("Failed to decode data using Windows-1252 encoding.") from e      
    
        if not decoded_data.endswith("\x00"):
            raise ValueError("Data does not end with 0x00.")
            
        # Split by line breaks or "RECORD" to handle separate blocks
        decoded_data = decoded_data[:-1].replace("|RECORD", "\n|RECORD")
        blocks = [block for block in decoded_data.splitlines() if block]
    
        self.num_blocks = len(blocks)

        for block in blocks:
            record = {}
            for entry in block.split("|"):
                if "=" in entry:
                    key, value = entry.split("=", 1)
                    if key in record:
                        raise ValueError(f"Invalid data. Record {key} already exists in parsed data!")
                    record[key] = value
                    
            if len(record):
                self.collection.append(record)
            
        if len(self.collection) != self.num_blocks:
            raise ValueError("Invalid data. Length of parameter collection not expected!")
            