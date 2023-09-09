

# Format an announcement that server is available
# Example "Fortune server active on 20m, send request to group @FORTUNE

class FortuneAnnouncement:

# Fortune metadata, make sure there are some that are short enough to send
    def setup_announcement(self):

        file_list = sorted(glob.glob(fortunes_dir + '*.dat'), reverse=True)
        for entry in file_list:
            logmsg(1,"Checking files ")


    def send_mb_announcement(self, js8call_api: Js8CallApi):
        # get the current epoch
        epoch = time.time()
        if epoch > self.next_announcement:
            message = "Msg to call group @FORTUNE, returns short unix fortune "
            js8call_api.send('TX.SEND_MESSAGE', message)
            # update the next announcement epoch
            self.next_announcement = epoch + (mb_announcement_timer * 60)



