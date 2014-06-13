# Twitter Plugin
import twitter




class Twitter_Plugin(object):

    def __init__(self):
    #def setUp(self):
        print "setup"
        api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                              consumer_secret=TWITTER_CONSUMER_SECRET,
                              access_token_key=TWITTER_OAUTH_TOKEN,
                              access_token_secret=TWITTER_OAUTH_TOKEN_SECRET)
        self._api = api

    def send_twit(self, approver, vapp_vm):
        '''
        Mention al approver with info for the task: VM/Vapp Name
        TODO: Listener a reply. How?
        '''
        twit = approver + " please confirm my request for " + vapp_vm
        self._api.PostUpdate(twit)
        return "sent"

    def twitter_main(self, tasks):
        # parse tasks to get enterprise_name, vapp_vm
        enterprise_name = 'fake'
        vapp_vm = 'other'
        self.send_twit(enterprise_name, vapp_vm)

    def workflow_approved():
        return True

if __name__ == '__main__':
    Twitter_Plugin().send_twit("@xfernadez", "Guindous")
