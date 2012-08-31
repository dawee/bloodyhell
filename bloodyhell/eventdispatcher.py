

class EventDispatcher(object):

    def __init__(self, auto_listen_keys=True):
        self._callbacks = {}
        self._keys_callbacks = {}
        self._sub_dispatchers = []
        if auto_listen_keys:
            self.listen('keydown')
            self.listen('keyup')

    def add(self, dispatcher):
        self._sub_dispatchers.append(dispatcher)

    def remove(self, dispatcher_to_remove):
        index = 0
        for dispatcher in self._sub_dispatchers:
            if dispatcher is dispatcher_to_remove:
                self._sub_dispatchers.pop(index)
            index += 1

    def listen(self, event_name):
        pass

    def listen_key(self, key_name):
        pass

    def on_frame(self, delta):
        for dispatcher in self._sub_dispatchers:
            dispatcher.on_frame(delta)

    def on_event(self, event):
        for dispatcher in self._sub_dispatchers:
            dispatcher.on_event(event)
        if event.type in self._callbacks:
            self._callbacks[event.type](event)

    def on_keydown(self, event):
        if event.key in self._keys_callbacks:
            self._keys_callbacks[event.key]['down']()

    def on_keyup(self, event):
        if event.key in self._keys_callbacks:
            self._keys_callbacks[event.key]['up']()
