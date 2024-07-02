-- unit and intergratoin test

-- formatting
isort
black
pylint
pyproject.toml

-- Git pre-commit rules
do a git init to create a temp git repo (remove after)
- pre-commit sample-config
- pre-commit install
asdasd

-- Terraform
install terraform
VSCode - install terraform and azure terraform extensions
Azure - Access Entra ID and create application
Subscription - IAM, give contributor role to application
write main.tf
terraform init
terraform plan -out main.tfplan 
terraform apply main.tfplan 



psql -h cm37-example-postgresql-server.postgres.database.azure.com -U testadmin@cm37-example-postgresql-server -d postgres -p 5432

psql "host=cm37-example-postgresql-server.postgres.database.azure.com port=5432 user=testadmin@cm37-example-postgresql-server dbname=exampledb sslmode=require"

PGPASSWORD='Plokijuh1!' psql -v "host=cm37-example-postgresql-server.postgres.database.azure.com port=5432 user=testadmin@cm37-example-postgresql-server dbname=exampledb sslmode=require"


psql -U testadmin -d <database_name> -h <hostname> -p <port>