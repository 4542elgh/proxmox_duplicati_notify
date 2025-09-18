import json
import config
import logging
from model import DuplicatiBackupResult
from Notification.Notification import Notification
from config import Config
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()
config = Config()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    """
    Duplicati Backup Webhook Listener

    In Duplicati, you need to add --send-http-json-urls flag in Options tab (Step 5)
    Each time a backup is finished, Duplicati will send a json object to this url. 
    This Flask server capture the json object, extract useful fields, and send message if there is an error
    """
    logger: logging.Logger = logging.getLogger()

    duplicati_obj:DuplicatiBackupResult = DuplicatiBackupResult(**(request.get_json()))
    logger.debug(duplicati_obj)

    notification = Notification(config.NOTIFICATION_SERVICE, config.WEBHOOK_URL, config.APPRISE_TAG, config.DUPLICATI_URL) # type: ignore

    if (duplicati_obj.Data.ErrorsActualLength > 0):
        logger.info("Found error in backup process: %s", duplicati_obj.Extra.OperationName)
        notification.send(f"{duplicati_obj.Extra.OperationName} task failed for **{duplicati_obj.Extra.backup_name}** with message:\n{"\n".join([line for line in duplicati_obj.Exception.split("\n") if not line.strip().startswith("at")])}", severity="error")
    elif (duplicati_obj.Data.WarningsActualLength > 0):
        logger.info("Found warning in backup process: %s", duplicati_obj.Extra.OperationName)
        notification.send(f"{duplicati_obj.Extra.OperationName} task completed for **{duplicati_obj.Extra.OperationName}** with {duplicati_obj.Data.WarningsActualLength} warnings", severity="error")

    return (json.dumps({'success':True}), 200, { 'ContentType':'application/json' })

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = config.PORT)
