import logging
import os 
from dotenv import load_dotenv
from pathlib import Path
from imbox import Imbox 

def setup_logging(file_path):
    # grab filename from path
    filename = file_path.split('/')[-1].split('.csv')[0]
    if not os.path.isdir('../logs'):
        os.mkdir('../logs')
   
    logging.basicConfig(filename=f'../logs/{filename}.log', level=logging.INFO)
    logging.info('BEGIN LOGGING')
    logging.info('Loading env file.')
    


def connect_gmail():
    filenames = []
    data_path = '../data'
    # create data path if needed
    if not os.path.isdir('../data'):
        os.makedirs(data_path, exist_ok=True)
    # create inbox connection to google
    mail = Imbox(os.getenv('APP_HOST'), username=os.getenv('APP_USER'), password=os.getenv('APP_PASSWORD'), ssl=True, ssl_context=None, starttls=False)
    # Grab unread messages containing PARSE in subject. 
    #TODO: Add safe sender only
    messages = mail.messages(subject="[PARSE]",unread=True) 
    # download attachments
    for (uid, message) in messages:
        mail.mark_seen(uid) # optional, mark message as read
        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                filenames.append(att_fn)
                download_path = f"{data_path}/{att_fn}"
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
            except Exception as e:
                print(e)
    mail.logout()
    return filenames



def load_env():
    if not os.path.isdir('../env'):
        os.mkdir('../env')
        with open('../env/.env', "w+") as f:
            f.write("APP_PASSWORD=")
    dotenv_path = Path('../env/.env')
    load_dotenv(dotenv_path=dotenv_path)


def main():
    load_env()
    connect_gmail()

if __name__ == "__main__":
    main()