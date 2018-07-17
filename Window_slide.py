# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 09:47:01 2018

@author: gurpreet.mohaar
"""

class Window_slide:
    def __init__(self, dataframe, window_size, overlap):
        self._validate(dataframe, window_size, overlap)
        self.df = dataframe
        self._window_size = window_size
        self._overlap = overlap
        self._window_start_index = 0
        self._window_data = None

    def slide(self):
        self._window_data = self.df.iloc[self._window_start_index:self._window_start_index + self._window_size,:]
        if len(self._window_data) == self._window_size:
            self._window_start_index = self._next_window_start_index()
        return self._window_data

    def _validate(self, dataframe, window_size, overlap):
        list_length = len(dataframe)
        if list_length == 0:
            raise ValueError('List cannot be empty')
        if list_length < window_size:
            raise ValueError('Bucket size should be smaller than list size')
        if overlap >= window_size:
            raise ValueError('Overlap count should be lesser than bucket_size')

    def current_position(self):
        if self._window_start_index == 0:
            raise RuntimeError('Slide window first')
        start = (self._window_start_index - self._window_size) + self._overlap
        end = (start + self._window_size) - 1
        if len(self._window_data) < self._window_size:
            start = self._window_start_index
            end = self._list_length() - 1
        return start, end

    def reached_end_of_list(self):
        return len(self._window_data) < self._window_size

    def _list_length(self):
        return len(self.df)

    def _next_window_start_index(self):
        return (self._window_start_index) + self._overlap