import logging
from qlik_sdk import Qlik, NxApp, Doc, GenericObjectProperties, NxInfo, NxMetaDef
from utils.config import getConfig
from utils.helpers import return_relative_url
from time import sleep


def create_app(q: Qlik):
    app = {"attributes": {"name": "App Demo"}}
    r = q.rest(method="POST", path="/apps", data=app)
    if r.status_code != 200:
        logging.error(
            "App could not be created. Please check the response for more details.")
        exit()
    logging.info("App created successfully")
    return r


def set_script(q: Qlik, app_id: str):
    script = {"script": "t1:LOAD RAND()*1000 AS A, RAND()*10000 AS B, RECNO() AS ID,Mod(RECNO(),33) AS DIM AUTOGENERATE 1000;",
              "versionMessage": "initial version"}
    r = q.rest(method="POST", path=f"/apps/{app_id}/scripts", data=script)
    if r.status_code != 200:
        logging.error(
            "Could not be the script. Please check the response for more details.")
        exit()
    logging.info("Script set successfully")
    return r


def reload_app(q: Qlik, app_id: str):
    d = {"appId": app_id}
    r = q.rest(method="POST", path="/reloads", data=d)
    if r.status_code != 201:
        logging.error(
            "Could not reload the app. Please check the response for more details.")
        exit()
    logging.info("Reload started successfully, waiting for it to finish")
    sleep(5)
    try:
        href = r.json()['links']['self']['href']
    except KeyError:
        logging.error(
            "The response JSON does not contain 'links' or 'self' or 'id'.")
        exit()
    r = q.rest(method="GET", path=return_relative_url(href))
    if r.status_code != 200:
        logging.error(
            "Could not get the reload status. Please check the response for more details.")
        exit()
    logging.info("Reload finished successfully")
    return r


def create_sheet(q: Qlik, app_id: str):
    app: NxApp = q.apps.get(app_id)  # type: NxApp
    sheet = app.create_object(qProp=GenericObjectProperties(
        qInfo=NxInfo(qType="sheet"), qMetaDef=NxMetaDef(title="Sheet Demo")))
    obj = sheet.create_child(Doc(type="list-object", title="List Object Demo"))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if (config := getConfig()):
        q = Qlik(config)
        r = create_app(q)
        try:
            app_id = r.json()['attributes']['id']
        except KeyError:
            logging.error(
                "The response JSON does not contain 'attributes' or 'id'.")
            exit()
        set_script(q, app_id)
        reload_app(q, app_id)
        create_sheet(q, app_id)
