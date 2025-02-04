import yaml
import zlib
import os
import threading

class _Types():
    def __init__(self):
        self.ACTION_ADD_VALUE = -101
        self.ACTION_REMOVE_VALUE = -102
        self.ACTION_READ_VALUES = -103
        self.ACTION_READ_VALUE = -104
        self.ACTION_SET_VALUE = -105
        self.ACTION_GET_LAST_ID = -106
types = _Types()

class _Action():
    def __init__(self, type, action_id, args={}):
        self.type = type
        self.action_id = action_id
        self.args = args

class DatabaseNotFound(Exception): pass
class HeaderNotFound(Exception): pass
class ServiceNotWorking(Exception): pass

def _read(filename):
    with open(filename, 'rb') as f:
        raw = f.read()
        text = zlib.decompress(raw)
        return yaml.load(text, yaml.Loader)

def _write(filename, data):
    with open(filename, 'wb') as f:
        raw = yaml.dump(data)
        text = zlib.compress(raw.encode())
        f.write(text)

class Service():
    def __init__(self, filename):
        self.queue = []
        self.filename = filename + '.nxdb'
        if not os.path.exists(self.filename):
            raise DatabaseNotFound(f'Try to use "nxdb-cli create_db {filename}" in terminal')
        self.working = False
        self._lastid = -1
        self.ids = {}
    def _new_action(self):
        if not self.working:
            raise ServiceNotWorking()
        self._lastid += 1
        return self._lastid
    def _wait_for_return(self, id):
        while True:
            if id in self.ids:
                return self.ids[id]
    def add_value(self, key, values):
        id = self._new_action()
        self.queue.append(_Action(types.ACTION_ADD_VALUE, id, {'key': key, 'values': values}))
    def read_values(self):
        id = self._new_action()
        self.queue.append(_Action(types.ACTION_READ_VALUES, id))
        return self._wait_for_return(id)
    def remove_value(self, key):
        id = self._new_action()
        self.queue.append(_Action(types.ACTION_REMOVE_VALUE, id, {'key': key}))
    def get_last_id(self):
        id = self._new_action()
        self.queue.append(_Action(types.ACTION_GET_LAST_ID, id, {}))
        return self._wait_for_return(id)
    def _start_service(self):
        while True:
            if not self.working:
                break
            if len(self.queue) > 0:
                action = self.queue[0]
                # Start processing
                if action.type == types.ACTION_ADD_VALUE:
                    db = _read(self.filename)
                    item = {}
                    for k, v in action.args['values'].items():
                        item[k] = v
                    db[action.args['key']] = item
                    _write(self.filename, db)
                elif action.type == types.ACTION_READ_VALUES:
                    self.ids[action.action_id] = _read(self.filename)
                elif action.type == types.ACTION_GET_LAST_ID:
                    max_id = -1
                    for k, v in _read(self.filename).items():
                        if k > max_id: max_id = k
                    self.ids[action.action_id] = max_id
                elif action.type == types.ACTION_REMOVE_VALUE:
                    db = _read(self.filename)
                    if action.args['key'] in db:
                        db.pop(action.args['key'])
                        _write(self.filename, db)
                    else: pass
                # End processing
                self.queue.pop(0)
    def start_service(self):
        self.working = True
        self.thread = threading.Thread(target=self._start_service)
        self.thread.start()
    def stop_service(self):
        self.working = False
