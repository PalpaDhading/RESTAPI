from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('dateandtime',
        type=str,
        required=False,
        help="This field cannot be left blank!"
    )
    parser.add_argument('itemLocation',
        type =str,
        required = False,
        help ="This field can't be left blank "
        )
    parser.add_argument('itemCondition',
        type =str,
        required = False,
        help ="This field can't be left blank "
        )

    parser.add_argument('symptomDetails',
        type =str,
        required = False,
        help ="symptomType -This field can't be left blank "
        )
    parser.add_argument('resolutionDetails',
        type =str,
        required = False,
        help ="resolutionDetails -This field can't be left blank "
        )
    parser.add_argument('currentstatus',
        type =str,
        required = False,
        help ="currentstatus- This field can't be left blank "
        )
    parser.add_argument('DateofResolution',
        type =str,
        required = False,
        help ="Date of resolution - This field can't be left blank "
        )
    parser.add_argument('currentRSSI',
        type =float,
        required = False,
        help ="RSSI - This field needs decimal or integer value and can't be left blank "
        )
    parser.add_argument('currentVSWR',
        type =float,
        required = False,
        help ="VSWR - This field needs decimal or integer value and can't be left blank "
        )
    parser.add_argument('currentSQIDVoltage',
        type =float,
        required = False,
        help ="Voltage- This field needs decimal or integer value and can't be left blank "
        )
    parser.add_argument('otherOpportunityDetails',
        type =str,
        required = False,
        help ="Opportunity - This field can't be left blank "
        )
    parser.add_argument('sitename',
        type=str,
        required= True,
        help="Every item needs a sitename."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_itemname_sitename(name,data['sitename']):
            return {'message': "An item with name '{}' already exists on site.".format(name)}, 400

        #data = Item.parser.parse_args()

        item = ItemModel(data['dateandtime'],name,data['itemLocation'],data['itemCondition'],data['symptomDetails'],data['resolutionDetails'],data['currentstatus'],data['DateofResolution'],\
                data['currentRSSI'],data['currentVSWR'],data['currentSQIDVoltage'],data['otherOpportunityDetails'],data['sitename'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the {} item.".format(name)}, 500

        return item.json(), 201

    def delete(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_itemname_sitename(name,data['sitename'])
        if item :
            item.delete_from_db()

        return {'message': "Item on site {} is deleted".format(data['sitename'])}

    def put(self, name):
        data = Item.parser.parse_args()

        #item = ItemModel.find_by_name(name)
        item = ItemModel.find_by_itemname_sitename(name,data['sitename'])

        #if ItemModel.find_by_store_itemname_storename(name,data['store_name']):
        if item:
            item.itemLocation = data['itemLocation']
            item.itemCondition = data['itemCondition']
            item.symptomDetails = data['symptomDetails']
            item.resolutionDetails = data['resolutionDetails']
            item.currentstatus = data['currentstatus']
            item.DateofResolution = data['DateofResolution']
            item.currentRSSI = data['currentRSSI']
            item.currentVSWR = data['currentVSWR']
            item.currentSQIDVoltage = data['currentSQIDVoltage']
            item.otherOpportunityDetails = data['otherOpportunityDetails']

        else:
            item = ItemModel(data['dateandtime'],name,data['itemLocation'],data['itemCondition'],data['symptomDetails'],data['resolutionDetails'],data['currentstatus'],data['DateofResolution'],\
                    data['currentRSSI'],data['currentVSWR'],data['currentSQIDVoltage'],data['otherOpportunityDetails'],data['sitename'])

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    def get(self):
        return {'ItemList': list(map(lambda x: x.json(), ItemModel.query.all()))}
