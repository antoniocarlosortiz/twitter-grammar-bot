import sys
import tweepy
import json
from datetime import datetime
import os
from grammar_parser import get_spellings
from pprint import pprint
import pickle
import random
import time
import sys
 
auth = tweepy.OAuthHandler(consumer_key = '<get this from twitter>',
                           consumer_secret = '<get this from twitter>')                      
auth.set_access_token(key = '<get this from twitter>',
                      secret = '<get this from twitter>')
                           
api = tweepy.API(auth)
 
MESSAGES = u'''
$USERNAME c'mon son! Its "$CORRECT"!
Hope you remember that "$MISTAKE" is spelled "$CORRECT" in the future, $USERNAME.
'''.split('\n')
 
def search(word):
    '''
    Search twitter for uses of a word, return one if it it's been used recently/
    Otherwise return none.
    '''
    print '------'
    print 'Searching for uses of %s...' % word
    results = api.search(word)
    if results:
        for result in results:
            print "\n"
            print result.user.screen_name
            message = result.text.encode('ascii', 'ignore')
            print message
            word = str(word)
            if not check_if_done(result.id):
                if not result.user.screen_name == 'letsbuyavowel':
                    if word in message or unicode(word) in message or str(word) in message:
                        print "word in message"
                        return result
                    else:
                        print "Either word in username, or word is used as proper noun."
                        print "search for new entry of the chosen word.\n"
 
    return None
 
def update_done(id):
    '''
    Updates a list of tweets that's been replied to.
    '''
    print 'updating done list...'
    if os.path.exists('done.pkl'):
        with open('done.pkl', 'r') as f:
            done = pickle.load(f)
             
        done.append(id)
        with open('done.pkl', 'w') as f:
            pickle.dump(done, f)
            print 'updated done list..'
             
     
def check_if_done(id):
    '''
    Checks if a tweet has already been responded to.
    '''
    if os.path.exists('done.pkl'):
        with open('done.pkl', 'r') as f:
            done = pickle.load(f)
        if id in done:
            return True
        else:
            return False
    else:
        done = []
        with open('done.pkl', 'w') as f:
            pickle.dump(done, f)
     
        return False
 
def compose_message(twitter_post, mistake, correct):
    '''
    Choose a message from MESSAGES at random, substitute fields to personalize it and check
    if it exceeds the twitter message. Try this 100 times before failing.
    '''
    retries = 0
    while retries < 100:
        message = random.choice(MESSAGES)
        message = message.replace('$USERNAME', '@%s' % twitter_post.user.screen_name)
        message = message.replace('$MISTAKE', '%s' % mistake).replace('$CORRECT', '%s' % correct)
        print "message length %s" % len(message)
        if len(message) < 141:
            return message
     
    return None
 
def correct_spelling(twitter_post, mistake, correct):
    '''
    Correct someone's spelling in a twitter post
    '''
    print 'Correcting %s for using %s...' % (twitter_post.user.screen_name, mistake)
    message = compose_message(twitter_post, mistake, correct)
    if not message:
        print 'Message were too long... Aborting...'
        return False
     
    else:
        failures = 0
        try:
            #try if it can be a reply
            api.update_status(message)
        except Exception, e:
            print 'Failed to submit tweet reply to %s' % twitter_post.id
            print e
            return False
         
        return True
         
def main():
    '''
    main program flow
    '''
    words = get_spellings()
    counter = 0
    while True:
        if counter > 10:
            print "Done %s tweets"
            sys.exit()
             
        word = random.choice(words.keys())
        post = search(word)
         
        if post:
            result = correct_spelling(post, word, words[word])
            if result:
                print "post successful"
                update_done(post.id)
                sleeptime = random.randint(300, 400)
                print "sleeping for %s seconds..." % sleeptime
                time.sleep(sleeptime)
                counter = counter + 1
                print "%s Done" % counter
 
if __name__ == "__main__":
    main()
