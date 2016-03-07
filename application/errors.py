"""
    errors.py
    
    Python source file declaring exception types that may be thrown at
    any time during the import process.

    Copyright (c) 2016 Robert MacGregor
    This software is licensed under the MIT license. Refer to LICENSE.txt for
    more information.
"""

class ImporterError(Exception):
    """
        A generic importer exception type. All exceptions thrown by the importer
        code itself should be of at least this type.
    """
    pass
