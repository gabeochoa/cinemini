import re 

#converts from 00:00:00.000 to 0 seconds 
def cvsecs(time):
	if (',' not in time) and ('.' not in time):
		time = time + '.0'
	expr = r"(\d+):(\d+):(\d+)[,|.](\d+)"
	finds = re.findall(expr, time)[0]
	nums = list( map(float, finds) )
	return ( 3600*int(finds[0])
			+ 60*int(finds[1])
			+ int(finds[2])
			+ nums[3]/(10**len(finds[3])))