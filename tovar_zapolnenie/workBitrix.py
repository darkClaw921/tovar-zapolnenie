from fast_bitrix24 import Bitrix
import os
from dotenv import load_dotenv
from pprint import pprint
from dataclasses import dataclass
from datetime import datetime
# import urllib3
import urllib.request
import time
import asyncio
# from workFlask import send_log
import requests
load_dotenv()
webhook = os.getenv('WEBHOOK')
PORT=os.getenv('PORT')
HOST=os.getenv('HOST')

bit = Bitrix(webhook)

def send_log(message, level='INFO'):
    requests.post(f'http://{HOST}:{PORT}/logs', json={'log_entry': message, 'log_level': level})
@dataclass
class Lead:
    userName:str
    title:str='TITLE'
    userID:str='UF_CRM_1709220784686'
    photos:str='UF_CRM_1709223951925'
    urlUser:str='UF_CRM_1709224894080'
    messageURL:str='UF_CRM_1709293438392'

    description:str='COMMENTS'

@dataclass
class Deal:
    id:str='ID'
    title:str='TITLE'
    categoryID:str='CATEGORY_ID'
    statusID:str='STATUS_ID'
    comments:str='COMMENTS'
    responsibleID:str='ASSIGNED_BY_ID'
    renewals:str='UF_CRM_1717532980'
    renewals2:str="UF_CRM_1718111853"
@dataclass
class Renewal: #товары
    assignedDeal:str='parentId2'
    title:str='title'
    serialNumber:str='ufCrm12_1717525290496'
    productName:str='ufCrm12_1717525467171'
    
    UF_CRM_14_1719314433381='ufCrm14_1719314433381'

@dataclass
class Product_ENTY:
    # id:str='ID'
    assignedDeal:str='parentId2'
    title:str='title'
    priceZakyp:str='ufCrm14_1719314433381'
    discount1:str='ufCrm14_1719314095902'
    discount2:str='ufCrm14_1719314108491'
    # description:str='DESCRIPTION'
    # categoryID:str='CATEGORY_ID'
    # statusID:str='STATUS_ID'
    # responsibleID:str='ASSIGNED_BY_ID'
    

    
# PAY_ENTY_ID=155
# INVOICE_ID=31
PAY_ENTY_ID=os.getenv('PAY_ENTY_ID')
INVOICE_ID=os.getenv('INVOICE_ID')
NUMBER_INVOICE_POLE=os.getenv('NUMBER_INVOICE_POLE')
DATE_INVOICE_POLE=os.getenv('DATE_INVOICE_POLE')
POLE_INVOICE=os.getenv('POLE_INVOICE')

RENEVAL_ENTY_ID=os.getenv('RENEVAL_ENTY_ID')
TOVAR_ENTY_ID=os.getenv('TOVAR_ENTY_ID')




# async def te
def find_deal(dealID:str):
    deal = bit.call('crm.deal.get', items={'id': dealID}, raw=True)['result']
    return deal

def find_lead(leadID:str):
    lead = bit.call('crm.lead.get', params={'id': leadID})
    return lead

def find_invoice(number, date):
    invoice = bit.call('crm.invoice.list', items={'filter': 
                                             {'ACCOUNT_NUMBER':number, 'BEGINDATE':date}}, raw=True)['result']
    return invoice

def find_all_tovar_items(dealID):
    items = bit.call('crm.item.list', items={'entityTypeId':RENEVAL_ENTY_ID, 'filter': 
                                             {Renewal.assignedDeal:dealID}}, raw=True)['result']['items']
    return items
    







def get_deals():
    prepareDeal=[]
    deals = bit.call('crm.deal.list', items={'filter': 
                                             {'STAGE_SEMANTIC_ID':'S'}}, raw=True)['result']
    for deal in deals:
        
        product=bit.call('crm.deal.productrows.get', items={'id': int(deal['ID'])}, raw=True)['result']
        
        a={'deal':deal,
            'product':product}
        
        prepareDeal.append(a)
    pprint(prepareDeal)
    return prepareDeal

def get_products(poductID):
    products=bit.call('crm.product.get', items={'ID':poductID}, raw=True)['result']

    pprint(products)

    return products

def get_users():
    prepareUser = []
    # users = bit.call('user.get', items={'filter' :{'ACTIVE':False}})
    users = bit.call('user.get', raw=True)['result']
    # for user in users:
        # prepareUser.append(f'[{user["ID"]}] {user["NAME"]} {user["LAST_NAME"]}')
    # pprint(users)
    # print(prepareUser)
    return users

def get_departments():
    departments = bit.call('department.get', raw=True)['result']
    pprint(departments)
    return departments

def get_task_work_time(id)->list:
    # task=bit.call('tasks.task.get', items={'taskId': id}, raw=True)['result']
    task=bit.call('task.elapseditem.getlist', items={'ID': id}, raw=True)['result']
    # pprint(task)
    return task

def get_item(entityID,itemID):
    item=bit.call('crm.item.get', items={'entityTypeId':entityID, 'id': itemID}, raw=True)['result']['item']
    return item

def get_product_rows(dealID):
    product=bit.call('crm.deal.productrows.get', items={'id': dealID}, raw=True)['result']
    return product


def find_invoice(entityID, number, date):
    """_summary_

    Args:
        entityID (_type_): _description_
        number (_type_):'0000-000014'
        date (_type_): '2024-05-07T03:00:00'

    Returns:
        _type_: _description_
    """

    item = bit.call('crm.item.list', items={'entityTypeId':entityID, 'filter': 
                            { 'accountNumber':number, 'begindate':date}}, raw=True)['result']['items']
    
    return item

# def get_invoice(invoiceID):
#     invoice=bit.call('crm.invoice.get', items={'id': invoiceID}, raw=True)['result']
#     return invoice

def create_item(duretion,taskID, comment, dateClose):
    bit.call('crm.item.add', items={
                            'entityTypeId':179, #биллинг
                            'fields': {'title': comment,
                                'ufCrm9_1713363122': duretion,
                                'ufCrm9_1713363093': dateClose.split('+')[0],}})

def add_new_post_timeline(itemID, entityID, entityType):
    bit.call('crm.timeline.comment.add', items={
                            'fields': {'ENTITY_ID': entityID,
                                'ENTITY_TYPE': entityType,
                                'COMMENT': """Создан новый пост
                                Test comment [URL=/crm/deal/details/26/]test123[/URL]""",}}) #для ссылки в нутри битрикса

def create_product(fields:dict):
    pprint(fields)
    bit.call('crm.product.add', items={'fields':fields},)

def create_renewal(fields:dict):
    renevalID=bit.call('crm.item.add', items={'entityTypeId':RENEVAL_ENTY_ID, 'fields':fields})
    return renevalID

def create_tovar_entity(fields:dict):
    tovarID=bit.call('crm.item.add', items={'entityTypeId':TOVAR_ENTY_ID, 'fields':fields})
    return tovarID 

def update_product(productID, fields:dict):
    bit.call('crm.product.update', items={'ID':productID, 'fields':fields})

def update_item(entityID, itemID, parentID):
    bit.call('crm.item.update', items={'entityTypeId':entityID, 'id':itemID, 'fields':{POLE_INVOICE:parentID}})

def update_deal(dealID, fields:dict):
    bit.call('crm.deal.update', items={'ID':dealID, 'fields':fields})

def len_count_tovar_deal(tovarDeal:list[dict])->int:
    count=0
    for tovar in tovarDeal:
        count += int(tovar['QUANTITY'])

def prepare_tovar_deal(tovarDeal:list[dict], isRenewal:bool=False)->dict:
    tovarItem={}
    for tovar in tovarDeal:
        if isRenewal:
            try:
                tovarItem[tovar['title']]+=1
            except KeyError:
                tovarItem[tovar['title']]=1
        else:
            try:
                tovarItem[tovar['PRODUCT_NAME']]+=tovar['QUANTITY']
            except KeyError:
                tovarItem[tovar['PRODUCT_NAME']]=tovar['QUANTITY']
        
            
                
        
    #InfoWorks ICM - Ultimate 2025 Not For Resale New : 3
    return tovarItem



def check_more_tovar(tovarDeal:list[dict], tovarItem:list[dict])->list[dict]|None:
    newTovar=[]

    if len(tovarDeal)==len(tovarItem): return None
    else: newTovarCount=len(tovarDeal)-len(tovarItem)
    for i in range(newTovarCount):
        newTovar.append(tovarDeal[i])
    return newTovar

    
def compare_dictionaries(dict1, dict2):
    missing_products = {}

    for product, quantity in dict1.items():
        if product not in dict2:
            missing_products[product] = quantity
        elif dict2[product] < quantity:
            missing_products[product] = quantity - dict2[product]

    return missing_products   
    
            
    
    


# 17440
# if __name__ == '__main__':
def main(dealID:str=None):
    #Renewal == Товары

    productsDeal=get_product_rows(dealID)
    pprint(productsDeal)
    productsItem=find_all_tovar_items(dealID)
    pprint(productsItem)
    prepareTovarDeal=prepare_tovar_deal(productsDeal)
    pprint(prepareTovarDeal)
    prepareTovarRenewal=prepare_tovar_deal(productsItem, True)
    pprint(prepareTovarRenewal)

    missingRenewal=compare_dictionaries(prepareTovarDeal, prepareTovarRenewal)
    
    pprint(missingRenewal)
    newRenewasl=[]
    for product, quantity in missingRenewal.items():
        fieldsItemReneweal={
            Renewal.assignedDeal:dealID,
            Renewal.title:product,
            Renewal.serialNumber:quantity,
            Renewal.productName:product
        }
        fieldsItemTovar={
            Product_ENTY.assignedDeal:dealID,
            Product_ENTY.title:product,
            Product_ENTY.priceZakyp:quantity,
            Product_ENTY.discount1:0,
            Product_ENTY.discount2:0
        }
        for _ in range(quantity):
            renewalID=create_renewal(fieldsItemReneweal)['id']
            create_tovar_entity(fieldsItemTovar)
            print(f'{renewalID=}')
            newRenewasl.append(renewalID)

            # fields
            # update_deal()
            # print('create_renewal', fieldsItemReneweal)
        
            # create_renewal(fieldsItemReneweal)
    renDeal=find_deal(dealID)[Deal.renewals]
    1+0
    if renDeal==['None']: renDeal=[]
    newRenewasl.extend(renDeal)
    print(f'{newRenewasl=}')
    fieldsDeal={
        Deal.renewals:newRenewasl
    }
    update_deal(dealID, fieldsDeal)
    # newTovar=check_more_tovar(productsDeal, productsItem)
    # pprint(newTovar)
    
    # for tovar in newTovar:
    #     fieldsItemReneweal={
    #         Renewal.assignedDeal:dealID,
    #         Renewal.title:tovar['PRODUCT_NAME'],
    #         Renewal.serialNumber:tovar['PRODUCT_ID']
    #     }
    #     create_renewal(fieldsItemReneweal)    
    


# item=get_item(TOVAR_ENTY_ID,4)
# pprint(item)

    
# dealID='17442'
# a=find_deal(dealID=dealID)
# pprint(a)

# main(dealID=dealID)


