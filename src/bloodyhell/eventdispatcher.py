import pygame


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

    def listen(self, event_name):
        self._callbacks[getattr(pygame, event_name.upper())] = getattr(
            self, 'on_%s' % event_name
        )

    def listen_key(self, key_name):
        self._keys_callbacks[getattr(pygame, 'K_%s' % key_name.upper())] = {
            'down': getattr(self, 'on_%s_pressed' % key_name.lower()),
            'up': getattr(self, 'on_%s_released' % key_name.lower()),
        }

    def on_frame(self, delta):
        for dispatcher in self._sub_dispatchers:
            dispatcher.on_frame(delta)

    def on_event(self, event):
        for dispatcher in self._sub_dispatchers:
            if dispatcher.on_event(event) == False:
                return False
        if event.type in self._callbacks:
            self._callbacks[event.type](event)

    def on_keydown(self, event):
        if event.key in self._keys_callbacks:
            self._keys_callbacks[event.key]['down']()

    def on_keyup(self, event):
        if event.key in self._keys_callbacks:
            self._keys_callbacks[event.key]['up']()
