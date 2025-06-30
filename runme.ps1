# Check Python version
$python_version = python --version
if ($python_version -notmatch "Python 3.12") {
    Write-Output "Error: Python 3.12 is required."
    exit 1
}

# Check if pip is installed
if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Output "Error: 'pip' is not installed."
    exit 1
}

# Check for virtualenv package
if (-not (pip show virtualenv -ErrorAction SilentlyContinue)) {
    Write-Output "Installing virtualenv..."
    pip install virtualenv
}

# Create and activate virtual environment
Write-Output "Creating virtual environment..."
virtualenv myenv
Write-Output "Activating virtual environment..."
.\myenv\Scripts\Activate

# Install required packages
Write-Output "Installing required packages..."
pip install -r requirements.txt

# Run the server
Write-Output "Running the server..."
python manage.py runserver

# Display server link
Write-Output "Server is running. Visit http://127.0.0.1:8000/ in your browser to view the application."
