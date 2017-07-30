list1 = [1,2,6,7,8,11,12,14,15]
list2 = [0,3,4,5,9,10,13]

'''
 A problem with deleting multiple items from qlistwidget using QListWidget.takeItem is that 
 the index of each item will change relative to the deleted position, thus making a for loop for deletion impossible.
 A solution for this problem is to find the the correct position of item's index with each deletion. 
 To understand the algo, note that the new position will tends to 0 as each deletion from the chain
 since we are removing it sequentially. However, we have checked items as
 well as unchecked items, thus, the item's new position will tend to the closest uncheckable items (lower in index)
 relative to the item's current position.

'''

if __name__ == '__main__':
	count = 0
	for e in range(len(list1)):
		while count < len(list2):
			if list1[e] < list2[count]:
				list1[e] = count
				break
			else:
				count = count + 1
		if count == len(list2):
				list1[e] = count
	print(list1)

	#[1, 1, 4, 4, 4, 6, 6, 7, 7]
