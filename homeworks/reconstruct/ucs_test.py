import util

frontier = util.PriorityQueue()
frontier.update(1, 0)
frontier.update(1, 1)
print frontier.removeMin()
print frontier.removeMin()