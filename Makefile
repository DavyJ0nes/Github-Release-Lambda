all: go

app = vault-demo-example
service ?= app
bucket_name ?= cr-davy-agileops-training
bucket_prefix ?= github-notifier
stack_name ?= davyj-ao-testing-gh-notifier

package:
	$(call blue, "# Packaging Cloudfomration Template...")
	aws --profile default --region eu-west-1 cloudformation package --template-file template.yml --s3-bucket ${bucket_name} --s3-prefix ${bucket_prefix} --output-template-file packaged-template.yml

deploy: package
	$(call blue, "# Deploying Cloudformation Stack...")
	aws --region eu-west-1 cloudformation deploy --template-file $(CURDIR)/packaged-template.yml --stack-name ${stack_name} --parameter-overrides $(cat vars/app-vars-production) --capabilities CAPABILITY_IAM


define blue
  @tput setaf 4
        @echo $1
        @tput sgr0
endef
