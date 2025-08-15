# Doximity Scraper

A comprehensive web scraper for Doximity profiles that automatically collects detailed information about healthcare professionals across all medical specialties.

## Features

### Automatic Detailed Profile Scraping
- **No prompts or options** - runs automatically
- **Address Information**: Practice and personal addresses with full details
- **Phone Numbers**: Mobile, home, office, and practice phone numbers
- **Education**: Academic background and degrees
- **Training**: Medical training and residency information
- **Certifications**: Professional certifications and credentials
- **Licenses**: State medical licenses and status

## Data Fields Collected

### Detailed Profile Data
#### Addresses
- Address line 1 & 2
- City, state, country, ZIP code
- Practice name (if applicable)
- Primary address indicator
- GPS coordinates

#### Phone Numbers
- Mobile phone
- Home phone
- Office phone
- Practice phone numbers
- Phone extensions
- Fax numbers

#### Professional Information
- **Education**: Institution, degree, field of study, dates
- **Training**: Institution, specialty, start/end dates, type
- **Certifications**: Name, issuing organization, dates, credential ID
- **Licenses**: State, license number, issue/expiration dates, status

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd doximity_scraper
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set your bearer token in `doximity_scraper.py`:
```python
BEARER_TOKEN = "your_actual_token_here"
```

4. Configure specialty codes (currently only "AM00" is active):
```python
SPECIALTY_CODES = [
    "AM00",  # Allergy & Immunology
    # "AN00",  # Anesthesiology (commented out)
    # "CA00",  # Cardiology (commented out)
    # ... add more as needed
]
```

## Usage

### Simple Run
Just run the scraper and it will automatically process all active specialty codes:

```bash
python doximity_scraper.py
```

The scraper will:
1. Process each specialty code in the list
2. Collect up to 50 detailed profiles per specialty
3. Save detailed profiles to JSON files
4. Save structured data summaries to CSV files
5. Show progress for each specialty

### Output Files

For each specialty code, you'll get:
- `{specialty_code}_detailed_profiles.json` - Full detailed profiles with all data
- `{specialty_code}_structured_data.csv` - Summary with counts and JSON-encoded detailed data

## GraphQL Queries Used

The scraper uses three main GraphQL queries:

1. **Profile Sections Query**: Extracts education, training, certifications, and licenses
2. **Private Lines Query**: Gets private contact information (phone numbers, emails)
3. **Locations Query**: Retrieves address and practice location information

## Rate Limiting

- 2 second delay between detailed profile requests
- Adjustable in the code if needed

## Error Handling

- Graceful handling of API errors
- Continues processing on individual profile failures
- Saves partial results
- Shows progress for each specialty

## Specialties Supported

The scraper supports all major medical specialties. Currently active:
- **AM00** - Allergy & Immunology

To enable more specialties, uncomment the desired codes in the `SPECIALTY_CODES` list.

## Notes

- Requires valid Doximity bearer token for authentication
- Respects API rate limits to avoid being blocked
- Data quality depends on profile completeness
- Some profiles may have limited information available
- Limit of 50 profiles per specialty to avoid overwhelming the API

## Troubleshooting

### Common Issues
1. **Authentication Error**: Check your bearer token is valid
2. **Rate Limiting**: Increase delays between requests in the code
3. **Empty Results**: Verify specialty codes are correct
4. **API Errors**: Check Doximity's API status

## Legal and Ethical Considerations

- Respect Doximity's terms of service
- Use data responsibly and ethically
- Consider privacy implications
- Comply with applicable data protection laws
- Use for legitimate research purposes only

## License

This project is for educational and research purposes. Please ensure compliance with Doximity's terms of service and applicable laws.
