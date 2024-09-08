

## This system consists of two components:
1. A Python API that receives and stores IP information
2. A PowerShell script that collects and sends IP information
   
## Python API (ip_info_api.py)

### Description
This Flask-based API listens for POST requests containing IP information and stores it in a CSV file. It also provides a simple GET endpoint to check if the API is running.

### Requirements
- Python 3.6+
- Flask
```python
pip3.12 install flask
```

### Installation
1. Install Flask:

2. Save the script

### Usage
Run the script with a filename argument: Example 

```python3.12 simple-data-collection-api.py mydata.csv```

The API will start and listen on port 8080. All received data will be appended to `mydata.csv` in the `ip_info_data` directory in the script root Directory

### Endpoints
- GET `/`: Returns "Data collector API is up" if the API is running.
- POST `/ip-info`: Accepts JSON data with IP information and appends it to the CSV file.

### JSON Data Format
```json
{
  "hostname": "example-host",
  "ip": "192.168.1.100",
  "subnetmask": "255.255.255.0",
  "gateway": "192.168.1.1",
  "dns": "8.8.8.8"
}
```

## PowerShell Script (DataCollection_posh-script.ps1)

### Description
This PowerShell script collects network information from the local machine and sends it to the Python API.

### Requirements

- PowerShell 5.1+

## Usage

- Save the script
- Run the script via your RMM or using GPO

### Configuration
Before running, update the $apiUrl variable in the script to match your API's address:

```powershell
$apiUrl = "http://your_api_ip:8080/ip-info"
```

## Security Considerations

- This system is designed for use within a trusted network environment.
- Consider implementing authentication and HTTPS for the API in production environments.
- Review and adapt the scripts according to your organization's security policies before deployment.
