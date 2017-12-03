'''
"""
Created on Sat Nov 18 16:23:04 2017

@author: guglielmo
"""
'''


class binary_search():
    
    def binary_search(self, array,value):
        return self._binary_search(array, 0, len(array)-1, value)
    
    def _binary_search(self, array, low, high, value):
        if low == high:
            if array[low] == value:
                return True
            else:
                return False
        mid = (low + high) // 2
        if array[mid] == value:
            return True
        elif array[mid] < value:
            return self._binary_search(array, mid+1, high, value)
        else:
            return self._binary_search(array, low , mid, value)
        
    def binary_search_index(self, array,value):
        return self._binary_search_index(array, 0, len(array)-1, value)
    
    def _binary_search_index(self, array, low, high, value):
        if low == high:
            if array[low] == value:
                return low
            else:
                return False
        mid = (low + high) // 2
        if array[mid] == value:
            return mid
        elif array[mid] < value:
            return self._binary_search_index(array, mid+1, high, value)
        else:
            return self._binary_search_index(array, low , mid, value)