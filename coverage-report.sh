# Create the output directory if it doesn't exist
mkdir -p coverage_reports

# Run tests with coverage
coverage run manage.py test

# Generate HTML, XML and text report in the specified directory
coverage html -d coverage_reports/html
coverage xml -o coverage_reports/coverage.xml
coverage report > coverage_reports/coverage_report.txt
