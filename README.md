# Doximity Scraper

A configurable Python scraper for extracting user data from Doximity's GraphQL API based on specialty codes.

## Features

- **Configurable**: Easy to modify settings via `config.py`
- **Multi-specialty support**: Scrape multiple specialty codes in one run
- **Pagination handling**: Automatically handles all pages of results
- **Multiple output formats**: CSV, JSON, or both
- **Comprehensive logging**: Console and file logging with configurable levels
- **Rate limiting**: Respectful API usage with configurable delays
- **Error handling**: Graceful error handling and recovery
- **Field filtering**: Option to extract only specific data fields
- **Comprehensive GraphQL query**: Uses the full Doximity API schema with all available fields and filter options

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the scraper**:
   - Copy `sample.config.py` to `config.py`
   - Edit `config.py` with your settings:
     - Add your Doximity bearer token
     - Configure specialty codes to scrape
     - Set output preferences
     - Adjust rate limiting and other options

3. **Run the scraper**:
   ```bash
   # Option 1: Run directly
   python doximity_scraper.py
   
   # Option 2: Use the runner script
   python run_scraper.py
   ```

## Configuration Options

### DOXIMITY_CONFIG
- `bearer_token`: Your Doximity API authentication token
- `base_url`: GraphQL API endpoint
- `request_delay`: Seconds between API requests (rate limiting)
- `users_per_page`: Number of users per page (max 100)
- `max_pages`: Safety limit for pagination

### SPECIALTY_CODES
List of specialty codes to scrape. Examples:
- `"AN00"` - Anesthesiology
- `"NC00"` - Oncology
- `"IM00"` - Internal Medicine
- `"SU00"` - Surgery
- `"PE00"` - Pediatrics

### OUTPUT_CONFIG
- `output_dir`: Directory for output files
- `output_format`: "csv", "json", or "both"
- `include_timestamp`: Add timestamps to filenames
- CSV and JSON specific options

### LOGGING_CONFIG
- `level`: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `log_to_file`: Enable/disable file logging
- `log_file`: Log file path
- `format`: Log message format

### EXTRACT_FIELDS
Optional list of specific fields to extract. If empty, all available fields are extracted.

### FILTERS
Optional additional filters like state, city, or credentials.

## Usage Examples

### Basic Usage
```python
# config.py
SPECIALTY_CODES = ["AN00", "NC00"]
OUTPUT_CONFIG["output_format"] = "both"
```

### Field Filtering
```python
# config.py
EXTRACT_FIELDS = [
    "id",
    "fullName", 
    "specialtyName",
    "cityName",
    "stateAbbreviation"
]
```

### Location Filtering
```python
# config.py
FILTERS = {
    "statePostalCodeFilter": "CA",
    "locationNameFilter": "Los Angeles"
}
```

## Output

The scraper creates:
- `output/` directory for all files
- CSV files: `{SPECIALTY_CODE}_users{timestamp}.csv`
- JSON files: `{SPECIALTY_CODE}_users{timestamp}.json`
- Log file: `output/scraper.log`

## Rate Limiting

The scraper includes configurable rate limiting to be respectful to Doximity's API. Default is 0.5 seconds between requests.

## Error Handling

- Graceful handling of API errors
- Continues processing other specialty codes if one fails
- Comprehensive logging of all operations
- Safety limits to prevent infinite loops

## Security

- Bearer token is stored in `config.py` (keep this file secure)
- Never commit `config.py` to version control
- Use `sample.config.py` as a template

## Troubleshooting

1. **Authentication errors**: Check your bearer token in `config.py`
2. **Rate limiting**: Increase `request_delay` in configuration
3. **Missing data**: Check `EXTRACT_FIELDS` configuration
4. **API errors**: Review log files for detailed error messages

## License

This project is for educational purposes. Please respect Doximity's terms of service and API usage guidelines.
