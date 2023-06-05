import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions





def get_request(url, **kwargs):
    print(kwargs)
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={
                                    'Content-Type': 'application/json'}, params=kwargs, auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'}, params=kwargs)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
    except Exception as e:
        print("Error ", e)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    print(json_payload)
    print("POST from {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        print(json_data)
        return json_data
    except:
        print("Network exception occurred")


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        # For each dealer object
        for dealer_doc in dealers:
            
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(
                    address=dealer_doc["address"],
                    city=dealer_doc["city"],
                    full_name=dealer_doc["full_name"],
                    id=dealer_doc["id"],
                    lat=dealer_doc["lat"],
                    long=dealer_doc["long"],
                    short_name=dealer_doc["short_name"],
                    st=dealer_doc["st"],
                    zip=dealer_doc["zip"]
                )
            results.append(dealer_obj)

    return results




def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealer_id=dealer_id)
    if json_result:
        for review in json_result:
            if review["dealership"] == dealer_id:
                if review["purchase"]:
                    review_obj = DealerReview(
                        dealership=review["dealership"],
                        name=review["name"],
                        purchase=review["purchase"],
                        review=review["review"],
                        purchase_date=review["purchase_date"],
                        car_make=review["car_make"],
                        car_model=review["car_model"],
                        car_year=review["car_year"],
                        sentiment=analyze_review_sentiments(review["review"]),
                        id=review['id']
                    )
                else:
                    review_obj = DealerReview(
                        dealership=review["dealership"],
                        name=review["name"],
                        purchase=review["purchase"],
                        review=review["review"],
                        purchase_date=None,
                        car_make=None,
                        car_model=None,
                        car_year=None,
                        sentiment=analyze_review_sentiments(review["review"]),
                        id=review['id']
                    )
                results.append(review_obj)
    return results



def analyze_review_sentiments(dealerreview, **kwargs):
    API_KEY="crhi2bSpCait493IYsJsbmO0LAfECyfD2FXe9tbhrNjx"
    NLU_URL='https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/c78eab26-8a5f-4416-a7bd-1ef61f9dc3dd'
    params = json.dumps({"text": dealerreview, "features": {"sentiment": {}}})
    response = requests.post(NLU_URL,data=params,headers={'Content-Type':'application/json'},auth=HTTPBasicAuth("apikey", API_KEY))
    
    #print(response.json())
    try:
        sentiment=response.json()['sentiment']['document']['label']
        return sentiment
    except:
        return "neutral"

# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



