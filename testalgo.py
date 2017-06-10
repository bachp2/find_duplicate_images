list1 = [1,2,6,7,8,11,12,14,15]
list2 = [0,3,4,5,9,10,13]

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