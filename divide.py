def main():
	print("Let's implement division. Type two numbers for x and y")
	
	x=int(input("x > "))
	y=int(input("y > "))
	if divide(x,y)=="no":
		return()	
	else:
		print("%d / %d = %0.3f" % (x,y,divide(x,y)))
		
def divide(x,y):
	if y==0:
		print("Error: cannot divide by zero.")
		return("no")
	else:
		return(x/y)

if __name__=="__main__":
	main()
