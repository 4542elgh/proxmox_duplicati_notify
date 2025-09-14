import json
import config
from model import DuplicatiBackupResult
from notification import Notification
from config import Config
from flask import Flask, request
from dotenv import load_dotenv

# In Duplicati, you need to add --send-http-json-urls flag in Options tab (Step 5)
# Each time a backup is finished, Duplicati will send a json object to the url. This basically capture the json, abstract the small bits, and send message if there is an error
load_dotenv()
config = Config()

app = Flask(__name__)

@app.route('/', methods=['POST'])
def main():
    duplicati_obj:DuplicatiBackupResult = DuplicatiBackupResult(**(request.get_json()))
    notification = Notification(config.NOTIFICATION_SERVICE, config.WEBHOOK_URL, config.APPRISE_TAG, config.DUPLICATI_URL)

    if (duplicati_obj.Data.ErrorsActualLength > 0):
        notification.send(f"{duplicati_obj.Extra.OperationName} task failed for **{duplicati_obj.Extra.backup_name}** with message:\n{"\n".join([line for line in duplicati_obj.Exception.split("\n") if not line.strip().startswith("at")])}", severity="error")
    elif (duplicati_obj.Data.WarningsActualLength > 0):
        notification.send(f"{duplicati_obj.Extra.OperationName} task completed for **{duplicati_obj.Extra.OperationName}** with {duplicati_obj.Data.WarningsActualLength} warnings", severity="error")

    return (
        json.dumps({'success':True}),
        200,
        { 'ContentType':'application/json' }
    )

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = config.PORT)
