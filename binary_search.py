'''
"""
Created on Sat Nov 18 16:23:04 2017

@author: DataHubBocconi
"""
'''



def binary_search(array, value):
	return _binary_search(array, 0, len(array)-1, value)

def _binary_search(array, low, high, value):
	if low == high:
		if array[low] == value:
			return True
		else:
			return False
	mid = (low + high) // 2
	if array[mid] == value:
		return True
	elif array[mid] < value:
		return _binary_search(array, mid+1, high, value)
	else:
		return _binary_search(array, low , mid, value)
	
def binary_search_index(array,value):
	return _binary_search_index(array, 0, len(array)-1, value)

def _binary_search_index(array, low, high, value):
	if low == high:
		if array[low] == value:
			return low
		else:
			return False
	mid = (low + high) // 2
	if array[mid] == value:
		return mid
	elif array[mid] < value:
		return _binary_search_index(array, mid+1, high, value)
	else:
		return _binary_search_index(array, low , mid, value)