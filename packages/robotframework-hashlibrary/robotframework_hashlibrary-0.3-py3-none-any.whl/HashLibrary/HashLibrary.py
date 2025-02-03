import base64
import binascii
import hashlib

class HashLibrary:
    """This is a Robot Framework library to create base64 hashes from strings.
    This library may be updated in the future in order to provide more hashes and more input types."""
    
    def get_base64_hash_from_string(self, string):
        """Returns the base64 hash of the string that is supplied.
        
        Example:
            | ${hash} | Get Base64 Hash From String | david |
        """
        string_in_bytes = string.encode('utf-8')
        base64_bytes = base64.b64encode(string_in_bytes)
        base64_string = base64_bytes.decode('utf-8')
        print(base64_string)
        return base64_string

    def get_crc32_hash_from_string(self, string):
        """Returns the crc32 hash of the string that is supplied.
        
        Example:
            | ${hash} | Get crc32 Hash From String | david |
        """
        string_in_bytes = string.encode('utf-8')
        crc32_bytes = binascii.crc32(string_in_bytes)
        return hex(crc32_bytes)

    def get_md5_hash_from_string(self, string):
        """Returns the md5 hash of the string that is supplied. 
        
        Example:
            | ${hash} | Get md5 Hash From String | david |
        """
        data = string
        md5_hash = hashlib.md5()
        md5_hash.update(data.encode('utf-8'))
        hash_result = md5_hash.hexdigest()
        return(hash_result)
    
    def get_base64_hash_from_file(self, file_path):
        """Returns the base64 hash of the file that is supplied.
        
        Example:
            | ${hash} | Get Base64 Hash From File | path/to/file.txt |
        """
        try:
            with open(file_path, 'rb') as file:
                base64_encoded = base64.b64encode(file.read()).decode('utf-8')
            print(base64_encoded)
            return base64_encoded
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")
        
    def get_sha256_hash_from_file(self, filepath):
        """Returns the sha256 hash of the file that is supplied.
        
        Example:
            | ${hash} | Get sha256 Hash From File | path/to/file.txt |
        """
        sha256 = hashlib.sha256()
    
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):  # Read file in chucks of 8kb
                sha256.update(chunk)

        return sha256.hexdigest()