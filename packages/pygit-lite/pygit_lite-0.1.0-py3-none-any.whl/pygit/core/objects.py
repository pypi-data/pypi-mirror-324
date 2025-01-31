# pygit/core/objects.py
import hashlib
import zlib
import os
import json

class GitObject:
    def __init__(self, data=None):
        self.data = data

    def serialize(self):
        """Serialize the data"""
        raise NotImplementedError

    def deserialize(self, data):
        """Deserialize the data"""
        raise NotImplementedError

class Blob(GitObject):
    fmt = b'blob'

    def serialize(self):
        return self.data

    def deserialize(self, data):
        self.data = data

class Tree(GitObject):
    fmt = b'tree'

    def __init__(self, data=None):
        super().__init__()
        self.data = data or {}  # Initialize empty dict if no data

    def serialize(self):
        return json.dumps(self.data).encode()

    def deserialize(self, data):
        self.data = json.loads(data.decode())
        return self

def hash_object(data, obj_type, write=True):
    """Hash contents and optionally write to object store"""
    header = f"{obj_type} {len(data)}".encode()
    full_data = header + b'\x00' + data
    sha1 = hashlib.sha1(full_data).hexdigest()
    
    if write:
        path = os.path.join('.pygit', 'objects', sha1[:2], sha1[2:])
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'wb') as f:
                f.write(zlib.compress(full_data))
    
    return sha1

def read_object(sha1):
    """Read object with given SHA-1 from object store"""
    path = os.path.join('.pygit', 'objects', sha1[:2], sha1[2:])
    
    if not os.path.exists(path):
        raise Exception(f"Object {sha1} not found")
        
    with open(path, 'rb') as f:
        raw = zlib.decompress(f.read())
        
    # Read object type
    x = raw.find(b'\x00')
    if x < 0:
        raise Exception("Invalid object format")
    fmt = raw[0:x].decode().split()[0]
    
    # Read and convert object data
    data = raw[x+1:]
    
    if fmt == 'blob':
        return Blob(data)
    elif fmt == 'tree':
        tree = Tree()
        tree.deserialize(data)
        return tree
    elif fmt == 'commit':
        from .commit import Commit
        return Commit.deserialize(data)
    else:
        raise Exception(f"Unknown object type {fmt}")
