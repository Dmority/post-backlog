import requests
import os

def lambda_handler(event, context):
    
    if 0 >= len(event["detail"]["affectedEntities"]):
        return 0
    
    ##リスト定義
    listincident = []
    listaffectedInstances = []
    listbacklogdetail = []

    ##件名設定
    strbacklogtitle = "{0}  {1}".format(event["detail-type"], event["detail"]["eventTypeCode"])

    ##通知内容取得
    for info in range(0,len(event["detail"]["eventDescription"])):
        listincident.append(event["detail"]["eventDescription"][info]["latestDescription"])
    
    ##影響対象取得    
    for item in range(0, len(event["detail"]["affectedEntities"])):
        listaffectedInstances.append(event["detail"]["affectedEntities"][item]["tags"]["Name"])
    
    ##backlogにアウトプットする文面を作成
    strbacklogdetail = "AWSより次の通知を受信しました。\n\
                        {detail}\n\
                        対象サービス\n\
                        {service}\n\
                        対象インスタンス\n\
                        {instance}\n\
                        ご担当者様はご対応をお願いします。\
                        ".format(detail = "\n".join(listincident), service = event["detail"]["service"], instance = "\n".join(listaffectedInstances))

    payload = {
        "projectId" : os.environ['project_id'],
        "summary" : strbacklogtitle,
        "description" : strbacklogdetail,
        "issueTypeId" : "167245",
        "priorityId" : "1"
    }

    print(payload)

## manageタグ毎に異なるプロジェクトにPostするロジック追加予定

    r = requests.post(os.environ['backlog_url'], data=payload)
    print(r.text)

    return 0

