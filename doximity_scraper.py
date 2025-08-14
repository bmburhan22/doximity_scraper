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
    "SG00",  # General Surgery
    "GE00",  # Geriatrics
    "HE00",  # Hematology
    "FD00",  # Infectious Disease
    "TM00",  # Internal Medicine
    "IR00",  # Interventional Radiology
    "MG00",  # Medical Genetics
    "MP00",  # Medicine/Pediatrics
    "NN00",  # Neonat/Perinatology
    "NE00",  # Nephrology
    "NG00",  # Neurology
    "NS00",  # Neurosurgery
    "NM00",  # Nuclear Medicine
    "BG00",  # Obstetrics & Gynecology
    "CM00",  # Occupational Medicine
    "NC00",  # Oncology
    "TH00",  # Ophthalmology
    "OM00",  # Oral & Maxillofacial Surgery
    "RT00",  # Orthopaedic Surgery
    "MD00",  # Other MD/DO
    "TY00",  # Otolaryngology (ENT)
    "PH00",  # Pathology
    "PGS00", # Pediatric (General) Surgery
    "CP00",  # Pediatric Cardiology
    "PEM00", # Pediatric Emergency Medicine
    "EP00",  # Pediatric Endocrinology
    "GP00",  # Pediatric Gastroenterology
    "HN00",  # Pediatric Hematology & Oncology
    "DP00",  # Pediatric Infectious Disease
    "FP00",  # Pediatric Nephrology
    "PP00",  # Pediatric Pulmonology
    "RP00",  # Pediatric Rheumatology
    "PE00",  # Pediatrics
    "PM00",  # Physical Medicine/Rehab
    "PS00",  # Plastic Surgery
    "GM00",  # Preventive Medicine
    "PY00",  # Psychiatry
    "PU00",  # Pulmonology
    "RC00",  # Radiation Oncology
    "RA00",  # Radiology
    "RE00",  # Research
    "RS00",  # Resident Physician
    "RH00",  # Rheumatology
    "TS00",  # Thoracic Surgery
    "UR00",  # Urology
    "VS00",  # Vascular Surgery
    
    # Nurse Practitioner Specialties
    "AC00",  # Acute Care Nurse Practitioner
    "AD00",  # Adult Care Nurse Practitioner
    "AS00",  # Certified Nurse Midwife
    "AF00",  # Family Nurse Practitioner
    "AG00",  # Geriatric Nurse Practitioner
    "AE00",  # Neonatal Nurse Practitioner
    "NP00",  # Nurse Practitioner
    "AH00",  # Occupational Health Nurse Practitioner
    "AP00",  # Pediatric Nurse Practitioner
    "AT00",  # Psychiatric-Mental Health Nurse Practitioner
    "AW00",  # Women's Health Nurse Practitioner
    
    # Physician Assistant Specialties
    "WA00",  # Academic Medicine
    "WB00",  # Allergy and Immunology
    "WC00",  # Anesthesiology
    "WD00",  # Cardiology
    "WE00",  # Colon & Rectal Surgery
    "WF00",  # Critical Care
    "WG00",  # Dermatology
    "WH00",  # Emergency Medicine
    "WI00",  # Endocrinology
    "WJ00",  # Family Medicine
    "WK00",  # Gastroenterology
    "WL00",  # General Hospitalist
    "WM00",  # General Surgery
    "WN00",  # Hematology
    "WO00",  # Infectious Disease
    "WP00",  # Internal Medicine
    "WQ00",  # Interventional Radiology
    "WR00",  # Medical Genetics
    "WS00",  # Medicine/Pediatrics
    "WT00",  # Neonat/Perinatology
    "WU00",  # Nephrology
    "WV00",  # Neurology
    "WW00",  # Neurosurgery
    "WX00",  # Nuclear Medicine
    "WY00",  # Obstetrics & Gynecology
    "WZ00",  # Occupational Medicine
    "FA00",  # Oncology
    "FB00",  # Ophthalmology
    "FC00",  # Oral and Maxillofacial Surgery
    "FE00",  # Orthopedics
    "FF00",  # Otolaryngology (ENT)
    "FG00",  # Pain Management
    "FH00",  # Pathology
    "FI00",  # Pediatrics
    "FJ00",  # Physical Medicine/Rehab
    "PA00",  # Physician Assistant
    "FK00",  # Plastic Surgery
    "FL00",  # Preventive Medicine
    "FN00",  # Psychiatry
    "FO00",  # Public Health
    "FQ00",  # Pulmonology
    "FR00",  # Radiology
    "FS00",  # Rheumatology
    "FT00",  # Thoracic Surgery
    "FU00",  # Urology
    "FV00",  # Vascular Surgery
    
    # Pharmacist Specialties
    "CX00",  # Clinical Pharmacist
    "RX00",  # Pharmacist
    
    # Other Healthcare Professionals
    "CH00",  # Chiropractor
    "DN00",  # Diet/Nutritionist
    "HM00",  # Genetic Counselor
    "TT00",  # Optometrist
    "HP00",  # Other Healthcare Professional
    "PT00",  # Physical Therapist
    "PL00",  # Psychologist
    "RN00",  # Registered Nurse
    "SW00",  # Social Worker
    
    # CRNA
    "NA00",  # Certified Registered Nurse Anesthetist
    
    # Student Categories
    "MS00",  # Med Student
    "NPS00", # NP Student
    "PAS00", # PA Student
    "OHS00", # Other Healthcare Student
    "RXS00", # Pharmacy Student
    "RNAX00" # CRNA Student
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
            "first": 10
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
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return None
            
            return response.json()
            
        except Exception as e:
            print(f"❌ Request Error: {e}")
            return None
    
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

def main():
    scraper = DoximityScraper()
    total_users = 0
    
    print(f"📋 Processing {len(SPECIALTY_CODES)} specialties...")
    
    for i, specialty_code in enumerate(SPECIALTY_CODES, 1):
        try:
            print(f"\n{'='*50}")
            print(f"Processing: {specialty_code} ({i}/{len(SPECIALTY_CODES)})")
            print(f"{'='*50}")
            
            users = scraper.scrape_all_users(specialty_code)
            total_users += len(users)
            
            if users:
                filename = f"output/{specialty_code}.csv"
                scraper.save_to_csv(users, filename)
            else:
                print(f"⚠️  No users found for {specialty_code}")
            
            # Progress update
            print(f"📊 Progress: {i}/{len(SPECIALTY_CODES)} specialties completed")
            print(f"📊 Total users collected so far: {total_users}")
            
        except Exception as e:
            print(f"❌ Error processing {specialty_code}: {e}")
            continue
    
    print(f"\n{'='*50}")
    print(f"🎉 All scraping completed!")
    print(f"📊 Total specialties processed: {len(SPECIALTY_CODES)}")
    print(f"📊 Total users collected: {total_users}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
