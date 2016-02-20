import re
import pprint

TALENTBOT_USER_ID = 'U0CJKS2DD'

class SlackEvent:

    prefixedTalentBotId = '<@{}>'.format(TALENTBOT_USER_ID)

    def __init__(self, jsonStr):
        self.jsonStr = jsonStr
        
    def __str__(self):
        #return str(self.jsonStr)
        return pprint.pformat(self.jsonStr, indent=1, width=60)

    def isMessage(self):
        return ('type' in self.jsonStr) and ('message' in self.jsonStr['type'])
    
    def hasUser(self):
        return 'user' in self.jsonStr
        
    def isTalentBot(self):
        return self.jsonStr['user'] == TALENTBOT_USER_ID

    def isForTalentBot(self):
        return self.jsonStr['text'].find(self.prefixedTalentBotId) == 0

    def hasAdditionalAddressee(self):
        return self.jsonStr['text'].rfind('<@') > 0

    def isDirectMsgForTalentBot(self):
        return self.jsonStr.get('channel','').find('D') == 0

    def channel(self):
        return self.jsonStr['channel']
        
    def text(self):
        return self.jsonStr['text']
        
    def textContains(self, inputStr):
        return ('text' in self.jsonStr) and inputStr in self.jsonStr['text']
        
    def textContainsKeyword(self, keyword):
        return ('text' in self.jsonStr) and re.compile('^' + keyword + '(\\s|$)', re.IGNORECASE).match(self.jsonStr['text'])

    def getKeywordArguments(self, keyword):
        return self.text().replace(keyword, '').strip()

    def userKey(self):
        jsonStrText = self.jsonStr['text']
        jsonStrText = jsonStrText.replace(self.prefixedTalentBotId,'')
        jsonStrText = jsonStrText.replace(':','').strip()[2:-1]
        return jsonStrText
