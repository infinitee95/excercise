import requests
from dummy_output import dummy_data
import json
url ='http://127.0.0.1:5000/get_linkedin_data?email=example@mail.com'

def call_api(url, method="GET", params=None, data=None, headers=None):
  """
  This function makes an API call to the specified URL.

  Args:
      url (str): The URL of the API endpoint.
      method (str, optional): The HTTP method (GET, POST, PUT, etc.). Defaults to "GET".
      params (dict, optional): Dictionary of query parameters for GET requests. Defaults to None.
      data (dict, optional): Dictionary of data for POST or PUT requests. Defaults to None.
      headers (dict, optional): Dictionary of headers for the request. Defaults to None.

  Returns:
      requests.Response: The response object from the API call.
  """

  try:
    response = requests.request(method, url, params=params, data=data, headers=headers)
    response.raise_for_status()  # Raise an exception for non-2xx status codes
    return response.json()
  except requests.exceptions.RequestException as e:
    print(f"Error calling API: {e}")
    return None

result = call_api(url)
# print (result)
def extract_time(date):
    if date:
        date_parts = []
        for key in ["day", "month", "year"]:
            if date.get(key) is not None:
                date_parts.append(str(date[key]))
        return "-".join(date_parts)
    else: return "NULL"
def transform_response(response):
    person = response.get('person', None)
    if person:
        individual_data = {
        "first_name": person.get("firstName","NA"),
        "last_name": person.get("lastName","NA",),
        "public_identifier": person.get("publicIdentifier","NA"),
        "headline": person.get("headline","NA"),
        "location": person.get("location","NA"),
        "photo_url": person.get("photoUrl","NA"),
        "creation_date": person.get("creationDate"),
        "follower_count": person.get("followerCount","NA"),
        "connection_count": person.get("connectionCount","NA"),
        "languages": person.get("languages",[]),
        "work_experience": person.get("positions", {}),
        "education": person.get("schools", {}),
        "skills": person.get("skills",[]),
        "company": person.get("company",{}),
        }
        # transform creation_date:
        individual_data["creation_date"] = extract_time(individual_data.get("creation_date"))
        # Transform work experience
        work_experience=individual_data.get("work_experience").get('positionHistory')
        if work_experience:
            exp = []
            for position in work_experience:
                date = position.get("startEndDate")

                if date:
                    start_date = extract_time(date.get("start"))
                    end_date = extract_time(date.get("end"))
                else: 
                    start_date ="NULL"
                    end_date="NULL"
                experience = {
                "title": position.get("title", "NA"),
                "description": position.get("description", "NA"),
                "company_name": position.get("companyName", "NA"),
                "company_location": position.get("companyLocation", "NA"),
                "company_logo_url": position.get("companyLogo", "NA"),  # Use get() for optional field
                "start_date": start_date,
                "end_date": end_date,
                }
                exp.append(experience)
            individual_data["work_experience"] = exp
        
        # Transform education
        educations=individual_data.get("education").get('educationHistory')
        if educations:
            schools = []
            for edu in educations:
                date = edu.get("startEndDate")
                if date:
                    start_date = extract_time(date.get("start"))
                    end_date = extract_time(date.get("end"))
                else: 
                    start_date ="NULL"
                    end_date="NULL"
                education_entry = {
                    "school_name": edu.get("schoolName", "NA"),
                    "description": edu.get("description", "NA"),
                    "degree_name": edu.get("degreeName", "NA"),
                    "field_of_study": edu.get("fieldOfStudy", "NA"),
                    "start_date": start_date,
                    "end_date": end_date,
                    "school_logo_url": edu.get("schoolLogo","NA"),
                }
                schools.append(education_entry)
            individual_data["education"] = education_entry
        # Extract company data
        company=individual_data.get("company")
        if company:
            headquarter = company.get("headquarter",{})
            geographic_area = company.get("headquarter")
            if geographic_area:
                geographic_area = geographic_area.get('geographicArea', "NA")
            else: geographic_area ="NA"
            
            geographic_area = company.get("headquarter")
            if geographic_area:
                geographic_area = geographic_area.get('geographicArea', "NA")
            else: geographic_area ="NA"
            
            company_data = {
            "name": company.get("name", "NA"),
            "website_url": company.get("websiteUrl", "NA"),
            "logo_url": company.get("logo", "NA"),
            "employee_count": company.get("employeeCount", "NA"),
            "description": company.get("description", "NA"),
            "tagline": company.get("tagline", "NA"),
            "specialties": company.get("specialities", "NA"),
            "headquarters": {
                "country": headquarter.get("country", "NA"),
                "geographic_area": headquarter.get("geographic_area", "NA"),
                "city": headquarter.get("city", "NA"),
                "postal_code": headquarter.get("postal_code", "NA"),
            },
            "industry": company.get("industry", "NA"),
            "universal_name": company.get("universalName", "NA"),
            "linkedin_url": company.get("linkedinUrl", "NA"),
            "linkedin_id": company.get("linkedinId", "NA"),
            }
            individual_data["company"] = company_data
        return individual_data
    else: return dummy_data

output=transform_response(result)
print(output)
with open('result.json', 'w') as fp:
    json.dump(output, fp)

