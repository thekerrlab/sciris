"""
datastore.py -- code related to Sciris database persistence
    
Last update: 2018aug20
"""

import os
import redis
from tempfile import mkdtemp
from shutil import rmtree
import atexit
import sciris as sc

#__all__ = ['data_store', 'file_save_dir', 'uploads_dir', 'downloads_dir', 'FileSaveDirectory', 'StoreObjectHandle', 'DataStore']
__all__ = ['globalvars', 'FileSaveDirectory', 'StoreObjectHandle', 'DataStore']

################################################################################
### Globals
################################################################################

# These will get set by calling code -- these need to be in a class so they can be imported.
class GlobalVars:
    data_store    = None # The DataStore object for persistence for the app.  Gets initialized by and loaded by init_datastore().
    file_save_dir = None # Directory (FileSaveDirectory object) for saved files.
    uploads_dir   = None # Directory (FileSaveDirectory object) for file uploads to be routed to.
    downloads_dir = None # Directory (FileSaveDirectory object) for file downloads to be routed to.

globalvars = GlobalVars()

################################################################################
### Classes
################################################################################
    
class FileSaveDirectory(object):
    """
    An object wrapping a directory where files may get saved by the web 
    application.
    
    Methods:
        __init__(dir_path: str [None], temp_dir: bool [False]): void -- 
            constructor
        cleanup(): void -- clean up after web app is exited
        clear(): void -- erase the contents of the directory
        delete(): void -- delete the entire directory
                    
    Attributes:
        dir_path (str) -- the full path of the directory on disk
        is_temp_dir (bool) -- is the directory to be spawned on startup and 
            erased on exit?
        
    Usage:
        >>> new_dir = FileSaveDirectory(transfer_dir_path, temp_dir=True)
    """
    
    def __init__(self, dir_path=None, temp_dir=False):
        # Set whether we are a temp directory.
        self.is_temp_dir = temp_dir
               
        # If no path is specified, create the temp directory.
        if dir_path is None:
            self.dir_path = mkdtemp()
            
        # Otherwise...
        else:
            # Set the path to what was passed in.
            self.dir_path = dir_path
            
            # If the directory doesn't exist yet, create it.
            if not os.path.exists(dir_path):            
                os.mkdir(dir_path)
            
        # Register the cleanup method to be called on web app exit.
        atexit.register(self.cleanup)
            
    def cleanup(self):
        # If we are a temp directory and the directory still exists, do the cleanup.
        if self.is_temp_dir and os.path.exists(self.dir_path):
            # Show cleanup message.
            print('>> Cleaning up FileSaveDirectory at %s' % self.dir_path)
            
            # Delete the entire directory (file contents included).
            self.delete()
            
    def clear(self):
        # Delete the entire directory (file contents included).
        rmtree(self.dir_path)
        
        # Create a fresh direcgtory
        os.mkdir(self.dir_path)
    
    def delete(self):
        # Delete the entire directory (file contents included).
        rmtree(self.dir_path)



class StoreObjectHandle(object):
    """
    An object associated with a Python object which permits the Python object 
    to be stored in and retrieved from a DataStore object.
    
    Methods:
        __init__(uid: UUID [None], type_prefix: str ['obj'], 
            file_suffix: str ['.obj'], instance_label: str['']): void --
            constructor
        get_uid(): UUID -- return the StoreObjectHandle's UID
        file_store(dir_path: str, obj: Object): void -- store obj in 
            the dir_path directory
        file_retrieve(dir_path: str): void -- retrieve the stored object from 
            the dir_path directory
        file_delete(dir_path: str): void -- delete the stored object from the 
            dir_path directory
        redis_store(obj: Object, redis_db: redis.client.StrictRedis): 
            void -- store obj in Redis
        redis_retrieve(redis_db: redis.client.StrictRedis): void -- retrieve 
            the stored object from Redis
        redis_delete(redis_db: redis.client.StrictRedis): void -- delete the 
            stored object from Redis
        show(): void -- print the contents of the object
                    
    Attributes:
        uid (UUID) -- the unique ID for the handle (uuid Python library-related)
        type_prefix (str) -- a prefix that gets added to the UUID to give either 
            a file name or a Redis key
        file_suffix (str) -- a suffix that gets added to files
        instance_label (str) -- a name of the object which should at least be 
            unique across other handles of the save type_prefix
        
    Usage:
        >>> new_handle = StoreObjectHandle(uuid.UUID('12345678123456781234567812345678'), 
            type_prefix='project', file_suffix='.prj', instance_label='Project 1')
    """
    
    def __init__(self, uid=None, type_prefix='obj', file_suffix='.obj', 
        instance_label=''):
        self.uid = sc.uuid(uid) # Set the UID to what was passed in, or if None was passed in, generate and use a new one
        self.type_prefix = type_prefix
        self.file_suffix = file_suffix
        self.instance_label = instance_label
        
    def get_uid(self):
        return self.uid
    
    def file_store(self, dir_path, obj):
        file_name = '%s-%s%s' % (self.type_prefix, self.uid.hex, self.file_suffix) # Create a filename containing the type prefix, hex UID code, and the appropriate file suffix.
        full_file_name = '%s%s%s' % (dir_path, os.sep, file_name) # Generate the full file name with path.
        sc.saveobj(full_file_name, obj) # Write the object to a Gzip string pickle file.
        return None
    
    def file_retrieve(self, dir_path):
        file_name = '%s-%s%s' % (self.type_prefix, self.uid.hex, self.file_suffix) # Create a filename containing the type prefix, hex UID code, and the appropriate file suffix.
        full_file_name = '%s%s%s' % (dir_path, os.sep, file_name) # Generate the full file name with path.
        obj = sc.loadobj(full_file_name) # Return object from the Gzip string pickle file.
        return obj
    
    def file_delete(self, dir_path):
        file_name = '%s-%s%s' % (self.type_prefix, self.uid.hex, self.file_suffix) # Create a filename containing the type prefix, hex UID code, and the appropriate file suffix.
        full_file_name = '%s%s%s' % (dir_path, os.sep, file_name) # Generate the full file name with path.
        if os.path.exists(full_file_name): # Remove the file if it's there.
            os.remove(full_file_name)
        return None
    
    def redis_store(self, obj, redis_db):
        key_name = '%s-%s' % (self.type_prefix, self.uid.hex) # Make the Redis key containing the type prefix, and the hex UID code.
        redis_db.set(key_name, sc.dumpstr(obj)) # Put the object in Redis.
        return None
    
    def redis_retrieve(self, redis_db):
        key_name = '%s-%s' % (self.type_prefix, self.uid.hex) # Make the Redis key containing the type prefix, and the hex UID code.
        obj = sc.loadstr(redis_db.get(key_name)) # Get and return the object with the key in Redis.
        return obj
    
    def redis_delete(self, redis_db):
        key_name = '%s-%s' % (self.type_prefix, self.uid.hex) # Make the Redis key containing the type prefix, and the hex UID code.
        redis_db.delete(key_name) # Delete the entry from Redis.
        return None
        
    def show(self):
        print('          UUID: %s' % self.uid.hex)
        print('   Type prefix: %s' % self.type_prefix)
        print('   File suffix: %s' % self.file_suffix)
        print('Instance label: %s' % self.instance_label)



class DataStore(object):
    """
    An object allowing storage and retrieval of Python objects using either 
    files or the Redis database.  You can think of it as being a generalized 
    key/value-pair-based database.
    
    Methods:
        __init__(db_mode: str ['redis'], redis_db_URL: str [None]): void -- 
            constructor
        save(): void -- save the state of the DataStore either to file or 
            Redis, depending on the mode
        load(): void -- load the state of the DataStore either from file or 
            Redis, depending on the mode
        get_handle_by_uid(uid: UUID or str): StoreObjectHandle -- get the 
            handle (if any) pointed to by an UID            
        get_uid(type_prefix: str, instance_label: str): UUID -- 
            find the UID of the first matching case where a handle in the dict 
            has the same type prefix and instance label        
        add(obj: Object, uid: UUID or str [None], type_label: str ['obj'], 
            file_suffix: str ['.obj'], instance_label: str [''], 
            save_handle_changes: bool [True]): void -- add a Python object to 
            the DataStore, creating also a StoreObjectHandle for managing it, 
            and return the UUID (useful if no UID was passed in, and a 
            new one had to be generated)
        retrieve(uid: UUID or str): Object -- retrieve a Python object 
            stored in the DataStore, keyed by a UID
        update(uid: UUID or str, obj: Object): void -- update a Python object 
            stored in the DataStore, keyed by a UID
        delete(uid: UUID or str, save_handle_changes=True): void -- delete a 
            Python object stored in the DataStore, keyed by a UID
        delete_all(): void -- delete all of the Python objects in the DataStore
        show_handles(): void -- show all of the StoreObjectHandles in the 
            DataStore
        show_redis_keys(): void -- show all of the keys in the Redis database 
            we are using
        clear_redis_keys(): void -- delete all of the keys in the Redis database
            we are using
                    
    Attributes:
        handle_dict (dict) -- the Python dictionary holding the StoreObjectHandles
        db_mode (str) -- the mode of persistence the DataStore uses (either 
            'redis' or 'file')
        redis_db (redis.client.StrictRedis) -- link to the Redis database we 
            are using
        
    Usage:
        >>> data_store = DataStore(redis_db_URL='redis://localhost:6379/0/')                      
    """
    
    def __init__(self, db_mode='redis', redis_db_URL=None):
        self.handle_dict = {} # Start with an empty dictionary.
        if redis_db_URL is not None:
            self.db_mode = 'redis'
        else:
            self.db_mode = db_mode
        if self.db_mode == 'redis': # If we are using Redis...
            self.redis_db = redis.StrictRedis.from_url(redis_db_URL)
        return None
        
    def save(self):
        if self.db_mode == 'redis': # If we are using Redis...
            self.redis_db.set('scirisdatastore-handle_dict',  # Set the entries for all of the data items.
                sc.dumpstr(self.handle_dict))
            self.redis_db.set('scirisdatastore-db_mode', 
                sc.dumpstr(self.db_mode))
        else: # Otherwise (we are using files)...
            outfile = open('.\\sciris.ds', 'wb')
            sc.pickle.dump(self.handle_dict, outfile)
            sc.pickle.dump(self.db_mode, outfile)
        return None
    
    def load(self):
        if self.db_mode == 'redis': # If we are using Redis...
            if self.redis_db.get('scirisdatastore-handle_dict') is None:
                print('Error: DataStore object has not been saved yet.')
                return None
            self.handle_dict = sc.loadstr(self.redis_db.get('scirisdatastore-handle_dict')) # Get the entries for all of the data items.
            self.db_mode = sc.loadstr(self.redis_db.get('scirisdatastore-db_mode'))
        else: # Otherwise (we are using files)...
            if not os.path.exists('.\\sciris.ds'):
                print('Error: DataStore object has not been saved yet.')
                return None
            infile = open('.\\sciris.ds', 'rb')
            self.handle_dict = sc.pickle.load(infile)
            self.db_mode = sc.pickle.load(infile)
        return None
    
    def get_handle_by_uid(self, uid):
        valid_uid = sc.uuid(uid) # Make sure the argument is a valid UUID, converting a hex text to a UUID object, if needed.       
        if valid_uid is not None: # If we have a valid UUID...
            return self.handle_dict.get(valid_uid, None)
        else:
            return None
        
    def get_uid(self, type_prefix, instance_label):
        uid_matches = [] # Initialize an empty list to put the matches in.
        for key in self.handle_dict: # For each key in the dictionary...
            handle = self.handle_dict[key] # Get the handle pointed to.
            if handle.type_prefix == type_prefix and handle.instance_label == instance_label:
                uid_matches.append(handle.uid) # If both the type prefix and instance label match, add the UID of the handle to the list.
        if len(uid_matches) == 0: # If there is no match, return None.   
            return None
        elif len(uid_matches) > 1: # Else, if there is more than one match, give a warning.
            print('Warning: get_uid() only returning the first match.')
        return uid_matches[0] # Return the first (and hopefully only) matching UID.  
        
    def add(self, obj, uid=None, type_label='obj', file_suffix='.obj', instance_label='', save_handle_changes=True):
        valid_uid = sc.uuid(uid) # Make sure the argument is a valid UUID, converting a hex text to a UUID object, if needed.  If no UID is passed in, generate a new one.
        new_handle = StoreObjectHandle(valid_uid, type_label, file_suffix, instance_label) # Create the new StoreObjectHandle.
        self.handle_dict[valid_uid] = new_handle # Add the handle to the dictionary.
        if self.db_mode == 'redis': # If we are using Redis...
            new_handle.redis_store(obj, self.redis_db) # Put the object in Redis.
        else: # Otherwise (we are using files)...
            new_handle.file_store('.', obj) # Put the object in a file.
        if save_handle_changes: # Do a save of the database so change is kept.
            self.save()
        return valid_uid # Return the UUID.
    
    def retrieve(self, uid):
        valid_uid = sc.uuid(uid) # Make sure the argument is a valid UUID, converting a hex text to a UUID object, if needed.   
        if valid_uid is not None:  # If we have a valid UUID...
            handle = self.get_handle_by_uid(valid_uid) # Get the handle (if any) matching the UID.
            if handle is not None: # If we found a matching handle...
                if self.db_mode == 'redis': # If we are using Redis...   
                    return handle.redis_retrieve(self.redis_db) # Return the object pointed to by the handle.
                else: # Otherwise (we are using files)...
                    return handle.file_retrieve('.') # Return the object pointed to by the handle.
        return None # Return None (a failure to find a match).
    
    def update(self, uid, obj):
        valid_uid = sc.uuid(uid) # Make sure the argument is a valid UUID, converting a hex text to a UUID object, if needed. 
        if valid_uid is not None:   # If we have a valid UUID...
            handle = self.get_handle_by_uid(valid_uid) # Get the handle (if any) matching the UID.
            if handle is not None: # If we found a matching handle...
                if self.db_mode == 'redis':    # If we are using Redis...
                    handle.redis_store(obj, self.redis_db) # Overwrite the old copy of the object using the handle.
                else: # Otherwise (we are using files)...
                    handle.file_store('.', obj)  # Overwrite the old copy of the object using the handle.
        return None
     
    def delete(self, uid, save_handle_changes=True):
        valid_uid = sc.uuid(uid) # Make sure the argument is a valid UUID, converting a hex text to a UUID object, if needed.    
        if valid_uid is not None:  # If we have a valid UUID...
            handle = self.get_handle_by_uid(valid_uid)  # Get the handle (if any) matching the UID.
            if handle is not None: # If we found a matching handle...
                if self.db_mode == 'redis': # If we are using Redis...
                    handle.redis_delete(self.redis_db) # Delete the key using the handle.
                else: # Otherwise (we are using files)...
                    handle.file_delete('.') # Delete the file using the handle.
                del self.handle_dict[valid_uid] # Delete the handle from the dictionary.
                if save_handle_changes: # Do a save of the database so change is kept.     
                    self.save()
        return None
               
    def delete_all(self):
        '''
        For each key in the dictionary, delete the key and handle, but don't do the 
        save of the DataStore object until after the changes are made.
        '''
        all_keys = [key for key in self.handle_dict]
        for key in all_keys:
            self.delete(key, save_handle_changes=False)
        self.save() # Save the DataStore object.
        return None
    
    def show_handles(self):
        for key in self.handle_dict: # For each key in the dictionary...
            handle = self.handle_dict[key] # Get the handle pointed to.
            print('--------------------------------------------')
            handle.show() # Show the handle contents.
        print('--------------------------------------------')
        return None
    
    def show_redis_keys(self):
        ''' Show all of the keys in the Redis database we are using. '''
        print(self.redis_db.keys())
        
    def clear_redis_keys(self):
        ''' Delete all of the keys in the Redis database we are using. '''
        for key in self.redis_db.keys():
            self.redis_db.delete(key)