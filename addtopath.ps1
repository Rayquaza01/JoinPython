[Environment]::SetEnvironmentVariable( "Path", $env:Path + ";" + (Get-Location).path, [System.EnvironmentVariableTarget]::Machine )
