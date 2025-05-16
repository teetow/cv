#!/usr/bin/env pwsh
# GitHub Actions workflow validator using act (https://github.com/nektos/act)

$workflowPath = ".github/workflows/github-pages.yml"

function Write-ErrorAndExit($message) {
    Write-Host "ERROR: $message" -ForegroundColor Red
    exit 1
}

# Check prerequisites
if (-not (Test-Path $workflowPath)) { Write-ErrorAndExit "Workflow file not found" }
if (-not (Get-Command act -ErrorAction SilentlyContinue)) { 
    Write-Host "Please install act: https://github.com/nektos/act#installation" -ForegroundColor Yellow
    Write-ErrorAndExit "'act' is not installed or not in PATH" 
}
try { 
    $null = docker info 2>&1
    if ($LASTEXITCODE -ne 0) { Write-ErrorAndExit "Docker is not running. Please start Docker to use act" }
} catch { 
    Write-ErrorAndExit "Docker is not installed or not in PATH. Docker is required for act" 
}

# Run validation and workflow
try {
    Write-Host "Running workflow validation with act..." -ForegroundColor Cyan
    act --dryrun -W $workflowPath
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "SUCCESS: Workflow validation passed" -ForegroundColor Green
          # Create temporary event file to skip deployment
        $tempEventFile = Join-Path $env:TEMP "act_event.json"
        '{"act": true}' | Out-File -FilePath $tempEventFile -Encoding UTF8
        
        # Local PDF generation instead of using the GitHub Action
        Write-Host "Converting Markdown to PDF locally..." -ForegroundColor Cyan
        
        # Check if md-to-pdf is installed and install if needed
        if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
            Write-ErrorAndExit "npm is not installed. Please install Node.js to continue."
        }
        
        if (-not (Get-Command md-to-pdf -ErrorAction SilentlyContinue)) {
            Write-Host "Installing md-to-pdf globally..." -ForegroundColor Yellow
            npm install -g md-to-pdf
            if ($LASTEXITCODE -ne 0) {
                Write-ErrorAndExit "Failed to install md-to-pdf"
            }
        }
        
        # Convert CV to PDF
        md-to-pdf cv.md
        
        # Verify if PDFs were generated
        if (Test-Path "cv.pdf" -ErrorAction SilentlyContinue) {
            Write-Host "SUCCESS: PDF generation worked correctly" -ForegroundColor Green
        } else {
            Write-Host "WARNING: PDF generation failed." -ForegroundColor Yellow
        }
        
        # Run workflow without the PDF generation step (for testing other functionality)
        Write-Host "Executing workflow (skipping Deploy step)..." -ForegroundColor Cyan
        act -W $workflowPath -j deploy -e $tempEventFile --skip-steps "Generate PDF files"
        
        Remove-Item -Path $tempEventFile -ErrorAction SilentlyContinue
    } else {
        Write-ErrorAndExit "Workflow validation failed"
    }
} catch {
    Write-ErrorAndExit $_
}
