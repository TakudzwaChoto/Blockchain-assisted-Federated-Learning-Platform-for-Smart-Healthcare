Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Path)

if (!(Test-Path -Path "frontend")) {
  Write-Error "frontend folder not found"
  exit 1
}

Set-Location -Path "frontend"

npm install
npm run dev
