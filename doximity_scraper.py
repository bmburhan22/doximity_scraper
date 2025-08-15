import requests
import csv
import json
import time
import os
from datetime import datetime

# Configuration - only the essentials
SPECIALTY_CODES = [
    # MD/DO Specialties
    "AM00",  # Allergy & Immunology
    "AN00",  # Anesthesiology
    "CA00",  # Cardiology
    "CN00",  # Child Neurology
    "CR00",  # Colon & Rectal Surgery
    "DE00",  # Dermatology
    "EM00",  # Emergency Medicine
    "EN00",  # Endocrinology
    "FM00",  # Family Medicine
    "GA00",  # Gastroenterology
    # "SG00",  # General Surgery
    # "GE00",  # Geriatrics
    # "HE00",  # Hematology
    # "FD00",  # Infectious Disease
    # "TM00",  # Internal Medicine
    # "IR00",  # Interventional Radiology
    # "MG00",  # Medical Genetics
    # "MP00",  # Medicine/Pediatrics
    # "NN00",  # Neonat/Perinatology
    # "NE00",  # Nephrology
    # "NG00",  # Neurology
    # "NS00",  # Neurosurgery
    # "NM00",  # Nuclear Medicine
    # "BG00",  # Obstetrics & Gynecology
    # "CM00",  # Occupational Medicine
    # "NC00",  # Oncology
    # "TH00",  # Ophthalmology
    # "OM00",  # Oral & Maxillofacial Surgery
    # "RT00",  # Orthopaedic Surgery
    # "MD00",  # Other MD/DO
    # "TY00",  # Otolaryngology (ENT)
    # "PH00",  # Pathology
    # "PGS00", # Pediatric (General) Surgery
    # "CP00",  # Pediatric Cardiology
    # "PEM00", # Pediatric Emergency Medicine
    # "EP00",  # Pediatric Endocrinology
    # "GP00",  # Pediatric Gastroenterology
    # "HN00",  # Pediatric Hematology & Oncology
    # "DP00",  # Pediatric Infectious Disease
    # "FP00",  # Pediatric Nephrology
    # "PP00",  # Pediatric Pulmonology
    # "RP00",  # Pediatric Rheumatology
    # "PE00",  # Pediatrics
    # "PM00",  # Physical Medicine/Rehab
    # "PS00",  # Plastic Surgery
    # "GM00",  # Preventive Medicine
    # "PY00",  # Psychiatry
    # "PU00",  # Pulmonology
    # "RC00",  # Radiation Oncology
    # "RA00",  # Radiology
    # "RE00",  # Research
    # "RS00",  # Resident Physician
    # "RH00",  # Rheumatology
    # "TS00",  # Thoracic Surgery
    # "UR00",  # Urology
    # "VS00",  # Vascular Surgery
    
    # # Nurse Practitioner Specialties
    # "AC00",  # Acute Care Nurse Practitioner
    # "AD00",  # Adult Care Nurse Practitioner
    # "AS00",  # Certified Nurse Midwife
    # "AF00",  # Family Nurse Practitioner
    # "AG00",  # Geriatric Nurse Practitioner
    # "AE00",  # Neonatal Nurse Practitioner
    # "NP00",  # Nurse Practitioner
    # "AH00",  # Occupational Health Nurse Practitioner
    # "AP00",  # Pediatric Nurse Practitioner
    # "AT00",  # Psychiatric-Mental Health Nurse Practitioner
    # "AW00",  # Women's Health Nurse Practitioner
    
    # # Physician Assistant Specialties
    # "WA00",  # Academic Medicine
    # "WB00",  # Allergy and Immunology
    # "WC00",  # Anesthesiology
    # "WD00",  # Cardiology
    # "WE00",  # Colon & Rectal Surgery
    # "WF00",  # Critical Care
    # "WG00",  # Dermatology
    # "WH00",  # Emergency Medicine
    # "WI00",  # Endocrinology
    # "WJ00",  # Family Medicine
    # "WK00",  # Gastroenterology
    # "WL00",  # General Hospitalist
    # "WM00",  # General Surgery
    # "WN00",  # Hematology
    # "WO00",  # Infectious Disease
    # "WP00",  # Internal Medicine
    # "WQ00",  # Interventional Radiology
    # "WR00",  # Medical Genetics
    # "WS00",  # Medicine/Pediatrics
    # "WT00",  # Neonat/Perinatology
    # "WU00",  # Nephrology
    # "WV00",  # Neurology
    # "WW00",  # Neurosurgery
    # "WX00",  # Nuclear Medicine
    # "WY00",  # Obstetrics & Gynecology
    # "WZ00",  # Occupational Medicine
    # "FA00",  # Oncology
    # "FB00",  # Ophthalmology
    # "FC00",  # Oral and Maxillofacial Surgery
    # "FE00",  # Orthopedics
    # "FF00",  # Otolaryngology (ENT)
    # "FG00",  # Pain Management
    # "FH00",  # Pathology
    # "FI00",  # Pediatrics
    # "FJ00",  # Physical Medicine/Rehab
    # "PA00",  # Physician Assistant
    # "FK00",  # Plastic Surgery
    # "FL00",  # Preventive Medicine
    # "FN00",  # Psychiatry
    # "FO00",  # Public Health
    # "FQ00",  # Pulmonology
    # "FR00",  # Radiology
    # "FS00",  # Rheumatology
    # "FT00",  # Thoracic Surgery
    # "FU00",  # Urology
    # "FV00",  # Vascular Surgery
    
    # # Pharmacist Specialties
    # "CX00",  # Clinical Pharmacist
    # "RX00",  # Pharmacist
    
    # # Other Healthcare Professionals
    # "CH00",  # Chiropractor
    # "DN00",  # Diet/Nutritionist
    # "HM00",  # Genetic Counselor
    # "TT00",  # Optometrist
    # "HP00",  # Other Healthcare Professional
    # "PT00",  # Physical Therapist
    # "PL00",  # Psychologist
    # "RN00",  # Registered Nurse
    # "SW00",  # Social Worker
    
    # # CRNA
    # "NA00",  # Certified Registered Nurse Anesthetist
    
    # # Student Categories
    # "MS00",  # Med Student
    # "NPS00", # NP Student
    # "PAS00", # PA Student
    # "OHS00", # Other Healthcare Student
    # "RXS00", # Pharmacy Student
    # "RNAX00" # CRNA Student
]
BEARER_TOKEN = ""  # Replace with your actual token

class DoximityScraper:
    def __init__(self):
        self.bearer_token = BEARER_TOKEN
        self.base_url = "https://graphql.doximity.com/graphql"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.bearer_token}"
        }
        
        # Create output directory
        os.makedirs("output", exist_ok=True)
    

    
    def get_users_page(self, specialty_code: str, after: str = None):
        """Get a single page of users"""
        
        variables = {
            "specialtyCodeListFilter": [specialty_code],
            "first": 100
        }
        
        if after:
            variables["after"] = after
        
        query = """
        query userSearchQuery($specialtyCodeListFilter: [String!], $first: Int, $after: String) {
            search {
                users(filters: {specialtyCodeListFilter: $specialtyCodeListFilter}, first: $first, after: $after) {
                    totalCount
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    edges {
                        cursor
                        node {
                            id
                            fullName
                            specialtyName
                            cityName
                            stateAbbreviation
                            description
                            profilePhotoUrl
                            trackingId
                            uuid
                            coordinates {
                                latitude
                                longitude
                            }
                            networkContexts {
                                fullDescription
                            }
                        }
                    }
                }
            }
        }
        """
        
        payload = {
            "operationName": "userSearchQuery",
            "variables": variables,
            "query": query
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                print(f"❌ HTTP Error {response.status_code} for specialty {specialty_code}")
                print(f"📝 Response headers: {dict(response.headers)}")
                print(f"📝 Response text: {response.text}")
                return None
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Request Error for specialty {specialty_code}: {e}")
            return None

    def get_profile_sections(self, profile_uuid: str, first: int = 7, section_limit: int = 5, section_cursor: str = None):
        """Get profile sections including education, training, certifications, licenses"""
        
        variables = {
            "profileUUID": profile_uuid,
            "first": first,
            "sectionLimit": section_limit
        }
        
        if section_cursor:
            variables["sectionCursor"] = section_cursor
        
        query = """
        query sduiProfileSections($profileUUID: ID!, $first: Int, $cursor: String, $profileSectionName: [ProfileSectionName!], $sectionLimit: Int, $sectionCursor: String) {
          profile(uuid: $profileUUID) {
            id
            sduiSectionsConnection(first: $sectionLimit, after: $sectionCursor, profileSectionName: $profileSectionName) {
              pageInfo {
                endCursor
                hasNextPage
                __typename
              }
              edges {
                node {
                  section
                  sectionLayoutType
                  title
                  titleSubtext
                  hasItems
                  layout {
                    __typename
                    ...SingleColumnListFragment
                    ...NestedSingleColumnListFragment
                  }
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
        }

        fragment SingleColumnListFragment on Sdui_SingleColumnListLayout {
          id
          actionButtonText
          hasShowMoreAction
          hasViewDetailsAction
          viewDetailsUrl
          _links {
            section {
              href
              __typename
            }
            create {
              href
              __typename
            }
            __typename
          }
          items(first: $first, after: $cursor) {
            totalCount
            pageInfo {
              hasNextPage
              endCursor
              __typename
            }
            edges {
              node {
                id
                primaryText
                secondaryText
                tertiaryText
                quaternaryText
                hasInlineEditButton
                hasMoveToTopAction
                url
                _links {
                  self {
                    href
                    __typename
                  }
                  __typename
                }
                hasLogo
                logoUrl
                logo {
                  id
                  title
                  fullpath
                  __typename
                }
                tags {
                  text
                  backgroundColor
                  __typename
                }
                primaryCallout {
                  count
                  recentCount
                  text
                  extraProps
                  __typename
                }
                secondaryCallout {
                  count
                  recentCount
                  text
                  extraProps
                  __typename
                }
                itemAction {
                  action
                  target
                  __typename
                }
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }

        fragment NestedSingleColumnListFragment on Sdui_NestedSingleColumnListLayout {
          id
          actionButtonText
          _links {
            section {
              href
              __typename
            }
            create {
              href
              __typename
            }
            __typename
          }
          nestedSections {
            section
            sectionLayoutType
            title
            titleSubtext
            hasItems
            layout {
              __typename
              ...SingleColumnListFragment
            }
            __typename
          }
          __typename
        }
        """
        
        payload = {
            "operationName": "sduiProfileSections",
            "variables": variables,
            "query": query
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                print(f"❌ Profile sections error for {profile_uuid}: HTTP {response.status_code}")
                print(f"📝 Response headers: {dict(response.headers)}")
                print(f"📝 Response text: {response.text}")
                return None
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Profile sections request error for {profile_uuid}: {e}")
            return None

    def get_profile_private_lines(self, profile_uuid: str):
        """Get private contact information including phone numbers"""
        
        variables = {
            "uuid": profile_uuid
        }
        
        query = """
        query ProfilePrivateLinesQuery($uuid: ID) {
          profile(uuid: $uuid) {
            id
            ...ProfilePrivateLinesQueryFragment
            __typename
          }
        }

        fragment ProfilePrivateLinesQueryFragment on Profile {
          back_office
          mobile_phone
          home_phone
          other_phone
          pager
          admit_number
          other_email
          note
          private_lines_visible
          __typename
        }
        """
        
        payload = {
            "operationName": "ProfilePrivateLinesQuery",
            "variables": variables,
            "query": query
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                print(f"❌ Private lines error for {profile_uuid}: HTTP {response.status_code}")
                print(f"📝 Response headers: {dict(response.headers)}")
                print(f"📝 Response text: {response.text}")
                return None
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Private lines request error for {profile_uuid}: {e}")
            return None

    def get_profile_locations(self, profile_uuid: str):
        """Get location information including addresses and phone numbers"""
        
        variables = {
            "uuid": profile_uuid
        }
        
        query = """
        query ProfileLocationsQuery($uuid: ID) {
          profile(uuid: $uuid) {
            id
            ...ProfileLocationsQueryFragment
            __typename
          }
        }

        fragment ProfileLocationsQueryFragment on Profile {
          full_name
          formatted_doxfax_number: doxfax_number(formatted: true)
          locations {
            edges {
              node {
                ...ProfileLocationFieldsFragment
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }

        fragment ProfileLocationFieldsFragment on Location {
          id
          uuid
          name
          address_1
          address_2
          coordinates {
            latitude
            longitude
            __typename
          }
          zip_code
          phone_number
          formatted_phone_number: phone_number(formatted: true)
          phone_number_extension
          fax_number
          formatted_fax_number: fax_number(formatted: true)
          primary
          city {
            id
            uuid
            name
            description
            country {
              id
              abbreviation
              name
              __typename
            }
            __typename
          }
          _links {
            update {
              href
              __typename
            }
            __typename
          }
          __typename
        }
        """
        
        payload = {
            "operationName": "ProfileLocationsQuery",
            "variables": variables,
            "query": query
        }
        
        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                print(f"❌ Locations error for {profile_uuid}: HTTP {response.status_code}")
                print(f"📝 Response headers: {dict(response.headers)}")
                print(f"📝 Response text: {response.text}")
                return None
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Locations request error for {profile_uuid}: {e}")
            return None

    def get_detailed_profile(self, profile_uuid: str):
        """Get comprehensive profile information including all requested data"""
        
        print(f"🔍 Getting detailed profile for: {profile_uuid}")
        
        # Get all three types of data
        sections_data = self.get_profile_sections(profile_uuid)
        private_lines_data = self.get_profile_private_lines(profile_uuid)
        locations_data = self.get_profile_locations(profile_uuid)
        
        # Combine all data
        detailed_profile = {
            "uuid": profile_uuid,
            "sections": {},
            "contact_info": {},
            "locations": []
        }
        
        # Process sections data (education, training, certifications, licenses)
        if sections_data and "data" in sections_data and sections_data["data"]:
            try:
                profile_data = sections_data["data"].get("profile", {})
                if profile_data and "sduiSectionsConnection" in profile_data:
                    sections = profile_data["sduiSectionsConnection"].get("edges", [])
                    for section_edge in sections:
                        section_node = section_edge.get("node", {})
                        section_name = section_node.get("section", "unknown")
                        section_title = section_node.get("title", "")
                        
                        # Extract items from the section
                        items = []
                        if "layout" in section_node and section_node["layout"]:
                            layout = section_node["layout"]
                            if "items" in layout and "edges" in layout["items"]:
                                for item_edge in layout["items"]["edges"]:
                                    item = item_edge.get("node", {})
                                    items.append({
                                        "primary_text": item.get("primaryText", ""),
                                        "secondary_text": item.get("secondaryText", ""),
                                        "tertiary_text": item.get("tertiaryText", ""),
                                        "quaternary_text": item.get("quaternaryText", ""),
                                        "tags": [tag.get("text", "") for tag in item.get("tags", [])]
                                    })
                        
                        detailed_profile["sections"][section_name] = {
                            "title": section_title,
                            "items": items
                        }
            except Exception as e:
                print(f"⚠️  Error processing sections data for {profile_uuid}: {e}")
                detailed_profile["sections"] = {}
        
        # Process private lines data (phone numbers, emails)
        if private_lines_data and "data" in private_lines_data and private_lines_data["data"]:
            try:
                profile_data = private_lines_data["data"].get("profile", {})
                if profile_data:
                    detailed_profile["contact_info"] = {
                        "back_office": profile_data.get("back_office", ""),
                        "mobile_phone": profile_data.get("mobile_phone", ""),
                        "home_phone": profile_data.get("home_phone", ""),
                        "other_phone": profile_data.get("other_phone", ""),
                        "pager": profile_data.get("pager", ""),
                        "other_email": profile_data.get("other_email", ""),
                        "note": profile_data.get("note", ""),
                        "private_lines_visible": profile_data.get("private_lines_visible", False)
                    }
            except Exception as e:
                print(f"⚠️  Error processing private lines data for {profile_uuid}: {e}")
                detailed_profile["contact_info"] = {}
        
        # Process locations data (addresses, phone numbers)
        if locations_data and "data" in locations_data and locations_data["data"]:
            try:
                profile_data = locations_data["data"].get("profile", {})
                if profile_data:
                    detailed_profile["full_name"] = profile_data.get("full_name", "")
                    detailed_profile["doxfax_number"] = profile_data.get("formatted_doxfax_number", "")
                    
                    locations = profile_data.get("locations", {}).get("edges", [])
                    for location_edge in locations:
                        location = location_edge.get("node", {})
                        city = location.get("city", {})
                        country = city.get("country", {})
                        
                        location_info = {
                            "name": location.get("name", ""),
                            "address_1": location.get("address_1", ""),
                            "address_2": location.get("address_2", ""),
                            "city": city.get("name", ""),
                            "state": city.get("description", ""),
                            "country": country.get("name", ""),
                            "zip_code": location.get("zip_code", ""),
                            "phone_number": location.get("formatted_phone_number", ""),
                            "phone_extension": location.get("phone_number_extension", ""),
                            "fax_number": location.get("formatted_fax_number", ""),
                            "primary": location.get("primary", False),
                            "coordinates": {
                                "latitude": location.get("coordinates", {}).get("latitude"),
                                "longitude": location.get("coordinates", {}).get("longitude")
                            }
                        }
                        detailed_profile["locations"].append(location_info)
            except Exception as e:
                print(f"⚠️  Error processing locations data for {profile_uuid}: {e}")
                detailed_profile["locations"] = []
        
        return detailed_profile

    def extract_structured_data(self, detailed_profile, search_full_name=""):
        """Extract structured data from detailed profile for easier analysis"""
        
        if not detailed_profile:
            print(f"⚠️  Warning: detailed_profile is None or empty")
            return {
                "uuid": "",
                "full_name": search_full_name,
                "addresses": [],
                "phone_numbers": [],
                "education": [],
                "training": [],
                "certifications": [],
                "licenses": [],
                "work_experience": [],
                "skills": [],
                "contact_info": []
            }
        
        structured_data = {
            "uuid": detailed_profile.get("uuid", ""),
            "full_name": search_full_name or detailed_profile.get("full_name", ""),
            "addresses": [],
            "phone_numbers": [],
            "education": [],
            "training": [],
            "work_experience": [],
            "certifications": [],
            "licenses": [],
            "skills": [],
            "contact_info": []
        }
        
        try:
            # Extract addresses from locations
            for location in detailed_profile.get("locations", []):
                if location and location.get("address_1"):
                    address = {
                        "type": "practice" if location.get("name") else "personal",
                        "name": location.get("name", ""),
                        "address_1": location.get("address_1", ""),
                        "address_2": location.get("address_2", ""),
                        "city": location.get("city", ""),
                        "state": location.get("state", ""),
                        "country": location.get("country", ""),
                        "zip_code": location.get("zip_code", ""),
                        "primary": location.get("primary", False)
                    }
                    structured_data["addresses"].append(address)
        except Exception as e:
            print(f"⚠️  Error extracting addresses: {e}")
            structured_data["addresses"] = []
        
        try:
            # Extract phone numbers from contact info and locations
            contact_info = detailed_profile.get("contact_info", {})
            
            # Add private phone numbers
            for phone_type, number in contact_info.items():
                if phone_type.endswith("_phone") and number:
                    structured_data["phone_numbers"].append({
                        "type": phone_type.replace("_phone", ""),
                        "number": number,
                        "source": "private_lines"
                    })
            
            # Add location phone numbers
            for location in detailed_profile.get("locations", []):
                if location and location.get("phone_number"):
                    structured_data["phone_numbers"].append({
                        "type": "practice",
                        "number": location.get("phone_number", ""),
                        "extension": location.get("phone_extension", ""),
                        "source": "location"
                    })
        except Exception as e:
            print(f"⚠️  Error extracting phone numbers: {e}")
            structured_data["phone_numbers"] = []
        
        try:
                         # Extract education, training, certifications, licenses from sections
             sections = detailed_profile.get("sections", {})
             
             # Map section names to our categories based on actual API response
             section_mapping = {
                 "TRAINING": "training",
                 "EMPLOYMENTS": "work_experience", 
                 "EDUCATION": "education",
                 "CERTIFICATIONS": "certifications",
                 "LICENSES": "licenses",
                 "SKILLS": "skills",
                 "CONTACT_INFO": "contact_info"
             }
             
             for section_name, section_data in sections.items():
                 if section_name in section_mapping and section_data:
                     category = section_mapping[section_name]
                     for item in section_data.get("items", []):
                         if item:
                             # Create structured item
                             structured_item = {
                                 "primary_text": item.get("primary_text", ""),
                                 "secondary_text": item.get("secondary_text", ""),
                                 "tertiary_text": item.get("tertiary_text", ""),
                                 "quaternary_text": item.get("quaternary_text", ""),
                                 "tags": item.get("tags", [])
                             }
                             structured_data[category].append(structured_item)
                             
                             # Create human-readable text version
                             readable_text = self.create_readable_text(structured_item, category)
                             if readable_text:
                                 # Add to a new field for readable text
                                 readable_field = f"{category}_readable"
                                 if readable_field not in structured_data:
                                     structured_data[readable_field] = []
                                 structured_data[readable_field].append(readable_text)
        except Exception as e:
            print(f"⚠️  Error extracting sections data: {e}")
            # Keep the empty lists as they were initialized
        
        return structured_data
    
    def create_readable_text(self, item, category):
         """Convert structured item to human-readable text"""
         try:
             parts = []
             
             # Add primary text (usually institution/company name)
             if item.get("primary_text"):
                 parts.append(item["primary_text"])
             
             # Add secondary text (usually degree/position details)
             if item.get("secondary_text"):
                 parts.append(item["secondary_text"])
             
             # Add tertiary text (usually dates or additional details)
             if item.get("tertiary_text"):
                 parts.append(item["tertiary_text"])
             
             # Add quaternary text (usually extra information)
             if item.get("quaternary_text"):
                 parts.append(item["quaternary_text"])
             
             # Add tags if any
             if item.get("tags"):
                 tags_text = ", ".join([tag for tag in item["tags"] if tag])
                 if tags_text:
                     parts.append(f"Tags: {tags_text}")
             
             # Join all parts with appropriate separators
             if category in ["education", "training"]:
                 # For education/training, use line breaks for better readability
                 return " | ".join(parts)
             elif category == "work_experience":
                 # For work experience, use line breaks
                 return " | ".join(parts)
             else:
                 # For other categories, use simple separator
                 return " | ".join(parts)
                 
         except Exception as e:
             print(f"⚠️  Error creating readable text: {e}")
             return ""
     
     # Detailed profile method - commented out for now, can be enabled later
    # def get_profile_details(self, profile_id: str):
    #     """Get detailed profile information for a specific user"""
    #     
    #     query = """
    #     query getProfileDetails($id: ID!) {
    #         profile(id: $id) {
    #             id
    #             fullName
    #             specialtyName
    #             cityName
    #             stateAbbreviation
    #             description
    #             profilePhotoUrl
    #             education {
    #                 institution
    #                 degree
    #                 fieldOfStudy
    #                 startDate
    #                 endDate
    #                 type
    #             }
    #             training {
    #                 institution
    #                 specialty
    #                 startDate
    #                 endDate
    #                 type
    #             }
    #             certifications {
    #                 name
    #                 issuingOrganization
    #                 issueDate
    #                 expirationDate
    #                 credentialId
    #             }
    #             licenses {
    #                 state
    #                 licenseNumber
    #                 issueDate
    #                 expirationDate
    #                 status
    #             }
    #             coordinates {
    #                 latitude
    #                 longitude
    #             }
    #             networkContexts {
    #                 fullDescription
    #             }
    #         }
    #     }
    #     """
    #     
    #     variables = {"id": profile_id}
    #     
    #     payload = {
    #             "operationName": "getProfileDetails",
    #             "variables": variables,
    #             "query": query
    #         }
    #     
    #     try:
    #             response = requests.post(self.base_url, headers=self.headers, json=payload)
    #             
    #             if response.status_code != 200:
    #                 print(f"❌ Profile details error for {profile_id}: {response.status_code}")
    #                 return None
    #             
    #             return response.json()
    #             
    #     except Exception as e:
    #                 print(f"❌ Profile details request error for {profile_id}: {e}")
    #                 return None
    
    def scrape_all_users(self, specialty_code: str):
        """Scrape all users for a specialty code"""
        
        print(f"Starting to scrape users for specialty: {specialty_code}")
        
        all_users = []
        page_count = 0
        has_next_page = True
        after_cursor = None
        
        while page_count < 100:  # Safety limit
            page_count += 1
            print(f"Fetching page {page_count}...")
            
            result = self.get_users_page(specialty_code, after=after_cursor)
            
            if not result or "errors" in result:
                if result and "errors" in result:
                    print(f"❌ GraphQL Error: {json.dumps(result['errors'], indent=2)}")
                else:
                    print(f"❌ No response received")
                break
            
            # Extract data
            users_data = result.get("data", {}).get("search", {}).get("users", {})
            page_info = users_data.get("pageInfo", {})
            has_next_page = page_info.get("hasNextPage", False)
            after_cursor = page_info.get("endCursor")
            
            # Debug pagination info
            print(f"   hasNextPage: {has_next_page}")
            print(f"   after_cursor: {after_cursor}")
            print(f"   totalCount: {users_data.get('totalCount', 0)}")
            
            # Get users from edges
            edges = users_data.get("edges", [])
            for edge in edges:
                user = edge.get("node", {})
                user["specialty_code"] = specialty_code
                
                all_users.append(user)
            
            total_count = users_data.get("totalCount", 0)
            print(f"Page {page_count}: Got {len(edges)} users. Total: {len(all_users)}/{total_count}")
            
            # Stop if no more pages or no cursor for next page
            if not has_next_page or not after_cursor:
                print(f"   No more pages available")
                break
            
            # Rate limiting
            time.sleep(1)
        
        print(f"Scraping complete for {specialty_code}! Total users: {len(all_users)}")
        return all_users
    
    def scrape_detailed_profiles(self, specialty_code: str, max_profiles: int = 10):
        """Scrape detailed profiles for a limited number of users in a specialty"""
        
        print(f"🔍 Starting detailed profile scraping for specialty: {specialty_code}")
        print(f"📊 Will collect up to {max_profiles} detailed profiles")
        
        # First get basic user list
        basic_users = self.scrape_all_users(specialty_code)
        
        if not basic_users:
            print(f"❌ No basic users found for {specialty_code}")
            return [], []
        
        # Limit to max_profiles
        users_to_process = basic_users[:max_profiles]
        detailed_profiles = []
        structured_data_list = []
        failed_profiles = 0
        
        print(f"📋 Processing {len(users_to_process)} profiles for detailed data...")
        
        for i, user in enumerate(users_to_process, 1):
            try:
                uuid = user.get("uuid")
                if not uuid:
                    print(f"⚠️  User {i} has no UUID, skipping")
                    failed_profiles += 1
                    continue
                
                print(f"🔍 Processing profile {i}/{len(users_to_process)}: {user.get('fullName', 'Unknown')}")
                
                # Get detailed profile
                detailed_profile = self.get_detailed_profile(uuid)
                
                if detailed_profile:
                    # Add basic user info to detailed profile
                    detailed_profile.update({
                        "basic_info": {
                            "fullName": user.get("fullName", ""),
                            "specialtyName": user.get("specialtyName", ""),
                            "cityName": user.get("cityName", ""),
                            "stateAbbreviation": user.get("stateAbbreviation", ""),
                            "description": user.get("description", ""),
                            "profilePhotoUrl": user.get("profilePhotoUrl", ""),
                            "trackingId": user.get("trackingId", "")
                        }
                    })
                    
                    detailed_profiles.append(detailed_profile)
                    
                    # Extract structured data
                    try:
                        structured_data = self.extract_structured_data(detailed_profile, user.get("fullName", ""))
                        structured_data_list.append(structured_data)
                        print(f"✅ Profile {i} processed successfully")
                    except Exception as e:
                        print(f"⚠️  Error extracting structured data for profile {i}: {e}")
                        # Add empty structured data to maintain consistency
                        empty_data = {
                            "uuid": uuid,
                            "full_name": user.get("fullName", ""),
                            "addresses": [],
                            "phone_numbers": [],
                            "education": [],
                            "training": [],
                            "work_experience": [],
                            "certifications": [],
                            "licenses": [],
                            "skills": [],
                            "contact_info": []
                        }
                        structured_data_list.append(empty_data)
                        print(f"✅ Profile {i} processed with empty structured data")
                else:
                    print(f"⚠️  Could not get detailed profile for user {i}")
                    failed_profiles += 1
                    
                    # Add empty structured data to maintain consistency
                    empty_data = {
                        "uuid": uuid,
                        "full_name": user.get("fullName", ""),
                        "addresses": [],
                        "phone_numbers": [],
                        "education": [],
                        "training": [],
                        "work_experience": [],
                        "certifications": [],
                        "licenses": [],
                        "skills": [],
                        "contact_info": []
                    }
                    structured_data_list.append(empty_data)
                
                # Rate limiting for detailed profiles
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error processing detailed profile {i}: {e}")
                failed_profiles += 1
                
                # Add empty structured data to maintain consistency
                try:
                    uuid = user.get("uuid", "")
                    empty_data = {
                        "uuid": uuid,
                        "full_name": user.get("fullName", ""),
                        "addresses": [],
                        "phone_numbers": [],
                        "education": [],
                        "training": [],
                        "work_experience": [],
                        "certifications": [],
                        "licenses": [],
                        "skills": [],
                        "contact_info": []
                    }
                    structured_data_list.append(empty_data)
                except:
                    pass
                
                continue
        
        # Save detailed profiles as JSON for each specialty
        if detailed_profiles:
            try:
                json_filename = f"output/{specialty_code}_detailed_profiles.json"
                self.save_detailed_profile_to_json(detailed_profiles, json_filename)
                print(f"📁 Detailed profiles saved to: {json_filename}")
            except Exception as e:
                print(f"❌ Error saving JSON file for {specialty_code}: {e}")
        
        print(f"🎉 Detailed profile scraping complete for {specialty_code}")
        print(f"📊 Total detailed profiles: {len(detailed_profiles)}")
        print(f"📊 Failed profiles: {failed_profiles}")
        
        return detailed_profiles, structured_data_list
    
    def save_to_csv(self, users, filename):
        """Save users to CSV"""
        if not users:
            print("No users to save")
            return
        
        # Get all field names
        fieldnames = set()
        for user in users:
            fieldnames.update(user.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for user in users:
                # Handle nested objects
                row = {}
                for field in fieldnames:
                    value = user.get(field)
                    if isinstance(value, (dict, list)):
                        row[field] = json.dumps(value)
                    else:
                        row[field] = value
                writer.writerow(row)
        
        print(f"CSV saved to {filename}")

    def save_detailed_profile_to_json(self, detailed_profile, filename):
        """Save detailed profile data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(detailed_profile, jsonfile, indent=2, ensure_ascii=False)
            print(f"✅ Detailed profile saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving detailed profile to {filename}: {e}")

    def save_structured_data_to_csv(self, structured_data_list, filename):
        """Save structured data to CSV for easier analysis"""
        if not structured_data_list:
            print("No structured data to save")
            return
        
        # Define CSV fields for structured data
        fieldnames = [
            "uuid", "full_name",
            "addresses_count", "phone_numbers_count", 
            "education_count", "training_count", "work_experience_count", "certifications_count", "licenses_count", "skills_count", "contact_info_count",
            "addresses_json", "phone_numbers_json", "education_json", "training_json", 
            "work_experience_json", "certifications_json", "licenses_json", "skills_json", "contact_info_json",
            "education_readable", "training_readable", "work_experience_readable", "certifications_readable", "licenses_readable", "skills_readable"
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for data in structured_data_list:
                row = {
                    "uuid": data.get("uuid", ""),
                    "full_name": data.get("full_name", ""),
                    "addresses_count": len(data.get("addresses", [])),
                    "phone_numbers_count": len(data.get("phone_numbers", [])),
                    "education_count": len(data.get("education", [])),
                    "training_count": len(data.get("training", [])),
                    "work_experience_count": len(data.get("work_experience", [])),
                    "certifications_count": len(data.get("certifications", [])),
                    "licenses_count": len(data.get("licenses", [])),
                    "skills_count": len(data.get("skills", [])),
                    "contact_info_count": len(data.get("contact_info", []))
                }
                
                # Convert lists to JSON strings for CSV storage
                for field in ["addresses", "phone_numbers", "education", "training", "work_experience", "certifications", "licenses", "skills", "contact_info"]:
                    row[f"{field}_json"] = json.dumps(data.get(field, []), ensure_ascii=False)
                
                # Add readable text fields
                for field in ["education", "training", "work_experience", "certifications", "licenses", "skills"]:
                    readable_field = f"{field}_readable"
                    readable_data = data.get(readable_field, [])
                    if readable_data:
                        # Join multiple readable entries with line breaks
                        row[readable_field] = "\n".join(readable_data)
                    else:
                        row[readable_field] = ""
                
                writer.writerow(row)
        
        print(f"✅ Structured data CSV saved to {filename}")

def main():
    scraper = DoximityScraper()
    
    print("🚀 Doximity Detailed Profile Scraper")
    print("=" * 50)
    print("Automatically scraping detailed profiles for all specialties...")
    
    total_detailed_profiles = 0
    
    for i, specialty_code in enumerate(SPECIALTY_CODES, 1):
        try:
            print(f"\n{'='*50}")
            print(f"Processing: {specialty_code} ({i}/{len(SPECIALTY_CODES)})")
            print(f"{'='*50}")
            
            # Scrape detailed profiles for this specialty (limit to 50 per specialty to avoid overwhelming)
            detailed_profiles, structured_data = scraper.scrape_detailed_profiles(specialty_code, max_profiles=50)
            total_detailed_profiles += len(detailed_profiles) if detailed_profiles else 0
            
            # Save structured data for this specialty to its own CSV file
            if structured_data:
                try:
                    csv_filename = f"output/{specialty_code}.csv"
                    scraper.save_structured_data_to_csv(structured_data, csv_filename)
                    print(f"📁 Data saved to: {csv_filename}")
                except Exception as e:
                    print(f"❌ Error saving CSV file for {specialty_code}: {e}")
            
            print(f"✅ Completed {specialty_code}: {len(detailed_profiles) if detailed_profiles else 0} detailed profiles")
            print(f"📊 Total detailed profiles so far: {total_detailed_profiles}")
            
        except Exception as e:
            print(f"❌ Error processing {specialty_code}: {e}")
            continue
    
    print(f"\n{'='*50}")
    print(f"🎉 All detailed profile scraping completed!")
    print(f"📊 Total specialties processed: {len(SPECIALTY_CODES)}")
    print(f"📊 Total detailed profiles collected: {total_detailed_profiles}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
