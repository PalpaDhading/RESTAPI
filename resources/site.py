from flask_restful import Resource, reqparse
from models.site import SiteModel

class Site(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('street',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )
    parser.add_argument('city',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )
    parser.add_argument('state',
            type =str,
            required = True,
            help ="This field can't be left blank "
        )
    def get(self, sitename):
        site = SiteModel.find_by_name(sitename)
        if site:
            return site.json()
        return {'message': "Site {} not found".format(sitename)}, 404

    def post(self, sitename):
        data = Site.parser.parse_args()
        if SiteModel.find_by_name(sitename):
            return {'message': "A cell site with name '{}' already exists.".format(sitename)}, 400

        site = SiteModel(sitename,data['street'],data['city'],data['state'])

        try:
            site.save_to_db()
        except:
            return {"message": "An error occurred creating the {} site.".format(sitename)}, 500

        return site.json(), 201

    def put(self, sitename):
        data = Site.parser.parse_args()

        site = SiteModel.find_by_name(sitename)

        if site:
            site.street = data['street']
            site.city = data['city']
            site.state = data['state']

        else:
            site = SiteModel(sitename,data['street'],data['city'],data['state'])

        site.save_to_db()

        return site.json()

    def delete(self, sitename):
        site = SiteModel.find_by_name(sitename)
        if site:
            site.delete_from_db()

        return {'message': "Site {} deleted".format(sitename)}

class SiteList(Resource):
    def get(self):
        return {'SiteList': list(map(lambda x: x.json(), SiteModel.query.all()))}
