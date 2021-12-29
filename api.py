import math
def bin_search_f(l,x):
	st=0
	end=len(l)-1
	while st<=end:
		mid=(st+end)//2
		if l[mid]==x:
			if mid==0 or l[mid-1]<x:
				return mid
			else:
				end=mid-1
		if l[mid]<x:
			st=mid+1
		if l[mid]>x:
			end=mid-1
def bin_search_l(l,x):
	st=0
	end=len(l)-1
	while st<=end:
		mid=(st+end)//2
		if l[mid]==x:
			if mid==len(l)-1 or l[mid+1]>x:
				return mid
			else:
				st=mid+1
		if l[mid]<x:
			st=mid+1
		if l[mid]>x:
			end=mid-1
def occurrence(L, x):
	f=bin_search_f(L,x)
	l=bin_search_l(L,x)
	return f,l
L = [int(item) for item in input().split(" ")]
x = int(input())
print(occurrence(L,x))