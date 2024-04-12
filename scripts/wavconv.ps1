param (
	[string]$Folder
)

# Check if the folder path is provided
if (-not $Folder) {
	Write-Host "Please provide a folder path as an argument."
	exit 1
}

if (-not (Test-Path "$Folder\qmw" -PathType Container)) {
  New-Item -ItemType Directory -Path "$Folder\qmw"
	Write-Host "Created qmw folder"
}

# Get all files in the folder
$files = Get-ChildItem -Path $folderPath -Filter *.mp3

# Iterate through each file and execute the command
foreach ($file in $files) {
	# Ensure the item is a file and not a directory
	if ($file.PSIsContainer -eq $false) {
		$outputFileName = "{0}-qm{1}" -f $file.BaseName, ".wav"
		# Build the command with the file as an argument
		$fullCommand = "sox '$($file.FullName)' -b 16 -c 1 -r 22050 '$($file.DirectoryName)\qmw\$outputFileName'"

		# Execute the command
		Invoke-Expression -Command $fullCommand

		# If you want to see the progress, you can print the file name
		Write-Host "Processed file: $($file.Name)"
	}
}