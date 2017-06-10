list1 = [1,2,6,7,8,11,12,14,15]
list2 = [0,3,4,5,9,10,13]

# A problem with deleting multiple items from qlistwidget using QListWidget.takeItem is that 
# the index of each item will change relative to the deleted position, thus making a for loop for deletion impossible.
# A solution for this problem is using this algo to find the the correct position of item's index with each deletion. 
# To understand the algo, notice that the new position will tends to 0 as each deletion from the chain. However, we have checked items as
# well as unchecked items, thus, the item's new position will tend to the closest uncheckable items (lower in index) relative to the 
# item's current position.

if __name__ == '__main__':
	count = 0
	for e in range(len(list1)):
		for m in range(len(list2)):
			if list1[e] < list2[m]:
				list1[e] = count
				break
			else: 
				if count == len(list2)-1:
					list1[e] = count+1
					break
				count = count+1
		count = 0
	print(list1)

	#[1, 1, 4, 4, 4, 6, 6, 7, 7]