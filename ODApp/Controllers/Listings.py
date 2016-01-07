
import flask
from flask import request

import json
import decimal

from ODApp.Models.Listing import Listing

class Listings():

    @staticmethod
    def get_listings(od_app):
        listing_query = od_app.get_listings_session().query(Listing)

        # grab parameters
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        min_bed = request.args.get('min_bed')
        max_bed = request.args.get('max_bed')
        min_bath = request.args.get('min_bath')
        max_bath = request.args.get('max_bath')

        if (min_price):
            listing_query = listing_query.filter(Listing.price >= float(min_price))
        if (max_price):
            listing_query = listing_query.filter(Listing.price <= float(max_price))
        if (min_bed):
            listing_query = listing_query.filter(Listing.bedrooms >= float(min_bed))
        if (max_bed):
            listing_query = listing_query.filter(Listing.bedrooms <= float(max_bed))
        if (min_bath):
            listing_query = listing_query.filter(Listing.bathrooms >= float(min_bath))
        if (max_bath):
            listing_query = listing_query.filter(Listing.bathrooms <= float(max_bath))

        # determine count + offset
        page_num = request.args.get('page')
        if not page_num:
            page_num = 1
        page_num = int(page_num)

        count = request.args.get('count')
        if not count:
            count = 50
        count = int(count)

        total = listing_query.count()
        pre_idx = (page_num - 1) * count
        if pre_idx > total:
            post_idx = total - count

        post_idx = page_num * count
        if post_idx > total:
            post_idx = total

        # query data
        features = []
        for listing in listing_query[pre_idx:post_idx]:
            features.append(Listings.listing_feature_dict(listing))

        # serialize
        info_json = {
          "type": "FeatureCollection",
          "features" : features
        }

        data_resp = flask.Response(json.dumps(info_json, default=Listings.listing_json_decimal_default))

        # determine pagination header link
        base = request.base_url + '?'
        if (min_price):
            base += '&min_price=' + str(min_price)
        if (max_price):
            base += '&max_price=' + str(max_price)
        if (min_bed):
            base += '&min_bed=' + str(min_bed)
        if (max_bed):
            base += '&max_bed=' + str(max_bed)
        if (min_bath):
            base += '&min_bath=' + str(min_bath)
        if (max_bath):
            base += '&max_bath=' + str(max_bath)

        next_url = base + '&count=' + str(count) + '&page=' + str((page_num + 1))
        last_url = base + '&count=' + str(count) + '&page=' + str((int(total/count) + 1))
        data_resp.headers['Link'] = '<' + next_url + '>; rel=\"next\", <' + last_url + '>; rel=\"last\"'

        return data_resp

    @staticmethod
    def listing_feature_dict(listing):
        return {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [listing.lat,listing.lng]},
            "properties": {
                "id": listing.id, # CSV id
                "street": listing.street,
                "price": listing.price, # Price in Dollars
                "bedrooms": listing.bedrooms, # Bedrooms
                "bathrooms": listing.bathrooms, # Bathrooms
                "sq_ft": listing.sq_ft, # Square Footage
            }
        }

    @staticmethod
    def listing_json_decimal_default(obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError
