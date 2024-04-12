$currDir = Get-Location
# $targetDir = "F:"

# #Remove-Item $targetDir* -Recurse -Force
# Copy-Item $currDir/src/*.py $targetDir -Recurse -Force
# Copy-Item $currDir/thunder/ $targetDir/lib/ -Recurse -Force

# Check if a drive with label "NANOKID" exists
$nanokidDrive = Get-WmiObject Win32_Volume | Where-Object { $_.Label -eq 'NANOKID' }

if ($nanokidDrive) {
	# Copy contents to the root of "NANOKID" drive
	Copy-Item $currDir/src/*.py -Destination "$($nanokidDrive.DriveLetter)\" -Recurse -Force
	Copy-Item $currDir/thunder/ -Destination "$($nanokidDrive.DriveLetter)\lib\" -Recurse -Force
	Write-Host "Contents copied to NANOKID drive successfully."
} else {
	# Check if a drive with label "CIRCUITPY" exists
	$circuitpyDrive = Get-WmiObject Win32_Volume | Where-Object { $_.Label -eq 'CIRCUITPY' }

	if ($circuitpyDrive) {
		# Copy contents to the root of "CIRCUITPY" drive
		Copy-Item $currDir/src/*.py -Destination "$($circuitpyDrive.DriveLetter)\" -Recurse -Force
	Copy-Item $currDir/thunder/ -Destination "$($circuitpyDrive.DriveLetter)\lib\" -Recurse -Force
		Write-Host "Contents copied to CIRCUITPY drive successfully."
	} else {
		Write-Host "Error: Neither NANOKID nor CIRCUITPY drive found."
	}
}
