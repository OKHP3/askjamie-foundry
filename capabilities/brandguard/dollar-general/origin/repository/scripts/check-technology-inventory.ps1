param(
    [string]$InventoryPath = "docs/technology-inventory.md",
    [int]$MaxAgeDays = 120
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $InventoryPath)) {
    throw "Technology inventory not found: $InventoryPath"
}

$inventory = Get-Content -Raw -LiteralPath $InventoryPath
$match = [regex]::Match($inventory, 'Inventory date: (?<date>\d{4}-\d{2}-\d{2})')

if (-not $match.Success) {
    throw "Technology inventory must contain an ISO-8601 Inventory date."
}

$inventoryDate = [datetime]::ParseExact(
    $match.Groups['date'].Value,
    'yyyy-MM-dd',
    [Globalization.CultureInfo]::InvariantCulture
)
$age = ([datetime]::UtcNow.Date - $inventoryDate.Date).Days

if ($age -gt $MaxAgeDays) {
    throw "Technology inventory is $age days old. Refresh $InventoryPath before merging."
}

Write-Output "Technology inventory is current: $($match.Groups['date'].Value) ($age days old)."
