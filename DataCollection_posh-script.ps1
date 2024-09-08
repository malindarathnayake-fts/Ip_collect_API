# Malinda 2024
# Script to gther network information and send it to the flask API

# Function to get primary DNS server
function Get-PrimaryDNS {
    $dnsServers = Get-DnsClientServerAddress -AddressFamily IPv4 | 
                  Where-Object {$_.InterfaceAlias -eq (Get-NetAdapter | Where-Object {$_.Status -eq "Up"}).Name} | 
                  Select-Object -ExpandProperty ServerAddresses
    if ($dnsServers.Count -gt 0) {
        return $dnsServers[0]
    }
    return "N/A"
}

# Gather network information
$hostname = $env:COMPUTERNAME
$ipConfig = Get-NetIPConfiguration | Where-Object {$_.IPv4DefaultGateway -ne $null -and $_.NetAdapter.Status -ne "Disconnected"}
$ipAddress = $ipConfig.IPv4Address.IPAddress
$subnetMask = (Get-NetIPAddress -InterfaceIndex $ipConfig.InterfaceIndex -AddressFamily IPv4).PrefixLength
$gateway = $ipConfig.IPv4DefaultGateway.NextHop
$dns = Get-PrimaryDNS

# Construct the data object
$data = @{
    hostname = $hostname
    ip = $ipAddress
    subnetmask = "$subnetMask"  # Convert to string as it's in CIDR notation
    gateway = $gateway
    dns = $dns
}

# Convert data to JSON
$jsonData = $data | ConvertTo-Json

# Send POST request to the API
$apiUrl = "http://192.168.94.181:8080/ip-info"
$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Body $jsonData -Headers $headers
    Write-Output "Data sent successfully. Response: $($response | ConvertTo-Json)"
}
catch {
    Write-Error "Failed to send data to API. Error: $_"
}
