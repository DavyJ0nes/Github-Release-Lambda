all: run

aws_region ?= eu-west-1
function_name ?=
event_type ?=
bucket_name ?=
bucket_prefix ?=
stack_name ?=

package:
	$(call blue, "# Packaging Cloudfomration Template...")
	$(call check_defined, bucket_name, S3 Bucket Name to Deploy To)
	$(call check_defined, bucket_prefix, S3 Bucket Directory to Deploy To)
	aws --region ${aws_region} cloudformation package --template-file template.yml --s3-bucket ${bucket_name} --s3-prefix ${bucket_prefix} --output-template-file packaged-template.yml

deploy: package
	$(call blue, "# Deploying Cloudformation Stack...")
	$(call check_defined, stack_name, The name of the Cloudformation stack to use)
	aws --region ${aws_region} cloudformation deploy --template-file "$(CURDIR)"/packaged-template.yml --stack-name ${stack_name} --parameter-overrides $(cat vars/app-vars-production) --capabilities CAPABILITY_IAM

run:
	$(call blue, "# Running Function Locally...")
	$(call check_defined, function_name, The Name of the Function to Run)
	$(call check_defined, event_type, The Type of Sample to Event to use with the Function)
	sam local invoke -e events/${event_type}.json ${function_name}


define blue
  @tput setaf 4
  @echo $1
  @tput sgr0
endef

check_defined = \
	$(strip $(foreach 1,$1, \
	$(call __check_defined,$1,$(strip $(value 2)))))
__check_defined = \
	$(if $(value $1),, \
	$(error Undefined $1$(if $2, ($2))))
