stop_words=set()
with open("food_stop.txt") as file:
	stops = [line.strip() for line in file]
	stop_words=set(stops)
