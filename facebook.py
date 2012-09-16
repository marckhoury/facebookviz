from urllib import urlopen
import json
import sys
import os

access_token = '<ACCESS_TOKEN>'

FRIEND_URL = 'https://graph.facebook.com/me/friends?access_token=%s'
MUTUAL_FRIEND_URL = 'https://graph.facebook.com/me/mutualfriends?user=%s&access_token=%s'


def get_json_data(url):
    urldata = urlopen(url)
    fh = urldata.read()
    return json.loads(fh)

def get_friend_ids(json_data):
	ids = {}
	for friend in json_data['data']:
        	ids[friend['id']] = friend['name']
	return ids

def main(argv):
	json_friends = get_json_data(FRIEND_URL % access_token)
	friends = get_friend_ids(json_friends)
	edges = {}
	print 'graph facebook {'
	for fid in friends.iterkeys():
		edges[friends[fid]] = []
		json_mutual = get_json_data(MUTUAL_FRIEND_URL % (fid,access_token))
		has_mutual = False
		for mutual in json_mutual['data']:
			has_mutual = True
			if mutual['name'] not in edges or friends[fid] not in edges[mutual['name']]:
				print '\t"%s" -- "%s";' % (friends[fid].encode('utf-8'), mutual['name'].encode('utf-8'))
				edges[friends[fid]].append(mutual['name'])
		if not has_mutual:
			print '\t"%s"' % friends[fid].encode('utf-8')
	print '}'

if __name__ == '__main__':
	main(sys.argv[1:])
